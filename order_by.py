import sqlite3

with sqlite3.connect("brasil.db") as conexão:
    conexão.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    print(f"{'Id':3s} {'Estado':<20s} {'População':>12s}")
    print("=" * 40)
    for estado in conexão.execute("SELECT * FROM estados ORDER BY nome"):
        print(f"{estado['id']:3d} {estado['nome']:<20s} {estado['populacao']:12d}")
