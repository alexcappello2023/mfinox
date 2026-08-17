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

**Pubblicare una bozza:** non serve fare nulla. Appena un `.md` arriva in
`content/` sul branch `main`, il workflow parte da sé e la bozza compare in
WordPress. Il riepilogo dell'esecuzione riporta l'ID dell'articolo, il link di
modifica e i tre campi da incollare in Yoast SEO.

L'esecuzione manuale resta disponibile per i casi particolari: `Actions` →
*Pubblica bozza su WordPress* → `Run workflow`, dove si può provare a vuoto
(`dry_run`), forzare una categoria, o limitarsi a un singolo file indicandone il
percorso. Lasciando il campo `articolo` vuoto viene valutata tutta la cartella.

**Sapere cosa scrivere:** `Actions` → *Piano editoriale* → `prossimo`.

## Il ciclo di lavoro

```
data/piano-editoriale.csv ──semina──> Google Sheet (DA FARE)
                                            │
                              si scrive content/<slug>.md
                                            │
                                    push su main
                                            │
                        WordPress: bozza creata ──> Sheet: INSERITO
```

## Perché rieseguire è sicuro

Lo script crea articoli, non li aggiorna. Da solo, una seconda esecuzione
produrrebbe un doppione. Per questo prima di scrivere verifica se l'articolo
esiste già su WordPress, in qualunque stato: cerca per slug e, se la bozza non
ha lo slug memorizzato, per titolo esatto. Se lo trova, lo salta.

La conseguenza pratica è che il workflow può girare su tutta la cartella
`content/` a ogni push senza effetti collaterali: pubblica solo ciò che manca.
Se una pubblicazione fallisce, il push successivo la ritenta da sé.

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
categoria: "News"        # per nome; più categorie separate da virgola
lingua: it
stato: draft
---
```

La categoria si indica per nome e non per ID: lo script la traduce nell'ID
numerico interrogando WordPress, così il file resta leggibile e non dipende da
numeri che cambiano tra un sito e l'altro. Se il nome non esiste, l'errore
elenca le categorie disponibili. Il campo si può scavalcare al volo con il
parametro `categoria` del workflow.

Il campo `titolo` è la chiave con cui lo script trova la riga del foglio da
aggiornare: se non coincide, la bozza viene creata comunque e il workflow
avvisa che lo stato va messo a mano.

## Sicurezza

Nessuna credenziale nel repository. Tutto passa dai GitHub Secrets, e
`.gitignore` esclude i file di credenziali più comuni. L'application password
usata in fase di analisi va rigenerata (vedi `docs/SETUP.md`).
