from sqlalchemy import Column, Integer, String, Date, BigInteger
from db import Base
from dotenv import load_dotenv


load_dotenv()

class User(Base):
    __tablename__ = 'users'

    cpf = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String(50), index=True)
    data_nascimento = Column(Date)