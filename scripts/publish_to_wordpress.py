#!/usr/bin/env python3
"""Carica un articolo come BOZZA su WordPress tramite REST API.

L'articolo è un file Markdown con front matter YAML: i metadati stanno nel
front matter, il corpo (già in blocchi Gutenberg) è tutto ciò che segue.

Uso tipico:
    python scripts/publish_to_wordpress.py --file content/articolo.md

Variabili d'ambiente richieste:
    WP_USER            utente WordPress (es. alberto.lupi)
    WP_APP_PASSWORD    application password generata da WordPress
Opzionali:
    WP_BASE_URL        default https://mfinox.com
    SHEET_ID           per segnare la riga come INSERITO
    GOOGLE_SERVICE_ACCOUNT_JSON  credenziali del service account

Lo script non pubblica mai online: lo stato predefinito è "draft".
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
from pathlib import Path

import requests
import yaml

DEFAULT_BASE_URL = "https://mfinox.com"
TIMEOUT = 60


class ErroreFatale(RuntimeError):
    pass


def leggi_articolo(percorso: Path) -> tuple[dict, str]:
    """Separa il front matter YAML dal corpo dell'articolo."""
    testo = percorso.read_text(encoding="utf-8")
    if not testo.startswith("---"):
        raise ErroreFatale(f"{percorso}: manca il front matter YAML iniziale (---).")

    parti = testo.split("---", 2)
    if len(parti) < 3:
        raise ErroreFatale(f"{percorso}: front matter non chiuso da una riga '---'.")

    try:
        meta = yaml.safe_load(parti[1]) or {}
    except yaml.YAMLError as exc:
        raise ErroreFatale(f"{percorso}: front matter YAML non valido: {exc}") from exc

    corpo = parti[2].strip()
    if not corpo:
        raise ErroreFatale(f"{percorso}: il corpo dell'articolo è vuoto.")
    if not isinstance(meta, dict) or not meta.get("titolo"):
        raise ErroreFatale(f"{percorso}: il front matter deve contenere 'titolo'.")

    return meta, corpo


def credenziali() -> tuple[str, str]:
    utente = os.environ.get("WP_USER", "").strip()
    # L'application password viene mostrata da WordPress con degli spazi di
    # sola leggibilità: il valore reale non li contiene.
    password = re.sub(r"\s+", "", os.environ.get("WP_APP_PASSWORD", ""))
    if not utente or not password:
        raise ErroreFatale(
            "WP_USER e WP_APP_PASSWORD non sono impostati. "
            "In GitHub Actions vanno configurati come repository secrets."
        )
    return utente, password


def categorie_richieste(meta: dict, override: str | None) -> list[str]:
    """Nomi di categoria da assegnare: l'opzione da riga di comando vince."""
    valore = override if override else meta.get("categoria")
    if not valore:
        return []
    if isinstance(valore, str):
        valore = valore.split(",")
    return [str(v).strip() for v in valore if str(v).strip()]


def risolvi_categorie(nomi: list[str], base_url: str, auth: tuple[str, str]) -> list[int]:
    """Traduce i nomi di categoria negli ID numerici che l'API richiede.

    WordPress accetta solo ID. I nomi si risolvono per nome esatto o per slug,
    ignorando maiuscole: così nel front matter si scrive "News" e non un numero
    che cambierebbe da un sito all'altro.
    """
    if not nomi:
        return []

    endpoint = f"{base_url.rstrip('/')}/wp-json/wp/v2/categories"
    intestazioni = {"User-Agent": "mfinox-editorial-bot/1.0"}

    def interroga(parametri: dict) -> list[dict]:
        try:
            risposta = requests.get(
                endpoint, params=parametri, auth=auth, timeout=TIMEOUT, headers=intestazioni
            )
            risposta.raise_for_status()
            return risposta.json()
        except requests.RequestException as exc:
            raise ErroreFatale(f"Lettura delle categorie da {endpoint} fallita: {exc}") from exc

    ids: list[int] = []
    for nome in nomi:
        atteso = nome.casefold()
        candidate = interroga({"search": nome, "per_page": 100})
        trovata = next(
            (
                c
                for c in candidate
                if c.get("name", "").casefold() == atteso or c.get("slug", "").casefold() == atteso
            ),
            None,
        )
        if trovata is None:
            tutte = interroga({"per_page": 100, "orderby": "name"})
            elenco = ", ".join(f"{c['name']} ({c['slug']})" for c in tutte) or "nessuna"
            raise ErroreFatale(
                f"Categoria «{nome}» non trovata su {base_url}. Categorie disponibili: {elenco}. "
                "Nei siti multilingua le categorie sono separate per lingua: verifica di usare "
                "quella della lingua in cui pubblichi."
            )
        ids.append(int(trovata["id"]))
    return ids


