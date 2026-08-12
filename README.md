
<div align="center">

# Am I Delusional?

**An AI agent that uses Zero-Knowledge cryptography and clinical psychology to give you a ruthless, unfiltered report of your relationship.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python&logoColor=white)](#)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js-black.svg?style=flat&logo=next.js&logoColor=white)](#)
[![Web3](https://img.shields.io/badge/Web3-Semaphore_ZK-purple.svg?style=flat)](#)
[![Gemini](https://img.shields.io/badge/LLM-Gemini_3.5_Flash-orange.svg?style=flat)](#)
[![Pinecone](https://img.shields.io/badge/VectorDB-Pinecone-lightgrey.svg?style=flat)](#)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-1C3C3C.svg?style=flat&logo=langchain&logoColor=white)](#)
[![Status](https://img.shields.io/badge/Status-Active-success.svg?style=flat)](#)

</div>

> **AmIDelusional** is an AI-powered agent designed to give you a realistic, unfiltered, and psychologically grounded report on the health of your relationship. Built for the IITG.eth Hackathon, this agent analyzes your relationship dynamics and tells you exactly where you stand. Oh, and it uses Ethereum Zero-Knowledge proofs so you can get wrecked by the AI with absolute privacy.

---

## 🚀 The TL;DR (What is this actually?)

Officially, **Am I Delusional?** is a privacy-preserving, AI-powered clinical evaluator that analyzes raw WhatsApp chat exports. It leverages Semaphore Zero-Knowledge proofs on the Ethereum Sepolia network to guarantee absolute anonymity before processing sensitive telemetry through a custom Gemini + Pinecone RAG pipeline.

The USP of this product is the unique training method with 100 yrs worth of real Indian Relationships. True trained hyper-locally with research papers from famous Indian researchers. Real chat data with no AI non-sense uploaded to custom train the model and the RAG model. I take pride in the training of this model. We pick up western philosophy indianise it with Indian values and understanding Indian family structures to give real advice.

Genuinely try our legacy agents here:
*   **Telegram:**  [@amidelusionalbot](https://t.me/amidelusionalbot)
*    **WEBSITE:**  http://34.14.222.173:3000/

---

## 🛠️ The  Tech Stack

| Component | Technology | Why we used it (and suffered for it) |
| :--- | :--- | :--- |
| **Frontend** | Next.js, React, Tailwind | Beautiful UI where you drag-and-drop your toxic chats. |
| **Privacy Layer** | Semaphore Protocol | A zero-knowledge tool developed by the Ethereum Foundation's PSE team that generates ZK proofs locally in the browser so you don't dox yourself. Along with server level smart contract.|
| **Smart Contract** | Ethereum (Sepolia Testnet) | Verifies the ZK proof on-chain to prevent double-spending. |
| **Backend / Relayer** | FastAPI & Web3.py | Bypasses glitchy MetaMask popups by programmatically paying gas and relaying transactions to the blockchain. |
| **Core Brain** | Gemini 3.5 Flash | Provides near-Pro intelligence with a massive 1M token context window, analyzing your red flags at lightning speed. |
| **Vector DB** | Pinecone | Stores and retrieves clinical psychology context via RAG. |
| **Embeddings** | `BAAI/bge-en-v1.5` | Fast local embeddings via Hugging Face. |
| **Artifact Gen** | ReportLab | Generates the ultimate PDF receipt directly from Python so you can win the argument. |

---

## 📖 Complete Setup Manual (Local Installation)

If you want to run this agent locally, modify the prompts, or experience the joy of compiling `.wasm` circuits, follow these steps.

### 1. Prerequisites
You will need active API keys and a wallet with Sepolia ETH:
*   **Google Gemini API** 
*   **Pinecone API**
*   **Ethereum Private Key** *(A MetaMask wallet holding Sepolia ETH for the relayer)*
*   **Telegram Bot Token & Caspian SDK** *(For the listener bots)*

### 2. Backend Setup (The Python Relayer)
Install the dependencies (including `web3` for our sanity-saving relayer):
```bash
pip install fastapi uvicorn python-multipart reportlab google-generativeai web3 python-dotenv caspian_sdk pydantic langchain-google-genai langchain-core pinecone langchain-huggingface
```


### 3. Create .env file

Create a `.env` file in the root of your project directory and add your keys securely. 


Remember never commit you API keys, it can be missused.


```env

GEMINI_API_KEY="your_gemini_key"
PINECONE_API_KEY="your_pinecone_key"
TELEGRAM_BOT_TOKEN="your_telegram_token"
EMAIL_CONNECTION_ID="your_caspian_email_id"
# The wallet that pays the gas so your users don't have to:
RELAYER_PRIVATE_KEY="your_ethereum_private_key"

```


### 4. Finally run the program

Run the command:

```bash

python main.py

```

Feed the data through your desired channels and wait for the report to be generated and sent as a reply.



## What I have done till now?


- [ ] **Chat Log Analysis:** Allow users to upload exported WhatsApp or iMessage text files for the agent to analyze tone, conflict resolution styles, and response times.

- [x] **Integrated Modern Psych Research:** Taken contemporary literature on healthy relationships and built a RAG model deployed on Pinecone. Upon testing the RAG model it is giving extremely useful snippets for the AI agent to analyse.

- [x] **Built the RAG Pipeline:** Successfully implemented Pinecone to retrieve relevant psychological context and embedded it using the lightweight, fast `BAAI/bge-small-en-v1.5` model.
    
- [x] **Integrated Semaphore Based Privacy:** 2 Stage privacy at server level and browser level with layered encryption for data.

- [x] **Connected the "Brain":** Hooked up Gemini 3.6 Flash as the core reasoning engine for fast, empathetic, yet highly analytical responses.

- [x] **Multi-Channel Deployment:** Successfully routed the agent through Caspian AI to enable seamless, concurrent user access via Telegram and Email.

- [x] **Schema & Validation:** Implemented Pydantic for robust data validation and structured outputs.

- [x] **Reply in Basic PDF:** Implemented json to pdf conversion within python to return pdf file to end user as a "relationship report."

- [x] **Hosted on 24/7 Server:** Hosted on server so listener is active 24/7 with enough credits to analyse and generate reports autonomously.


## Future Plans:


- [ ] **Long-Term Memory:** Allowing personalization based on client. Build a profile to give more specific answers and requires no need to give context each time it is run.

- [ ] **Expanded Platform Support:** Deploy the bot to Instagram(the graveyard of relationships), discord and whatsapp natively.

- [ ] **Voice Note Processing:** Integrate speech-to-text models to allow users to send voice notes of arguments (or their feelings) to analyze vocal tone and emotion.

- [ ] **Interactive Dashboard:** Build a web frontend (e.g., Streamlit or React) to give users a visual "Relationship Health Scorecard."

- [ ] **Partner Compatibility Mode:** Create a flow where both partners can submit their perspectives independently to generate a unified conflict-resolution report.

- [ ] **Live Relationship Score Integration:** Future where messages are being tracked real-time to give real-time relationship status and advice to the partner.


## Contact Me:
Please reach out if you want to collaborate. Email ID: vansh@iitg.ac.in
