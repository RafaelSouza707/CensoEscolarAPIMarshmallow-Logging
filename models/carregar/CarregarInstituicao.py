import csv
from models.objeto.InstituicaoEnsino import InstituicaoEnsino

def _safe_int(value):
    try:
        return int(str(value).strip() or 0)
    except (ValueError, TypeError):
        return 0

def carregarInstituicao(CAMINHO_INSTITUICOES):
    instituicoes = []
    with open(CAMINHO_INSTITUICOES, "r", encoding="latin1") as f:
        leitor = csv.DictReader(f, delimiter=';')
        #print("Verificar Nomes: ")
        #print(leitor.fieldnames)

        for linha in leitor:
            codigo = linha.get("CO_ENTIDADE")
            nome = linha.get("NO_ENTIDADE")

            if not codigo or not nome:
                continue

            instituicoes.append(
                InstituicaoEnsino(
                    codigo=codigo,
                    nome=nome,
                    co_regiao=_safe_int(linha.get("CO_REGIAO")),
                    no_regiao=_safe_int(linha.get("NO_REGIAO")),
                    co_uf=_safe_int(linha.get("CO_UF")),
                    no_uf=_safe_int(linha.get("NO_UF")),
                    co_municipio=_safe_int(linha.get("CO_MUNICIPIO")),
                    qt_mat_bas=_safe_int(linha.get("QT_MAT_BAS")),
                    qt_mat_prof=_safe_int(linha.get("QT_MAT_PROF")),
                    qt_mat_eja=_safe_int(linha.get("QT_MAT_EJA")),
                    qt_mat_esp=_safe_int(linha.get("QT_MAT_ESP")),
                    qt_mat_fund=_safe_int(linha.get("QT_MAT_FUND")),
                    qt_mat_inf=_safe_int(linha.get("QT_MAT_INF")),
                    qt_mat_med=_safe_int(linha.get("QT_MAT_MED")),
                    qt_mat_zr_na=_safe_int(linha.get("QT_MAT_ZR_NA")),
                    qt_mat_zr_rur=_safe_int(linha.get("QT_MAT_ZR_RUR")),
                    qt_mat_zr_urb=_safe_int(linha.get("QT_MAT_ZR_URB")),
                )
            )

    return instituicoes