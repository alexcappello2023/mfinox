"""Accesso al Google Sheet del piano editoriale.

Il foglio ha tre colonne: titolo | key | stato
Lo stato vale "DA FARE" (argomento ancora da scrivere) oppure
"INSERITO" (bozza già caricata su WordPress).

L'autenticazione usa un service account Google: il contenuto del file JSON
va messo nel secret GOOGLE_SERVICE_ACCOUNT_JSON e il foglio va condiviso
in scrittura con l'indirizzo email del service account.

Se il secret non è configurato, tutte le funzioni sollevano SheetNotConfigured
e lo script chiamante degrada senza bloccare la pubblicazione.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

DA_FARE = "DA FARE"
INSERITO = "INSERITO"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]


class SheetNotConfigured(RuntimeError):
    """Il service account non è disponibile in questo ambiente."""


@dataclass
class Riga:
    """Una riga del piano editoriale, con il suo numero di riga nel foglio."""

    numero: int  # 1-based, come lo mostra Google Sheets
    titolo: str
    key: str
    stato: str


def _credentials():
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        raise SheetNotConfigured(
            "GOOGLE_SERVICE_ACCOUNT_JSON non impostato: salto l'aggiornamento del foglio."
        )
    try:
        info = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SheetNotConfigured(f"GOOGLE_SERVICE_ACCOUNT_JSON non è un JSON valido: {exc}") from exc

    from google.oauth2.service_account import Credentials

    return Credentials.from_service_account_info(info, scopes=SCOPES)


def apri_foglio(sheet_id: str, worksheet: str | None = None):
    """Restituisce il worksheet indicato, o il primo se non specificato."""
    import gspread

    client = gspread.authorize(_credentials())
    spreadsheet = client.open_by_key(sheet_id)
    if worksheet:
        return spreadsheet.worksheet(worksheet)
    return spreadsheet.sheet1


def leggi_righe(ws) -> list[Riga]:
    """Legge il foglio saltando l'eventuale riga di intestazione."""
    valori = ws.get_all_values()
    righe: list[Riga] = []
    for idx, cella in enumerate(valori, start=1):
        campi = (cella + ["", "", ""])[:3]
        titolo, key, stato = (c.strip() for c in campi)
        if not titolo:
            continue
        if idx == 1 and titolo.lower() in {"titolo", "title"}:
            continue  # intestazione
        righe.append(Riga(numero=idx, titolo=titolo, key=key, stato=stato.upper()))
    return righe


def prossima_da_fare(ws) -> Riga | None:
    """Prima riga con stato DA FARE, in ordine di foglio."""
    for riga in leggi_righe(ws):
        if riga.stato == DA_FARE:
            return riga
    return None


def trova_per_titolo(ws, titolo: str) -> Riga | None:
    """Cerca una riga per titolo esatto, ignorando maiuscole e spazi."""
    atteso = " ".join(titolo.split()).casefold()
    for riga in leggi_righe(ws):
        if " ".join(riga.titolo.split()).casefold() == atteso:
            return riga
    return None


def segna_inserito(ws, riga: Riga) -> None:
    """Porta la colonna stato di quella riga a INSERITO."""
    ws.update_cell(riga.numero, 3, INSERITO)


def semina(ws, righe: list[tuple[str, str]], forza: bool = False) -> int:
    """Popola il foglio con (titolo, key) in stato DA FARE.

    Non duplica i titoli già presenti. Scrive l'intestazione se il foglio è vuoto.
    Restituisce il numero di righe aggiunte.
    """
    esistenti = leggi_righe(ws)
    noti = {" ".join(r.titolo.split()).casefold() for r in esistenti}

    if not ws.get_all_values():
        ws.append_row(["titolo", "key", "stato"], value_input_option="USER_ENTERED")

    da_aggiungere = [
        [titolo, key, DA_FARE]
        for titolo, key in righe
        if forza or " ".join(titolo.split()).casefold() not in noti
    ]
    if da_aggiungere:
        ws.append_rows(da_aggiungere, value_input_option="USER_ENTERED")
    return len(da_aggiungere)
