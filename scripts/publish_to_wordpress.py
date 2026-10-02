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
import time
from pathlib import Path

import requests
import yaml

DEFAULT_BASE_URL = "https://mfinox.com"
TIMEOUT = 60
INTESTAZIONI = {"User-Agent": "mfinox-editorial-bot/1.0"}

# Il sito è dietro un firewall applicativo che, in modo intermittente,
# restituisce la propria pagina di attesa con codice 200 invece di inoltrare la
# richiesta a WordPress. Il fenomeno non è deterministico — un rilancio
# immediato passa — quindi vale la pena ritentare prima di arrendersi.
# Vedi docs/audit-tecnico-2026-10-01.md.
RITENTATIVI = 3
ATTESA_BASE = 3.0  # secondi; triplica a ogni tentativo: 3, 9


class ErroreFatale(RuntimeError):
    pass


class RispostaNonJson(RuntimeError):
    """Codice di successo ma corpo non JSON.

    È la firma di un firewall che si interpone: il client riceve 200 e crede di
    aver parlato con WordPress. Si distingue da un errore vero perché è
    transitoria, e quindi ritentabile.
    """

    def __init__(self, risposta, contesto: str):
        self.risposta = risposta
        self.contesto = contesto
        tipo = risposta.headers.get("Content-Type", "assente")
        super().__init__(
            f"codice {risposta.status_code} ma corpo non JSON "
            f"(Content-Type: {tipo}). Primi 200 caratteri: {risposta.text[:200]!r}"
        )


def corpo_json(risposta, contesto: str):
    try:
        return risposta.json()
    except ValueError as exc:
        raise RispostaNonJson(risposta, contesto) from exc


def attendi(tentativo: int, contesto: str, motivo) -> None:
    attesa = ATTESA_BASE * (3 ** (tentativo - 1))
    print(
        f"  {contesto}: tentativo {tentativo} di {RITENTATIVI} non riuscito "
        f"({motivo}). Riprovo fra {attesa:.0f}s.",
        file=sys.stderr,
    )
    time.sleep(attesa)


def chiama(
    metodo: str,
    url: str,
    *,
    auth: tuple[str, str],
    contesto: str,
    params: dict | None = None,
    corpo: dict | None = None,
):
    """Chiama le REST API e restituisce il JSON, ritentando quando ha senso.

    Si ritenta su errore di rete, su 5xx e sulle risposte non JSON: sono tutte
    condizioni transitorie. Non si ritenta sui 4xx, che descrivono un problema
    della richiesta e non cambierebbero esito a forza di tentativi.

    Da NON usare per creare contenuti: un POST di creazione ritentato alla cieca
    produrrebbe un doppione. La creazione è gestita in pubblica(), che prima di
    riprovare verifica se l'articolo è stato creato comunque.
    """
    ultimo: object = "nessun dettaglio"
    for tentativo in range(1, RITENTATIVI + 1):
        try:
            risposta = requests.request(
                metodo,
                url,
                params=params,
                json=corpo,
                auth=auth,
                timeout=TIMEOUT,
                headers=INTESTAZIONI,
            )
        except requests.RequestException as exc:
            ultimo = exc
        else:
            if 400 <= risposta.status_code < 500:
                raise ErroreFatale(
                    f"{contesto}: WordPress ha risposto {risposta.status_code}. "
                    f"{risposta.text[:300]}"
                )
            if risposta.status_code >= 500:
                ultimo = f"{risposta.status_code} dal server"
            else:
                try:
                    return corpo_json(risposta, contesto)
                except RispostaNonJson as exc:
                    ultimo = exc
        if tentativo < RITENTATIVI:
            attendi(tentativo, contesto, ultimo)

    raise ErroreFatale(
        f"{contesto}: {RITENTATIVI} tentativi falliti. Ultimo esito: {ultimo}. "
        "Se il corpo è una pagina HTML, è il firewall che intercetta le chiamate "
        "REST: vedi docs/audit-tecnico-2026-10-01.md."
    )


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


