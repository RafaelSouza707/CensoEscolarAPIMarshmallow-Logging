from marshmallow import Schema, fields, validates, ValidationError


class InstituicaoCreateSchema(Schema):
    codigo = fields.String(required=True)
    nome = fields.String(required=True)

    no_entidade = fields.String(allow_none=True)
    co_entidade = fields.Integer(allow_none=True)

    co_regiao = fields.Integer(required=True)
    no_regiao = fields.String(allow_none=True)

    co_uf = fields.Integer(required=True)
    sg_uf = fields.String(allow_none=True)

    co_municipio = fields.Integer(required=True)

    no_mesorregiao = fields.String(allow_none=True)
    co_mesorregiao = fields.Integer(allow_none=True)

    no_microrregiao = fields.String(allow_none=True)
    co_microrregiao = fields.Integer(allow_none=True)

    nu_ano_censo = fields.Integer(allow_none=True)

    qt_mat_bas = fields.Integer(required=True)
    qt_mat_prof = fields.Integer(required=True)
    qt_mat_eja = fields.Integer(required=True)
    qt_mat_esp = fields.Integer(required=True)
    qt_mat_fund = fields.Integer(required=True)
    qt_mat_inf = fields.Integer(required=True)
    qt_mat_med = fields.Integer(required=True)

    qt_mat_zr_na = fields.Integer(required=True)
    qt_mat_zr_rur = fields.Integer(required=True)
    qt_mat_zr_urb = fields.Integer(required=True)

    qt_mat_total = fields.Integer(required=True)


# Schema para o PUT (tudo opcional)
class InstituicaoUpdateSchema(Schema):
    codigo = fields.String(required=False)
    nome = fields.String(required=False)

    no_entidade = fields.String(required=False)
    co_entidade = fields.Integer(required=False)

    co_regiao = fields.Integer(required=False)
    no_regiao = fields.String(required=False)

    co_uf = fields.Integer(required=False)
    sg_uf = fields.String(required=False)

    co_municipio = fields.Integer(required=False)

    no_mesorregiao = fields.String(required=False)
    co_mesorregiao = fields.Integer(required=False)

    no_microrregiao = fields.String(required=False)
    co_microrregiao = fields.Integer(required=False)

    nu_ano_censo = fields.Integer(required=False)

    qt_mat_bas = fields.Integer(required=False)
    qt_mat_prof = fields.Integer(required=False)
    qt_mat_eja = fields.Integer(required=False)
    qt_mat_esp = fields.Integer(required=False)
    qt_mat_fund = fields.Integer(required=False)
    qt_mat_inf = fields.Integer(required=False)
    qt_mat_med = fields.Integer(required=False)

    qt_mat_zr_na = fields.Integer(required=False)
    qt_mat_zr_rur = fields.Integer(required=False)
    qt_mat_zr_urb = fields.Integer(required=False)

    qt_mat_total = fields.Integer(required=False)