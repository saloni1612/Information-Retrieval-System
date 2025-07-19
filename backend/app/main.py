from fastapi import FastAPI, UploadFile, Form, HTTPException,File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.models import init_db, add_business, get_businesses
from app.utils import save_pdf, extract_text_from_pdf
from app.rag_engine import embed_and_store, query_pdf

app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.get("/businesses")
def get_all_businesses():
    return get_businesses()

@app.post("/upload")
async def upload_catalog(
    name: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDFs allowed")

    file_path = save_pdf(file, name)
    text = extract_text_from_pdf(file_path)
    embed_and_store(name, text)
    add_business(name, category, file_path)
    return {"message": "Uploaded successfully"}

@app.post("/ask")
async def ask_question(name: str = Form(...), question: str = Form(...)):
    try:
        answer = query_pdf(name, question)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(content={"answer": f"[LLM Error] {str(e)}"}, status_code=500)

