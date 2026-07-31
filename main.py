"""
BUILT by Vansh Aggarwal. File dated Jun-28.
UPDATED for 24/7 Server Deployment.
"""

import os
import re
import time
import httpx
import json
import requests as bolo
from datetime import datetime
from dotenv import load_dotenv
from caspian_sdk import CommClient
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

"""
Loading relevant agents. 
1. .env is loaded 
2. caspian_sdk is loaded 
3. pinecone and local llm loaded.
"""

load_dotenv()
client = CommClient()

client.connect_telegram(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))
client.connect_email(connection_id=os.getenv("EMAIL_CONNECTION_ID"))

print("Connecting to Pinecone and loading BAAI embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("relationship-kb")

print("Server running! Listening for Telegram and Email messages...")

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


# PERFORMANCE FIX (MOVED HERE): Initialize Gemini once at startup, 
# and now safely AFTER FullAIReport is defined!
print("Initializing Gemini AI...")
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash", 
    max_retries=5
)
structured_llm = llm.with_structured_output(FullAIReport)


"""
Calculations using python. Basic Data analysis to prevent AI based hallucinations.
"""

def analyze_chat_stats(chat_file_path):
    stats = {
        "metadata": {"dates": []},
        "general_stats": {"total_messages": 0, "late_night_messages": 0},
        "hourly_activity": {str(i): 0 for i in range(24)},
        "participants": {}
    }

    pattern = r"\[?(\d{1,2}/\d{1,2}/\d{2,4})[,\]\s]+(\d{1,2}:\d{2}(?::\d{2})?\s*[a-zA-Z]{0,2})\]?\s*(?:-\s*)?(.*?):\s*(.*)"
    last_sender, last_time = None, None

    try:
        with open(chat_file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(pattern, line.strip())
                if not match: continue

                date_str, time_str, sender, text = match.groups()
                sender = sender.strip()
                
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
                    time_clean = time_str.replace('\u202f', ' ').strip().upper()
                    has_seconds = time_clean.count(':') == 2
                    
                    if "M" in time_clean:
                        fmt = "%I:%M:%S %p" if has_seconds else "%I:%M %p"
                    else:
                        fmt = "%H:%M:%S" if has_seconds else "%H:%M"
                        
                    msg_time = datetime.strptime(time_clean, fmt)
                    
                    hour = msg_time.hour
                    stats["hourly_activity"][str(hour)] += 1
                    if hour >= 23 or hour <= 4: stats["general_stats"]["late_night_messages"] += 1

                    if last_sender:
                        if last_sender == sender:
                            p["double_texts"] += 1
                        else:
                            if last_time:
                                mins = (msg_time - last_time).total_seconds() / 60
                                if 0 <= mins < 720: p["response_times_mins"].append(mins)
                                    
                    last_time, last_sender = msg_time, sender
                except Exception:
                    pass

    except Exception as e:
        print(f"Error reading file: {e}")
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

    stats["metadata"]["start_date"] = stats["metadata"]["dates"][0]
    stats["metadata"]["end_date"] = stats["metadata"]["dates"][-1]
    del stats["metadata"]["dates"]

    peak_hour = max(stats["hourly_activity"], key=stats["hourly_activity"].get)
    stats["general_stats"]["most_active_hour"] = f"{peak_hour}:00"
    del stats["hourly_activity"]

    return stats


"""
querying pinecone
"""

def query_pinecone_rag(search_query, top_k=3):
    """
    Retrieves the TOP 3 most relevant research excerpts from Pinecone
    using BAAI/bge-small-en-v1.5 local embeddings.
    """
    try:
        print("📚 Querying Pinecone RAG with BAAI/bge-small-en-v1.5...")
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
        print(f"⚠️ Pinecone RAG Retrieval Warning: {e}")
        return "RAG Knowledge Base lookup failed."


"""
brain is working to take RAG data and relevant bg and chats to build a final report
"""

def generate_ai_report(background_text, chat_text, math_stats):
    rag_search_query = f"{background_text[:300]} {chat_text[:500]}".strip()
    rag_context = query_pinecone_rag(rag_search_query, top_k=3)

    participant_names = list(math_stats["participants"].keys())
    name_a = participant_names[0] if len(participant_names) > 0 else "Person A"
    name_b = participant_names[1] if len(participant_names) > 1 else "Person B"

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an elite, Gottman-certified clinical relationship psychologist and a cultural sociology expert specializing in Indian and South Asian relationship dynamics. 
        You possess a profound understanding of the delicate interplay between modern romance, traditional expectations, family/societal pressures, and localized communication nuances.

        YOUR CLINICAL MANIFESTO:
        - **Bilateral Objectivity:** You maintain deep, equal empathy and analytical rigor for both Person A ({name_a}) and Person B ({name_b}). You understand both sides of every conflict and act as an impartial mirror for the relationship.
        - **Unflinching Truth with Compassion:** You deliver measured, thoughtful opinions, but you never shy away from taking a strong, clear clinical stance when spotting destructive patterns or toxic communication loops. You do not sugarcoat reality. However, you remain cautiously optimistic and do not overstate more than the clear communication indicates.
        - **Architectural Mastery & RAG Citation Integration:** You MUST evaluate and correlate the findings in the TOP 3 RAG RESEARCH EXCERPTS below with the specific behavioral markers, personality traits, and Gottman indicators observed in the chat log. Incorporate insights from the citations directly into your analysis.
        - **Strengths-Based Focus:** While you must point out communication flaws, you MUST spend equal energy identifying the couple's underlying resilience, shared humor, and 'Green Flags'. Frame your diagnosis around growth and healing. But be brutally honest. Point out mistakes. Criticise openly. Do not be a fake positive beacon.
        
        ====================================================
        TOP 3 RAG RESEARCH EXCERPTS (FROM KNOWLEDGE BASE):
        {rag_context}
        ====================================================

        Analyze the provided quantitative chat metrics, background narrative, raw transcripts, and the TOP 3 RAG RESULTS above to construct your final diagnostic report.
        MAPPING: Person A = {name_a}, Person B = {name_b}.
        Fill out all subjective and psychological sections requested in the schema."""),
        ("human", """BACKGROUND:\n{background}\n\nQUANTITATIVE STATS:\n{stats}\n\nCHAT:\n{chat}""")
    ])
    
    chain = prompt | structured_llm
    print(f"🧠 Gemini + BAAI RAG is diagnosing the relationship between {name_a} and {name_b}...")
    
    result = chain.invoke({
        "name_a": name_a, 
        "name_b": name_b,
        "rag_context": rag_context,
        "background": background_text,
        "stats": json.dumps(math_stats),
        "chat": chat_text
    })
    
    return result.model_dump()


"""
 DATA EXTRACTION & MASTER LISTENER
"""

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

@client.on_message
def handle_message(message):
    # ERROR HANDLING FIX: Wrapped everything in try/except to prevent the loop from dying
    try:
        data = rawdataextract(message)
        user_id = str(data['sender_id'])
        
        # FILE PATH FIX: Saves to the current working directory, not a non-existent GUI Desktop
        user_folder = os.path.join(os.getcwd(), "Caspian_Clients", user_id)
        os.makedirs(user_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        background_path, target_chat_path = None, None

        # 1. Save Text (Background)
        if data['text'].strip():
            background_path = os.path.join(user_folder, f"background_{timestamp}.txt")
            with open(background_path, "w", encoding="utf-8") as f: 
                f.write(data['text'])
            print(f"Background saved: {background_path}")
        
        # 2. Save Attachments
        if data['attachments']:
            for file in data['attachments']:
                base_name, ext = os.path.splitext(file['filename'])
                local_path = os.path.join(user_folder, f"{base_name}_{timestamp}{ext}")
                
                # If we have a URL (Telegram), download it via requests
                if file['url']:
                    print(f"Downloading attachment from URL: {file['filename']}...")
                    response = bolo.get(file['url'], timeout=30)
                    response.raise_for_status()
                    file_bytes = response.content
                
                # If we have raw content/bytes instead (Email SDK), use that directly
                elif file['content']:
                    print(f"Processing raw attachment content for: {file['filename']}...")
                    file_bytes = file['content']
                    if isinstance(file_bytes, str):
                        file_bytes = file_bytes.encode('utf-8')
                
                else:
                    print(f" Warning: No valid download URL or content found for {file['filename']}.")
                    print(f" DEBUG Raw Attachment Data: {file['raw_data']}")
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
            
            with open(target_chat_path, "r", encoding="utf-8") as f:
                chat_text = f.read()

            print("\n2. Running Gemini + RAG Diagnostics...")
            ai_stats = generate_ai_report(background_text, chat_text, math_stats)
            
            print("\n3. Compiling Final 9-Section JSON...")
            final_report = {
                "section_1_transcript_metadata": {
                    "chat_platform": "WhatsApp (Auto-detected)",
                    "date_range": f"{math_stats['metadata'].get('start_date')} to {math_stats['metadata'].get('end_date')}",
                    "total_files_analyzed": len(data['attachments'])
                },
                "section_2_profiles_and_baseline": ai_stats["section_2_profiles"],
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
                "section_5_positive_behavioral_markers": ai_stats["section_5_green_flags"],
                "section_6_gottman_conflict_markers": ai_stats["section_6_gottman"],
                "section_7_psychological_factors": ai_stats["section_7_psychology"],
                "section_8_trend_analysis": ai_stats["section_8_trajectory"],
                "section_9_ai_diagnosis": ai_stats["section_9_diagnosis"]
            }

            # Save Final JSON
            json_path = os.path.join(user_folder, f"final_report_{timestamp}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(final_report, f, indent=4)
                
            print(f"\nCOMPLETE! Final RAG-Enhanced 9-Section Report saved to: {json_path}")
            print("="*50)
            
    except Exception as e:
        print(f" CRITICAL ERROR processing message: {e}")
        print("Bot is continuing to listen for other users.")
        print("="*50)

if __name__ == "__main__":
    print("Initializing robust listener...")
    while True:
        try:
            client.listen()
        except httpx.ReadTimeout:
            print("Network timeout (waiting for messages). Auto-reconnecting in 3 seconds...")
            time.sleep(3)
        except Exception as e:
            print(f"Connection interrupted ({e}). Auto-reconnecting in 5 seconds...")
            time.sleep(5)