import pandas as pd
import sqlite3

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

DATABASE_NAME = "censoescolar.db"

def mostrar_pagina_sql(pagina=1, tamanho=100):
    conn = sqlite3.connect(DATABASE_NAME)

    total = pd.read_sql_query("SELECT COUNT(*) as total FROM tb_instituicao", conn)["total"][0]
    total_paginas = (total + tamanho - 1) // tamanho

    if pagina < 1 or pagina > total_paginas:
        print(f"Página inválida! Selecione entre 1 e {total_paginas}")
        conn.close()
        return
    
    offset = (pagina - 1) * tamanho
    query = f"SELECT * FROM tb_instituicao LIMIT {tamanho} OFFSET {offset}"
    df = pd.read_sql_query(query, conn)

    conn.close()

    print(f"\nMostrando {len(df)} linhas — registros {offset+1} até {min(offset+tamanho, total)} de {total}")
    print(df)


mostrar_pagina_sql(pagina=1, tamanho=100)
