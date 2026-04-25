from fastapi import FastAPI
from app.db.database import Base, engine
from app.db import models
from app.auth.auth import router as auth_router
from app.roles.roles import router as roles_router
from app.documents.documents import router as doc_router

app = FastAPI()   # ✅ MUST come before include_router

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(doc_router)


@app.get("/")
def home():
    return {"message": "API is running"}