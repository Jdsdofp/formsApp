from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from models import *

def create_report(pdf_file, dados):
    # Crie um arquivo PDF usando reportlab com o tamanho A4
    pdf = canvas.Canvas(pdf_file, pagesize=A4)

    # Adicione cabeçalho
    add_header(pdf)

    # Adicione corpo do relatório
    add_body(pdf, dados)

    # Adicione rodapé
    add_footer(pdf)

    # Salve o PDF
    pdf.save()

def add_header(pdf):
    # Adicione um título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColorRGB(0.4, 0.4, 0.5)
    pdf.drawString(18, 815, "Relatório Controle de Solicitação")

    # Adicione um bloco com bordas arredondadas que ocupa todo o espaço superior
    pdf.setStrokeColorRGB(0.4, 0.4, 0.5)  # Cor preta
    pdf.setFillColorRGB(1, 1, 1)  # Cor branca para o preenchimento interno
    pdf.roundRect(110, 650, 470, 150, radius=10, fill=1)  # Coordenadas e tamanhos do bloco

    # Retângulo para imagem com bordas arredondadas
    pdf.setStrokeColorRGB(0.4, 0.4, 0.5)  # Cor preta
    pdf.setFillColorRGB(1, 1, 1)  # Cor branca para o preenchimento interno
    pdf.roundRect(18, 650, 90, 150, radius=10, fill=1)  # Coordenadas e tamanhos do bloco

    # Adicione a imagem ao retângulo
    imagem_path = "lg_Drogaria_Globo.png"  # Substitua pelo caminho da sua imagem
    pdf.drawImage(imagem_path, 20, 650, width=80, height=150, preserveAspectRatio=True)
    pdf.setFont("Helvetica", 9)
    pdf.setFillColorRGB(0.4, 0.4, 0.5)
    pdf.drawString(38, 659, f"Control SCs")

    # Adicione o conteúdo do bloco
    pdf.setFont("Helvetica", 12)
    pdf.setFillColorRGB(0, 0, 0)  # Mude a cor do texto para preto
    pdf.drawString(115, 780, f"Nº REGISTRO: {dados['cod_registro']}")
    pdf.drawString(115, 760, f"SOLICITANTE: {dados['solicitante']}")
    pdf.drawString(115, 740, f"LOJA: {dados['loja']} - {dados['cod_loja']}")
    pdf.drawString(115, 720, f"Nº SOLICITAÇÃO: {dados['nr_solicitacao']}")
    pdf.drawString(115, 700, f"STATUS: {dados['status']}")
    pdf.drawString(115, 680, f"CHAMADO: {dados['nr_chamado']}")
    pdf.drawString(115, 660, f"DATA ABERTURA: {dados['data_abertura']}")


    #ORDEM DE COMPRAS
    pdf.drawString(230, 780, f"Nº REGISTRO: {dados['cod_registro']}")

def add_body(pdf, dados):
    # Adicione um bloco com bordas arredondadas que ocupa todo o espaço do corpo
    pdf.setStrokeColorRGB(0.4, 0.4, 0.5)  # Cor preta
    pdf.setFillColorRGB(1, 1, 1)  # Cor branca para o preenchimento interno
    pdf.roundRect(20, 27, 560, 620, radius=10, fill=1)  # Coordenadas e tamanhos do bloco

    # Adicione o texto desc_servico
    pdf.setFont("Helvetica", 12)  # Escolha a fonte e tamanho desejados
    pdf.setFillColorRGB(0, 0, 0)  # Cor preta

    # Adicione o texto desc_servico
    pdf.setFont("Helvetica", 10)  # Escolha a fonte e tamanho desejados
    pdf.setFillColorRGB(0, 0, 0)  # Cor preta

    desc_servico = dados.get("desc_servico", "")

    # Define a posição inicial do texto
    text_object = pdf.beginText(30, 620)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColorRGB(0, 0, 0)  # Cor preta

    # Adiciona o conteúdo do texto com quebras de linha
    text_object.textLine("Descrição do Serviço:")
    for line in desc_servico.splitlines():
        text_object.textLine(line)

    # Adicione a classificação do serviço sem aspas e colchetes
    class_servico = ", ".join(dados.get("class_servico", []))
    pdf.drawString(30, 585, f"Classificação Serviço: {class_servico}")

    # Desenha o texto no PDF
    pdf.drawText(text_object)


def add_footer(pdf):
    # Adicione um rodapé simples
    pdf.setFont("Helvetica", 10)
    pdf.drawString(18, 30, "Este é o rodapé do relatório.")

# Restante do código permanece inalterado

# Dados para inserir no relatório
dados = [registros for registros in col_solicitacao.find()][0]


# Caminho para o PDF do relatório
pdf_report_path = 'relatorio_servico.pdf'

# Criar o relatório com os dados fornecidos
create_report(pdf_report_path, dados)
