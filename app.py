from flask import Flask, request, jsonify
import sqlite3
import math

app = Flask(__name__)
DATABASE = "censoescolar.db"


# Rota inicial
@app.get("/")
def index():
    return '{"versao":"2.0.0"}', 200


# Para realizar paginação => http://127.0.0.1:5000/instituicoesensino?pagina=2
# Por padrão a página inicial é a 1 com 100 entidades carregadas
@app.get("/instituicoesensino")
def getInstituicoesEnsinoCSV():

    pagina = int(request.args.get("pagina", 1))
    tamanho = int(request.args.get("tamanho", 100))

    if pagina < 1:
        pagina = 1

    offset = (pagina - 1) * tamanho

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM tb_instituicao")
    total = cursor.fetchone()["total"]

    total_paginas = math.ceil(total/tamanho)

    cursor.execute("SELECT * FROM tb_instituicao LIMIT ? OFFSET ?", (tamanho, offset))
    registros = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return jsonify(registros), 200


@app.get("/instituicoesensino/<codigo>")
def getInstituicaoByCodigo(codigo: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp, qt_mat_fund, qt_mat_inf, qt_mat_med, qt_mat_zr_na, qt_mat_zr_rur, qt_mat_zr_urb FROM tb_instituicao WHERE codigo = ?", (codigo,))
    linha = cursor.fetchone()
    conn.close()

    if linha is None:
        return jsonify({"erro": "Instituição não encontrada"}), 404
    
    instituicoes = { "id": linha[0], "codigo": linha[1], "nome": linha[2], "co_uf": linha[3], "co_municipio": linha[4], "qt_mat_bas": linha[5], "qt_mat_prof": linha[6], "qt_mat_eja": linha[7], "qt_mat_esp": linha[8], "qt_mat_fund": linha[9], "qt_mat_inf": linha[10], "qt_mat_med": linha[11], "qt_mat_zr_na": linha[12], "qt_mat_zr_rur": linha[13], "qt_mat_zr_urb": linha[14]}
    return jsonify(instituicoes), 200


# === End Instituições ===
if __name__ == '__main__':
    
    app.run(debug=True)