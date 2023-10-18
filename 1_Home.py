import streamlit as st
from logo import *
import pandas as pd
from models import *
import datetime


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

# # # # # # # # # contagem de solicitaçoes de hoje # # # # # # # # #
dataAbertura=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
sc_aberta = [documento for documento in col_solicitacao.find({"status": "aberto"})]
datas = [dado['data_abertura'] for dado in sc_aberta]
datasShr = [data_hora.split(' ')[0] for data_hora in datas]
data_especifica = datetime.datetime.now().strftime("%d/%m/%Y")
ocorrencias_hj = datasShr.count(data_especifica)

# # # # # # # # # FIM contagem de solicitaçoes de hoje # # # # # # # # #


# # # # # # # # # contagem de solicitações fechadas # # # # # # # # # #
sc_fechada = [documento for documento in col_solicitacao.find({"status": "fechado"})]
contagem_fechado = sum(1 for dado in sc_fechada if dado.get('status') == 'fechado')
print(contagem_fechado)
# # # # # # # # # FIM contagem de solicitações fechadas # # # # # # # # #

# # # # # # # # # total de solicitações abertas # # # # # # # # # # # 
total_registros = col_solicitacao.count_documents({}) 
# # # # # # # # # FIM total de solicitações abertas # # # # # # # # # 

# # # # # # # # contagem de chamados abertos no total geral # # # # # # # # 
sc_tt_aberto = [documento for documento in col_solicitacao.find({"status": "aberto"})]
contagem_tt_aberto = sum(1 for dado in sc_tt_aberto if dado.get('status') == 'aberto')
# # # # # # # # FIM contagem de chamados abertos no total geral # # # # # # # 

col1, col2, col3, col4 = st.columns(4)
with col1:
    col1.metric(label="Aberto Hoje",value=ocorrencias_hj, help="Numero de Solicitações que foram abertas hoje", delta="+1")
with col2:
    col2.metric(label="Total Aberto",value=contagem_tt_aberto, help="Total de solicitações abertas", delta=f"+{ocorrencias_hj}")
with col3:
    col3.metric(label="Fechado",value=contagem_fechado, help="Numero de Solicitações fechadas", delta="-2")
with col4:
    col4.markdown(
            f"<p style='margin: 1px; color: #6E6F6E'>Total Geral</p>"
            f"<div style='background-color: #F5EEEF; border-radius: 20px; padding: 10px; height: 80px; width: 60%; box-shadow: 1px 1px 10px #D3DBD6; border: solid #D3DBD6 1px; font-size: 35px;'>{total_registros}</div>",
            unsafe_allow_html=True
        )

        #tabela de registros
st.divider()
st.markdown("<p style='color: #555555;font-family: 'Roboto Mono', monospace;'>Lista de registros</p>", unsafe_allow_html=True)
st.divider()
scs_db = [documento for documento in col_solicitacao.find()]

if scs_db:
    df = pd.DataFrame(scs_db)

    df = df.rename(columns={
        'solicitante': 'Solicitante',
        'cod_loja': 'Código da Loja',
        'loja': 'Loja',
        'data_abertura': 'Data de Abertura',
        'data_solicitacao': 'Data de Solicitação',
        'forncedor': 'Fornecedor',
        'tp_urg': 'Tipo de Urgência',
        'gr_complexidade': 'Grau de Complexidade',
        'nr_chamado': 'Número do Chamado',
        'status': 'Status',
        'desc_servico': 'Descrição Serviço'
    })

    # Remover colunas indesejadas
    colunas_para_remover = ['_id', 'arquivo_1', 'arquivo_2']
    df['class_servico'] = df['class_servico'].apply(lambda x: str(x).strip("[]"))
    df = df.drop(colunas_para_remover, axis=1)
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('cod_registro')))
    df = df[cols]
    st.markdown("""<h5 style='color: #D24545'>Lista de registros</h5>""", unsafe_allow_html=True)

    # Mudar a cor do cabeçalho da tabela
    def set_background_color(s, color):
        return f"background-color: {color}"

    # Aplicar a cor ao cabeçalho

    # Mudar a cor das linhas com base no status "aberto"
    def color_rows(row):
        if row['Status'] == 'aberto':
            return ['background-color: #EF8989'] * len(row)
        else:
            return ['background-color: white'] * len(row)

    # Aplicar a cor condicional às linhas
    styled_df = df.style.apply(color_rows, axis=1)


    # Mostrar a tabela no Streamlit
    st.write(styled_df)
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

