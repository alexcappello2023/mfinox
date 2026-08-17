#!/usr/bin/env python3
"""Diagnostica di categorie e articoli su WordPress.

Serve a capire cosa c'è davvero sul sito quando l'esito non corrisponde alle
attese: quali categorie esistono, con quale ID e in quale lingua, e quali
categorie risultano effettivamente assegnate a un articolo.

    python scripts/diagnostica_wp.py --post-ids 8787,8789,8791

Non modifica nulla: fa solo richieste in lettura.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys

import requests

TIMEOUT = 60
INTESTAZIONI = {"User-Agent": "mfinox-editorial-bot/1.0"}


def credenziali() -> tuple[str, str]:
    utente = os.environ.get("WP_USER", "").strip()
    password = re.sub(r"\s+", "", os.environ.get("WP_APP_PASSWORD", ""))
    if not utente or not password:
        print("ERRORE: WP_USER e WP_APP_PASSWORD non impostati.", file=sys.stderr)
        raise SystemExit(1)
    return utente, password


def chiama(url: str, auth: tuple[str, str], parametri: dict) -> tuple[list | dict | None, str]:
    try:
        r = requests.get(url, params=parametri, auth=auth, timeout=TIMEOUT, headers=INTESTAZIONI)
    except requests.RequestException as exc:
        return None, f"richiesta fallita: {exc}"
    if r.status_code >= 300:
        return None, f"HTTP {r.status_code}: {r.text[:200]}"
    return r.json(), ""


def mostra_categorie(base: str, auth: tuple[str, str], lang: str | None) -> None:
    etichetta = f"lang={lang}" if lang else "senza parametro lingua"
    parametri: dict[str, object] = {"per_page": 100, "orderby": "id", "order": "asc"}
    if lang:
        parametri["lang"] = lang

    dati, errore = chiama(f"{base}/wp-json/wp/v2/categories", auth, parametri)
    print(f"\n--- CATEGORIE ({etichetta}) ---")
    if errore:
        print(f"  {errore}")
        return
    if not dati:
        print("  nessuna categoria restituita")
        return

    print(f"  {len(dati)} categorie")
    print(f"  {'ID':>6}  {'name':<28} {'slug':<28} {'articoli':>8}  parent")
    for c in dati:
        nome = html.unescape(c.get("name", ""))
        print(
            f"  {c.get('id'):>6}  {nome[:28]:<28} {c.get('slug', '')[:28]:<28} "
            f"{c.get('count', 0):>8}  {c.get('parent', 0)}"
        )


def mostra_articoli(base: str, auth: tuple[str, str], ids: list[str]) -> None:
    print("\n--- ARTICOLI ---")
    for pid in ids:
        dati, errore = chiama(f"{base}/wp-json/wp/v2/posts/{pid}", auth, {"context": "edit"})
        if errore:
            print(f"  ID {pid}: {errore}")
            continue
        titolo = html.unescape((dati.get("title") or {}).get("raw") or "")
        print(f"\n  ID {pid} — {titolo[:70]}")
        print(f"    stato      : {dati.get('status')}")
        print(f"    slug       : {dati.get('slug')!r}")
        print(f"    categories : {dati.get('categories')}")
        print(f"    lingua     : {dati.get('lang', '(campo assente)')}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url", default=os.environ.get("WP_BASE_URL", "https://mfinox.com")
    )
    parser.add_argument("--post-ids", default="", help="ID separati da virgola.")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    auth = credenziali()
    print(f"Sito: {base}")

    # Senza parametro lingua si vede cosa risolve lo script di pubblicazione;
    # con lang=it si vede quali termini appartengono davvero all'italiano.
    # Se le due liste differiscono, il sito separa le categorie per lingua.
    mostra_categorie(base, auth, None)
    mostra_categorie(base, auth, "it")

    ids = [p.strip() for p in args.post_ids.split(",") if p.strip()]
    if ids:
        mostra_articoli(base, auth, ids)
    return 0


if __name__ == "__main__":
    sys.exit(main())
