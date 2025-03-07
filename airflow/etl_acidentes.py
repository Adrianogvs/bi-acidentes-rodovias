# airflow/dags/etl_acidentes.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from etl.web_scraping import WebScraper
from etl.extrator import Extrator
from etl.carga import Carga

def extrair_dados():
    scraper = WebScraper("https://dados.antt.gov.br/dataset/acidentes-rodovias")
    scraper.baixar_csv("/tmp/acidentes.csv")

def transformar_dados():
    extrator = Extrator("/tmp/acidentes.csv")
    df = extrator.carregar_dados()
    df_transformado = extrator.transformar_dados(df)
    df_transformado.to_csv("/tmp/acidentes_transformado.csv", index=False)

def carregar_dados():
    db_url = "postgresql://usuario:senha@servidor:porta/banco"
    carga = Carga(db_url)
    df = pd.read_csv("/tmp/acidentes_transformado.csv")
    carga.salvar_no_banco(df, "dw_acidentes")

default_args = {"owner": "airflow", "start_date": datetime(2024, 3, 7)}

with DAG("etl_acidentes", default_args=default_args, schedule_interval="@daily") as dag:
    tarefa_extrair = PythonOperator(task_id="extrair", python_callable=extrair_dados)
    tarefa_transformar = PythonOperator(task_id="transformar", python_callable=transformar_dados)
    tarefa_carregar = PythonOperator(task_id="carregar", python_callable=carregar_dados)

    tarefa_extrair >> tarefa_transformar >> tarefa_carregar
