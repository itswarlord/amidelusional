"""
BUILT by Vansh Aggarwal. 
"""
# importing all the dependencies


import os
import re
import time
import httpx
import json
import threading
import requests as bolo
from datetime import datetime, timedelta
from dotenv import load_dotenv #keys 
from caspian_sdk import CommClient #chat interface module
from pydantic import BaseModel, Field #class for query
from langchain_google_genai import ChatGoogleGenerativeAI #downstream
from langchain_core.prompts import ChatPromptTemplate #querying
from langchain_huggingface import HuggingFaceEmbeddings #upstreat
from pinecone import Pinecone #vector-db
import uuid #encoding
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from web3 import Web3
import base64

import shutil

"""
importing reportlab from github
using documentation from github (credit where credit is due)
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

"""
Loading relevant agents. 
note to self remember to make .env on server 
1. .env is loaded 
2. caspian_sdk is loaded 
3. pinecone and local llm loaded.
"""

load_dotenv()
client = CommClient()

client.connect_telegram(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))
client.connect_email(connection_id=os.getenv("EMAIL_CONNECTION_ID"))
client.connect_discord(connection_id=os.getenv("DISCORD_BOT_CONNECTION_ID"), bot_token=os.getenv("DISCORD_BOT_TOKEN"))

print("Connecting to Pinecone and loading BAAI embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("relationship-kb")


print("Connecting to Sepolia Testnet for ZK Validation...")
SEPOLIA_RPC = "https://ethereum-sepolia-rpc.publicnode.com"
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))

# NOTE: Add RELAYER_PRIVATE_KEY to your .env file!
RELAYER_PRIVATE_KEY = os.getenv("RELAYER_PRIVATE_KEY") 
if RELAYER_PRIVATE_KEY:
    relayer_account = w3.eth.account.from_key(RELAYER_PRIVATE_KEY)
else:
    relayer_account = None
    print("WARNING: RELAYER_PRIVATE_KEY not found in .env. Contract validation will be bypassed.")

CONTRACT_ADDRESS = "0x1e0d760a8d53a51a07b5d1e2e4f0a2f61e1a33f5"
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "merkleTreeRoot", "type": "uint256"},
            {"internalType": "uint256", "name": "nullifierHash", "type": "uint256"},
            {"internalType": "uint256", "name": "signal", "type": "uint256"},
            {"internalType": "uint256", "name": "externalNullifier", "type": "uint256"},
            {"internalType": "uint256[8]", "name": "proof", "type": "uint256[8]"}
        ],
        "name": "verifyAndRecord",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
if relayer_account:
    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
app = FastAPI(title="Am I Delusional API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def safe_read_file(file_path):
    """Tries multiple encodings to safely read iPhone and Android txt exports."""
    encodings_to_try = ['utf-8', 'utf-16', 'utf-8-sig', 'windows-1252', 'latin-1']
    for enc in encodings_to_try:
        try:
            with open(file_path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

# double check on uploading and providing link
def link_generato_for_file(file_path):    
    # tmpfiles.org
    try:
        with open(file_path, 'rb') as f:
            response = bolo.post('https://tmpfiles.org/api/v1/upload', files={'file': f}, timeout=30)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get('status') == 'success':
                    url = res_json['data']['url']
                    return url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
    except Exception as e:
        print(f" tmpfiles.org upload attempt failed: {e}")

    #transfer.sh
    try:
        with open(file_path, 'rb') as f:
            filename = os.path.basename(file_path)
            response = bolo.put(f'https://transfer.sh/{filename}', data=f, timeout=30)
            if response.status_code == 200:
                return response.text.strip()
    except Exception as e:
        print(f" transfer.sh upload attempt failed: {e}")

    return None

'''
PDF generation 
report labs documentation
'''

def reportlabdirectpdfconvertor(report_dict, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    
    title_style = ParagraphStyle(
        'CustomTitle', fontName='Times-Bold', fontSize=30, 
        alignment=TA_CENTER, spaceAfter=20
    )
    score_style = ParagraphStyle(
        'ScoreStyle', fontName='Times-Bold', fontSize=24, 
        alignment=TA_CENTER, spaceAfter=30, textColor='black'
    )
    heading_style = ParagraphStyle(
        'CustomHeading', fontName='Times-Bold', fontSize=18, 
        alignment=TA_CENTER, spaceAfter=15, spaceBefore=20
    )
    body_style = ParagraphStyle(
        'CustomBody', fontName='Times-Roman', fontSize=14, 
        alignment=TA_LEFT, spaceAfter=10, leading=18
    )

    story = []

    story.append(Paragraph("Relationship Report", title_style))

    score = report_dict.get('section_9_ai_diagnosis', {}).get('relationship_score', 'N/A')
    story.append(Spacer(1, 14))
    story.append(Spacer(1, 14))


    story.append(Paragraph(f"Relationship Score:        {score}/100", score_style))

    story.append(Spacer(1, 14))

    story.append(Spacer(1, 14))
    story.append(Spacer(1, 14))


    def clean_text(text):
        """Prepares text for ReportLab XML parsing"""
        text = str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        text = text.replace("\n", "<br/>")
        return text

    def format_value(val):
        """Handles lists and nested dictionaries neatly"""
        if isinstance(val, list):
            return ", ".join(clean_text(str(v)) for v in val)
        elif isinstance(val, dict):
            lines = [f"<br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>{k.replace('_', ' ').title()}:</b> {clean_text(v)}" for k, v in val.items()]
            return "".join(lines)
        return clean_text(str(val))

    section_order = [
        "section_9_ai_diagnosis",
        "section_7_psychological_factors",
        "section_5_positive_behavioral_markers",
        "section_8_trend_analysis",
        "section_2_profiles_and_baseline",
        "section_1_transcript_metadata",
        "section_6_gottman_conflict_markers",
        "section_3_quantitative_metrics",
        "section_4_latency_and_responsiveness"
    ]

    for section_key in section_order:
        section_data = report_dict.get(section_key)
        if not section_data:
            continue #skip if not found

        header_text = section_key[10:].title()
        story.append(Paragraph(header_text, heading_style))
        story.append(Spacer(1, 14))
        story.append(Spacer(1, 14))

        if isinstance(section_data, dict):
            for key, val in section_data.items():
                if key == "relationship_score":
                    continue 
                
                k_clean = key.replace('_', ' ').title()
                v_clean = format_value(val)
                story.append(Paragraph(f"<b>{k_clean}:</b> {v_clean}", body_style))
                story.append(Spacer(1, 14))
                story.append(Spacer(1, 14))

    doc.build(story)


"""
Langchain class implementation
"""

class Section2_Profiles(BaseModel):
    ages_and_gap: str = Field(description="Ages of A and B, and difference")
    occupation: str = Field(description="Occupations/roles of A and B")
    locations_and_distance: str = Field(description="Cities and distance between them")
    time_zone_diff: str = Field(description="Time zone difference")
    origin_how_they_met: str = Field(description="How they met")
    relationship_status_duration: str = Field(description="Status and duration")
    meeting_frequency: str = Field(description="How often they meet in person")

class Section5_GreenFlags(BaseModel):
    openness_score_a: int = Field(description="Emotional vulnerability score for A (0-100)")
    openness_score_b: int = Field(description="Emotional vulnerability score for B (0-100)")
    gratitude_appreciation: str = Field(description="Analysis of gratitude expressions")
    shared_humor_index: str = Field(description="Frequency of laughter/jokes")
    we_us_pronoun_ratio: str = Field(description="Ratio of team vs singular pronouns")
    affectionate_nicknames: str = Field(description="Nicknames used")
    positive_reinforcement: str = Field(description="Supportiveness instances A vs B")
    active_constructive_responding: str = Field(description="How they react to good news")

class Section6_Gottman(BaseModel):
    criticism_instances: str = Field(description="Instances of criticism (A vs B)")
    defensiveness_instances: str = Field(description="Instances of defensiveness (A vs B)")
    contempt_instances: str = Field(description="Instances of contempt (A vs B)")
    stonewalling_instances: str = Field(description="Instances of stonewalling (A vs B)")
    gaslighting_instances: str = Field(description="Instances of gaslighting (A vs B)")
    general_red_flags: str = Field(description="Broader toxic patterns spotted")
    repair_attempts: str = Field(description="Count and type of de-escalation efforts")
    repair_success_rate: str = Field(description="How often repair attempts work (%)")
    bids_for_connection: str = Field(description="Acceptance vs rejection of bids")
    gottman_magic_ratio: str = Field(description="Estimated ratio of positive to negative interactions")

class Section7_Psychology(BaseModel):
    qualities_a: str = Field(description="Core personality traits of A")
    qualities_b: str = Field(description="Core personality traits of B")
    family_societal_pressure: str = Field(description="Level of outside pressure felt")
    attachment_style_a: str = Field(description="Inferred attachment style for A")
    attachment_style_b: str = Field(description="Inferred attachment style for B")
    primary_conflict_triggers: list[str] = Field(description="Top 3 root causes of friction")
    emotional_labor_balance: str = Field(description="Who carries the heavier load")

class Section8_Trajectory(BaseModel):
    message_volume_trend: str = Field(description="Increasing, Plateauing, or Dropping")
    sentiment_drift: str = Field(description="Warming, Cooling, or Volatile")

class Section9_Diagnosis(BaseModel):
    top_3_strengths: list[str] = Field(description="Core pillars keeping them grounded")
    anchor_partner: str = Field(description="The partner who brings stability")
    ai_positive_affirmation: str = Field(description="Affirming paragraph highlighting genuine love/resilience")
    advice_for_a: str = Field(description="Personalized communication fixes for A")
    advice_for_b: str = Field(description="Personalized communication fixes for B")
    relationship_score: int = Field(description="Final comprehensive score (0-100)")

class FullAIReport(BaseModel):
    section_2_profiles: Section2_Profiles
    section_5_green_flags: Section5_GreenFlags
    section_6_gottman: Section6_Gottman
    section_7_psychology: Section7_Psychology
    section_8_trajectory: Section8_Trajectory
    section_9_diagnosis: Section9_Diagnosis


"""
Loading the outside llm
"""


print("Initializing Gemini AI...")
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite", 
    max_retries=5
)
structured_llm = llm.with_structured_output(FullAIReport)

def analyze_chat_stats(chat_file_path):
    stats = {
        "metadata": {"dates": []},
        "general_stats": {"total_messages": 0, "late_night_messages": 0},
        "hourly_activity": {str(i): 0 for i in range(24)},
        "participants": {}
    }

    pattern = re.compile(r"^\[?(\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4})[,\]\s]+(\d{1,2}:\d{2}(?::\d{2})?[ \u202f]?(?:[aA][mM]|[pP][mM])?)\]?\s*(?:-\s*)?([^:]+):\s*(.*)$")
    
    last_sender, last_datetime = None, None

    try:
        raw_text = safe_read_file(chat_file_path)
        for line in raw_text.splitlines():
            match = pattern.match(line.strip())
            if not match: 
                continue

            date_str, time_str, sender, text = match.groups()
            sender = sender.strip()
            
            # Skip system encryption messages
            if "messages and calls are end-to-end encrypted" in text or "changed their phone number" in text:
                continue
                
            stats["metadata"]["dates"].append(date_str)
            
            if sender not in stats["participants"]:
                stats["participants"][sender] = {
                    "msg_count": 0, "word_count": 0, "char_count": 0,
                    "questions_asked": 0, "deleted_messages": 0, 
                    "double_texts": 0, "response_times_mins": []
                }
            
            p = stats["participants"][sender]
            stats["general_stats"]["total_messages"] += 1
            p["msg_count"] += 1
            p["word_count"] += len(text.split())
            p["char_count"] += len(text)
            
            if "?" in text: p["questions_asked"] += 1
            if "This message was deleted" in text or "null" in text: p["deleted_messages"] += 1

            try:
                time_clean = re.sub(r'[\u202f\u200e\u200f]', ' ', time_str).strip().upper()
                
                # Normalize AM/PM formatting for Python strptime
                if "AM" in time_clean and " AM" not in time_clean: time_clean = time_clean.replace("AM", " AM")
                if "PM" in time_clean and " PM" not in time_clean: time_clean = time_clean.replace("PM", " PM")
                
                has_seconds = time_clean.count(':') == 2
                is_ampm = "AM" in time_clean or "PM" in time_clean
                
                if is_ampm:
                    fmt = "%I:%M:%S %p" if has_seconds else "%I:%M %p"
                else:
                    fmt = "%H:%M:%S" if has_seconds else "%H:%M"
                    
                parsed_time = datetime.strptime(time_clean, fmt)
                
                current_datetime = datetime(2000, 1, 1, parsed_time.hour, parsed_time.minute, parsed_time.second)
                
                hour = current_datetime.hour
                stats["hourly_activity"][str(hour)] += 1
                if hour >= 23 or hour <= 4: stats["general_stats"]["late_night_messages"] += 1

                if last_sender:
                    if last_sender == sender:
                        p["double_texts"] += 1
                    else:
                        if last_datetime:
                            # If current message is earlier in the day than the last message, they crossed midnight.
                            if current_datetime < last_datetime:
                                current_datetime = current_datetime + timedelta(days=1)
                            
                            mins = (current_datetime - last_datetime).total_seconds() / 60.0
                            if 0 <= mins < 1440: # Ignore gaps larger than 24 hours to prevent skewed latency
                                p["response_times_mins"].append(mins)
                                
                last_datetime = current_datetime
                last_sender = sender
            except Exception:
                pass #exception handling for excess just store and ignore philosophy



    except Exception as e:
        print(f"Error reading file stats: {e}")
        return None

    if not stats["participants"]:
        return None

    for sender, data in stats["participants"].items():
        data["avg_words_per_msg"] = round(data["word_count"] / max(1, data["msg_count"]), 1)
        if data["response_times_mins"]:
            data["avg_response_time_mins"] = round(sum(data["response_times_mins"]) / len(data["response_times_mins"]), 1)
        else:
            data["avg_response_time_mins"] = 0
        del data["response_times_mins"]

    stats["metadata"]["start_date"] = stats["metadata"]["dates"][0] if stats["metadata"]["dates"] else "Unknown"
    stats["metadata"]["end_date"] = stats["metadata"]["dates"][-1] if stats["metadata"]["dates"] else "Unknown"
    del stats["metadata"]["dates"]

    peak_hour = max(stats["hourly_activity"], key=stats["hourly_activity"].get)
    stats["general_stats"]["most_active_hour"] = f"{peak_hour}:00"
    del stats["hourly_activity"]

    return stats


def query_pinecone_rag(search_query, top_k=3):
    try:
        print("Querying pinecone RAG with BAAI.")
        query_vector = embeddings.embed_query(search_query)
        response = index.query(
            vector=query_vector, top_k=top_k, include_metadata=True
        )

        matches = response.get("matches", [])
        if not matches:
            return "No relevant information found in the knowledge base."

        context_blocks = []
        for idx, match in enumerate(matches, 1):
            meta = match.get("metadata", {})
            source = meta.get("source", "Unknown_Book.pdf")
            page = meta.get("page", "?")
            text = meta.get("text", "")

            citation = f"{source} (Page {page})"
            context_blocks.append(
                f"[RAG RESULT #{idx} | Source: {citation}]\n{text.strip()}"
            )

        return "\n\n---\n\n".join(context_blocks)

    except Exception as e:
        print("Pinecone RAG Retrieval Warning:", e)
        return "RAG Knowledge Base lookup failed."


def generate_ai_report(background_text, chat_text, math_stats):
    rag_search_query = f"{background_text[:300]} {chat_text[:500]}".strip()
    rag_context = query_pinecone_rag(rag_search_query, top_k=3)

    participant_names = list(math_stats["participants"].keys())

    if len(participant_names) > 0:
        name_a = participant_names[0]
    else:
        name_a ="Person A"



    if len(participant_names) > 1:
        name_b = participant_names[1]
    else:
        name_b ="Person B"



    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a relationship psychologist and a cultural sociology expert specializing in Indian and South Asian relationship dynamics. You refer to healthy relationships through the lens on indian society feriving the teaching of famous psychologists and prominent research theories sources for which have been provided through inbuilt RAG model.
        You possess a profound understanding of the delicate interplay between modern romance, traditional expectations, family/societal pressures, and localized communication nuances. You understand indian texting dynamics on apps such as whatsapp.

        YOUR CLINICAL MANIFESTO:
        - **Bilateral Objectivity:** You maintain deep, equal empathy and analytical rigor for both Person A ({name_a}) and Person B ({name_b}). You understand both sides of every conflict and act as an impartial mirror for the relationship. You are raw with your observation and results but at the the same time constructive and you do not hallucinate conversations that do not take place.
        - **Unflinching Truth with Compassion:** You deliver measured, thoughtful opinions, but you never shy away from taking a strong, clear clinical stance when spotting destructive patterns or toxic communication loops. You do not sugarcoat reality. However, you remain cautiously optimistic and do not overstate more than the clear communication indicates.
        - **Architectural Mastery & RAG Citation Integration:** You MUST evaluate and correlate the findings in the TOP 3 RAG RESEARCH EXCERPTS below with the specific behavioral markers, personality traits, and Gottman indicators observed in the chat log. Incorporate insights from the citations directly into your analysis.
        - **Strengths-Based Focus:** While you must point out communication flaws, you MUST spend equal energy identifying the couple's underlying resilience, shared humor, and 'Green Flags'. Frame your diagnosis around growth and healing. But be brutally honest. Point out mistakes. Criticise openly. Do not be a fake positive beacon.
        
        TOP 3 RAG RESEARCH EXCERPTS (FROM KNOWLEDGE BASE):
        {rag_context}

        Analyze the provided quantitative chat metrics, background narrative, raw transcripts, and the TOP 3 RAG RESULTS above to construct your final diagnostic report. Spend your time carefully ananlysing these chats and place some weightage on the provided background as well.
        MAPPING: Person A = {name_a}, Person B = {name_b}.
        Fill out all subjective and psychological sections requested in the schema."""),
        ("human", """BACKGROUND:\n{background}\n\nQUANTITATIVE STATS:\n{stats}\n\nCHAT:\n{chat}""")
    ])
    
    chain = prompt | structured_llm
    print(f"Gemini + BAAI RAG is diagnosing the relationship between {name_a} and {name_b}...")
    
    result = chain.invoke({
        "name_a": name_a, 
        "name_b": name_b,
        "rag_context": rag_context,
        "background": background_text,
        "stats": json.dumps(math_stats),
        "chat": chat_text
    })
    
    return result.model_dump()


