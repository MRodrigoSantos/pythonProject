import sqlite3

with sqlite3.connect("brasil.db") as conexão:
    conexão.execute("""alter table estados
                       add sigla text""")
    conexão.execute("""alter table estados
                       add regiao text""")

dados = [
    ["SP", "SE", "São Paulo"],["MG", "SE", "Minas Gerais"],["RJ", "SE", "Rio de Janeiro"],["BA", "NE", "Bahia"],
    ["RS", "S", "Rio Grande do Sul"],["PR", "S", "Paraná"],["PE", "NE", "Pernambuco"],["CE", "NE", "Ceará"],
    ["PA", "N", "Pará"],["MA", "NE", "Maranhão"],["SC", "S", "Santa Catarina"],["GO", "CO", "Goiás"],
    ["PB", "NE", "Paraíba"],["ES", "SE", "Espírito Santo"],["AM", "N", "Amazonas"],["RN", "NE", "Rio Grande do Norte"],
    ["AL", "NE", "Alagoas"],["PI", "NE", "Piauí"],["MT", "CO", "Mato Grosso"],["DF", "CO", "Distrito Federal"],
    ["MS", "CO", "Mato Grosso do Sul"],["SE", "NE", "Sergipe"],["RO", "N", "Rondônia"],["TO", "N", "Tocantins"],
    ["AC", "N", "Acre"],["AP", "N", "Amapá"],["RR", "N", "Roraima"],
]

with sqlite3.connect("brasil.db") as conexão:
    conexão.executemany(
        """update estados
           set sigla = ?,
           regiao = ?
           where nome = ?""",
        dados,
    )
