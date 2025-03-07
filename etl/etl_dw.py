from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

# 🔹 Carregar variáveis de ambiente do arquivo .env (credenciais do banco)
load_dotenv()

# 🔹 Configuração do Banco de Dados
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 🔹 Criando a conexão com o banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


# 🛑 Função para limpar todas as tabelas antes de carregar novos dados
def limpar_tabelas():
    """
    Remove todos os dados das tabelas Fato e Dimensões 
    antes de carregar os novos dados da Staging Area.
    """
    with engine.connect() as conn:
        print("🗑️ Limpando todas as tabelas de Fatos e Dimensões...")

        # 🔄 Ordem correta para evitar problemas de chave estrangeira
        tabelas = [
            "fato_acidentes",
            "dim_tipo_vitima",
            "dim_veiculo",
            "dim_tipo_acidente",
            "dim_data",
            "dim_rodovia"
        ]

        # 🔄 Deletando os dados de cada tabela
        for tabela in tabelas:
            conn.execute(text(f"DELETE FROM {tabela};"))  # Apaga os dados, mas mantém a estrutura
            print(f"✅ Tabela {tabela} limpa com sucesso!")

        conn.commit()


# 🔽 Funções para Inserção das Dimensões e da Fato

def inserir_dim_rodovia(df):
    """
    Cria a Dimensão Rodovia com os dados únicos de trecho e sentido.
    """
    dim_rodovia = df[['trecho', 'sentido']].drop_duplicates().reset_index(drop=True)
    dim_rodovia.to_sql("dim_rodovia", engine, if_exists="append", index=False)
    print("✅ Dimensão Rodovia carregada com sucesso!")


def inserir_dim_data(df):
    """
    Cria a Dimensão Data extraindo dia, mês e ano da coluna 'data'.
    """
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')  # Converte string para datetime
    dim_data = df[['data']].drop_duplicates().reset_index(drop=True)
    dim_data['ano'] = dim_data['data'].dt.year
    dim_data['mes'] = dim_data['data'].dt.month
    dim_data['dia'] = dim_data['data'].dt.day
    dim_data.to_sql("dim_data", engine, if_exists="append", index=False)
    print("✅ Dimensão Data carregada com sucesso!")


def inserir_dim_tipo_acidente(df):
    """
    Cria a Dimensão Tipo de Acidente a partir dos valores únicos da coluna 'tipo_de_acidente',
    removendo valores nulos para evitar erros.
    """
    tipos_unicos = df[['tipo_de_acidente']].drop_duplicates().rename(columns={'tipo_de_acidente': 'descricao'})
    
    # 🔥 Remover valores nulos (evita erro de NOT NULL)
    tipos_unicos = tipos_unicos.dropna(subset=['descricao'])
    
    # 📥 Insere os dados no banco
    tipos_unicos.to_sql("dim_tipo_acidente", engine, if_exists="append", index=False)
    
    print("✅ Dimensão Tipo de Acidente carregada com sucesso!")



def inserir_dim_veiculo(df):
    """
    Cria a Dimensão Veículo transformando as colunas de tipos de veículos em um formato unpivot.
    Apenas registros com quantidade maior que 0 são considerados.
    """
    veiculos = ['automovel', 'bicicleta', 'caminhao', 'moto', 'onibus', 'outros', 
                'tracao_animal', 'transporte_de_cargas_especiais', 'trator_maquinas', 'utilitarios']
    
    # 🔄 Transforma os veículos de colunas para linhas (unpivot)
    dim_veiculo = pd.melt(df, id_vars=['n_da_ocorrencia'], value_vars=veiculos, var_name="tipo_veiculo", value_name="quantidade")
    
    # 🔢 Converte a coluna "quantidade" para numérico (caso tenha sido interpretada como string)
    dim_veiculo["quantidade"] = pd.to_numeric(dim_veiculo["quantidade"], errors='coerce').fillna(0).astype(int)
    
    # 📌 Mantém apenas os registros com quantidade maior que 0 (veículos envolvidos)
    dim_veiculo = dim_veiculo[dim_veiculo['quantidade'] > 0].drop(columns=['quantidade'])
    
    # 📥 Insere os dados no banco de dados
    dim_veiculo.to_sql("dim_veiculo", engine, if_exists="append", index=False)
    print("✅ Dimensão Veículo carregada com sucesso!")


def inserir_dim_tipo_vitima(df):
    """
    Cria a Dimensão Tipo de Vítima transformando os tipos de vítimas em um formato unpivot.
    Apenas registros com quantidade maior que 0 são considerados.
    """
    vitimas = ['ilesos', 'levemente_feridos', 'moderadamente_feridos', 'gravemente_feridos', 'mortos']

    # 🔄 Transforma os tipos de vítimas de colunas para linhas (unpivot)
    dim_tipo_vitima = pd.melt(df, id_vars=['n_da_ocorrencia'], value_vars=vitimas, var_name="tipo_vitima", value_name="quantidade")
    
    # 📌 Mantém apenas os registros com quantidade maior que 0 (vítimas envolvidas)
    dim_tipo_vitima = dim_tipo_vitima[dim_tipo_vitima['quantidade'] > 0].drop(columns=['quantidade'])
    
    # 📥 Insere os dados no banco de dados
    dim_tipo_vitima.to_sql("dim_tipo_vitima", engine, if_exists="append", index=False)
    print("✅ Dimensão Tipo de Vítima carregada com sucesso!")


def inserir_fato_acidentes(df):
    """
    Carrega os dados na Fato Acidentes, unindo as dimensões através das chaves substitutas.
    """
    query = """
    INSERT INTO fato_acidentes (id_rodovia, id_data, id_tipo_acidente, id_veiculo, id_tipo_vitima, km)
    SELECT 
        r.id AS id_rodovia,
        d.id AS id_data,
        ta.id AS id_tipo_acidente,
        v.id AS id_veiculo,
        tv.id AS id_tipo_vitima,
        s.km::NUMERIC
    FROM stg_acidentes s
    JOIN dim_rodovia r ON s.trecho = r.trecho AND s.sentido = r.sentido
    JOIN dim_data d ON s.data = d.data
    JOIN dim_tipo_acidente ta ON s.tipo_de_acidente = ta.descricao
    LEFT JOIN dim_veiculo v ON s.n_da_ocorrencia = v.n_da_ocorrencia
    LEFT JOIN dim_tipo_vitima tv ON s.n_da_ocorrencia = tv.n_da_ocorrencia
    """
    with engine.connect() as conn:
        conn.execute(text(query))  # 📥 Executa a inserção no banco
        conn.commit()
    
    print("✅ Tabela Fato Acidentes carregada com sucesso!")


# 📌 Executando o ETL (Extração, Transformação e Carga)
if __name__ == "__main__":
    print("🚀 Iniciando ETL para Data Warehouse...\n")

    # 🔄 Carrega os dados da Staging Area (Área Temporária)
    df_stg = pd.read_sql("SELECT * FROM stg_acidentes", con=engine)

    # 🔥 Limpa as tabelas antes de inserir os novos dados
    limpar_tabelas()

    # 📌 Inserindo Dimensões
    inserir_dim_rodovia(df_stg)
    inserir_dim_data(df_stg)
    inserir_dim_tipo_acidente(df_stg)
    inserir_dim_veiculo(df_stg)
    inserir_dim_tipo_vitima(df_stg)

    # 📌 Inserindo Fato Acidentes
    inserir_fato_acidentes(df_stg)

    print("\n🎯 ETL concluído com sucesso!")
