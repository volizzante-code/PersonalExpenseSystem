import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "spese.db"
SQL_PATH = BASE_DIR / "sql" / "database.sql"


def connetti():
    """Apre il database; se non esiste lo crea eseguendo database.sql."""
    nuovo = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    if nuovo:
        with open(SQL_PATH, encoding="utf-8") as f:
            conn.executescript(f.read())
    return conn


def trova_categoria(conn, nome):
    riga = conn.execute(
        "SELECT id_categoria FROM categorie WHERE lower(nome) = lower(?)",
        (nome,),
    ).fetchone()
    return riga[0] if riga else None


def leggi_importo(testo):
    try:
        return float(testo.replace(",", "."))
    except ValueError:
        return None


# ---------- MODULO 1 ----------
def gestione_categorie(conn):
    nome = input("Nome della categoria: ").strip()
    if nome == "":
        print("Errore: il nome non puo' essere vuoto.")
        return
    if trova_categoria(conn, nome) is not None:
        print("La categoria esiste gia'.")
        return
    conn.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
    conn.commit()
    print("Categoria inserita correttamente.")


# ---------- MODULO 2 ----------
def inserisci_spesa(conn):
    data = input("Data (YYYY-MM-DD): ").strip()
    importo_txt = input("Importo: ").strip()
    nome_cat = input("Nome della categoria: ").strip()
    descrizione = input("Descrizione (facoltativa): ").strip()

    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        print("Errore: data non valida. Usa il formato YYYY-MM-DD.")
        return

    importo = leggi_importo(importo_txt)
    if importo is None:
        print("Errore: importo non valido.")
        return
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return

    id_cat = trova_categoria(conn, nome_cat)
    if id_cat is None:
        print("Errore: la categoria non esiste.")
        return

    conn.execute(
        "INSERT INTO spese (data, importo, id_categoria, descrizione) "
        "VALUES (?, ?, ?, ?)",
        (data, importo, id_cat, descrizione or None),
    )
    conn.commit()
    print("Spesa inserita correttamente.")


# ---------- MODULO 3 ----------
def definisci_budget(conn):
    mese = input("Mese (YYYY-MM): ").strip()
    nome_cat = input("Nome della categoria: ").strip()
    importo_txt = input("Importo del budget: ").strip()

    try:
        datetime.strptime(mese, "%Y-%m")
    except ValueError:
        print("Errore: mese non valido. Usa il formato YYYY-MM.")
        return

    importo = leggi_importo(importo_txt)
    if importo is None:
        print("Errore: importo non valido.")
        return
    if importo <= 0:
        print("Errore: il budget deve essere maggiore di zero.")
        return

    id_cat = trova_categoria(conn, nome_cat)
    if id_cat is None:
        print("Errore: la categoria non esiste.")
        return

    # Inserisce, oppure aggiorna se esiste gia' (mese, categoria)
    conn.execute(
        "INSERT INTO budget (mese, id_categoria, importo) VALUES (?, ?, ?) "
        "ON CONFLICT (mese, id_categoria) DO UPDATE SET importo = excluded.importo",
        (mese, id_cat, importo),
    )
    conn.commit()
    print("Budget mensile salvato correttamente.")


# ---------- MODULO 4 ----------
def report_totale_per_categoria(conn):
    righe = conn.execute(
        "SELECT c.nome, COALESCE(SUM(s.importo), 0) "
        "FROM categorie c LEFT JOIN spese s ON s.id_categoria = c.id_categoria "
        "GROUP BY c.id_categoria ORDER BY c.nome"
    ).fetchall()
    print()
    print(f"{'Categoria':<20}{'Totale Speso':>12}")
    print("-" * 32)
    for nome, totale in righe:
        print(f"{nome:<20}{totale:>12.2f}")


def report_spese_vs_budget(conn):
    righe = conn.execute(
        "SELECT b.mese, c.nome, b.importo, COALESCE(SUM(s.importo), 0) "
        "FROM budget b "
        "JOIN categorie c ON c.id_categoria = b.id_categoria "
        "LEFT JOIN spese s ON s.id_categoria = b.id_categoria "
        "  AND strftime('%Y-%m', s.data) = b.mese "
        "GROUP BY b.id_budget ORDER BY b.mese, c.nome"
    ).fetchall()
    if not righe:
        print("Nessun budget definito.")
        return
    for mese, nome, budget, speso in righe:
        if speso > budget:
            stato = "SUPERAMENTO BUDGET"
        else:
            stato = "Nel budget"
        print()
        print(f"Mese: {mese}")
        print(f"Categoria: {nome}")
        print(f"Budget: {budget:.2f}")
        print(f"Speso: {speso:.2f}")
        print(f"Stato: {stato}")


def report_elenco_spese(conn):
    righe = conn.execute(
        "SELECT s.data, c.nome, s.importo, COALESCE(s.descrizione, '') "
        "FROM spese s JOIN categorie c ON c.id_categoria = s.id_categoria "
        "ORDER BY s.data"
    ).fetchall()
    print()
    print(f"{'Data':<12}{'Categoria':<16}{'Importo':>10}  Descrizione")
    print("-" * 62)
    for data, nome, importo, descr in righe:
        print(f"{data:<12}{nome:<16}{importo:>10.2f}  {descr}")


def menu_report(conn):
    while True:
        print()
        print("-------------------------")
        print("         REPORT")
        print("-------------------------")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        print("-------------------------")
        scelta = input("Inserisci la tua scelta: ").strip()
        match scelta:
            case "1":
                report_totale_per_categoria(conn)
            case "2":
                report_spese_vs_budget(conn)
            case "3":
                report_elenco_spese(conn)
            case "4":
                return
            case _:
                print("Scelta non valida. Riprovare.")


# ---------- MENU PRINCIPALE ----------
def main():
    conn = connetti()
    print("Benvenuto nel Sistema Spese Personali!")
    while True:
        print()
        print("-------------------------")
        print("SISTEMA SPESE PERSONALI")
        print("-------------------------")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        print("-------------------------")
        scelta = input("Inserisci la tua scelta: ").strip()
        match scelta:
            case "1":
                gestione_categorie(conn)
            case "2":
                inserisci_spesa(conn)
            case "3":
                definisci_budget(conn)
            case "4":
                menu_report(conn)
            case "5":
                print("Arrivederci!")
                break
            case _:
                print("Scelta non valida. Riprovare.")
    conn.close()


if __name__ == "__main__":
    main()