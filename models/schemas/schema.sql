CREATE TABLE IF NOT EXISTS tb_instituicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,

    no_entidade TEXT,
    co_entidade INTEGER,

    co_regiao INTEGER NOT NULL,
    no_regiao TEXT,

    co_uf INTEGER NOT NULL,
    sg_uf TEXT,

    co_municipio INTEGER NOT NULL,

    no_mesorregiao TEXT,
    co_mesorregiao INTEGER,

    no_microrregiao TEXT,
    co_microrregiao INTEGER,

    nu_ano_censo INTEGER,

    qt_mat_bas INTEGER NOT NULL,
    qt_mat_prof INTEGER NOT NULL,
    qt_mat_eja INTEGER NOT NULL,
    qt_mat_esp INTEGER NOT NULL,
    qt_mat_fund INTEGER NOT NULL,
    qt_mat_inf INTEGER NOT NULL,
    qt_mat_med INTEGER NOT NULL,

    qt_mat_zr_na INTEGER NOT NULL,
    qt_mat_zr_rur INTEGER NOT NULL,
    qt_mat_zr_urb INTEGER NOT NULL,
    qt_mat_total INTEGER NOT NULL
);
