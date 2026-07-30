import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone

# 1. Load Environment Variables
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

if not google_api_key or not pinecone_api_key:
    raise ValueError(
        "Missing GEMINI_API_KEY or PINECONE_API_KEY in .env file."
    )

# 2. Connect to Pinecone & Load BAAI Embeddings
print("Connecting to Pinecone and loading BAAI embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

pc = Pinecone(api_key=pinecone_api_key)
index_name = "relationship-kb"
index = pc.Index(index_name)

# 3. Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite", 
    google_api_key=google_api_key,
    temperature=0.3)

def query_rag(question: str, top_k: int = 4):
    # Embed question and query Pinecone
    query_vector = embeddings.embed_query(question)
    response = index.query(
        vector=query_vector, top_k=top_k, include_metadata=True
    )

    matches = response.get("matches", [])
    if not matches:
        return "No relevant information found in the knowledge base.", []

    # Build context block and collect source citations
    context_blocks = []
    sources = []

    for match in matches:
        meta = match.get("metadata", {})
        source = meta.get("source", "Unknown_Book.pdf")
        page = meta.get("page", "?")
        text = meta.get("text", "")

        citation = f"{source} (Page {page})"
        if citation not in sources:
            sources.append(citation)

        context_blocks.append(f"[Source: {citation}]\n{text}")

    combined_context = "\n\n---\n\n".join(context_blocks)

    # Prompt Gemini
    prompt = f"""
You are an expert relationship assistant. Answer the user's question accurately using ONLY the context provided below.
Always cite the source book name and page number when stating facts or advice.

Context from Knowledge Base:
{combined_context}

Question: {question}

Answer:
"""

    answer = llm.invoke(prompt)
    return answer.content, sources


def main():
    print("\n" + "=" * 55)
    print(" Relationship RAG Assistant Loaded & Ready!")
    print("Type your question below. Type 'exit' or 'quit' to stop.")
    print("=" * 55 + "\n")

    while True:
        try:
            user_input = input("\nUser: ").strip()

            # Skip empty inputs
            if not user_input:
                continue

            # Exit condition
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nExiting chat. Good luck with the hackathon!")
                break

            print("\n🔍 Searching Pinecone...")
            answer, sources = query_rag(user_input)

            # Print source documents used
            if sources:
                print("\n📚 [Sources Found]")
                for src in sources:
                    print(f"  • {src}")

            # Print Gemini's response
            print("\n🤖 [Assistant]")
            print(answer)

        except KeyboardInterrupt:
            print("\n\nExiting chat...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()