import hashlib
import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Load environment variables
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# 2. Connect to Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index_name = "relationship-kb" 
index = pc.Index(index_name)

# 3. Load all PDFs
print("Loading PDFs from knowledge_base folder...")
loader = PyPDFDirectoryLoader("knowledge_base/") 
raw_documents = loader.load()
print(f"Loaded {len(raw_documents)} total pages.")

# 4. Split raw text into chunks
print("Splitting text into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = text_splitter.split_documents(raw_documents)
print(f"Created {len(chunks)} chunks of text.")

# 5. Initialize Local HuggingFace Embeddings (100% Free, NO LIMITS)
print("Downloading local AI model (only happens once)...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# 6. Batch embed and upload directly to Pinecone (No rate limits!)
print("Converting to vectors and uploading to Pinecone fast...")
batch_size = 100  # We can do bigger batches now!

for i in range(0, len(chunks), batch_size):
    batch_chunks = chunks[i:i + batch_size]
    texts = [chunk.page_content for chunk in batch_chunks]
    
    # Clean Metadata
    metadatas = []
    for chunk in batch_chunks:
        raw_source = chunk.metadata.get("source", "Unknown_Book.pdf")
        clean_file_name = os.path.basename(raw_source)
        raw_page = chunk.metadata.get("page", 0)
        
        metadatas.append({
            "source": clean_file_name,
            "page": int(raw_page) + 1,
            "text": chunk.page_content
        })

    # Unique IDs
    batch_ids = []
    for j, chunk in enumerate(batch_chunks):
        source_path = chunk.metadata.get("source", "doc")
        file_name = os.path.basename(source_path)
        clean_name = "".join(c for c in file_name if c.isalnum() or c in ("_", "-"))
        content_hash = hashlib.md5(chunk.page_content.encode("utf-8")).hexdigest()[:8]
        batch_ids.append(f"{clean_name}_{i + j}_{content_hash}")
    
    # Instant Upload (No sleep/pauses needed!)
    vector_embeddings = embeddings.embed_documents(texts)
    records = zip(batch_ids, vector_embeddings, metadatas)
    index.upsert(vectors=records)
    print(f"Successfully uploaded chunks {i} to {i + len(batch_chunks)} of {len(chunks)}...")

print("\nSUCCESS! Your entire library is uploaded.")

