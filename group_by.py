import sqlite3

with sqlite3.connect("exemplo.db") as conexão:
    conexão.execute("PRAGMA foreign_keys = ON")  # Ativa suporte a chave estrangeira

    conexão.execute("""
        CREATE TABLE IF NOT EXISTS departamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    conexão.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            departamento_id INTEGER,
            FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
        )
    """)
