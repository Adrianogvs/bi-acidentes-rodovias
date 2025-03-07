# dashboard/app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

db_url = "postgresql://usuario:senha@servidor:porta/banco"
engine = create_engine(db_url)

def carregar_dados():
    query = "SELECT * FROM dw_acidentes"
    return pd.read_sql(query, engine)

st.title("🚗 Dashboard de Acidentes Rodoviários")
df = carregar_dados()

st.write("### Evolução dos Acidentes")
st.line_chart(df.groupby("ano").size())

st.write("### Ranking por Estado")
st.bar_chart(df.groupby("estado").size())
