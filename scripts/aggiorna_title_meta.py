#!/usr/bin/env python3
"""Aggiorna title SEO e meta description su WordPress tramite REST API.

Legge data/title-meta.csv (colonne: url, title_seo, meta_description,
titolo_post, stato) e scrive i campi Yoast dei contenuti indicati.

Lo script è prudente per costruzione:
  * senza --applica non scrive nulla, stampa solo cosa farebbe;
  * il titolo visibile del post si cambia solo con --applica-titolo, perché è
    l'unica modifica che l'utente vede in pagina;
  * se i campi Yoast non sono esposti alle REST API lo dice e si ferma, invece
    di ricevere un 200 e credere di aver scritto qualcosa.

Uso tipico:
    python scripts/aggiorna_title_meta.py                 # prova a vuoto
    python scripts/aggiorna_title_meta.py --applica       # scrive title e meta
    python scripts/aggiorna_title_meta.py --applica --applica-titolo

Variabili d'ambiente richieste:
    WP_USER            utente WordPress
    WP_APP_PASSWORD    application password
Opzionali:
    WP_BASE_URL        default https://mfinox.com
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

DEFAULT_BASE_URL = "https://mfinox.com"
DEFAULT_CSV = Path("data/title-meta.csv")
TIMEOUT = 60
INTESTAZIONI = {"User-Agent": "mfinox-seo-bot/1.0"}

CHIAVE_TITLE = "_yoast_wpseo_title"
CHIAVE_META = "_yoast_wpseo_metadesc"

LIMITE_TITLE = 60
LIMITE_META = 160


class ErroreFatale(RuntimeError):
    pass


def credenziali() -> tuple[str, str]:
    utente = os.environ.get("WP_USER", "").strip()
    # L'application password viene mostrata da WordPress con spazi di sola
    # leggibilità: il valore reale non li contiene.
    password = re.sub(r"\s+", "", os.environ.get("WP_APP_PASSWORD", ""))
    if not utente or not password:
        raise ErroreFatale(
            "WP_USER e WP_APP_PASSWORD non sono impostati. "
            "In GitHub Actions vanno configurati come repository secrets."
        )
    return utente, password


def leggi_csv(percorso: Path) -> list[dict]:
    if not percorso.exists():
        raise ErroreFatale(f"{percorso} non esiste.")
    with percorso.open(newline="", encoding="utf-8-sig") as f:
        righe = [r for r in csv.DictReader(f) if (r.get("url") or "").strip()]
    if not righe:
        raise ErroreFatale(f"{percorso} non contiene righe utilizzabili.")
    attese = {"url", "title_seo", "meta_description"}
    mancanti = attese - set(righe[0])
    if mancanti:
        raise ErroreFatale(f"{percorso}: colonne mancanti: {', '.join(sorted(mancanti))}")
    return righe


def slug_da_url(url: str) -> str:
    """Ultimo segmento del percorso: è lo slug con cui WordPress indicizza."""
    percorso = urlparse(url).path if "://" in url else url
    segmenti = [s for s in percorso.split("/") if s]
    if not segmenti:
        raise ErroreFatale(f"Da '{url}' non si ricava nessuno slug.")
    return segmenti[-1]


def tipi_interrogabili(base_url: str, auth: tuple[str, str]) -> list[str]:
    """Elenco dei rest_base dei tipi di contenuto pubblici del sito.

    Le schede materiale non sono necessariamente dei 'post': il sito può usare
    un custom post type. Invece di indovinarlo lo chiediamo a WordPress.
    """
    endpoint = f"{base_url.rstrip('/')}/wp-json/wp/v2/types"
    try:
        risposta = requests.get(endpoint, auth=auth, timeout=TIMEOUT, headers=INTESTAZIONI)
        risposta.raise_for_status()
        tipi = risposta.json()
    except requests.RequestException as exc:
        raise ErroreFatale(f"Lettura dei tipi di contenuto da {endpoint} fallita: {exc}") from exc
    except ValueError as exc:
        raise ErroreFatale(f"{endpoint} non ha risposto in JSON: {exc}") from exc

    basi: list[str] = []
    for nome, dati in (tipi or {}).items():
        if nome in {"attachment", "wp_block", "nav_menu_item"}:
            continue
        base = (dati or {}).get("rest_base")
        if base and base not in basi:
            basi.append(base)
    # pagine e articoli per primi: è lì che sta la maggior parte dei contenuti
    for preferito in ("pages", "posts"):
        if preferito in basi:
            basi.remove(preferito)
            basi.insert(0, preferito)
    if not basi:
        raise ErroreFatale("Nessun tipo di contenuto interrogabile trovato.")
    return basi


def trova_contenuto(
    slug: str, basi: list[str], base_url: str, auth: tuple[str, str]
) -> tuple[str, dict]:
    """Cerca lo slug in tutti i tipi di contenuto e restituisce (rest_base, dato)."""
    for base in basi:
        endpoint = f"{base_url.rstrip('/')}/wp-json/wp/v2/{base}"
        try:
            risposta = requests.get(
                endpoint,
                params={"slug": slug, "status": "publish,draft,private", "per_page": 10},
                auth=auth,
                timeout=TIMEOUT,
                headers=INTESTAZIONI,
            )
        except requests.RequestException as exc:
            raise ErroreFatale(f"Ricerca di '{slug}' su {endpoint} fallita: {exc}") from exc
        if risposta.status_code in (400, 401, 403, 404):
            continue
        try:
            risultati = risposta.json()
        except ValueError:
            continue
        if isinstance(risultati, list) and risultati:
            return base, risultati[0]
    raise ErroreFatale(f"Nessun contenuto trovato con slug '{slug}'.")


def yoast_scrivibile(dato: dict) -> bool:
    """True se i campi Yoast sono esposti nel sottooggetto 'meta'."""
    meta = dato.get("meta")
    return isinstance(meta, dict) and CHIAVE_TITLE in meta


def avvisi_lunghezza(riga: dict) -> list[str]:
    avvisi = []
    titolo = (riga.get("title_seo") or "").strip()
    descrizione = (riga.get("meta_description") or "").strip()
    if len(titolo) > LIMITE_TITLE:
        avvisi.append(f"title di {len(titolo)} caratteri (oltre {LIMITE_TITLE}: Google lo troncherà)")
    if len(descrizione) > LIMITE_META:
        avvisi.append(
            f"meta di {len(descrizione)} caratteri (oltre {LIMITE_META}: Google la troncherà)"
        )
    return avvisi


def aggiorna(
    riga: dict,
    base: str,
    dato: dict,
    base_url: str,
    auth: tuple[str, str],
    applica_titolo: bool,
) -> dict:
    corpo: dict = {"meta": {}}
    titolo = (riga.get("title_seo") or "").strip()
    descrizione = (riga.get("meta_description") or "").strip()
    if titolo:
        corpo["meta"][CHIAVE_TITLE] = titolo
    if descrizione:
        corpo["meta"][CHIAVE_META] = descrizione

    titolo_post = (riga.get("titolo_post") or "").strip()
    if titolo_post and applica_titolo:
        # Cambia il testo visibile in pagina. Lo slug non si tocca mai: l'URL
        # porta impressioni acquisite e un cambio di slug le butterebbe via.
        corpo["title"] = titolo_post

    if not corpo["meta"] and "title" not in corpo:
        raise ErroreFatale("La riga non contiene niente da scrivere.")

    endpoint = f"{base_url.rstrip('/')}/wp-json/wp/v2/{base}/{dato['id']}"
    try:
        risposta = requests.post(
            endpoint, json=corpo, auth=auth, timeout=TIMEOUT, headers=INTESTAZIONI
        )
    except requests.RequestException as exc:
        raise ErroreFatale(f"Scrittura su {endpoint} fallita: {exc}") from exc
    if risposta.status_code >= 400:
        raise ErroreFatale(
            f"WordPress ha rifiutato la scrittura su {endpoint} "
            f"({risposta.status_code}): {risposta.text[:300]}"
        )
    try:
        return risposta.json()
    except ValueError as exc:
        raise ErroreFatale(
            f"WordPress ha risposto {risposta.status_code} ma con un corpo non JSON "
            f"({exc}). Content-Type: {risposta.headers.get('Content-Type', 'assente')}. "
            f"Primi 300 caratteri: {risposta.text[:300]!r}"
        ) from exc


def verifica(riga: dict, risposta: dict) -> list[str]:
    """Rilegge la risposta e segnala i campi che WordPress non ha salvato."""
    problemi = []
    meta = risposta.get("meta") if isinstance(risposta.get("meta"), dict) else {}
    atteso_titolo = (riga.get("title_seo") or "").strip()
    atteso_meta = (riga.get("meta_description") or "").strip()
    if atteso_titolo and meta.get(CHIAVE_TITLE, "") != atteso_titolo:
        problemi.append(f"{CHIAVE_TITLE} non salvato (vale {meta.get(CHIAVE_TITLE, '')!r})")
    if atteso_meta and meta.get(CHIAVE_META, "") != atteso_meta:
        problemi.append(f"{CHIAVE_META} non salvato (vale {meta.get(CHIAVE_META, '')!r})")
    return problemi


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help=f"default {DEFAULT_CSV}")
    parser.add_argument("--url", help="elabora solo la riga con questo url")
    parser.add_argument("--applica", action="store_true", help="scrive davvero (senza, prova a vuoto)")
    parser.add_argument(
        "--applica-titolo",
        action="store_true",
        help="cambia anche il titolo visibile del post dove la colonna titolo_post è compilata",
    )
    args = parser.parse_args()

    base_url = os.environ.get("WP_BASE_URL", DEFAULT_BASE_URL)

    try:
        righe = leggi_csv(args.csv)
    except ErroreFatale as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 1

    if args.url:
        righe = [r for r in righe if r["url"].strip() == args.url.strip()]
        if not righe:
            print(f"ERRORE: nessuna riga con url {args.url}", file=sys.stderr)
            return 1

    if not args.applica:
        print("PROVA A VUOTO: nessuna scrittura. Aggiungi --applica per scrivere.\n")

    try:
        auth = credenziali()
        basi = tipi_interrogabili(base_url, auth)
    except ErroreFatale as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 1
    print(f"Tipi di contenuto da interrogare: {', '.join(basi)}\n")

    fatti: list[str] = []
    errori: list[str] = []
    yoast_chiuso = False

    for riga in righe:
        url = riga["url"].strip()
        print(f"— {url}")
        for avviso in avvisi_lunghezza(riga):
            print(f"  AVVISO: {avviso}")
        try:
            base, dato = trova_contenuto(slug_da_url(url), basi, base_url, auth)
            print(f"  trovato: {base}/{dato['id']}")

            if not yoast_scrivibile(dato):
                yoast_chiuso = True
                raise ErroreFatale(
                    f"i campi Yoast non sono esposti alle REST API su {base}/{dato['id']}: "
                    "WordPress accetterebbe la richiesta e scarterebbe i valori"
                )

            titolo = (riga.get("title_seo") or "").strip()
            descrizione = (riga.get("meta_description") or "").strip()
            print(f"  title: {titolo}")
            print(f"  meta:  {descrizione}")
            titolo_post = (riga.get("titolo_post") or "").strip()
            if titolo_post:
                if args.applica_titolo:
                    print(f"  titolo visibile: {titolo_post}")
                else:
                    print(f"  titolo visibile da cambiare in «{titolo_post}» (serve --applica-titolo)")

            if args.applica:
                risposta = aggiorna(riga, base, dato, base_url, auth, args.applica_titolo)
                problemi = verifica(riga, risposta)
                if problemi:
                    raise ErroreFatale("; ".join(problemi))
                print("  scritto e verificato")
            fatti.append(url)
        except ErroreFatale as exc:
            print(f"  ERRORE: {exc}", file=sys.stderr)
            errori.append(url)
        except Exception as exc:  # noqa: BLE001 — una riga rotta non deve fermare le altre
            print(f"  ERRORE IMPREVISTO: {type(exc).__name__}: {exc}", file=sys.stderr)
            errori.append(url)
        print()

    print(f"Righe elaborate: {len(fatti)} — errori: {len(errori)}")
    if yoast_chiuso:
        print(
            "\nI campi Yoast non sono scrivibili via REST. Serve la 'register_post_meta'\n"
            "descritta in docs/SETUP.md, estesa a tutti i tipi di contenuto pubblici.\n"
            "Finché non c'è, title e meta vanno incollati a mano dal pannello Yoast:\n"
            "la lista pronta è in docs/title-meta-da-riscrivere.md.",
            file=sys.stderr,
        )
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