TUTTI_GLI_STATI = "publish,draft,pending,private,future"


def articolo_esistente(meta: dict, base_url: str, auth: tuple[str, str]) -> dict | None:
    """Cerca un articolo già caricato, per slug e in subordine per titolo.

    È la chiave di idempotenza: lo script crea sempre articoli nuovi, quindi
    senza questo controllo una seconda esecuzione produrrebbe un doppione.

    Si cerca prima per slug, che è l'identificatore più stabile. Ma su una bozza
    WordPress può non aver memorizzato il campo slug, e in quel caso la ricerca
    non troverebbe nulla: da qui il secondo tentativo sul titolo esatto. Le due
    verifiche coprono anche il caso opposto, cioè il titolo cambiato in revisione
    a slug invariato.
    """
    endpoint = f"{base_url.rstrip('/')}/wp-json/wp/v2/posts"
    intestazioni = {"User-Agent": "mfinox-editorial-bot/1.0"}

    def interroga(parametri: dict) -> list[dict]:
        try:
            risposta = requests.get(
                endpoint,
                params={**parametri, "status": TUTTI_GLI_STATI},
                auth=auth,
                timeout=TIMEOUT,
                headers=intestazioni,
            )
            risposta.raise_for_status()
            return risposta.json()
        except requests.RequestException as exc:
            raise ErroreFatale(
                f"Verifica dei duplicati fallita su {endpoint}: {exc}. "
                "Interrompo per non rischiare di creare un doppione."
            ) from exc

    slug = (meta.get("slug") or "").strip()
    if slug:
        trovati = interroga({"slug": slug})
        if trovati:
            return trovati[0]

    titolo = " ".join(meta["titolo"].split()).casefold()
    for candidato in interroga({"search": meta["titolo"], "per_page": 50}):
        reso = candidato.get("title", {}).get("rendered", "")
        # WordPress restituisce il titolo con le entità HTML già codificate.
        reso = html.unescape(reso)
        if " ".join(reso.split()).casefold() == titolo:
            return candidato

    return None


