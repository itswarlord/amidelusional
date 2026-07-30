 <div align="center">


# Am I Delusional?


**An AI agent that gives you a realistic, unfiltered report of your relationship.**


[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python&logoColor=white)](#)

[![Gemini](https://img.shields.io/badge/LLM-Gemini_3.6_Flash-orange.svg?style=flat)](#)

[![Pinecone](https://img.shields.io/badge/VectorDB-Pinecone-lightgrey.svg?style=flat)](#)

[![LangChain](https://img.shields.io/badge/Framework-LangChain-1C3C3C.svg?style=flat&logo=langchain&logoColor=white)](#)

[![LangGraph](https://img.shields.io/badge/Agents-LangGraph-3178C6.svg?style=flat&logo=langchain&logoColor=white)](#)

[![Status](https://img.shields.io/badge/Status-Active-success.svg?style=flat)](#)


</div>


> **AmIDelusional** is an AI-powered agent designed to give you a realistic, unfiltered, and psychologically grounded report on the health of your relationship. Built strictly on the foundational research of Dr. John Gottman and Indian Psychologists to make this centered toward the Indian demographic, this agent analyzes your relationship dynamics and tells you exactly where you stand—no sugarcoating, just science. It 


---


## 🚀 Try It Live


You don't need to install anything to get a reality check. The code is already hosted on a 24/7 server. Talk to the agent directly right now for free:


*   📱 **Telegram:** [@amidelusionalbot](https://t.me/amidelusionalbot)

*   ✉️ **Email:** `agt-282ce9e5e2f667ff30594254-77e083@agents.trycaspianai.com`



Incase of any errors please contact me ASAP: vansh@iitg.ac.in

---


## 🛠️ Tech Stack & Architecture


| Component | Technology | Description |

| :--- | :--- | :--- |

| **Backend** | Python | Core logic and API integrations |

| **Core Brain** | Gemini 3.6 Flash | Fast, empathetic, yet highly analytical reasoning |

| **Agent Framework** | LangChain & LangGraph | Manages agentic workflows, stateful loops, and RAG chains |

| **Vector DB** | Pinecone | Stores and retrieves psychological context via RAG |

| **Embeddings** | `BAAI/bge-small-en-v1.5` | Fast local embeddings via Hugging Face |

| **Deployment** | Caspian AI SDK | Agent routing for seamless multi-channel access (Telegram & Email) |


---


## 📖 Complete Setup Manual (Local Installation)


If you want to run this agent locally, modify the prompts, or build upon the RAG architecture, follow these steps.


### 1. Prerequisites

You will need active API keys for the following services:

*   Google Gemini API *(Google AI Studios)*

*   Pinecone API 

*   Caspian AI *(if using their agent routing)*

*   Telegram Bot Token *(via BotFather)*

### 2. Install Dependencies


*(Note: `os`, `re`, `time`, `json`, and `datetime` are part of the Python Standard Library and do not need to be installed via pip.)*


You can install all the required external libraries directly via terminal.


```bash

pip install httpx requests python-dotenv caspian_sdk pydantic langchain-google-genai langchain-core pinecone langchain-huggingface

```


### 3. Create .env file

Create a `.env` file in the root of your project directory and add your keys securely. 


Remember never commit you API keys, it can be missused.


```env

GEMINI_API_KEY="your_gemini_api_key_here"

PINECONE_API_KEY="your_pinecone_api_key_here"

PINECONE_ENV="your_pinecone_environment_here"

CASPIAN_API_KEY="your_caspian_api_key_here"

TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"

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
