import streamlit as st
from logo import *

# Cabeçalho personalizado


st.set_page_config(
    page_icon="Logo_CoraçãoDrogaria_Globo.ico",
    page_title="Forms SCs",
    layout="wide"
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Formulario de abertura SCs", anchor=False)
config_lay()

col1, col2 = st.columns(2)
col1.metric(label="Aberto",value="20", help="Numero de Solicitações que foram abertas hoje", delta="+1")
col2.metric(label="Fechado",value="40", help="Numero de Solicitações fechadas", delta="-2")
