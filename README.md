# Personal Expense System

Sistema di gestione delle spese personali e del budget, con interfaccia a console.
Sviluppato in Python con database SQLite.

## Funzionalità
- Gestione delle categorie di spesa
- Inserimento delle spese (data, importo, categoria, descrizione)
- Definizione del budget mensile per categoria
- Report: totale per categoria, spese mensili vs budget, elenco spese per data

## Requisiti
- Python 3.10 o superiore (serve per l'istruzione `match`)
- Librerie: solo la libreria standard (`sqlite3`, `datetime`, `pathlib`). Nessuna installazione aggiuntiva.

## Come eseguire il programma
Non serve compilare. Dalla cartella principale del progetto esegui:

```
python src/main.py
```

Su Windows, se `python` non viene riconosciuto, usa `py src/main.py`.

Al primo avvio il programma crea il database `spese.db` eseguendo
`sql/database.sql` (con alcuni dati di esempio). Per ripartire da zero
basta cancellare il file `spese.db`.

## Struttura del repository
```
PersonalExpenseSystem/
├── src/
│   └── main.py
├── sql/
│   └── database.sql
├── demo/
│   └── demo_video.mp4
└── README.md
```