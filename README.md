# 📄 RAG-Based Financial Document Management System

## 🚀 Overview

This project is a **FastAPI-based Financial Document Management System** that enables secure storage and semantic analysis of documents using **Retrieval-Augmented Generation (RAG)**.

---

## 🔑 Features

* 🔐 JWT Authentication & Role-Based Access Control (RBAC)
* 📄 Document Upload (PDF)
* 🧠 Text Extraction from PDFs
* ✂️ Document Chunking
* 🔢 Embedding Generation (Sentence Transformers)
* ⚡ FAISS Vector Database
* 🔍 Semantic Search using RAG

---
## 🔄 RAG Pipeline

User Query  
→ Embedding  
→ FAISS Vector Search  
→ Retrieve Top Chunks  
→ Return Relevant Content
## 🏗️ Architecture

```text
Document → Text Extraction → Chunking → Embeddings → FAISS → Semantic Search
```

---

## 📡 APIs

### Auth

* `POST /auth/register`
* `POST /auth/login`

### Documents

* `POST /documents/upload`
* `GET /documents/search`

### RAG

* `POST /documents/rag/search`
* `POST /documents/rag/index-document`
* `GET /documents/rag/context/{title}`

---

## 🧪 Example Query

```json
{
  "query": "machine learning"
}
```

---

## 🛠️ Tech Stack

* FastAPI
* SQLite
* FAISS
* Sentence Transformers
* Python

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

---

## 📁 Project Structure

```text
app/
 ├── auth/
 ├── documents/
 ├── utils/
 ├── db/
 └── main.py
```
## 🧪 Example Output

Input:
"machine learning"

Output:
Top relevant document chunks returned from FAISS search.
---

## 🎯 Outcome

Implemented a complete **RAG pipeline** using embeddings and vector search for semantic document retrieval.

---

