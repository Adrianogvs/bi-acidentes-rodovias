from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import uuid  # Para gerar identificadores únicos

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configuração do Banco de Dados
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Criando a conexão com o banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Criando a base do SQLAlchemy
Base = declarative_base()

# 📌 Criando a tabela de Staging (stg_acidentes) com ID único e nome do arquivo
class StgAcidentes(Base):
    __tablename__ = "stg_acidentes"

    id = Column(String, primary_key=True)  # ID gerado automaticamente
    concessionaria = Column(String)
    data = Column(String)
    horario = Column(String)
    n_da_ocorrencia = Column(String)
    tipo_de_ocorrencia = Column(String)
    km = Column(String)
    trecho = Column(String)
    sentido = Column(String)
    tipo_de_acidente = Column(String)
    automovel = Column(String)
    bicicleta = Column(String)
    caminhao = Column(String)
    moto = Column(String)
    onibus = Column(String)
    outros = Column(String)
    tracao_animal = Column(String)
    transporte_de_cargas_especiais = Column(String)
    trator_maquinas = Column(String)
    utilitarios = Column(String)
    ilesos = Column(String)
    levemente_feridos = Column(String)
    moderadamente_feridos = Column(String)
    gravemente_feridos = Column(String)
    mortos = Column(String)

# Criando as tabelas no banco de dados
def criar_tabelas():
    Base.metadata.drop_all(engine)  # Remove a tabela anterior para evitar conflitos
    Base.metadata.create_all(engine)
    print("✅ Tabela de Staging recriada com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
