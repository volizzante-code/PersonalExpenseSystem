PRAGMA foreign_keys = ON;

CREATE TABLE categorie (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL UNIQUE
                 CHECK (length(trim(nome)) > 0)
);

CREATE TABLE spese (
    id_spesa     INTEGER PRIMARY KEY AUTOINCREMENT,
    data         TEXT NOT NULL
                 CHECK (data GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]'),
    importo      REAL NOT NULL CHECK (importo > 0),
    id_categoria INTEGER NOT NULL,
    descrizione  TEXT,
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria)
);

CREATE TABLE budget (
    id_budget    INTEGER PRIMARY KEY AUTOINCREMENT,
    mese         TEXT NOT NULL
                 CHECK (mese GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]'),
    id_categoria INTEGER NOT NULL,
    importo      REAL NOT NULL CHECK (importo > 0),
    UNIQUE (mese, id_categoria),
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria)
);

INSERT INTO categorie (nome) VALUES ('Alimentari'), ('Trasporti'), ('Svago');

INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES
('2025-01-15', 25.00, 1, 'Pranzo'),
('2025-01-20', 295.00, 1, 'Spesa mensile'),
('2025-01-22', 120.00, 2, 'Abbonamento bus'),
('2025-01-25', 40.00, 3, 'Cinema');

INSERT INTO budget (mese, id_categoria, importo) VALUES
('2025-01', 1, 300), ('2025-01', 2, 150), ('2025-01', 3, 50);