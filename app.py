from flask import Flask, request, jsonify
import sqlite3
import math
from logging_config import logger

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
    logger.info("Requisição realizada com sucesso.")
    return jsonify(registros), 200


@app.get("/instituicoesensino/<codigo>")
def getInstituicaoByCodigo(codigo: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp, qt_mat_fund, qt_mat_inf, qt_mat_med, qt_mat_zr_na, qt_mat_zr_rur, qt_mat_zr_urb FROM tb_instituicao WHERE codigo = ?", (codigo,))
    linha = cursor.fetchone()
    conn.close()

    if linha is None:
        logger.info("Falha na requisição: instituição não localizada...")
        return jsonify({"erro": "Instituição não encontrada"}), 404
    
    instituicoes = { "id": linha[0], "codigo": linha[1], "nome": linha[2], "co_uf": linha[3], "co_municipio": linha[4], "qt_mat_bas": linha[5], "qt_mat_prof": linha[6], "qt_mat_eja": linha[7], "qt_mat_esp": linha[8], "qt_mat_fund": linha[9], "qt_mat_inf": linha[10], "qt_mat_med": linha[11], "qt_mat_zr_na": linha[12], "qt_mat_zr_rur": linha[13], "qt_mat_zr_urb": linha[14]}
    logger.info("Requisição realizada com sucesso.")
    return jsonify(instituicoes), 200


@app.post("/instituicoesensino")
def addInstituicao():
    data = request.json

    campos_obrigatorios = [
        "codigo", "nome", "co_uf", "co_municipio",
        "qt_mat_bas", "qt_mat_prof", "qt_mat_eja", "qt_mat_esp",
        "qt_mat_fund", "qt_mat_inf", "qt_mat_med",
        "qt_mat_zr_na", "qt_mat_zr_rur", "qt_mat_zr_urb"
    ]

    # Verifica campos faltando
    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({"erro": f"Campo obrigatório faltando: {campo}"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO tb_instituicao
            (codigo, nome, co_uf, co_municipio,
             qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp,
             qt_mat_fund, qt_mat_inf, qt_mat_med,
             qt_mat_zr_na, qt_mat_zr_rur, qt_mat_zr_urb)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data["codigo"], data["nome"], data["co_uf"], data["co_municipio"],
            data["qt_mat_bas"], data["qt_mat_prof"], data["qt_mat_eja"], data["qt_mat_esp"],
            data["qt_mat_fund"], data["qt_mat_inf"], data["qt_mat_med"],
            data["qt_mat_zr_na"], data["qt_mat_zr_rur"], data["qt_mat_zr_urb"]
        ))

        conn.commit()
        novo_id = cursor.lastrowid
        logger.info("Instituição criada com sucesso.")

        return jsonify({"mensagem": "Instituição cadastrada", "id": novo_id}), 201

    except Exception as e:
        logger.error(f"Erro ao inserir: {e}")
        return jsonify({"erro": "Erro interno ao inserir."}), 500

    finally:
        conn.close()


@app.put("/instituicoesensino/<codigo>")
def updateInstituicao(codigo):
    data = request.json

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM tb_instituicao WHERE codigo = ?", (codigo,))
    linha = cursor.fetchone()

    if linha is None:
        conn.close()
        return jsonify({"erro": "Instituição não encontrada"}), 404

    try:
        cursor.execute("""
            UPDATE tb_instituicao SET
                nome = ?, co_uf = ?, co_municipio = ?,
                qt_mat_bas = ?, qt_mat_prof = ?, qt_mat_eja = ?, qt_mat_esp = ?,
                qt_mat_fund = ?, qt_mat_inf = ?, qt_mat_med = ?,
                qt_mat_zr_na = ?, qt_mat_zr_rur = ?, qt_mat_zr_urb = ?
            WHERE codigo = ?
        """, (
            data.get("nome"), data.get("co_uf"), data.get("co_municipio"),
            data.get("qt_mat_bas"), data.get("qt_mat_prof"), data.get("qt_mat_eja"), data.get("qt_mat_esp"),
            data.get("qt_mat_fund"), data.get("qt_mat_inf"), data.get("qt_mat_med"),
            data.get("qt_mat_zr_na"), data.get("qt_mat_zr_rur"), data.get("qt_mat_zr_urb"),
            codigo
        ))

        conn.commit()
        logger.info("Instituição atualizada com sucesso.")

        return jsonify({"mensagem": "Instituição atualizada"}), 200

    except Exception as e:
        logger.error(f"Erro ao atualizar: {e}")
        return jsonify({"erro": "Erro interno ao atualizar"}), 500

    finally:
        conn.close()


@app.delete("/instituicoesensino/<codigo>")
def deleteInstituicao(codigo):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM tb_instituicao WHERE codigo = ?", (codigo,))
    linha = cursor.fetchone()

    if linha is None:
        conn.close()
        return jsonify({"erro": "Instituição não encontrada"}), 404

    try:
        cursor.execute("DELETE FROM tb_instituicao WHERE codigo = ?", (codigo,))
        conn.commit()
        logger.info("Instituição removida com sucesso.")

        return jsonify({"mensagem": "Instituição removida"}), 200

    except Exception as e:
        logger.error(f"Erro ao deletar: {e}")
        return jsonify({"erro": "Erro interno ao remover"}), 500

    finally:
        conn.close()


# === End Instituições ===
if __name__ == '__main__':
    
    app.run(debug=True)