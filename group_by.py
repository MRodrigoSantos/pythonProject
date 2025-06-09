import sqlite3

print("Região Número de Estados")
print("====== =================")

with sqlite3.connect("brasil.db") as conexão:
    for região in conexão.execute("""
        select região, count(*)
        from estados
        group by região
    """):
        print("{0:6} {1:17}".format(*região))
