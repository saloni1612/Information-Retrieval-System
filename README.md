# Information Retrieval System 

A local chatbot that answers questions about your  PDF by extracting text, embedding it using Sentence Transformers, storing it in ChromaDB, and generating responses using a local LLM (like Mistral via Ollama).


## Features

- Extracts text from any PDF (for eg.product catalog)
- Splits text into manageable chunks
- Uses `all-MiniLM-L6-v2` for semantic search
- Stores vector embeddings in ChromaDB
- Uses Ollama (Mistral) locally for generating answers
- Fully offline — no cloud dependencies


## Requirements

- Python 3.8 or higher
- Ollama installed and running locally
- Mistral model pulled into Ollama (`ollama pull mistral`)

### Python Packages:
```bash
pip install pymupdf chromadb sentence-transformers requests
```

### How It Works
Text Extraction: Uses PyMuPDF to extract text from the PDF

Chunking: Splits the text into chunks of approximately 500 words

Embedding: Converts chunks into embeddings using all-MiniLM-L6-v2

Storage: Stores embeddings in ChromaDB

Querying: Finds relevant chunks using semantic similarity

LLM Response: Passes context to Mistral (via Ollama) to generate an answer
