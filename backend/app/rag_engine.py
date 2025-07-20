# import fitz  # PyMuPDF
# from sentence_transformers import SentenceTransformer
# import chromadb
# from chromadb.utils import embedding_functions
# import requests

# # --- PDF Text Extraction ---
# def extract_text_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text

# # --- Text Chunking ---
# def split_text(text, max_chunk_size=500):
#     words = text.split()
#     chunks = []
#     current = []
#     for word in words:
#         current.append(word)
#         if len(current) >= max_chunk_size:
#             chunks.append(" ".join(current))
#             current = []
#     if current:
#         chunks.append(" ".join(current))
#     return chunks

# # --- Vector DB Build ---
# def build_vector_db(chunks):
#     model = SentenceTransformer("all-MiniLM-L6-v2")
#     embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
#     chroma_client = chromadb.Client()
#     collection = chroma_client.create_collection(name="catalog", embedding_function=embed_fn)
#     for i, chunk in enumerate(chunks):
#         collection.add(
#             documents=[chunk],
#             ids=[f"chunk_{i}"],
#             metadatas=[{"source": "catalog"}]
#         )
#     return collection

# # --- RAG Query ---
# def get_relevant_chunks(query, collection, top_k=3):
#     results = collection.query(
#         query_texts=[query],
#         n_results=top_k
#     )
#     return results["documents"][0]

# # --- Local LLM (Ollama) ---
# def generate_response(context_chunks, query):
#     context = "\n".join(context_chunks)
#     prompt = f"""
# You are a helpful assistant for answering product catalog questions.

# Context:
# {context}

# Question:
# {query}

# Answer:
# """
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={"model": "mistral", "prompt": prompt, "stream": False}
#         )
#         return response.json()["response"].strip()
#     except Exception as e:
#         return "[LLM Error] " + str(e)


import os
from typing import List
from chromadb import PersistentClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from app.llm import query_llm as generate_response

CHROMA_DIR = "chroma"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Small, fast, and good enough

# Load embedding model
embedder = SentenceTransformer(EMBEDDING_MODEL)

# Setup ChromaDB
client = PersistentClient(path=CHROMA_DIR, settings=Settings(allow_reset=True))
collection = client.get_or_create_collection(name="business_docs")

CHUNK_SIZE = 300
OVERLAP = 50

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=OVERLAP) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def add_to_vectorstore(text: str, business_id: str):
    chunks = chunk_text(text)
    embeddings = embedder.encode(chunks).tolist()

    ids = [f"{business_id}_{i}" for i in range(len(chunks))]
    metadata = [{"business_id": business_id} for _ in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata,
        ids=ids
    )

def query_vectorstore(question: str, business_id: str, top_k=3) -> List[str]:
    q_embedding = embedder.encode(question).tolist()
    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=top_k,
        where={"business_id": business_id}
    )
    return results["documents"][0] if results["documents"] else []


def embed_and_store(business_id: str, text: str):
    add_to_vectorstore(text, business_id)

def query_pdf(business_id: str, question: str) -> str:
    chunks = query_vectorstore(question, business_id)
    context = "\n".join(chunks)
    prompt = f"""You are a helpful assistant for answering product catalog questions.

Context:
{context}

Question:
{question}

Answer:"""
    return generate_response(prompt)