def pubblica(
    meta: dict,
    corpo: str,
    base_url: str,
    stato: str,
    dry_run: bool,
    categoria: str | None = None,
) -> dict:
    endpoint = f"{base_url.rstrip('/')}/wp-json/wp/v2/posts"
    nomi_categorie = categorie_richieste(meta, categoria)

    payload: dict[str, object] = {
        "title": meta["titolo"],
        "content": corpo,
        "status": stato,
    }
    if meta.get("slug"):
        payload["slug"] = meta["slug"]
    if meta.get("meta_description"):
        payload["excerpt"] = meta["meta_description"]

    if dry_run:
        print("— DRY RUN: nessuna chiamata a WordPress —")
        print(f"  endpoint : POST {endpoint}")
        print(f"  titolo   : {payload['title']}")
        print(f"  slug     : {payload.get('slug', '(generato da WordPress)')}")
        print(f"  stato    : {stato}")
        print(f"  categorie: {', '.join(nomi_categorie) or '(nessuna)'} — risolte in ID al momento della pubblicazione")
        print(f"  caratteri: {len(corpo)}")
        return {"id": None, "link": None, "dry_run": True}

    utente, password = credenziali()
    esistente = articolo_esistente(meta, base_url, (utente, password))
    if esistente is not None:
        print(
            f"Già presente su WordPress (ID {esistente['id']}, stato {esistente['status']}): salto."
        )
        return {**esistente, "saltato": True}

    if nomi_categorie:
        ids = risolvi_categorie(nomi_categorie, base_url, (utente, password))
        payload["categories"] = ids
        print(f"Categorie risolte: {', '.join(nomi_categorie)} → {ids}")

    try:
        risposta = requests.post(
            endpoint,
            json=payload,
            auth=(utente, password),
            timeout=TIMEOUT,
            headers={"User-Agent": "mfinox-editorial-bot/1.0"},
        )
    except requests.RequestException as exc:
        raise ErroreFatale(f"Chiamata a {endpoint} fallita: {exc}") from exc

    if risposta.status_code == 401:
        raise ErroreFatale(
            "401 non autorizzato. Verifica WP_USER e rigenera l'application password. "
            "Attenzione: alcune configurazioni di sicurezza (o un plugin) possono "
            "bloccare l'autenticazione Basic sulle REST API."
        )
    if risposta.status_code == 403:
        raise ErroreFatale(
            "403 vietato. L'utente esiste ma non ha i permessi per creare articoli, "
            "oppure un WAF sta filtrando la richiesta."
        )
    if risposta.status_code == 404:
        raise ErroreFatale(
            f"404 su {endpoint}. Le REST API sembrano disattivate o l'URL base è errato "
            "(controlla WP_BASE_URL, es. presenza o assenza di www)."
        )
    if risposta.status_code >= 300:
        raise ErroreFatale(
            f"WordPress ha risposto {risposta.status_code}: {risposta.text[:500]}"
        )

    return risposta.json()


def aggiorna_foglio(meta: dict) -> str:
    """Segna la riga corrispondente come INSERITO. Non è mai bloccante."""
    sheet_id = os.environ.get("SHEET_ID", "").strip()
    if not sheet_id:
        return "SHEET_ID non impostato: foglio non aggiornato."

    try:
        import sheet as foglio

        ws = foglio.apri_foglio(sheet_id, os.environ.get("SHEET_WORKSHEET") or None)
        riga = foglio.trova_per_titolo(ws, meta["titolo"])
        if riga is None:
            return (
                f"Nessuna riga con titolo «{meta['titolo']}» nel foglio: "
                "stato da aggiornare a mano."
            )
        if riga.stato == foglio.INSERITO:
            return f"Riga {riga.numero} era già INSERITO."
        foglio.segna_inserito(ws, riga)
        return f"Riga {riga.numero} aggiornata a INSERITO."
    except Exception as exc:  # noqa: BLE001 — il foglio non deve far fallire il deploy
        return f"Foglio non aggiornato ({type(exc).__name__}): {exc}"


def scrivi_riepilogo(meta: dict, risultato: dict, nota_foglio: str) -> None:
    """Riepilogo nella pagina di esecuzione della GitHub Action."""
    percorso = os.environ.get("GITHUB_STEP_SUMMARY")
    if not percorso:
        return

    keyword = meta.get("focus_keyword", "—")
    righe = [
        "## Bozza creata su WordPress",
        "",
        f"- **Titolo:** {meta['titolo']}",
        f"- **ID articolo:** {risultato.get('id', '—')}",
        f"- **Stato:** {risultato.get('status', 'draft')}",
        f"- **Foglio:** {nota_foglio}",
        "",
        "### Campi da incollare in Yoast SEO",
        "",
        "Yoast non espone i suoi campi sulle REST API senza un filtro dedicato,",
        "quindi questi tre valori vanno inseriti a mano nell'editor:",
        "",
        f"- **Focus keyword:** `{keyword}`",
        f"- **Titolo SEO:** `{meta.get('meta_title', '—')}`",
        f"- **Meta description:** `{meta.get('meta_description', '—')}`",
        "",
    ]
    if meta.get("note_immagine"):
        righe += ["### Immagine in evidenza", "", str(meta["note_immagine"]), ""]

    with open(percorso, "a", encoding="utf-8") as fh:
        fh.write("\n".join(righe))


