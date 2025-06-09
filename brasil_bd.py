import sqlite3
from contextlib import closing

# Lista de estados e suas populações
dados = [
    ["São Paulo", 43663672], ["Minas Gerais", 20593366], ["Rio de Janeiro", 16369178],
    ["Bahia", 15044127], ["Rio Grande do Sul", 11164050], ["Paraná", 10997462],
    ["Pernambuco", 9208511], ["Ceará", 8778575], ["Pará", 7969655],
    ["Maranhão", 6794298], ["Santa Catarina", 6634250], ["Goiás", 6434052],
    ["Paraíba", 3914418], ["Espírito Santo", 3838363], ["Amazonas", 3807923],
    ["Rio Grande do Norte", 3373960], ["Alagoas", 3300938], ["Piauí", 3184165],
    ["Mato Grosso", 3182114], ["Distrito Federal", 2789761], ["Mato Grosso do Sul", 2587267],
    ["Sergipe", 2195662], ["Rondônia", 1728214], ["Tocantins", 1478163],
    ["Acre", 776463], ["Amapá", 734995], ["Roraima", 488072],
]

# Conectando ao banco de dados e criando a tabela
with sqlite3.connect("brasil.db") as conexão:
    conexão.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    with closing(conexão.cursor()) as cursor:
        # Criar tabela (caso ainda não exista)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                populacao INTEGER
            )
        """)
        # Inserir os dados
        cursor.executemany("INSERT INTO estados (nome, populacao) VALUES (?, ?)", dados)
    conexão.commit()
