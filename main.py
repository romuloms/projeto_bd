from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import date

load_dotenv()
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    cpf: int
    nome: str
    data_nascimento: date

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Métodos do FastAPI
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    try:
        user_db = models.User(cpf=user.cpf, nome=user.nome, data_nascimento=user.data_nascimento)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{cpf}", response_model=UserBase)
async def get_user(cpf: str, db: db_dependency):
    user_db = db.query(models.User).filter(models.User.cpf == cpf).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db