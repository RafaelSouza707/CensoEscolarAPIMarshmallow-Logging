import sqlite3
from models.carregar.CarregarInstituicao import carregarInstituicao

DATABASE_NAME = "censoescolar.db"
CAMINHO_INSTITUICOES = "data/microdados_ed_basica_2024.csv"
SCHEMA_FILE = "schema.sql"

def create_tables():
    print("Iniciando criação do banco de dados...")
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    with open(SCHEMA_FILE, encoding="utf-8") as f:
        print("Criando as tabelas...")
        conn.executescript(f.read())

    instituicoes = carregarInstituicao(CAMINHO_INSTITUICOES)
    instituicoesNordeste = [
        i for i in instituicoes if i.co_regiao == 2
    ]

    print("Inserindo instituições do CSV...")
    for i in instituicoesNordeste:
        cursor.execute("""
            INSERT INTO tb_instituicao(
                codigo, nome,
                no_entidade, co_entidade,
                co_regiao, no_regiao,
                co_uf, sg_uf,
                co_municipio,
                no_mesorregiao, co_mesorregiao,
                no_microrregiao, co_microrregiao,
                nu_ano_censo,
                qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp,
                qt_mat_fund, qt_mat_inf, qt_mat_med,
                qt_mat_zr_na, qt_mat_zr_rur, qt_mat_zr_urb,
                qt_mat_total
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            i.codigo, i.nome,
            i.no_entidade, i.co_entidade,
            i.co_regiao, i.no_regiao,
            i.co_uf, i.sg_uf,
            i.co_municipio,
            i.no_mesorregiao, i.co_mesorregiao,
            i.no_microrregiao, i.co_microrregiao,
            i.nu_ano_censo,
            i.qt_mat_bas, i.qt_mat_prof, i.qt_mat_eja, i.qt_mat_esp,
            i.qt_mat_fund, i.qt_mat_inf, i.qt_mat_med,
            i.qt_mat_zr_na, i.qt_mat_zr_rur, i.qt_mat_zr_urb,
            i.qt_mat_total
        ))

    conn.commit()

    print("Fechando conexão...")
    conn.close()


if __name__ == "__main__":
    create_tables()