import fitz  # PyMuPDF
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions


# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Step 2: Split into chunks
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

# Step 3: Embed and store in ChromaDB
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

# Step 4: Query the collection
def get_relevant_chunks(query, collection, top_k=3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results["documents"][0]

import requests

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

    print("[debug] Sending prompt to Ollama...")

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        print("[debug] Got response from Ollama.")
        data = response.json()
        return data["response"].strip()

    except Exception as e:
        print(f"[ERROR calling Mistral via Ollama]: {e}")
        return "[LLM error]"




# Main
def main():
    print("Product Catalog Chatbot (Local Mode)")
    pdf_path = input("Enter path to your catalog PDF: ").strip()

    print("→ Extracting and indexing catalog...")
    raw_text = extract_text_from_pdf(pdf_path)
    chunks = split_text(raw_text)
    collection = build_vector_db(chunks)

    print("\n Catalog ready! Ask me anything about it.")
    while True:
        query = input("\nYour Question (or 'exit'): ").strip()
        if query.lower() in ["exit", "quit"]:
            break

        top_chunks = get_relevant_chunks(query, collection)
        response = generate_response(top_chunks, query)
        print("\n Answer:\n", response)

if __name__ == "__main__":
    main()
