import subprocess

# Executa o comando pip freeze para obter as dependências instaladas
output = subprocess.check_output(['pip', 'freeze']).decode()

# Separa as linhas da saída
lines = output.split('\n')

# Remove números de versão e salva os nomes dos pacotes em uma lista
packages = [line.split('==')[0] for line in lines if line.strip()]

# Escreve os nomes dos pacotes no arquivo requirements.txt
with open('requirements.txt', 'w') as f:
    f.write('\n'.join(packages))

print("Arquivo requirements.txt gerado com sucesso.")
