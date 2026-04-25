from sqlalchemy import Column, Integer, String,ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy.sql import func

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # relationship with User (one role → many users)
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True,nullable=False)
    password = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    documents = relationship("Document", back_populates="owner")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company_name = Column(String, nullable=False, index=True)
    document_type = Column(String)
    content = Column(String)
    embedding = Column(String)   
    chunk_id = Column(Integer)  
    file_path = Column(String, nullable=False)

    uploaded_by = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="documents")