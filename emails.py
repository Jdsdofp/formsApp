import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Função para ler o conteúdo do arquivo HTML
def enviar_email(email_usuario, solicitante, solicitacao, loja, servico, chamado, atendente, data, registro):
    def read_template(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            template = file.read()
        return template

    # Configurações do servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Credenciais de login
    email_username = 'controlscsscs@gmail.com'
    email_password = 'cwnczfmxcamupyml'

    # Configurações do e-mail
    sent_from = email_username
    sent_to = str(email_usuario[0])
    email_subject = F'ATENDIMENTO DE SOLICITAÇÃO // LOJA {loja} - SOLICITAÇÃO {solicitacao}'

    

    # Carregando o template HTML
    template = read_template('template.html')

    # Substituindo a variável {{ nome }} pelo nome do destinatário
    nome_destinatario = str(solicitante)
    nrSolicitacao = str(solicitacao)
    nmLoja = str(loja)
    desServico = str(servico)
    nrChamado = str(chamado)
    nmAtendente = str(atendente)
    dtAtendimento = str(data)
    cdRegistro = str(registro)

    # Criando a mensagem multipart
    message = MIMEMultipart()
    message['From'] = sent_from
    message['To'] = sent_to
    message['Subject'] = email_subject

    # Substituindo as variáveis no template HTML pelos valores correspondentes
    email_body = template.replace('{{nomeSolicitante}}', nome_destinatario)
    email_body = email_body.replace('{{solicitacao}}', nrSolicitacao)
    email_body = email_body.replace('{{nomeLoja}}', nmLoja)
    email_body = email_body.replace('{{servico}}', desServico)
    email_body = email_body.replace('{{chamado}}', nrChamado)
    email_body = email_body.replace('{{atendente}}', nmAtendente)
    email_body = email_body.replace('{{data}}', dtAtendimento)
    email_body = email_body.replace('{{registro}}', cdRegistro)

    # Adicionando o corpo HTML ao e-mail
    message.attach(MIMEText(email_body, 'html', 'utf-8'))

    try:
        # Iniciando a conexão com o servidor SMTP
        smtpserver = smtplib.SMTP(smtp_server, smtp_port)
        smtpserver.ehlo()
        smtpserver.starttls()  # Habilitando a criptografia TLS
        smtpserver.ehlo()
        
        # Fazendo login
        smtpserver.login(email_username, email_password)
        
        # Enviando o e-mail
        smtpserver.sendmail(sent_from, sent_to, message.as_string())
        
        print(f'E-mail enviado com sucesso! - {nome_destinatario} / {nrSolicitacao}')

    except Exception as e:
        print('Erro ao enviar e-mail:', str(e))

    finally:
        # Fechando a conexão com o servidor SMTP
        if smtpserver:
            smtpserver.quit()
