import streamlit as st
from logo import *
import pandas as pd
import os
from config import *
from models import *
import datetime




# Cabeçalho personalizados
st.set_page_config(initial_sidebar_state="collapsed",page_icon="Logo_CoraçãoDrogaria_Globo.ico",layout="wide")

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

st.title("📊 Demonstrativo de abertura SCs", anchor=False)
config_lay()

# # # # # # # # # contagem de solicitaçoes de hoje # # # # # # # # #
data_atual = datetime.datetime.now(fuso_horario)
dataAbertura = data_atual.strftime("%d/%m/%Y %H:%M:%S")

sc_aberta = [documento for documento in col_solicitacao.find({"status": "aberto"})]
datas = [dado['data_abertura'] for dado in sc_aberta]
datasShr = [data_hora.split(' ')[0] for data_hora in datas]
data_especifica = data_atual.strftime("%d/%m/%Y")
ocorrencias_hj = datasShr.count(data_especifica)

# # # # # # # # # FIM contagem de solicitaçoes de hoje # # # # # # # # #


# # # # # # # # # contagem de solicitações fechadas # # # # # # # # # #
sc_fechada = [documento for documento in col_solicitacao.find({"status": "fechado"})]
contagem_fechado = sum(1 for dado in sc_fechada if dado.get('status') == 'fechado')
# # # # # # # # # FIM contagem de solicitações fechadas # # # # # # # # #

# # # # # # # # # total de solicitações abertas # # # # # # # # # # # 
total_registros = col_solicitacao.count_documents({}) 
# # # # # # # # # FIM total de solicitações abertas # # # # # # # # # 


# # # # # # # # # contagem de solicitações canceladas # # # # # # # # # #
sc_cancelada = [documento for documento in col_solicitacao.find({"status": "cancelado"})]
contagem_cancelada = sum(1 for dado in sc_cancelada if dado.get('status') == 'cancelado')
rgts=total_registros-contagem_cancelada
# # # # # # # # # FIM contagem de solicitações canceladas # # # # # # # # #


# # # # # # # # # contagem de solicitações finalizadas # # # # # # # # # #
sc_finalizada = [documento for documento in col_solicitacao.find({"status": "finalizada"})]
contagem_finalizada = sum(1 for dado in sc_finalizada if dado.get('status') == 'finalizada')
# # # # # # # # # FIM contagem de solicitações finalizadas # # # # # # # # #


# # # # # # # # contagem de chamados abertos no total geral # # # # # # # # 
sc_tt_aberto = [documento for documento in col_solicitacao.find({"status": "aberto"})]
contagem_tt_aberto = sum(1 for dado in sc_tt_aberto if dado.get('status') == 'aberto')
# # # # # # # # FIM contagem de chamados abertos no total geral # # # # # # # 




col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    col1.metric(label="Aberto Hoje", help="Número de Solicitações abertas hoje", value=ocorrencias_hj)
with col2:
    col2.metric(label="Total Aberto", help="Total de solicitações abertas", value=contagem_tt_aberto, delta=f"+{ocorrencias_hj}")
with col3:
    col3.metric(label="Fechado", help="Número de Solicitações fechadas", value=contagem_fechado, delta="-2")
with col4:
    col4.metric(label="Cancelado", help="Solicitações canceladas", value=contagem_cancelada)
with col5:
    col5.metric(label="Finalizada", help="Solicitações com OCs já emitidas",value=contagem_finalizada, delta="-2")

with col6:
    col6.markdown(
            f"<p style='margin: 1px; color: #6E6F6E'>Total Geral</p>"
            f"<div style='background-color: #F5EEEF; border-radius: 20px; padding: 10px; height: 80px; width: 60%; box-shadow: 1px 1px 10px #D3DBD6; border: solid #D3DBD6 1px; font-size: 35px;'>{rgts}</div>",
            unsafe_allow_html=True
        )

        #tabela de registros    
st.divider()
st.markdown("<h4 style='color: #D24545; font-family: 'Roboto Mono', monospace;'>Lista de registros</h4>", unsafe_allow_html=True)
st.divider()
scs_db = [documento for documento in col_solicitacao.find({'status': {'$in': ['aberto', 'fechado', 'finalizada']}})]

if scs_db:
    df = pd.DataFrame(scs_db).sort_values(by='status')
    


    df = df.rename(columns={
        'solicitante': 'Solicitante',
        'cod_loja': 'Nº Loja',
        'loja': 'Loja',
        'data_abertura': 'Data de Abertura',
        'data_solicitacao': 'Data de Solicitação',
        'forncedor': 'Fornecedor',
        'tp_urg': 'Urgente',
        'gr_complexidade': 'Grau de Complexidade',
        'nr_chamado': 'Nº Chamado',
        'nr_solicitacao':'Solicitação',
        'status': 'Status',
        'atendente': 'Atend.',
        'data_atendimento': 'Data Atendimento',
        'desc_servico': 'Descrição Serviço'
    })

    # Remover colunas indesejadas
    colunas_para_remover = ['_id', 'arquivo_1', 'arquivo_2', 'imagem_1', 'imagem_2', 'imagem_3', 'imagem_4']
    #df['class_servico'] = df['class_servico'].apply(lambda x: str(x).strip("[]"))
    df = df.drop(colunas_para_remover, axis=1)
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('cod_registro')))
    df = df[cols]

    # Aplicar a cor ao cabeçalho

    # Mudar a cor das linhas com base no status "aberto"
    def color_rows(row):
        if row['Status'] == 'aberto':
            return ['background-color: #EF8989'] * len(row)
        elif row['Status'] == 'fechado':
            return ['background-color: #FFF3CE'] * len(row)
        else:
            return ['background-color: white'] * len(row)

    # Aplicar a cor condicional às linhas
    styled_df = df.style.apply(color_rows, axis=1)

    # Mostrar a tabela no Streamlit
    #st.write(styled_df, unsafe_allow_html=True)
    #st.markdown(styled_df)
    st.dataframe(styled_df, use_container_width=True, height=350, hide_index=True)
else:
    df = pd.DataFrame(columns=[
        'Solicitante',
        'Código da Loja',
        'Loja',
        'Data de Abertura',
        'Data de Solicitação',
        'Fornecedor',
        'Tipo de Urgência',
        'Grau de Complexidade',
        'Número do Chamado',
        'Status','Descrição Serviço'
    ])
    