def rawdataextract(message):
    user_text = getattr(message, 'text', "")
    raw_media = getattr(message, 'media', [])
    customer_id = getattr(message, 'customer_id', 'Unknown_User')

    media_list = []
    for m in (raw_media or []):
        if isinstance(m, dict):
            fname = m.get('name') or m.get('filename') or 'chat.txt'
            furl = m.get('url') or m.get('download_url') or m.get('file_url') or m.get('link') or ''
            fcontent = m.get('content') or m.get('data') or m.get('bytes') or None
        else:
            fname = getattr(m, 'name', getattr(m, 'filename', 'chat.txt'))
            furl = getattr(m, 'url', getattr(m, 'download_url', getattr(m, 'file_url', getattr(m, 'link', ''))))
            fcontent = getattr(m, 'content', getattr(m, 'data', None))
        
        if "api.telegram.orgfile" in furl:
            furl = furl.replace("api.telegram.orgfile", "api.telegram.org/file")

        media_list.append({"filename": fname, "url": furl, "content": fcontent, "raw_data": m})

    return {
        "sender_id": customer_id,
        "text": user_text if user_text else "",
        "attachments": media_list
    }


def teach_rag_new_patterns(ai_report, raw_chat, math_stats):
    """
    Anonymizes the chat, extracts deep clinical insights, and stores them in Pinecone.
    Uses vector space for searchability and metadata for deep storage.
    """
    try:
        print("Extracting deep learnings and anonymizing chat...")
        
        participant_names = list(math_stats["participants"].keys())
        anon_chat = raw_chat
        
        for i, name in enumerate(participant_names):
            anon_chat = re.sub(re.escape(name), f"Partner_{chr(65+i)}", anon_chat, flags=re.IGNORECASE)
            
        anon_chat = re.sub(r'\+?\d{10,14}', '[REDACTED_NUMBER]', anon_chat)
        
        chat_sample = anon_chat[-3000:] 

        diag = ai_report.get('section_9_ai_diagnosis', {})
        psych = ai_report.get('section_7_psychological_factors', {})
        gottman = ai_report.get('section_6_gottman_conflict_markers', {})
        green = ai_report.get('section_5_positive_behavioral_markers', {})
        traj = ai_report.get('section_8_trend_analysis', {})

        strengths = ", ".join(diag.get('top_3_strengths', []))
        triggers = ", ".join(psych.get('primary_conflict_triggers', []))
        

        search_text = (
            f"Case Study of South Asian relationship dynamic. "
            f"Attachment Styles: {psych.get('attachment_style_a', 'N/A')} and {psych.get('attachment_style_b', 'N/A')}. "
            f"Conflict Triggers: {triggers}. Strengths: {strengths}. "
            f"Gottman Repair Success: {gottman.get('repair_success_rate', 'N/A')}. "
            f"Sentiment Drift is {traj.get('sentiment_drift', 'N/A')}."
        )


        #creating the load

        full_retrieval_payload = f"""
        [EMPIRICAL CASE STUDY - CASPIAN ARCHIVE]
        
        CLINICAL OVERVIEW:
        - Attachment Dynamics: {psych.get('attachment_style_a', 'N/A')} and {psych.get('attachment_style_b', 'N/A')}
        - Gottman Magic Ratio: {gottman.get('gottman_magic_ratio', 'N/A')}
        - Repair Success Rate: {gottman.get('repair_success_rate', 'N/A')}
        - Core Triggers: {triggers}
        - Stabilizing Pillars: {strengths}
        
        AI DIAGNOSTIC ADVICE PREVIOUSLY GIVEN:
        - To Partner A: {diag.get('advice_for_a', 'N/A')}
        - To Partner B: {diag.get('advice_for_b', 'N/A')}

        ANONYMIZED RAW CHAT SAMPLE (For context on how they speak):
        {chat_sample}
        """

        #sending the chat to RAG 

        vector = embeddings.embed_query(search_text)
        vector_id = f"caspian_case_{uuid.uuid4().hex[:8]}"
        
        index.upsert(
            vectors=[{
                "id": vector_id, 
                "values": vector, 
                "metadata": {
                    "source": "Anonymized_Caspian_Data", 
                    "type": "empirical_real_life_case_study",
                    "text": full_retrieval_payload 
                }
            }]
        )
        print(f"Deep Case Study Stored Successfully! Vector ID: {vector_id}")

    except Exception as e:
        print(f"RAG Deep Learning Failed (Skipping): {e}")

