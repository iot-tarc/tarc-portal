import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Configuração da URL do banco de dados
# Formato: postgresql://usuario:senha@host:porta/nome_do_banco
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tarc_db"
)

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Cria a classe base para os modelos
Base = declarative_base()

# Cria a factory de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
