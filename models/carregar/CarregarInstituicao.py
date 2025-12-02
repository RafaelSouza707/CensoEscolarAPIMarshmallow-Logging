import csv
from marshmallow import ValidationError
from logging_config import logger
from models.schemas.instituicao_schema import InstituicaoSchema
from models.objeto.InstituicaoEnsino import InstituicaoEnsino

def carregarInstituicao(CAMINHO_INSTITUICOES):
    schema = InstituicaoSchema()
    instituicoes = []

    with open(CAMINHO_INSTITUICOES, "r", encoding="latin1") as f:
        leitor = csv.DictReader(f, delimiter=';')

        for linha in leitor:

            try:
                dados = schema.load(linha)
            except ValidationError as e:
                logger.warning(
                    f"Erro na linha (CO_ENTIDADE={linha.get('CO_ENTIDADE')}): {e.messages}"
                )
                continue

            instituicoes.append(
                InstituicaoEnsino(**dados)
            )

    return instituicoes
