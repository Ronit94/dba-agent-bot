import logging
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
import os
from app.services.ingest import pdf_to_text_bytes,chunk_text,read_pdf
router = APIRouter()
from langchain_community.document_loaders import PyPDFLoader
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing_extensions import List, TypedDict
from fastapi_limiter.depends import RateLimiter


@router.post("/data/pdf", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def pdf_ingestion(file: UploadFile = File(...), request: Request = None):
    """
    Ingest a PDF file, extract text, chunk it, and store in Pinecone.
    """
    vector_store = request.app.state.vector_store
    upload_dir = request.app.state.UPLOAD_DIR
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    logging.info(f"Received file: {file.filename}")
    file_path = upload_dir / file.filename

    uuid_val = uuid.uuid4()

    file_path = os.path.join(os.getcwd(),upload_dir, f"{uuid_val}_{file.filename}")

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    logging.info(f"Saving uploaded file to {file_path}")

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)

    _ = vector_store.add_documents(documents=all_splits)

    os.remove(file_path)  # Clean up the saved file after reading

    # chunks = await chunk_text(content)

    return {"filename": file.filename, "file_content": docs[0].page_content[:500], "session_id":uuid_val}  # Return first 1000 characters for brevity


    
    
    