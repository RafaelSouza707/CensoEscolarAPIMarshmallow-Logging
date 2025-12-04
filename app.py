from flask import Flask, request, jsonify
import sqlite3
import math
from logging_config import logger
from marshmallow import ValidationError
from helpers.schemas.instituicao_schema import InstituicaoUpdateSchema, InstituicaoCreateSchema
from helpers.database import get_conn

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

    conn, cursor = get_conn()

    cursor.execute("SELECT COUNT(*) as total FROM tb_instituicao")
    total = cursor.fetchone()["total"]

    total_paginas = math.ceil(total/tamanho)

    cursor.execute("SELECT * FROM tb_instituicao LIMIT ? OFFSET ?", (tamanho, offset))
    registros = [dict(row) for row in cursor.fetchall()]

    logger.info("Requisição realizada com sucesso.")
    return jsonify(registros), 200


@app.get("/instituicoesensino/<codigo>")
def getInstituicaoByCodigo(codigo: str):
    conn, cursor = get_conn()
    cursor.execute("""
        SELECT
            codigo,
            nome,
            no_entidade,
            co_entidade,
            co_regiao,
            no_regiao,
            co_uf,
            sg_uf,
            co_municipio,
            no_mesorregiao,
            co_mesorregiao,
            no_microrregiao,
            co_microrregiao,
            nu_ano_censo,
            qt_mat_bas,
            qt_mat_prof,
            qt_mat_eja,
            qt_mat_esp,
            qt_mat_fund,
            qt_mat_inf,
            qt_mat_med,
            qt_mat_zr_na,
            qt_mat_zr_rur,
            qt_mat_zr_urb,
            qt_mat_total
        FROM tb_instituicao
        WHERE codigo = ?
    """, (codigo,))
    linha = cursor.fetchone()

    if linha is None:
        logger.info("Falha na requisição: instituição não localizada...")
        return jsonify({"erro": "Instituição não encontrada"}), 404
    
    instituicao = {
        "codigo": linha[0],
        "nome": linha[1],
        "no_entidade": linha[2],
        "co_entidade": linha[3],
        "co_regiao": linha[4],
        "no_regiao": linha[5],
        "co_uf": linha[6],
        "sg_uf": linha[7],
        "co_municipio": linha[8],
        "no_mesorregiao": linha[9],
        "co_mesorregiao": linha[10],
        "no_microrregiao": linha[11],
        "co_microrregiao": linha[12],
        "nu_ano_censo": linha[13],
        "qt_mat_bas": linha[14],
        "qt_mat_prof": linha[15],
        "qt_mat_eja": linha[16],
        "qt_mat_esp": linha[17],
        "qt_mat_fund": linha[18],
        "qt_mat_inf": linha[19],
        "qt_mat_med": linha[20],
        "qt_mat_zr_na": linha[21],
        "qt_mat_zr_rur": linha[22],
        "qt_mat_zr_urb": linha[23],
        "qt_mat_total": linha[24],
    }

    logger.info("Requisição realizada com sucesso.")
    return jsonify(instituicao), 200


@app.post("/instituicoesensino")
def addInstituicao():
    logger.info("Requisição para criação de uma nova instituição.")

    data = request.json

    if not data:
        logger.warning("Nenhum JSON enviado.")
        return jsonify({"erro": "JSON não enviado"}), 400

    schema = InstituicaoCreateSchema()

    try:
        dados_validados = schema.load(data)
    except ValidationError as err:
        logger.warning(f"Erro de validação: {err.messages}")
        return jsonify({"erro": err.messages}), 400

    conn, cursor = get_conn()

    try:
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
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            dados_validados["codigo"],
            dados_validados["nome"],
            dados_validados["no_entidade"],
            dados_validados["co_entidade"],
            dados_validados["co_regiao"],
            dados_validados["no_regiao"],
            dados_validados["co_uf"],
            dados_validados["sg_uf"],
            dados_validados["co_municipio"],
            dados_validados["no_mesorregiao"],
            dados_validados["co_mesorregiao"],
            dados_validados["no_microrregiao"],
            dados_validados["co_microrregiao"],
            dados_validados["nu_ano_censo"],
            dados_validados["qt_mat_bas"],
            dados_validados["qt_mat_prof"],
            dados_validados["qt_mat_eja"],
            dados_validados["qt_mat_esp"],
            dados_validados["qt_mat_fund"],
            dados_validados["qt_mat_inf"],
            dados_validados["qt_mat_med"],
            dados_validados["qt_mat_zr_na"],
            dados_validados["qt_mat_zr_rur"],
            dados_validados["qt_mat_zr_urb"],
            dados_validados["qt_mat_total"]
        ))

        novo_id = cursor.lastrowid

        logger.info("Instituição criada com sucesso.")
        return jsonify({"mensagem": "Instituição cadastrada", "id": novo_id}), 201

    except Exception as e:
        logger.error(f"Erro ao inserir: {e}")
        return jsonify({"erro": "Erro interno ao inserir."}), 500
        

