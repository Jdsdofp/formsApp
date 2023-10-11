import streamlit as st

st.set_page_config(
    page_icon="img\Logo_CoraçãoDrogaria_Globo.ico",
    page_title="Forms SCs | Lançar"
)

st.header(body="Registro de SC", anchor=False)

col1, col2 = st.columns(2)

with st.form("form1"):
    desc = col1.text_input("Descrição da solicitação", placeholder="Solicitante", disabled=True)
    tp_desc = col1.number_input("Loja", step=None, max_value=299)
    uploaded_file_1 = col1.file_uploader(label="Selecione um arquivo: 1", type=["csv", "txt", "xlsx", "pdf"])
    uploaded_file_2 = col1.file_uploader("Escolha um arquivo: 2", type=["csv", "txt", "xlsx", "pdf"])    


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

    # Inserir o código JavaScript no Streamlit
    col1.markdown(javascript_code, unsafe_allow_html=True)
    # Widget de entrada de data
    selected_date = col1.date_input("Data de abertura: ", disabled=True)
    selected_date_send = col1.date_input("Data da requisição: ")

    # # # # # # # # # COLUNA 02 DE FORMS # # # # # # # # # # # # # # # # #
    obs = col2.text_area(label="Descrição Serviços:")
    tp_urg = col2.selectbox(label="Emegencial?", options=['SIM', 'NÃO'])
    gr_complexidade = col2.selectbox(label="Classificação emergencial:", options=['Biologico', 'Estruturais', 'Eletricos', 'Perdas ou Avarias', 'Operação', 'Imagem'])
    nr_chamado = col2.text_input(label="Número do chamado")

css = """
<style>
/* Define a cor de fundo do botão */
.stButton>button {
    background-color: red; /* Altere a cor para a cor desejada */
    color: white; /* Define a cor do texto no botão */
}
</style>
"""

# Aplicar o CSS personalizado usando st.markdown
st.markdown(css, unsafe_allow_html=True)

st.button(label="Registar", use_container_width=True)