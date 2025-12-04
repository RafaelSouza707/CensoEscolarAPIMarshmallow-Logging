class InstituicaoEnsino:
    def __init__(
        self,
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
        qt_mat_zr_urb
    ):
        self.codigo = codigo
        self.nome = nome
        self.no_entidade = no_entidade
        self.co_entidade = co_entidade
        self.co_regiao = co_regiao
        self.no_regiao = no_regiao
        self.co_uf = co_uf
        self.sg_uf = sg_uf
        self.co_municipio = co_municipio
        self.no_mesorregiao = no_mesorregiao
        self.co_mesorregiao = co_mesorregiao
        self.no_microrregiao = no_microrregiao
        self.co_microrregiao = co_microrregiao
        self.nu_ano_censo = nu_ano_censo

        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_eja = qt_mat_eja
        self.qt_mat_esp = qt_mat_esp
        self.qt_mat_fund = qt_mat_fund
        self.qt_mat_inf = qt_mat_inf
        self.qt_mat_med = qt_mat_med
        self.qt_mat_zr_na = qt_mat_zr_na
        self.qt_mat_zr_rur = qt_mat_zr_rur
        self.qt_mat_zr_urb = qt_mat_zr_urb

        self.qt_mat_total = (
            qt_mat_bas +
            qt_mat_prof +
            qt_mat_eja +
            qt_mat_esp +
            qt_mat_fund +
            qt_mat_inf +
            qt_mat_med +
            qt_mat_zr_na +
            qt_mat_zr_rur +
            qt_mat_zr_urb
        )

    def to_json(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "co_uf": self.co_uf,
            "co_municipio": self.co_municipio,
            "qt_mat_bas": self.qt_mat_bas,
            "qt_mat_prof": self.qt_mat_prof,
            "qt_mat_eja": self.qt_mat_eja,
            "qt_mat_esp": self.qt_mat_esp,
            "qt_mat_fund": self.qt_mat_fund,
            "qt_mat_inf": self.qt_mat_inf,
            "qt_mat_med": self.qt_mat_med,
            "qt_mat_zr_na": self.qt_mat_zr_na,
            "qt_mat_zr_rur": self.qt_mat_zr_rur,
            "qt_mat_zr_urb": self.qt_mat_zr_urb,
            "qt_mat_total": self.qt_mat_total
        }
