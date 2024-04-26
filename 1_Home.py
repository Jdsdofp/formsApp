import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from logo import *
import pandas as pd
import os
from config import *
from models import *
import datetime
from babel.numbers import format_currency
import warnings
import base64
import io
import xlsxwriter  # Add this line



# Cabeçalho personalizados
st.set_page_config(initial_sidebar_state="collapsed",page_icon="Logo_CoraçãoDrogaria_Globo.ico",layout="wide")
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")
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


total_vlr_oc = 0

# Itera sobre os documentos da coleção
for documento in col_solicitacao.find({}, {"vlr_oc": 1}):
    # Obtém o valor da chave 'vlr_oc' como uma string
    vlr_oc_str = str(documento.get("vlr_oc", "0"))

    # Remove espaços não quebráveis e substitui vírgulas por pontos (formato brasileiro)
    vlr_oc_str = vlr_oc_str.replace("\xa0", "").replace(",", ".")

    try:
        # Tenta converter a string para float e adicionar ao total
        total_vlr_oc += float(vlr_oc_str)
    except ValueError:
        print(f"Ignorando valor não numérico: {vlr_oc_str}")

# Formatando o total como moeda BRL
total_vlr_oc_formatado = format_currency(total_vlr_oc, 'BRL', locale='pt_BR')




col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    col1.metric(label="Aberto Hoje", help="Número de Solicitações abertas hoje", value=ocorrencias_hj, delta=0)
with col2:
    col2.metric(label="Total Aberto", help="Total de solicitações abertas", value=contagem_tt_aberto, delta=f"+{ocorrencias_hj}")
with col3:
    col3.metric(label="Fechado", help="Número de Solicitações fechadas", value=contagem_fechado, delta="-2")
with col4:
    col4.metric(label="Cancelado", help="Solicitações canceladas", value=contagem_cancelada, delta=0)
with col5:
    col5.metric(label="Finalizada", help="Solicitações com OCs já emitidas",value=contagem_finalizada, delta="-2")
with col6:
    col6.metric(label="Valor Total", help="Valor Total das Solicitações ja finalizadas com OC/NF",value=total_vlr_oc_formatado)
    style_metric_cards(border_left_color="#f54e5c", box_shadow=True, border_radius_px=20)
with col7:
    col7.markdown(
            f"<p style='margin: 1px; color: #6E6F6E'>Total Geral</p>"
            f"<div style='background-color: #F5EEEF; border-radius: 20px; padding: 10px; height: 80px; width: 60%; box-shadow: 1px 1px 10px #D3DBD6; border: solid #D3DBD6 1px; font-size: 35px;'>{rgts}</div>",
            unsafe_allow_html=True
        )


#tabela de registros    
st.divider()
st.markdown("<h4 style='color: #D24545; font-family: 'Roboto Mono', monospace;'>Lista de registros</h4>", unsafe_allow_html=True)
st.divider()
scs_db = [documento for documento in col_solicitacao.find({'status': {'$in': ['aberto', 'fechado', 'finalizada']}})]


# Verificar o tema atual
theme = st.get_option("theme.primaryColor")
# Definir a cor do texto com base no tema
text_color = "#FFFFFF" if theme == "#262730" else "#000000"

if scs_db:
    
    df = pd.DataFrame(scs_db).sort_values(by='status')

    df = df.rename(columns={
        'solicitante': 'Solicitante',
        'cod_loja': 'Nº Loja',
        'loja': 'Loja',
        'data_solicitacao': 'Data de Solicitação',
        'forncedor': 'Fornecedor',
        'tp_urg': 'Urgente',
        'gr_complexidade': 'Grau de Complexidade',
        'nr_chamado': 'Nº Chamado',
        'nr_solicitacao': 'Solicitação',
        'status': 'Status',
        'atendente': 'Atend.',
        'data_atendimento': 'Data Atendimento',
        'desc_servico': 'Descrição Serviço'
    })

    # Remover colunas indesejadas
    colunas_para_remover = ['_id', 'data_abertura', 'arquivo_1', 'arquivo_2', 'imagem_1', 'imagem_2', 'imagem_3', 'imagem_4']
    df = df.drop(colunas_para_remover, axis=1)
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('cod_registro')))
    df = df[cols]

    # Extrair 'stts' da sublista 'situacao'
    df['Situação'] = df['situacao'].apply(lambda x: x['stts'] if isinstance(x, dict) else None)
    # Remover a coluna 'situacao'
    df = df.drop('situacao', axis=1)

    # Converter strings vazias para NaN (Not a Number)
    df['Solicitação'] = pd.to_numeric(df['Solicitação'], errors='coerce')

    # Preencher NaN com 0 ou outro valor padrão, se necessário
    #df['Solicitação'].fillna(0, inplace=True)
    # Para esta linha:
    df['Solicitação'] = df['Solicitação'].fillna(0)

    # Converter para inteiro
    df['Solicitação'] = df['Solicitação'].astype(int)


    # Aplicar a cor ao cabeçalho
    colunas_predefinidas = [
        'cod_registro',
        'Solicitante',
        'Nº Loja',
        'Loja',
        'class_servico',
        'Data de Solicitação',
        'Descrição Serviço',
        'Fornecedor',
        'Urgente',
        'Grau de Complexidade',
        'Nº Chamado',
        'tipologia',
        'Solicitação',
        'oc',
        'NF',
        'vlr_oc',
        'Status',
        'Atend.',
        'Data Atendimento',
        'Situação',  # Alterando de 'stts' para 'Situação'
    ]

    df = df[colunas_predefinidas]
    df_filtrado = df[df['Status'].isin(['aberto', 'fechado'])]

    # Mudar a cor das linhas com base no status "aberto"
    def color_rows(row):
        styles = []
        for value in row:
            if row['Status'] == 'aberto':
                styles.append('background-color: #EF8989; color: {};'.format(text_color))
            elif row['Status'] == 'fechado':
                styles.append('background-color: #FFF3CE; color: {};'.format(text_color))
            else:
                styles.append('background-color: white; color: {};'.format(text_color))
        return styles

    # Aplicar a cor condicional às linhas
    styled_df = df_filtrado.style.apply(color_rows, axis=1)


    # Mostrar a tabela no Streamlit
    st.dataframe(styled_df, use_container_width=True, height=600, hide_index=True)

    # Adicionar um botão de download para exportar para o Excel
    if st.button("Exportar para o Excel 📥"):
        # Obter a data e hora atual
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Construir o nome do arquivo com a data e hora atual
        file_name = f'relatorio_geral_{current_time}.xlsx'

        # Exportar o DataFrame para o Excel quando o botão é clicado
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Planilha1')
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()

        # Criar um link de download e acionar o download automaticamente
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Clique aqui para baixar o arquivo Excel</a>'
        st.markdown(href, unsafe_allow_html=True)

else:
    df = pd.DataFrame(columns=[
        'Solicitante',
        'Código da Loja',
        'Loja',
        'Data de Abertura',
        'Fornecedor',
        'Tipo de Urgência',
        'Grau de Complexidade',
        'Número do Chamado',
        'Status',
        'Descrição Serviço',
        'oc',
        'tipologia'
    ])
    