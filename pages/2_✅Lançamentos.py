import streamlit as st
import os
import tempfile
from logo import *
from models import *
from config import *
from mega import Mega
import datetime
import time
from streamlit_local_storage import LocalStorage



st.set_page_config(initial_sidebar_state="collapsed",page_icon="Logo_CoraçãoDrogaria_Globo.ico",layout="wide")
st.subheader("✅ Lançamentos")
col1, col2 = st.columns(2)

def LocalStorageManager():
    return LocalStorage()

localS = LocalStorageManager()


def clear_text_inputs():
    st.session_state["cod_loja_key"] = 0
    st.session_state["class_servico_key"] = []
    st.session_state["tipologia_key"] = "------"
    st.session_state["desc_servico_key"] = ""
    st.session_state["fornecedor_key"] = ""
    st.session_state["tp_urg_key"] = "NÃO"
    st.session_state["nr_chamado_key"] = ""



cod_loja = col1.number_input("Cod. Loja *", help=("Digite o codigo da loja"),step=0, key="cod_loja_key")
lojas={"nr_loja": cod_loja}
projecao = {"_id": 0, "nr_loja": 0}
result_filial = col_filiais.find_one(lojas, projecao)


with st.form("cadSolicitacao", clear_on_submit=True):
    with col1:
        lS = localS.getItem("user", key="test_get_item")
        urs = lS.get("storage", {}) if lS is not None else {}

        usr = urs.get("value") if isinstance(urs, dict) else ""

        # Obtendo os dados diretamente do banco de dados
        usuarios = [usr for usr in col_usuario.find({"time": "Manutenção"})]

        # Criar uma lista para armazenar apenas os nomes dos usuários
        nomes_usuarios = []

        # Adicionar uma opção vazia como a primeira opção
        nomes_usuarios.append('')

        # Iterar sobre os usuários e extrair apenas os nomes
        for usuario in usuarios:
            nomes_usuarios.append(usuario['nome'])

        
        if usr:
            solcitante = st.selectbox(label="Usuário", options=[str(usr)], key="solicitante_key", disabled=True)
            salvar_checkbox = st.checkbox("Salvar nome solicitante", disabled=True)
        else:
            solcitante = st.selectbox(label="Usuário", options=nomes_usuarios)
            salvar_checkbox = st.checkbox("Salvar nome solicitante")

        # Verifica quando o checkbox é alterado
        if salvar_checkbox:
            # Adiciona o valor ao local storage quando o checkbox é marcado
            localS.setItem("user", solcitante)

        if result_filial==None:
            loja = st.text_input("Loja", disabled=True)
        else:
            loja = st.text_input("Loja", result_filial["nome_loja"], disabled=True)
        with st.expander("Anexar Documentos 📜"):
            uploaded_file_1 = st.file_uploader(label="Selecione um arquivo: 1", type=["xlsx", "pdf"])
            uploaded_file_2 = st.file_uploader("Escolha um arquivo: 2", type=["xlsx", "pdf"])
        with st.expander("Anexar imagens📸"):
            uploaded_image_1 = st.file_uploader(label="Selecione uma imagem: 1", type=["jpg", "jpeg", "png", "gif"])
            uploaded_image_2 = st.file_uploader(label="Selecione uma imagem: 2", type=["jpg", "jpeg", "png", "gif"])
            uploaded_image_3 = st.file_uploader(label="Selecione uma imagem: 3", type=["jpg", "jpeg", "png", "gif"])
            uploaded_image_4 = st.file_uploader(label="Selecione uma imagem: 4", type=["jpg", "jpeg", "png", "gif"])
            
        class_servico = st.multiselect("Classificação Serviço:",options=['Corretiva','Preventiva', 'Melhoria', 'Mau uso', 'Desmobilização'], key="class_servico_key",on_change=None)
        tipologia = st.selectbox("Tipologia:", options=['------','CLIMATIZACAO',
                                                              'ESQUADRIAS',
                                                              'PAVIMENTAÇÃO EXTERNA / ESTACIONAMENTO',
                                                              'ESTRUTURA',
                                                              'FACHADA / COMUNICAÇÃO VISUAL',
                                                              'FORRO',
                                                              'GERADORES',
                                                              'TELHADO / IMPERMEABILIZAÇÕES',
                                                              'INSTALAÇÕES ELÉTRICAS',
                                                              'INSTALAÇÕES HIDROSSANITÁRIAS',
                                                              'LIMPEZAS',
                                                              'MOBILIÁRIOS / EQUIPAMENTOS',
                                                              'TOLDOS/PERSIANAS',
                                                              'ARMÁRIO DE CONTROLADOS',
                                                              'PAISAGISMO',
                                                              'PAREDES / DIVISÓRIAS',
                                                              'PINTURA',
                                                              'PISOS /  REVESTIMENTOS',
                                                              'PORTA DE ENROLAR',
                                                              'SERRALHERIA EM GERAL',
                                                              'SISTEMA DE COMBATE A INCÊNDIO',
                                                              'VIDRAÇARIA', 'MANUTENÇÃO DIVERSAS'], key="tipologia_key", on_change=None)

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
        

        data_atual = datetime.datetime.now(fuso_horario)
        data_formatada = data_atual.strftime("%d/%m/%Y %H:%M:%S")

        data_abertura = st.text_input("Data de abertura: ", value=data_formatada, disabled=True)
        data_solicitacao = st.date_input("Data da requisição:", datetime.date.today())

    with col2:
            # # # # # # # # # COLUNA 02 DE FORMS # # # # # # # # # # # # # # # # #
        desc_servico = st.text_area(label="Descrição Serviços:", key="desc_servico_key", on_change=None)
        forncedor = st.text_input(label="Fornecedor: ", placeholder="Fornecedor", key="fornecedor_key", on_change=None)
        tp_urg = st.selectbox(label="Emegencial?", options=['NÃO', 'SIM'], key="tp_urg_key", on_change=None)
        if tp_urg == "SIM":
            gr_complexidade = st.selectbox(label="Classificação emergencial: ", options=['Biologico', 'Estruturais', 'Eletricos', 'Perdas ou Avarias', 'Operação', 'Imagem'], on_change=None)
        else:
             gr_complexidade = st.selectbox(label="Classificação emergencial: ", options=[""], disabled=True)
        nr_chamado = st.text_input(label="Número do chamado: *", placeholder="Nº Chamado", key="nr_chamado_key",on_change=None)



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
    
    btn_cadastrar = st.form_submit_button("Cadastrar", use_container_width=True)
    btn_limpar=col2.button("Limpar🧹", on_click=clear_text_inputs, type="primary")
    
    if btn_cadastrar:
    
        with st.spinner('Cadastrando...') as loads:
            mega = Mega()

            def fazer_upload_mega(file_path):
                email = 'jdsdofp@gmail.com'
                password = '960012Jds'
                m = mega.login(email, password)
                return m.upload(file_path)

            def get_shared_link_mega(upld):
                return mega.get_upload_link(upld)

            links = []
            images= []

            start_time = time.time()

            if uploaded_file_1 is not None:
                temp_file1 = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf" if uploaded_file_1.type == "application/pdf" else ".xlsx")
                try:
                    temp_file1.write(uploaded_file_1.getvalue())
                    temp_file1.close()
                    upld1 = fazer_upload_mega(temp_file1.name)
                    link1 = get_shared_link_mega(upld1)
                    if link1 is not None:
                        links.append(link1)
                    else:
                        links.append('')
                finally:
                    os.unlink(temp_file1.name)

            if uploaded_file_2 is not None:
                temp_file2 = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf" if uploaded_file_2.type == "application/pdf" else ".xlsx")
                try:
                    temp_file2.write(uploaded_file_2.getvalue())
                    temp_file2.close()
                    upld2 = fazer_upload_mega(temp_file2.name)
                    link2 = get_shared_link_mega(upld2)
                    if link2 is not None:
                        links.append(link2)
                    else:
                        links.append('')
                finally:
                    os.unlink(temp_file2.name)



            if uploaded_image_1 is not None:
                temp_img_1 = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg" if uploaded_image_1.type == "image/jpeg" else ".png")
                try:
                    temp_img_1.write(uploaded_image_1.getvalue())
                    temp_img_1.close()
                    upld_img_1 = fazer_upload_mega(temp_img_1.name)
                    link_img_1 = get_shared_link_mega(upld_img_1)
                    if link_img_1 is not None:
                        images.append(link_img_1)
                    else:
                        images.append('')
                finally:
                    os.unlink(temp_img_1.name)

            if uploaded_image_2 is not None:
                temp_img_2 = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg" if uploaded_image_2.type == "image/jpeg" else ".png")
                try:
                    temp_img_2.write(uploaded_image_2.getvalue())
                    temp_img_2.close()
                    upld_img_2 = fazer_upload_mega(temp_img_2.name)
                    link_img_2 = get_shared_link_mega(upld_img_2)
                    if link_img_2 is not None:
                        images.append(link_img_2)
                    else:
                        images.append('')
                finally:
                    os.unlink(temp_img_2.name)

            if uploaded_image_3 is not None:
                temp_img_3 = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg" if uploaded_image_3.type == "image/jpeg" else ".png")
                try:
                    temp_img_3.write(uploaded_image_3.getvalue())
                    temp_img_3.close()
                    upld_img_3 = fazer_upload_mega(temp_img_3.name)
                    link_img_3 = get_shared_link_mega(upld_img_3)
                    if link_img_3 is not None:
                        images.append(link_img_3)
                    else:
                        images.append('')
                finally:
                    os.unlink(temp_img_3.name)

            if uploaded_image_4 is not None:
                temp_img_4 = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg" if uploaded_image_4.type == "image/jpeg" else ".png")
                try:
                    temp_img_4.write(uploaded_image_4.getvalue())
                    temp_img_4.close()
                    upld_img_4 = fazer_upload_mega(temp_img_4.name)
                    link_img_4 = get_shared_link_mega(upld_img_4)
                    if link_img_4 is not None:
                        images.append(link_img_4)
                    else:
                        images.append('')
                finally:
                    os.unlink(temp_img_4.name)
            
            
            if solcitante == "" or cod_loja is None or solcitante is None or nr_chamado == "" or nr_chamado is None or loja is None:
                st.warning("Favor preencha todos os campos")
            else:
                data = {
                    "solicitante": str(solcitante),
                    "cod_registro": cod_registro + 1,
                    "cod_loja": cod_loja,
                    "loja": loja,
                    "arquivo_1": links[0] if links else "",
                    "arquivo_2": links[1] if len(links) > 1 else "",
                    "imagem_1": images[0] if images else "",
                    "imagem_2": images[1] if len(images) > 1 else "",
                    "imagem_3": images[2] if len(images) > 2 else "",
                    "imagem_4": images[3] if len(images) > 3 else "",
                    "class_servico": class_servico,
                    "data_abertura": data_abertura,
                    "data_solicitacao": str(data_solicitacao.strftime("%d/%m/%Y")),
                    "desc_servico": str(desc_servico).upper(),
                    "forncedor": str(forncedor).upper() if forncedor else "*",
                    "tp_urg": tp_urg,
                    "gr_complexidade": gr_complexidade,
                    "nr_chamado": str(nr_chamado).upper(),
                    "atendente": "",
                    "data_atendimento": "",
                    "nr_solicitacao": 0,
                    "tipologia": tipologia,
                    "status": "aberto",
                    "situacao": [{
                        'stts': '',
                        'data': '',
                        'user': ''
                    }],
                    "oc": 0,
                    "vlr_oc": 0,
                    "NF": ""
                }

                registro = col_solicitacao.insert_one(data)
                result = col_solicitacao.find_one({"_id": registro.inserted_id})
                id_result = result["cod_registro"]

                end_time = time.time()
                duration = end_time - start_time
                
                if id_result:
                    st.success(f"Registro cadastrado com sucesso ID: {id_result}")
                else:
                    st.error("Erro ao registrar informações")
           

