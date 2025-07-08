from fastapi import FastAPI, UploadFile, Form
from chatbot import ask_question
from pdf_utils import extract_text_from_pdf
from vector_store import store_embeddings, query_embeddings

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile):
    text = extract_text_from_pdf(await file.read())
    store_embeddings(text)
    return {"message": "PDF processed"}

@app.post("/query/")
async def query_product(question: str = Form(...)):
    context = query_embeddings(question)
    response = ask_question(question, context)
    return {"answer": response}