def risolvi_categorie(
    nomi: list[str], base_url: str, auth: tuple[str, str], lingua: dict | None = None
) -> list[int]:
    """Traduce i nomi di categoria negli ID numerici che l'API richiede.

    WordPress accetta solo ID. I nomi si risolvono per nome esatto o per slug,
    ignorando maiuscole: così nel front matter si scrive "News" e non un numero
    che cambierebbe da un sito all'altro.
    """
    if not nomi:
        return []

    endpoint = f"{base_url.rstrip('/')}/wp-json/wp/v2/categories"

    def interroga(parametri: dict) -> list[dict]:
        return chiama(
            "GET",
            endpoint,
            auth=auth,
            contesto="Lettura delle categorie",
            params={**(lingua or {}), **parametri},
        )

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


def parametri_lingua(meta: dict) -> dict:
    """Parametro di lingua da accodare alle chiamate REST.

    Sui siti multilingua i termini di tassonomia sono legati a una lingua. Una
    chiamata REST che non la dichiara può vedersi scartare l'assegnazione di
    categoria senza alcun errore: WordPress risponde 200 e restituisce
    `categories` vuoto. Dichiararla esplicitamente è il tentativo più diretto.

    Se il sito non è multilingua il parametro viene semplicemente ignorato,
    quindi è innocuo. WP_LANG permette di sovrascriverlo o di disattivarlo
    impostandolo a stringa vuota.
    """
    lingua = os.environ.get("WP_LANG")
    if lingua is None:
        lingua = str(meta.get("lingua") or "").strip()
    return {"lang": lingua} if lingua else {}


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

    def interroga(parametri: dict) -> list[dict]:
        # Qui i ritentativi contano più che altrove: se questa lettura fallisce
        # non si sa se l'articolo esiste, e creare alla cieca significa un
        # doppione. Esaurite le prove, chiama() interrompe l'elaborazione.
        return chiama(
            "GET",
            endpoint,
            auth=auth,
            contesto="Verifica dei duplicati",
            params={**parametri, "status": TUTTI_GLI_STATI},
        )

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


