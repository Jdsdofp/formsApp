import streamlit as st
from logo import *
import pandas as pd


# Cabeçalho personalizados

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
            .st-eb {
                display: none;
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
col1, col2, col3 = st.columns(3)
col1.metric(label="Aberto",value="20", help="Numero de Solicitações que foram abertas hoje", delta="+1")
col2.metric(label="Fechado",value="40", help="Numero de Solicitações fechadas", delta="-2")
n=30
col3.markdown(
            f"<p style='margin: 1px; color: #6E6F6E'>Total Geral</p>"
            f"<div style='background-color: #F5EEEF; border-radius: 20px; padding: 10px; height: 80px; width: 60%; box-shadow: 1px 1px 10px #D3DBD6; border: solid #D3DBD6 1px; font-size: 35px;'>{n}</div>",
            unsafe_allow_html=True
        )

        #tabela de registros
st.divider()
df = pd.DataFrame(columns=['Nº Solicitação','Cod. Filial', 'Data Registro','Data Chamado', 'Tipo de serviço', 'Tipo Emergencia', 'Status'])
st.markdown("""<h5 style='color: #D24545'>Lista de registros</h5>""", unsafe_allow_html=True)
st.table(df)