def elabora(percorso: Path, args) -> bool:
    """Carica un singolo articolo. Restituisce True se non ci sono errori."""
    meta, corpo = leggi_articolo(percorso)
    print(f"\n=== {percorso.name} ===")

    risultato = pubblica(meta, corpo, args.base_url, args.status, args.dry_run, args.categoria)

    if args.dry_run:
        return True

    if not risultato.get("saltato"):
        print(f"Bozza creata. ID {risultato.get('id')}")
        print(
            f"Revisione: {args.base_url.rstrip('/')}/wp-admin/post.php?"
            f"post={risultato.get('id')}&action=edit"
        )

    # Il foglio si aggiorna anche per gli articoli saltati: se l'articolo è su
    # WordPress la riga va marcata INSERITO, che sia stata creata adesso o in
    # un'esecuzione precedente. Così una riga rimasta indietro si riallinea da
    # sé al primo passaggio successivo, invece di restare DA FARE per sempre.
    nota_foglio = (
        "Aggiornamento disattivato (--no-sheet)." if args.no_sheet else aggiorna_foglio(meta)
    )
    print(nota_foglio)

    if not risultato.get("saltato"):
        scrivi_riepilogo(meta, risultato, nota_foglio)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, help="Articolo Markdown da caricare.")
    parser.add_argument(
        "--cartella",
        type=Path,
        help="Elabora tutti i .md della cartella, saltando quelli già su WordPress. "
        "È la modalità usata dal trigger automatico al push.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("WP_BASE_URL", DEFAULT_BASE_URL),
        help=f"URL base del sito (default {DEFAULT_BASE_URL}).",
    )
    parser.add_argument(
        "--status",
        default="draft",
        choices=["draft", "pending", "private", "publish"],
        help="Stato dell'articolo. Default draft: il cliente deve poter revisionare.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Non chiama WordPress.")
    parser.add_argument(
        "--no-sheet", action="store_true", help="Non aggiornare il Google Sheet."
    )
    parser.add_argument(
        "--categoria",
        default=None,
        help="Categoria da assegnare, per nome (es. News). Più categorie separate da virgola. "
        "Se omessa vale il campo 'categoria' del front matter.",
    )
    args = parser.parse_args()

    if not args.file and not args.cartella:
        parser.error("serve --file oppure --cartella.")
    if args.file and args.cartella:
        parser.error("--file e --cartella si escludono a vicenda.")

    if args.file:
        da_fare = [args.file]
    else:
        da_fare = sorted(p for p in args.cartella.glob("*.md") if p.is_file())
        if not da_fare:
            print(f"Nessun file .md in {args.cartella}: niente da fare.")
            return 0
        print(f"{len(da_fare)} articoli da valutare in {args.cartella}.")

    if args.status == "publish":
        print("ATTENZIONE: stato 'publish' richiesto, gli articoli andranno online subito.")

    errori: list[str] = []
    for percorso in da_fare:
        try:
            elabora(percorso, args)
        except ErroreFatale as exc:
            # In modalità cartella un articolo malformato non deve bloccare gli altri.
            print(f"ERRORE su {percorso.name}: {exc}", file=sys.stderr)
            errori.append(percorso.name)

    if args.dry_run:
        print("\nDry run completato: nessuna modifica al sito né al foglio.")

    if errori:
        print(f"\n{len(errori)} articoli non elaborati: {', '.join(errori)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
