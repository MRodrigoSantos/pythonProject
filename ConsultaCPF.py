# Nome do arquivo que contém os dados dos clientes
arquivo = "clientes.txt"

# Solicita o CPF do cliente
cpf_busca = input("Digite o CPF do cliente que deseja buscar: ").strip()

# Variável para indicar se o cliente foi encontrado
cliente_encontrado = False

# Abre o arquivo para leitura
with open(arquivo, "r", encoding="utf-8") as f:
    for linha in f:
        nome, pix, cpf = linha.strip().split(", ")
        if cpf == cpf_busca:
            print("\nCliente encontrado:")
            print(f"Nome: {nome}")
            print(f"Chave Pix: {pix}")
            print(f"CPF: {cpf}")
            cliente_encontrado = True
            break

# Se nenhum cliente for encontrado com o CPF informado
if not cliente_encontrado:
    print("\nNenhum cliente encontrado com esse CPF.")