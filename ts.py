import streamlit as st

def main():
    st.title("Salvando texto no LocalStorage")

    # Definindo o JavaScript para salvar e carregar dados do LocalStorage
    save_script = """
    <script>
    // Função para salvar o texto no LocalStorage
    function saveText() {
        var text = document.getElementById('text').value;
        localStorage.setItem('savedText', text);
    }

    // Função para carregar o texto do LocalStorage
    function loadText() {
        var savedText = localStorage.getItem('savedText');
        if (savedText !== null) {
            document.getElementById('text').value = savedText;
        }
    }

    // Chamando a função para carregar o texto ao iniciar
    window.onload = loadText;
    </script>
    """

    # Exibindo a caixa de texto e chamando as funções JavaScript
    st.write(save_script, unsafe_allow_html=True)
    text = st.text_area("Digite um texto aqui:", key='text')
    
    # Salvando os dados no LocalStorage quando o usuário interagir com a caixa de texto
    st.write("<script>document.getElementById('text').addEventListener('input', saveText);</script>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
