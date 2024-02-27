from database import *


mydb = client["mydatabase"]

# Crie uma coleção chamada "customers"
col_solicitacao = mydb["registros"]
col_filiais = mydb["filiais"]
col_usuario = mydb["usuarios"]


# Critério de busca
filtro = {"solicitante": "Weslley"}

# Novo valor a ser definido
novo_valor = {"$set": {"solicitante": "Weslley Passos"}}

# Atualizando os documentos que correspondem ao critério
resultado = col_solicitacao.update_many(filtro, novo_valor)

# Exibindo o número de documentos atualizados
print(f"{resultado.modified_count} documentos foram atualizados.")