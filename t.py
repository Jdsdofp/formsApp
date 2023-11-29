import pkg_resources

def generate_requirements():
    # Obtém todas as distribuições instaladas
    installed_distributions = pkg_resources.working_set

    # Gera uma lista apenas com os nomes das bibliotecas
    libraries = [dist.project_name for dist in installed_distributions]

    # Escreve a lista no arquivo requirements.txt
    with open("requirements.txt", "w") as file:
        for library in libraries:
            file.write(f"{library}\n")

if __name__ == "__main__":
    generate_requirements()
