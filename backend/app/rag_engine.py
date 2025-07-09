import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import requests

# --- PDF Text Extraction ---
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# --- Text Chunking ---
def split_text(text, max_chunk_size=500):
    words = text.split()
    chunks = []
    current = []
    for word in words:
        current.append(word)
        if len(current) >= max_chunk_size:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks

# --- Vector DB Build ---
def build_vector_db(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="catalog", embedding_function=embed_fn)
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"chunk_{i}"],
            metadatas=[{"source": "catalog"}]
        )
    return collection

# --- RAG Query ---
def get_relevant_chunks(query, collection, top_k=3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results["documents"][0]

# --- Local LLM (Ollama) ---
def generate_response(context_chunks, query):
    context = "\n".join(context_chunks)
    prompt = f"""
You are a helpful assistant for answering product catalog questions.

Context:
{context}

Question:
{query}

Answer:
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        return response.json()["response"].strip()
    except Exception as e:
        return "[LLM Error] " + str(e)