def allinea_categorie(
    meta: dict, post: dict, base_url: str, categoria: str | None
) -> str:
    """Verifica che le categorie dichiarate siano davvero sull'articolo.

    Impostare `categories` nella POST di creazione non garantisce che il termine
    resti assegnato: un filtro lato WordPress o un plugin può riscrivere le
    tassonomie al salvataggio. Qui si ricontrolla il risultato e, se manca, si
    applica con un aggiornamento esplicito.

    L'aggiornamento fa l'unione con le categorie già presenti, così una
    categoria aggiunta a mano in revisione non viene rimossa.
    """
    nomi = categorie_richieste(meta, categoria)
    if not nomi:
        return "Categorie: nessuna dichiarata."

    utente, password = credenziali()
    auth = (utente, password)
    attesi = set(risolvi_categorie(nomi, base_url, auth, parametri_lingua(meta)))
    attuali = set(post.get("categories") or [])

    if attesi.issubset(attuali):
        return f"Categorie: già corrette {sorted(attuali)}."

    endpoint = f"{base_url.rstrip('/')}/wp-json/wp/v2/posts/{post['id']}"
    unione = sorted(attuali | attesi)
    try:
        # Aggiornare un post esistente per ID è idempotente: ritentare è sicuro.
        risultato = chiama(
            "POST",
            endpoint,
            auth=auth,
            contesto="Aggiornamento delle categorie",
            params=parametri_lingua(meta),
            corpo={"categories": unione},
        )
    except ErroreFatale as exc:
        return f"Categorie: aggiornamento fallito ({exc}). Da assegnare a mano."

    finali = risultato.get("categories") or []
    if attesi.issubset(set(finali)):
        return f"Categorie: corrette da {sorted(attuali)} a {finali}."
    return (
        f"Categorie: ATTENZIONE, dopo l'aggiornamento risultano {finali} invece di "
        f"{unione}. Qualcosa lato WordPress riscrive le tassonomie al salvataggio: "
        "assegnare a mano e verificare i plugin attivi."
    )


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
        ids = risolvi_categorie(
            nomi_categorie, base_url, (utente, password), parametri_lingua(meta)
        )
        payload["categories"] = ids
        print(f"Categorie risolte: {', '.join(nomi_categorie)} → {ids}")

    # La creazione NON passa da chiama(): un POST di creazione ritentato alla
    # cieca produrrebbe un doppione. Qui, prima di ogni nuovo tentativo, si
    # ricontrolla se l'articolo è stato creato comunque — perché una risposta
    # non JSON non dice se la richiesta è arrivata a WordPress o è stata
    # intercettata prima.
    ultimo: object = "nessun dettaglio"
    for tentativo in range(1, RITENTATIVI + 1):
        try:
            risposta = requests.post(
                endpoint,
                params=parametri_lingua(meta),
                json=payload,
                auth=(utente, password),
                timeout=TIMEOUT,
                headers=INTESTAZIONI,
            )
        except requests.RequestException as exc:
            ultimo = exc
        else:
            if risposta.status_code == 401:
                raise ErroreFatale(
                    "401 non autorizzato. Verifica WP_USER e rigenera l'application "
                    "password. Attenzione: alcune configurazioni di sicurezza (o un "
                    "plugin) possono bloccare l'autenticazione Basic sulle REST API."
                )
            if risposta.status_code == 403:
                raise ErroreFatale(
                    "403 vietato. L'utente esiste ma non ha i permessi per creare "
                    "articoli, oppure un WAF sta filtrando la richiesta."
                )
            if risposta.status_code == 404:
                raise ErroreFatale(
                    f"404 su {endpoint}. Le REST API sembrano disattivate o l'URL base "
                    "è errato (controlla WP_BASE_URL, es. presenza o assenza di www)."
                )
            if 400 <= risposta.status_code < 500:
                raise ErroreFatale(
                    f"WordPress ha risposto {risposta.status_code}: {risposta.text[:500]}"
                )
            if risposta.status_code >= 500:
                ultimo = f"{risposta.status_code} dal server"
            else:
                try:
                    return corpo_json(risposta, "Creazione dell'articolo")
                except RispostaNonJson as exc:
                    ultimo = exc

        if tentativo == RITENTATIVI:
            break

        attendi(tentativo, "Creazione dell'articolo", ultimo)

        # Il passaggio che rende sicuro il ritentativo.
        creato = articolo_esistente(meta, base_url, (utente, password))
        if creato is not None:
            print(
                f"L'articolo risulta creato nonostante la risposta non valida "
                f"(ID {creato['id']}, stato {creato['status']}): non lo ricreo."
            )
            return creato

    raise ErroreFatale(
        f"Creazione dell'articolo: {RITENTATIVI} tentativi falliti. Ultimo esito: "
        f"{ultimo}. Se il corpo è una pagina HTML, è il firewall che intercetta le "
        "chiamate REST: vedi docs/audit-tecnico-2026-10-01.md. L'articolo non "
        "risultava creato all'ultimo controllo, quindi un nuovo run è sicuro."
    )


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

    # Vale sia per gli articoli appena creati sia per quelli saltati: ogni
    # passaggio riporta le categorie a quanto dichiarato nel front matter.
    print(allinea_categorie(meta, risultato, args.base_url, args.categoria))

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
        except Exception as exc:  # noqa: BLE001
            # Rete di sicurezza: qualunque imprevisto su un articolo non deve
            # impedire l'elaborazione dei successivi. Il run resta rosso, ma il
            # log riporta il problema per ciascun file anziché fermarsi al primo.
            print(
                f"ERRORE IMPREVISTO su {percorso.name}: {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            errori.append(percorso.name)

    if args.dry_run:
        print("\nDry run completato: nessuna modifica al sito né al foglio.")

    if errori:
        print(f"\n{len(errori)} articoli non elaborati: {', '.join(errori)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
