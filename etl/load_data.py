import os
import pandas as pd
import uuid  # Para gerar identificadores únicos
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configuração do Banco de Dados
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Criando a conexão com o banco
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def carregar_csv_para_postgres():
    """ Lê os arquivos CSV e insere os dados na tabela de staging, limpando antes """
    
    pasta_csv = r"D:\Documents\GitHub\bi-acidentes-rodovias\data"

    with engine.connect() as connection:
        print("🗑️ Limpando a tabela stg_acidentes...")
        connection.execute(text("TRUNCATE TABLE stg_acidentes RESTART IDENTITY"))
        connection.commit()

    for arquivo in os.listdir(pasta_csv):
        if arquivo.endswith(".csv"):
            caminho_arquivo = os.path.join(pasta_csv, arquivo)
            nome_arquivo = arquivo.replace(".csv", "")  # 🔹 Extraindo o nome da rodovia

            print(f"📂 Carregando {arquivo}...")

            try:
                # Tenta carregar usando UTF-8 primeiro
                df = pd.read_csv(caminho_arquivo, delimiter=";", encoding="utf-8", dtype=str, low_memory=False)
            except UnicodeDecodeError:
                print(f"⚠️ Aviso: O arquivo {arquivo} não está em UTF-8. Tentando com Latin-1...")
                df = pd.read_csv(caminho_arquivo, delimiter=";", encoding="latin1", dtype=str, low_memory=False)

            # Renomear colunas para corresponder ao banco
            df.columns = df.columns.str.lower().str.replace(" ", "_")

            # 🔹 Adicionar colunas de ID único e nome do arquivo
            df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]
            df["nome_arquivo"] = nome_arquivo  # 🔹 Inclui o nome do arquivo no dataframe

            # Inserir os dados no banco
            df.to_sql("stg_acidentes", engine, if_exists="append", index=False)
            print(f"✅ {arquivo} carregado com sucesso!")

if __name__ == "__main__":
    carregar_csv_para_postgres()
