# Lista de clientes com nome, chave pix e CPF
clientes = [
    {"nome": "Ana Silva", "pix": "ana@gmail.com", "cpf": "123.456.789-00"},
    {"nome": "Bruno Souza", "pix": "bruno@empresa.com", "cpf": "987.654.321-00"},
    {"nome": "Carlos Lima", "pix": "carloslima@banco.com", "cpf": "111.222.333-44"}
]

# Nome do arquivo onde os dados serão salvos
arquivo = "clientes.txt"

# Abrindo o arquivo para escrita
with open(arquivo, "w", encoding="utf-8") as f:
    for cliente in clientes:
        linha = f"{cliente['nome']}, {cliente['pix']}, {cliente['cpf']}\n"
        f.write(linha)

print(f"Arquivo '{arquivo}' criado com sucesso.")