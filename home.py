import streamlit as st
from logo import *
import pandas as pd

# Cabeçalho personalizado


st.set_page_config(
    page_icon="Logo_CoraçãoDrogaria_Globo.ico",
    page_title="Forms SCs",
    layout="wide"
)
st.markdown(
    """
    <style>
    .css-1dp5vir.e13qjvis1{
        background-image: linear-gradient(90deg, rgb(229, 146, 146), rgb(214, 69, 69)); z-index: 999990;
    }
    </style>
    """,
    unsafe_allow_html=True
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

#tabela de registros
st.divider()
df = pd.DataFrame(columns=['Nº Solicitação','Cod. Filial', 'Data Registro','Data Chamado', 'Tipo de serviço', 'Tipo Emergencia'])
st.markdown("""<h5 style='color: #D24545'>Lista de registros</h5>""", unsafe_allow_html=True)
st.table(df)

