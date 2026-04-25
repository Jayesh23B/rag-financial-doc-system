from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

from app.db.database import SessionLocal
from app.db import models
from app.dependencies import get_current_user

from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.embedding import get_embedding
from app.utils.chunker import chunk_text
from app.utils.vector_store import add_embedding, search_embedding

router = APIRouter(prefix="/documents", tags=["Documents"])


# =========================
# ✅ DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 🚀 Upload Document (RAG Pipeline)
# =========================
@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        upload_dir = "app/data/uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get logged-in user
        db_user = db.query(models.User).filter(
            models.User.email == user.get("sub")
        ).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # 🔥 Step 1: Extract text
        text_content = extract_text_from_pdf(file_path)

        # 🔥 Step 2: Chunking
        chunks = chunk_text(text_content)

        # 🔥 Step 3: Process chunks
        for i, chunk in enumerate(chunks):
            embedding_vector = get_embedding(chunk)

            # Store in DB
            new_doc = models.Document(
                title=file.filename,
                company_name="demo_company",
                document_type="pdf",
                file_path=file_path,
                uploaded_by=db_user.id,
                content=chunk,
                embedding=str(embedding_vector),
                chunk_id=i
            )
            db.add(new_doc)

            # Store in FAISS
            add_embedding(embedding_vector, {
                "content": chunk,
                "title": file.filename
            })

        db.commit()

        return {
            "message": "File uploaded with chunking + embeddings",
            "chunks_created": len(chunks)
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# 🔍 Basic Metadata Search
# =========================
@router.get("/search")
def search_documents(
    company_name: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(models.Document).filter(
        models.Document.company_name == company_name
    ).all()


# =========================
# 🔥 RAG SEARCH (FAISS)
# =========================
@router.post("/rag/search")
def rag_search(
    query: str,
    user=Depends(get_current_user)
):
    try:
        query_embedding = get_embedding(query)

        results = search_embedding(query_embedding, k=5)

        return {
            "query": query,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# 🔥 INDEX DOCUMENT (REQUIRED BY ASSIGNMENT)
# =========================
@router.post("/rag/index-document")
def index_document(
    title: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    chunks = db.query(models.Document).filter(
        models.Document.title == title
    ).all()

    if not chunks:
        return {"message": "Document not found"}

    for chunk in chunks:
        embedding_vector = get_embedding(chunk.content)

        add_embedding(embedding_vector, {
            "content": chunk.content,
            "title": chunk.title
        })

    return {
        "message": "Document indexed successfully",
        "chunks_indexed": len(chunks)
    }


# =========================
# 🔥 CONTEXT API (REQUIRED)
# =========================
@router.get("/rag/context/{title}")
def get_document_context(
    title: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    chunks = db.query(models.Document).filter(
        models.Document.title == title
    ).all()

    if not chunks:
        return {"message": "No data found"}

    return [
        {
            "chunk_id": chunk.chunk_id,
            "content": chunk.content
        }
        for chunk in chunks
    ]