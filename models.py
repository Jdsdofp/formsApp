from database import *


mydb = client["mydatabase"]

# Crie uma coleção chamada "customers"
col_solicitacao = mydb["registros"]
col_filiais = mydb["filiais"]
col_usuario = mydb["usuarios"]


# Recuperar todos os documentos e ordená-los por cod_registro
documentos = col_solicitacao.find().sort("cod_registro")

# Inicializar um contador para a nova sequência de cod_registro
novo_cod_registro = 1

# Atualizar cada documento com o novo valor de cod_registro
for documento in documentos:
    # Atualizar o campo cod_registro com o novo valor sequencial
    col_solicitacao.update_one(
        {"_id": documento["_id"]},
        {"$set": {"cod_registro": novo_cod_registro}}
    )
    # Incrementar o contador para o próximo valor de cod_registro
    novo_cod_registro += 1

# Exibir mensagem de conclusão
print("Valores de cod_registro reordenados com sucesso.")