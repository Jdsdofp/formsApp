import streamlit as st
import logging
from logo import *
from models import *
import datetime
import time
import json

st.header(body=" Registro de SC", anchor=False)
col1, col2 = st.columns(2)

cod_loja = col1.number_input("Cod. Loja", step=0)
lojas={"nr_loja": cod_loja}
projecao = {"_id": 0, "nr_loja": 0}
result_filial = col_filial.find_one(lojas, projecao)


# Transformar o objeto em uma string e pegar tudo depois do ponto
dadoss = str(result_filial)
texto_limpo = dadoss.replace("(", "").replace(")", "").replace("{", "").replace("}", "")

string_objeto = str(texto_limpo)
partes = string_objeto.split(':')
resultado = partes[1] if len(partes) > 1 else None



with st.form("cadSolicitacao", clear_on_submit=True):
    with col1:
        solcitante = st.text_input("Solicitante", placeholder="Solicitante", key="solicitante")
        loja = st.text_input("Loja", resultado, disabled=True)
        uploaded_file_1 = st.file_uploader(label="Selecione um arquivo: 1", type=["csv", "txt", "xlsx", "pdf"], on_change=None)
        uploaded_file_2 = st.file_uploader("Escolha um arquivo: 2", type=["csv", "txt", "xlsx", "pdf"])    
        class_servico = st.multiselect("Classificação Serviço:",options=['Corretiva','Preventiva', 'Melhoria'], on_change=None)

        javascript_code = """
                <script>
                    document.addEventListener("DOMContentLoaded", function () {
                        const dateInput = document.querySelector('input[type="date"]');
                        dateInput.addEventListener("input", function () {
                            const value = this.value;
                            if (value.length === 4) {
                                this.value = value + "-";
                            }
                            if (value.length === 7) {
                                this.value = value + "-";
                            }
                        });
                    });
                </script>
                """

        col1.markdown(javascript_code, unsafe_allow_html=True)
                # Widget de entrada de data

        data_atual = datetime.datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%Y %H:%M:%S")

        data_abertura = st.text_input("Data de abertura: ", value=data_formatada, disabled=True)
        data_solicitacao = st.date_input("Data da requisição:", datetime.date.today())

    with col2:
            # # # # # # # # # COLUNA 02 DE FORMS # # # # # # # # # # # # # # # # #
        obs = st.text_area(label="Descrição Serviços:", on_change=None)
        forncedor = st.text_input(label="Fornecedor: ", placeholder="Fornecedor", on_change=None)
        tp_urg = st.selectbox(label="Emegencial?", options=['SIM', 'NÃO'], on_change=None)
        gr_complexidade = st.selectbox(label="Classificação emergencial: ", options=['Biologico', 'Estruturais', 'Eletricos', 'Perdas ou Avarias', 'Operação', 'Imagem'], on_change=None)
        nr_chamado = st.text_input(label="Número do chamado: ", placeholder="Nº Chamado", on_change=None)



            # Aplicar o CSS personalizado usando st.markdown
        st.markdown(
                """
                <style>
                #MainMenu {visibility: hidden;}
                </style>
                """,
                unsafe_allow_html=True
            )

    cod_registro = col_solicitacao.count_documents({}) 
    btn_cadastrar = st.form_submit_button("Cadastrar")

    if btn_cadastrar:
        with st.spinner('Aguardando resposta...'):
            # Simula um tempo de espera para a resposta
            time.sleep(5)

        if solcitante == "" or cod_loja == None:
            st.warning("Favor preencha todos os campos")
        else:
              data = {
                  "solicitante": solcitante,
                   "cod_registro": cod_registro+1, 
                   "cod_loja": cod_loja,
                   "loja": loja,
                   "arquivo_1": uploaded_file_1,
                   "arquivo_2": uploaded_file_2,
                   "class_servico": class_servico,
                   "data_abertura": data_abertura,
                   "data_solicitacao": str(data_solicitacao.strftime("%d/%m/%Y")),
                   "obs": obs,
                   "forncedor": forncedor,
                   "tp_urg": tp_urg,
                   "gr_complexidade": gr_complexidade,
                   "nr_chamado": nr_chamado,
                   "status": "aberto"
                  }
            
              registro = col_solicitacao.insert_one(data)
              result = col_solicitacao.find_one({"_id": registro.inserted_id})
              id_result = result["_id"]
              
              if id_result:

                  st.success(f"Registro cadastrado com sucesso ID {id_result}")
                  time.sleep(5)
                 # Limpar a mensagem após 5 segundos
                  st.experimental_rerun()
                  
              else:
                  st.error("Erro ao registrar informações")
        
    

