from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.rag_engine import extract_text_from_pdf, split_text, build_vector_db, get_relevant_chunks, generate_response
import shutil
import os

app = FastAPI()

# CORS for React/frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory reference to vector DB
collection = None

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save file
    upload_path = f"uploads/{file.filename}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Build vector DB
    global collection
    raw_text = extract_text_from_pdf(upload_path)
    chunks = split_text(raw_text)
    collection = build_vector_db(chunks)

    return {"message": "PDF uploaded and indexed successfully."}


@app.post("/query/")
async def query_pdf(question: str = Form(...)):
    global collection
    if collection is None:
        return {"error": "No PDF uploaded yet. Please upload a PDF first."}

    top_chunks = get_relevant_chunks(question, collection)
    answer = generate_response(top_chunks, question)
    return {"answer": answer}