def submit_proof_on_chain(zk_proof_json: str) -> str:
    """Submits the ZK proof to the Sepolia Smart Contract via the Relayer."""
    if not relayer_account:
        return "Simulated_Tx_Hash_No_Private_Key"
        
    try:
        proof_data = json.loads(zk_proof_json)
        
        # Parse Semaphore values
        root = int(proof_data["merkleTreeRoot"])
        nullifier_hash = int(proof_data["nullifierHash"])
        
        # Format signal and external nullifier
        signal_val = proof_data["signal"]
        ext_null_val = proof_data["externalNullifier"]
        signal = int(signal_val) if str(signal_val).isdigit() else int(Web3.keccak(text=str(signal_val)).hex(), 16)
        ext_nullifier = int(ext_null_val) if str(ext_null_val).isdigit() else int(Web3.keccak(text=str(ext_null_val)).hex(), 16)
        
        proof_points = [int(x) for x in proof_data["proof"]]

        # Build and send transaction
        nonce = w3.eth.get_transaction_count(relayer_account.address)
        txn = contract.functions.verifyAndRecord(
            root, nullifier_hash, signal, ext_nullifier, proof_points
        ).build_transaction({
            'from': relayer_account.address,
            'nonce': nonce,
            'gas': 500000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 11155111
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=RELAYER_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        print(f"Waiting for blockchain confirmation... Tx Hash: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status != 1:
            raise Exception("Smart contract transaction reverted (Possible double-spend or invalid proof).")
            
        return receipt.transactionHash.hex()
        
    except Exception as e:
        print(f"On-chain verification error: {str(e)}")
        raise ValueError(f"On-chain verification failed: {str(e)}")

@app.post("/api/analyze")
async def http_analyze_chat(
    background: str = Form(...),
    zk_proof: str = Form(None), # <--- Semaphore Zero-Knowledge proof parameter integrated
    chat_file: UploadFile = File(...)
):
    if not chat_file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    try:
        tx_hash = None
        # --- NEW BLOCKCHAIN GATEWAY ---
        if zk_proof:
            try:
                print("\n[HTTP] 0. Validating ZK Proof on Sepolia Smart Contract...")
                tx_hash = submit_proof_on_chain(zk_proof)
                print(f"[HTTP] ZK Proof Verified! Tx Hash: {tx_hash}")
            except ValueError as ve:
                # If the smart contract rejects the proof, stop the API completely.
                raise HTTPException(status_code=403, detail=str(ve))

        # --- REST OF YOUR EXISTING PIPELINE ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_folder = os.path.join(os.getcwd(), "Web_Clients", f"Session_{timestamp}")
        os.makedirs(user_folder, exist_ok=True)

        # saving
        target_chat_path = os.path.join(user_folder, f"chat_{timestamp}.txt")
        with open(target_chat_path, "wb") as buffer:
            shutil.copyfileobj(chat_file.file, buffer)

        background_path = os.path.join(user_folder, f"background_{timestamp}.txt")
        with open(background_path, "w", encoding="utf-8") as f:
            f.write(background)

        # pipeline
        print("\n[HTTP] 1. Running Math Engine...")
        math_stats = analyze_chat_stats(target_chat_path)
        if not math_stats:
            raise HTTPException(status_code=400, detail="Invalid WhatsApp chat format.")

        chat_text = safe_read_file(target_chat_path)

        print("\n[HTTP] 2. Running Gemini + RAG Diagnostics...")
        genenrator = generate_ai_report(background, chat_text, math_stats)

        print("\n[HTTP] 3. Compiling Final JSON & Generating PDF...")
        

        final_report = {
            "section_1_transcript_metadata": {
                "chat_platform": "WhatsApp",
                "date_range": f"{math_stats['metadata'].get('start_date')} to {math_stats['metadata'].get('end_date')}",
                "total_files_analyzed": 1,
                "blockchain_verification": tx_hash 
            },
            "section_2_profiles_and_baseline": genenrator["section_2_profiles"],
            "section_3_quantitative_metrics": {
                "total_messages": math_stats["general_stats"]["total_messages"],
                "late_night_messages": math_stats["general_stats"]["late_night_messages"],
                "most_active_hour": math_stats["general_stats"]["most_active_hour"],
                "participant_breakdown": math_stats["participants"]
            },
            "section_4_latency_and_responsiveness": {
                name: {"avg_response_time_mins": metrics["avg_response_time_mins"]} 
                for name, metrics in math_stats["participants"].items()
            },
            "section_5_positive_behavioral_markers": genenrator["section_5_green_flags"],
            "section_6_gottman_conflict_markers": genenrator["section_6_gottman"],
            "section_7_psychological_factors": genenrator["section_7_psychology"],
            "section_8_trend_analysis": genenrator["section_8_trajectory"],
            "section_9_ai_diagnosis": genenrator["section_9_diagnosis"]
        }

        pdf_path = os.path.join(user_folder, f"Relationship_Report_{timestamp}.pdf")
        reportlabdirectpdfconvertor(final_report, pdf_path)
        
        teach_rag_new_patterns(final_report, chat_text, math_stats)

        print("\n[HTTP] 4. Uploading PDF report to free host...")
        download_url = link_generato_for_file(pdf_path)

        if not download_url:
            raise HTTPException(status_code=500, detail="Failed to generate PDF link.")

        return {
            "status": "success",
            "download_url": download_url,
            "report_data": final_report
        }

    except Exception as e:
        print(f"[HTTP] ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@client.on_message
def handle_message(message):
    try:
        data = rawdataextract(message)
        #timestamp folder for compliance
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_folder = os.path.join(os.getcwd(), "Caspian_Clients", f"Session_{timestamp}")
        os.makedirs(user_folder, exist_ok=True)
        
        background_path, target_chat_path = None, None

        if data['text'].strip():
            background_path = os.path.join(user_folder, f"background_{timestamp}.txt")
            with open(background_path, "w", encoding="utf-8") as f: 
                f.write(data['text'])
            print(f"Background saved: {background_path}")
        
        if data['attachments']:
            for file in data['attachments']:
                base_name, ext = os.path.splitext(file['filename'])
                local_path = os.path.join(user_folder, f"{base_name}_{timestamp}{ext}")
                
                if file['url']:
                    print(f"Downloading attachment from URL: {file['filename']}...")
                    response = bolo.get(file['url'], timeout=30)
                    response.raise_for_status()
                    file_bytes = response.content
                elif file['content']:
                    print(f"Processing raw attachment content for: {file['filename']}...")
                    file_bytes = file['content']
                    if isinstance(file_bytes, str):
                        file_bytes = file_bytes.encode('utf-8')
                else:
                    print(f" Warning: No valid download URL or content found for {file['filename']}.")
                    continue

                with open(local_path, "wb") as f: 
                    f.write(file_bytes)
                
                print(f"Attachment saved: {local_path}")
                
                if ext.lower() == ".txt":
                    target_chat_path = local_path

        if target_chat_path:
            print("\n1. Running Math Engine...")
            math_stats = analyze_chat_stats(target_chat_path)
            
            if not math_stats:
                print("Error: File did not contain valid WhatsApp chat format. Aborting analysis.")
                return

            background_text = data['text'] if data['text'].strip() else "No background provided."
            
            chat_text = safe_read_file(target_chat_path)

            print("\n2. Running Gemini + RAG Diagnostics...")
            genenrator = generate_ai_report(background_text, chat_text, math_stats)
            
            print("\n3. Compiling Final 9-Section JSON & Generating PDF...")
            final_report = {
                "section_1_transcript_metadata": {
                    "chat_platform": "WhatsApp (Auto-detected)",
                    "date_range": f"{math_stats['metadata'].get('start_date')} to {math_stats['metadata'].get('end_date')}",
                    "total_files_analyzed": len(data['attachments'])
                },
                "section_2_profiles_and_baseline": genenrator["section_2_profiles"],
                "section_3_quantitative_metrics": {
                    "total_messages": math_stats["general_stats"]["total_messages"],
                    "late_night_messages": math_stats["general_stats"]["late_night_messages"],
                    "most_active_hour": math_stats["general_stats"]["most_active_hour"],
                    "participant_breakdown": math_stats["participants"]
                },
                "section_4_latency_and_responsiveness": {
                    name: {"avg_response_time_mins": metrics["avg_response_time_mins"]} 
                    for name, metrics in math_stats["participants"].items()
                },
                "section_5_positive_behavioral_markers": genenrator["section_5_green_flags"],
                "section_6_gottman_conflict_markers": genenrator["section_6_gottman"],
                "section_7_psychological_factors": genenrator["section_7_psychology"],
                "section_8_trend_analysis": genenrator["section_8_trajectory"],
                "section_9_ai_diagnosis": genenrator["section_9_diagnosis"]
            }

            json_path = os.path.join(user_folder, f"final_report_{timestamp}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(final_report, f, indent=4)
            
            pdf_path = os.path.join(user_folder, f"Relationship_Report_{timestamp}.pdf")
            reportlabdirectpdfconvertor(final_report, pdf_path)
                
            print(f"COMPLETE! Reports saved locally:\nJSON: {json_path}\nPDF: {pdf_path}")

            # making the rag learn
            teach_rag_new_patterns(final_report, chat_text, math_stats)            
            print("\n4. Uploading PDF report to free host...")
            download_url = link_generato_for_file(pdf_path)
            
            if download_url:
                print(f" Universal Shareable Link: {download_url}")
                
                success_message = (
                    "Your Relationship Diagnostic Report is ready! 🎉\n\n"
                    "You can view and download your full PDF report here:\n"
                    f"{download_url}"
                )
                
                try:
                    if hasattr(message, 'reply'):
                        message.reply(success_message)
                        print("Message containing PDF link replied directly to user.")
                    elif hasattr(client, 'send_message'):
                        client.send_message(data['sender_id'], success_message)
                        print("Message containing PDF link sent via client to user.")
                    else:
                        print("Could not auto-reply: Send method not found.")
                except Exception as send_err:
                    print(f"Error sending message to user: {send_err}")
            else:
                print("Failed to generate shareable link.")

            print("="*50)
            
    except Exception as e:
        print(" CRITICAL ERROR processing message:", e)
        print("Bot is continuing to listen for other users.")
        print("="*50)


def run_caspian_bot():
    """Runs the blocking Caspian listener in a separate thread."""


    print("Initializing robust Caspian listener on background thread...")
    while True:
        try:
            client.listen()
        except httpx.ReadTimeout:
            print("Caspian network timeout. Auto-reconnecting in 3 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Caspian connection interrupted ({e}). Auto-reconnecting in 5 seconds...")
            time.sleep(10)


if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_caspian_bot, daemon=True)
    bot_thread.start()

    
    print("Starting FastAPI HTTP Server for Next.js Frontend...")
    uvicorn.run(app, host="0.0.0.0", port=8000)