@app.put("/instituicoesensino/<codigo>")
def updateInstituicao(codigo):
    logger.info(f"Requisição PUT para atualizar instituição {codigo}")
    data = request.json

    schema = InstituicaoUpdateSchema()
    try:
        dados_validados = schema.load(data)
    except ValidationError as err:
        logger.warning(f"Erro de validação no PUT: {err.messages}")
        return jsonify({"erro": "Dados inválidos", "detalhes": err.messages}), 400

    conn, cursor = get_conn()

    cursor.execute("SELECT * FROM tb_instituicao WHERE codigo = ?", (codigo,))
    registro = cursor.fetchone()

    if registro is None:
        logger.info("Instituição não encontrada")
        return jsonify({"erro": "Instituição não encontrada"}), 404

    registro_dict = dict(registro)

    try:
        campos_matriculas = [
            "qt_mat_bas", "qt_mat_prof", "qt_mat_eja", "qt_mat_esp",
            "qt_mat_fund", "qt_mat_inf", "qt_mat_med",
            "qt_mat_zr_na", "qt_mat_zr_rur", "qt_mat_zr_urb"
        ]

        if any(campo in dados_validados for campo in campos_matriculas):
            novo_total = 0
            for campo in campos_matriculas:
                valor = dados_validados.get(campo, registro_dict[campo])
                novo_total += int(valor or 0)
            dados_validados["qt_mat_total"] = novo_total

        campos_update = ", ".join([f"{campo} = ?" for campo in dados_validados.keys()])
        valores = list(dados_validados.values())
        valores.append(codigo)

        cursor.execute(
            f"UPDATE tb_instituicao SET {campos_update} WHERE codigo = ?",
            valores
        )

        conn.commit()
        logger.info(f"Institution {codigo} atualizada com sucesso.")

        return jsonify({"mensagem": "Instituição atualizada"}), 200

    except Exception as e:
        logger.error(f"Erro ao atualizar instituição: {e}")
        return jsonify({"erro": "Erro interno ao atualizar"}), 500



@app.delete("/instituicoesensino/<codigo>")
def deleteInstituicao(codigo):
    conn, cursor = get_conn()

    cursor.execute("SELECT id FROM tb_instituicao WHERE codigo = ?", (codigo,))
    linha = cursor.fetchone()

    if linha is None:
        logger.info("Instituição não encontrada.")
        return jsonify({"erro": "Instituição não encontrada"}), 404

    try:
        cursor.execute("DELETE FROM tb_instituicao WHERE codigo = ?", (codigo,))
        conn.commit()
        logger.info("Instituição removida com sucesso.")

        return jsonify({"mensagem": "Instituição removida"}), 200

    except Exception as e:
        logger.error(f"Erro ao deletar: {e}")
        return jsonify({"erro": "Erro interno ao remover"}), 500


@app.get("/instituicoesensino/ranking/<ano>")
def ranking(ano):
    conn, cursor = get_conn()

    cursor.execute("""
        SELECT *
        FROM tb_instituicao
        WHERE nu_ano_censo = ?
        ORDER BY qt_mat_total DESC
        LIMIT 10;
    """, (ano,))

    registros = cursor.fetchall()

    lista = [dict(linha) for linha in registros]

    logger.info("Requisição realizada com sucesso.")
    return jsonify(lista), 200


if __name__ == '__main__':
    
    app.run(debug=True)