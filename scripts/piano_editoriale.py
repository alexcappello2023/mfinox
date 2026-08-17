#!/usr/bin/env python3
"""Gestione del piano editoriale sul Google Sheet.

    python scripts/piano_editoriale.py semina      # popola il foglio da data/piano-editoriale.csv
    python scripts/piano_editoriale.py prossimo    # mostra il prossimo argomento DA FARE
    python scripts/piano_editoriale.py elenco      # stampa lo stato di tutte le righe

Richiede SHEET_ID e GOOGLE_SERVICE_ACCOUNT_JSON. Senza credenziali il comando
"semina" stampa comunque le righe in formato TSV, pronte da incollare a mano
nel foglio.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
CSV_PIANO = RADICE / "data" / "piano-editoriale.csv"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sheet as foglio  # noqa: E402


def righe_dal_csv() -> list[tuple[str, str]]:
    with CSV_PIANO.open(encoding="utf-8") as fh:
        return [
            (r["titolo"].strip(), r["key"].strip())
            for r in csv.DictReader(fh)
            if r.get("titolo", "").strip()
        ]


def apri():
    sheet_id = os.environ.get("SHEET_ID", "").strip()
    if not sheet_id:
        raise foglio.SheetNotConfigured("SHEET_ID non impostato.")
    return foglio.apri_foglio(sheet_id, os.environ.get("SHEET_WORKSHEET") or None)


def cmd_semina(args) -> int:
    righe = righe_dal_csv()
    try:
        ws = apri()
    except foglio.SheetNotConfigured as exc:
        print(f"{exc}\n\nRighe da incollare nel foglio (titolo / key / stato):\n")
        print("titolo\tkey\tstato")
        for titolo, key in righe:
            print(f"{titolo}\t{key}\t{foglio.DA_FARE}")
        return 0

    aggiunte = foglio.semina(ws, righe, forza=args.forza)
    print(f"{aggiunte} righe aggiunte al foglio ({len(righe) - aggiunte} già presenti).")
    return 0


def cmd_prossimo(_args) -> int:
    riga = foglio.prossima_da_fare(apri())
    if riga is None:
        print("Nessun argomento DA FARE: il piano editoriale è esaurito.")
        return 0
    print(f"Riga {riga.numero}\nTitolo: {riga.titolo}\nKey: {riga.key}")
    return 0


def cmd_elenco(_args) -> int:
    righe = foglio.leggi_righe(apri())
    if not righe:
        print("Foglio vuoto.")
        return 0
    larghezza = max(len(r.stato) for r in righe)
    for r in righe:
        print(f"{r.numero:>3}  {r.stato:<{larghezza}}  {r.titolo}")
    da_fare = sum(1 for r in righe if r.stato == foglio.DA_FARE)
    print(f"\n{da_fare} da fare, {len(righe) - da_fare} inseriti, {len(righe)} totali.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="comando", required=True)

    p = sub.add_parser("semina", help="Popola il foglio dal CSV senza duplicare i titoli.")
    p.add_argument("--forza", action="store_true", help="Aggiungi anche i titoli già presenti.")
    p.set_defaults(func=cmd_semina)

    sub.add_parser("prossimo", help="Mostra il prossimo argomento DA FARE.").set_defaults(
        func=cmd_prossimo
    )
    sub.add_parser("elenco", help="Stato di tutte le righe.").set_defaults(func=cmd_elenco)

    args = parser.parse_args()
    try:
        return args.func(args)
    except foglio.SheetNotConfigured as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
