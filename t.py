import subprocess
import re

# Executar o comando pip freeze para obter as dependências
result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)
output = result.stdout.decode('utf-8')

# Remover números de versão das dependências
dependencies = [re.sub(r'==.*', '', line) for line in output.split('\n') if line]

# Escrever as dependências no arquivo requirements.txt
with open('requirements.txt', 'w') as file:
    file.write('\n'.join(dependencies))

print("Arquivo requirements.txt gerado com sucesso.")
