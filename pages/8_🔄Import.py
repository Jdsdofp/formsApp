import streamlit as st
import pandas as pd
import io
from models import col_solicitacao
import datetime
from config import *
from streamlit_local_storage import LocalStorage




def procurar_docs(df):
    total_documentos_atualizados = 0  # Inicializa o contador de documentos atualizados
    updates = []
    
    # Define o progresso inicial como 0
    progresso = st.progress(0)

    with st.spinner("Atualizando documentos..."):  # Exibe o spinner durante o processo
        for index, row in df.iterrows():
            nr_solicitacao = row['SC']
            situacao = row['Status']
            
            data_atual = datetime.datetime.now(fuso_horario)

            documento = col_solicitacao.find_one({'nr_solicitacao': nr_solicitacao})
            if documento:
                # Atualizar o documento no MongoDB
                update = {
                    'filter': {'nr_solicitacao': nr_solicitacao},
                    'update': {
                        '$set': {
                            'situacao': {
                                'stts': situacao,  # Atualiza o campo 'stts' com o status
                                'data': data_atual.strftime("%d/%m/%Y %H:%M:%S"),  # Define a data atual
                                'user': 'Marina - Suprimentos'  # Defina o nome do usuário
                            }
                        }
                    }
                }
                updates.append(update)
                total_documentos_atualizados += 1  # Incrementa o contador de documentos atualizados
            else:
                pass
            
            # Atualiza o indicador de progresso a cada iteração
            
            progresso.progress((index + 1) / len(df))
            

        # Atualizar os documentos no MongoDB
        for update in updates:
            col_solicitacao.update_many(update['filter'], update['update'])
            

    st.toast(f"Total de documentos atualizados: {total_documentos_atualizados}", icon="✅")

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_icon="Logo_CoraçãoDrogaria_Globo.ico",
    layout="wide"
)

st.subheader("🔄 Import")
registros = [rg for rg in col_solicitacao.find()]

# Lista para armazenar as datas dos objetos de situação
datas_situacao = []

# Iterar sobre os registros e listar as datas dos objetos de situação
for registro in registros:
    if 'situacao' in registro:  # Verificar se a chave 'situacao' está presente
        situacao = registro['situacao']
        if 'data' in situacao:  # Verificar se a chave 'data' está presente no objeto de situação
            data_situacao = situacao['data']
            datas_situacao.append(data_situacao)

# Imprimir as datas dos objetos de situação
st.markdown(f"Ultima Importação: <span style='color: #0b9c2f'>{datas_situacao[0]}<span>", unsafe_allow_html=True)


data_atual = datetime.datetime.now(fuso_horario)
data_formatada = data_atual.strftime("%d/%m/%Y %H:%M:%S")



with st.expander("Importação de Dados ⚡"):
                
    st.write("Carregar arquivo de planilha:")
    arquivo = st.file_uploader("Selecione o arquivo CSV ou Excel", type=["csv", "xlsx"])

    if arquivo is not None:
        if arquivo.name.endswith('.csv'):
            # Ler a planilha do Excel
            df = pd.read_csv(arquivo)
        elif arquivo.name.endswith('.xlsx'):
            # Ler a planilha do Excel
            df = pd.read_excel(arquivo, engine='openpyxl')

        st.write("Dados carregados:")
        st.write(df)

        if st.button("Importar", type='primary'):
            procurar_docs(df)
            # Limpar o arquivo selecionado definindo-o como None
            arquivo = None




    # Obtém a data atual
data_atual = datetime.datetime.now(fuso_horario)



# Subtrai 3 dias da data atual
data_tres_dias_atras = data_atual

# Formata a data para o formato "dd/mm/yyyy"
data_formatada_tres_dias_atras = data_tres_dias_atras.strftime("%d/%m/%Y")

# Filtra os documentos que possuem a chave "situacao"
dados_com_situacao = [data for data in col_solicitacao.find({"situacao.stts": {"$exists": True, "$ne": ""}})]

# Lista apenas os documentos cuja data da situação seja igual a três dias antes da data atual
dados_filtrados = [data for data in dados_com_situacao if datetime.datetime.strptime(data["situacao"]["data"], "%d/%m/%Y %H:%M:%S").date() == data_tres_dias_atras.date()]

# Verifica se há dados filtrados
if dados_filtrados:
    # Cria um DataFrame com os dados filtrados
    df = pd.DataFrame(dados_filtrados)

    # Seleciona apenas as colunas desejadas
    colunas_selecionadas = ['solicitante', 'cod_loja', 'loja', 'data_abertura', 'nr_solicitacao', 'oc', 'vlr_oc', 'situacao']
    df = df[colunas_selecionadas]

    # Adiciona colunas 'stts' e 'user' ao DataFrame
    df['stts'] = df['situacao'].apply(lambda x: x.get('stts', ''))
    df['user'] = df['situacao'].apply(lambda x: x.get('user', ''))
    df['data'] = df['situacao'].apply(lambda x: x.get('data', ''))

    # Remove a coluna 'situacao' do DataFrame
    df = df.drop(columns=['situacao'])

    # Renomeia as colunas para nomes mais amigáveis
    df = df.rename(columns={'solicitante': 'Solicitante', 'cod_loja': 'Código da Loja', 'loja': 'Loja', 'data_abertura': 'Data de Abertura', 'nr_solicitacao': 'Número da Solicitação', 'oc': 'OC', 'vlr_oc': 'Valor OC', 'stts': 'Situação', 'user': 'Usuário', 'data': 'Data Importação'})

    # Obtém o total de documentos filtrados
    total_documentos_filtrados = len(dados_filtrados)

    # Disponibiliza os dados para download em formato Excel
    excel_data = io.BytesIO()
    df.to_excel(excel_data, index=False, engine='xlsxwriter')
    excel_data.seek(0)

    st.download_button(
        label="Download dos dados (Excel)",
        data=excel_data,
        file_name=f"relatorio_{data_formatada_tres_dias_atras}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        help="Baixar os dados que foram exportados"
    )
else:
    st.write("Nenhum dado disponível para download.")