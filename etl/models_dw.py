from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

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

# 📌 Dimensão Rodovia
class DimRodovia(Base):
    __tablename__ = "dim_rodovia"

    id_rodovia = Column(Integer, primary_key=True, autoincrement=True)
    nome_arquivo = Column(String)
    concessionaria = Column(String)
    trecho = Column(String)
    sentido = Column(String)

# 📌 Dimensão Data
class DimData(Base):
    __tablename__ = "dim_data"

    id_data = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date)
    ano = Column(Integer)
    mes = Column(Integer)
    dia = Column(Integer)
    dia_da_semana = Column(String)

# 📌 Dimensão Tipo de Acidente
class DimTipoAcidente(Base):
    __tablename__ = "dim_tipo_acidente"

    id_tipo_acidente = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, unique=True, nullable=False)   # 🔹 Apenas uma descrição por linha

# 📌 Dimensão Tipo de Vítima
class DimTipoVitima(Base):
    __tablename__ = "dim_tipo_vitima"

    id_tipo_vitima = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, unique=True)  # 🔹 Ilesos, levemente feridos, etc.

# 📌 Dimensão Veículo
class DimVeiculo(Base):
    __tablename__ = "dim_veiculo"

    id_veiculo = Column(Integer, primary_key=True, autoincrement=True)  
    n_da_ocorrencia = Column(String, nullable=False)  
    tipo_veiculo = Column(String, nullable=False)


# 📌 Tabela Fato Acidentes (Informações do Acidente)
class FatoAcidentes(Base):
    __tablename__ = "fato_acidentes"

    id_fato = Column(Integer, primary_key=True, autoincrement=True)
    id_rodovia = Column(Integer, ForeignKey("dim_rodovia.id_rodovia"))
    id_data = Column(Integer, ForeignKey("dim_data.id_data"))
    km = Column(String)
    horario = Column(String)
    n_da_ocorrencia = Column(String)

# 📌 Relacionamento entre Acidente e Veículos Envolvidos
class FatoAcidenteVeiculo(Base):
    __tablename__ = "fato_acidente_veiculo"

    id_fato_veiculo = Column(Integer, primary_key=True, autoincrement=True)
    id_fato = Column(Integer, ForeignKey("fato_acidentes.id_fato"))
    id_veiculo = Column(Integer, ForeignKey("dim_veiculo.id_veiculo"))

# 📌 Relacionamento entre Acidente e Tipo de Acidente
class FatoAcidenteTipo(Base):
    __tablename__ = "fato_acidente_tipo"

    id_fato_tipo = Column(Integer, primary_key=True, autoincrement=True)
    id_fato = Column(Integer, ForeignKey("fato_acidentes.id_fato"))
    id_tipo_acidente = Column(Integer, ForeignKey("dim_tipo_acidente.id_tipo_acidente"))

# 📌 Relacionamento entre Acidente e Vítimas
class FatoVitimas(Base):
    __tablename__ = "fato_vitimas"

    id_fato_vitimas = Column(Integer, primary_key=True, autoincrement=True)
    id_fato = Column(Integer, ForeignKey("fato_acidentes.id_fato"))
    id_tipo_vitima = Column(Integer, ForeignKey("dim_tipo_vitima.id_tipo_vitima"))
    quantidade = Column(Integer)  # 🔹 Número de vítimas para cada tipo

# Criando as tabelas no banco de dados
def criar_tabelas_dw():
    Base.metadata.create_all(engine)
    print("✅ Tabelas do Data Warehouse criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas_dw()
