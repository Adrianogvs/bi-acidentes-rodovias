# 🚦 Desafio BI: Acidentes Rodoviários

## 📌 Sobre o Projeto
Este projeto tem como objetivo criar uma arquitetura de Business Intelligence (BI) para análise de acidentes rodoviários em rodovias concedidas no Brasil. A solução envolve a coleta, processamento e visualização dos dados de acidentes disponibilizados pela **Agência Nacional de Transportes Terrestres (ANTT)**.

## 🏗️ Arquitetura da Solução
A arquitetura do projeto foi desenvolvida utilizando ferramentas modernas para facilitar o processamento e análise dos dados:

- **Web Scraping**: Coleta dos dados diretamente do portal da ANTT.
- **ETL (Extract, Transform, Load)**:
  - Extração dos dados (CSV) utilizando Python.
  - Transformação e carregamento para um banco de dados PostgreSQL hospedado na **Cloud Render**.
- **Orquestração**: Automação do pipeline de dados com **Apache Airflow**.
- **Visualização**: Desenvolvimento de dashboards interativos utilizando **Streamlit**.
- **Infraestrutura**: Utilização de **Docker** para garantir a portabilidade e reprodutibilidade do ambiente.

---
## 🏗️ Estrutura do Projeto
```bash
📂 BI-ACIDENTES-RODOVIAS
├── 📂 airflow              # Orquestração do ETL com Apache Airflow
├── 📂 dashboard            # Implementação do dashboard (Streamlit)
├── 📂 data                 # Diretório para armazenamento dos dados
├── 📂 docker               # Configurações e arquivos Docker
├── 📂 etl                  # Pipeline de extração, transformação e carga (ETL)
│   ├── load_data.py        # Script de carga de dados no PostgreSQL
│   ├── models.py           # Definição do schema do banco de dados
│   ├── web_scraping.py     # Script para baixar os arquivos CSV do portal ANTT
├── 📂 notebooks            # Notebooks para análise exploratória
│   ├── anlise_stg.ipynb    # Notebook de análise dos dados da stage
├── 📂 sql                  # Scripts SQL para criação de tabelas e consultas
├── 📂 tests                # Testes unitários do projeto
├── .env                    # Arquivo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── docker-compose.yml      # Orquestração de serviços via Docker
├── LICENSE                 # Licença do projeto
├── README.md               # Documentação do projeto
├── requirements.txt        # Dependências do projeto
├── setup.py                # Configuração do ambiente Python

```

---
## 🛠️ Tecnologias Utilizadas

| Ferramenta | Descrição |
|------------|-------------|
| **Python** | Linguagem principal para desenvolvimento |
| **PostgreSQL** | Banco de dados relacional para armazenamento dos dados |
| **SQLAlchemy** | ORM para comunicação com o banco de dados |
| **Requests & BeautifulSoup** | Web scraping para coletar os dados |
| **Pandas & NumPy** | Manipulação e análise de dados |
| **Apache Airflow** | Orquestração dos processos ETL |
| **Streamlit** | Desenvolvimento do dashboard interativo |
| **Docker** | Containerização do ambiente |
| **Render** | Plataforma para hospedar o banco de dados PostgreSQL |

---
## ⚙️ Instalação e Execução
### 📌 Pré-requisitos
- Docker e Docker Compose instalados.
- PostgreSQL configurado na **Cloud Render**.
- Ambiente Python configurado.

### 🚀 Passos para Execução
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/bi-acidentes-rodovias.git
cd bi-acidentes-rodovias
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente no arquivo `.env`:
```ini
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=seu_host
DB_PORT=5432
DB_NAME=seu_banco
```

4. Execute o **web scraping** para baixar os dados:
```bash
python scripts/web_scraping.py
```

5. Crie as tabelas no banco de dados:
```bash
python scripts/models.py
```

6. Carregue os dados no banco:
```bash
python scripts/load_data.py
```

7. Suba a aplicação usando Docker:
```bash
docker-compose up
```

8. Acesse o dashboard **Streamlit**:
```
http://localhost:8501
```

---
## 📊 Indicadores no Dashboard
O dashboard contém os seguintes indicadores:
- 📈 **Evolução do total de acidentes por ano**
- ⚠️ **% de acidentes com vítima fatal**
- 🚗 **Ranking por tipo de veículo, estado e rodovia**
- ⏰ **Distribuição de acidentes por dia da semana e horário**
- 🔍 **Principais causas dos acidentes**

---
## 📩 Contato
📧 **Email:** dataengineer@adrianogvs.com.br  
🔗 **LinkedIn:** [linkedin.com/in/adrianogvs](https://linkedin.com/in/adrianogvs)  
🚀 **Portfólio:** [adrianogvs.com.br](https://adrianogvs.com.br)

---
## 📜 Licença
Este projeto é de código aberto sob a licença MIT. Sinta-se à vontade para contribuir e melhorar a solução! 🚀

