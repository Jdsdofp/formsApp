import streamlit as st
import pandas as pd
from models import col_solicitacao
import datetime
from config import *
from streamlit_local_storage import LocalStorage




def LocalStorageManager():
    return LocalStorage()

localS = LocalStorageManager()


def procurar_docs(df, usuario):
    total_documentos_atualizados = 0  # Inicializa o contador de documentos atualizados
    updates = []

    with st.spinner("Atualizando documentos..."):  # Exibe o spinner durante o processo
        for index, row in df.iterrows():
            nr_solicitacao = row['SC']
            situacao = row['Status']
            
            data_atual = datetime.datetime.now(fuso_horario)

            documento = col_solicitacao.find_one({'nr_solicitacao': int(nr_solicitacao)})
            if documento:
                # Atualizar o documento no MongoDB
                update = {
                    'filter': {'nr_solicitacao': nr_solicitacao},
                    'update': {
                        '$set': {
                            'situacao': {
                                'stts': situacao,  # Atualiza o campo 'stts' com o status
                                'data': data_atual.strftime("%d/%m/%Y %H:%M:%S"),  # Define a data atual
                                'user': str(usuario).upper()  # Defina o nome do usuário
                            }
                        }
                    }
                }
                updates.append(update)
                total_documentos_atualizados += 1  # Incrementa o contador de documentos atualizados
            else:
                st.write(f"Documento não encontrado para o número de solicitação {nr_solicitacao}")

        # Atualizar os documentos no MongoDB
        for update in updates:
            col_solicitacao.update_many(update['filter'], update['update'])

    st.success(f"Total de documentos atualizados: {total_documentos_atualizados}")

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_icon="Logo_CoraçãoDrogaria_Globo.ico",
    layout="wide"
)

st.subheader("⚙ Ajustes")



data_atual = datetime.datetime.now(fuso_horario)
data_formatada = data_atual.strftime("%d/%m/%Y %H:%M:%S")



with st.expander("Importação de Dados ⚡"):
    lS = localS.getItem("atends", key="get_item")
    urs = lS.get("storage", {}) if lS is not None else {}

    usr = urs.get("value") if isinstance(urs, dict) else ""
    

    if usr:
            atnd = st.text_input("Atendente: ", key="user_key", value=str(usr).upper(), disabled=True)
            salvar_checkbox = st.checkbox(" ", disabled=True)
    else:
            atnd = st.text_input("Atendente: ", key="user_key", placeholder="Atendente")
            salvar_checkbox = st.checkbox("Salvar nome")

                
    if salvar_checkbox:
                    # Adiciona o valor ao local storage quando o checkbox é marcado
            localS.setItem("atends", atnd)

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
            usuario=urs['value']
            procurar_docs(df, usuario)
            # Limpar o arquivo selecionado definindo-o como None
            arquivo = None
