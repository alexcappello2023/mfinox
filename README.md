# mfinox — contenuti SEO e pubblicazione automatica

Analisi SEO, piano editoriale e automazione per caricare gli articoli del blog
`mfinox.com` come **bozze** su WordPress, tenendo sincronizzato lo stato su un
Google Sheet.

Ogni articolo arriva in WordPress in stato `draft`: la pubblicazione resta una
decisione del cliente.

## Struttura

| Percorso | Contenuto |
|---|---|
| `docs/analisi-seo.md` | Analisi dei 16 mesi di Search Console, confronto con i concorrenti, motivazione dei dieci temi |
| `docs/GITHUB.md` | Percorso completo su GitHub: push iniziale, Actions, secrets, prima esecuzione |
| `docs/SETUP.md` | Dettaglio su secrets, variables, service account Google e campi Yoast |
| `data/piano-editoriale.csv` | I dieci titoli con la key e lo stato, da cui si popola il Google Sheet |
| `content/` | Gli articoli: front matter YAML con i metadati SEO, corpo in blocchi Gutenberg |
| `scripts/publish_to_wordpress.py` | Crea la bozza via REST API e segna la riga come `INSERITO` |
| `scripts/piano_editoriale.py` | Popola il foglio, mostra il prossimo argomento `DA FARE` |
| `scripts/sheet.py` | Accesso al Google Sheet |
| `.github/workflows/` | I due workflow, entrambi a esecuzione manuale |

## Come si usa

**Prima volta:** segui `docs/GITHUB.md`, che copre anche le tre trappole
tipiche (workflow non visibili, permessi delle GitHub App, Actions da abilitare).

**Popolare il foglio:** `Actions` → *Piano editoriale (Google Sheet)* → `semina`.
Aggiunge i dieci titoli in stato `DA FARE` senza duplicare quelli già presenti.

**Pubblicare una bozza:** `Actions` → *Pubblica bozza su WordPress* → `Run workflow`,
indicando il percorso del file in `content/`. Il riepilogo dell'esecuzione
riporta l'ID dell'articolo, il link di modifica e i tre campi da incollare in
Yoast SEO.

**Sapere cosa scrivere:** `Actions` → *Piano editoriale* → `prossimo`.

## Il ciclo di lavoro

```
data/piano-editoriale.csv ──semina──> Google Sheet (DA FARE)
                                            │
                              si scrive content/<slug>.md
                                            │
                            workflow "Pubblica bozza"
                                            │
                        WordPress: bozza creata ──> Sheet: INSERITO
```

Lo stato passa a `INSERITO` solo dopo che WordPress ha confermato la creazione:
il foglio non può segnalare come caricato un articolo che non esiste.

## Formato di un articolo

Front matter YAML, poi il corpo in blocchi Gutenberg (`<!-- wp:paragraph -->`…),
così il cliente lo trova editabile nell'editor invece che dentro un unico blocco
HTML.

```yaml
---
titolo: "…"              # deve coincidere con la riga del foglio
slug: "…"
focus_keyword: "…"
meta_title: "…"          # da incollare in Yoast
meta_description: "…"    # da incollare in Yoast, usata anche come excerpt
lingua: it
stato: draft
---
```

Il campo `titolo` è la chiave con cui lo script trova la riga del foglio da
aggiornare: se non coincide, la bozza viene creata comunque e il workflow
avvisa che lo stato va messo a mano.

## Sicurezza

Nessuna credenziale nel repository. Tutto passa dai GitHub Secrets, e
`.gitignore` esclude i file di credenziali più comuni. L'application password
usata in fase di analisi va rigenerata (vedi `docs/SETUP.md`).
