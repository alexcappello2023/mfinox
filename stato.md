# MF Inox — stato del lavoro SEO

Ultimo aggiornamento: **2 novembre 2026**
Branch di lavoro: `claude/mfinox-seo-content-analysis-fv1x9h`, specchiato su `main`
Repository: `alexcappello2023/mfinox`

Questo file serve a riprendere il lavoro in una chat nuova senza rileggere tutto.
Se qualcosa qui contraddice un documento in `docs/`, vince questo file: è il più recente.

---

## 1. Regole di sicurezza — da rispettare sempre

> **La password applicativa di WordPress non va MAI scritta in un file, in un
> commit, in un log o in un messaggio.** Vive solo nei GitHub Secrets del
> repository (`WP_USER`, `WP_APP_PASSWORD`). Chi riprende il lavoro non ne ha
> bisogno: i workflow la leggono da soli.

- **Da fare, ancora in sospeso:** la password è transitata in chat quando è
  stata comunicata. Va **rigenerata** in WordPress (Utenti → Profilo → Password
  per le applicazioni: revoca quella vecchia, creane una nuova) e il nuovo
  valore va messo nel Secret `WP_APP_PASSWORD` senza passare dalla chat.
- `.gitignore` esclude `*.env`, `.env*`, `service-account*.json`,
  `credentials*.json`, `.DS_Store`.
- Lo script di pubblicazione forza `status: draft`. Lo stato `publish` è
  possibile solo a mano e stampa un avviso: **la pubblicazione è decisione del
  cliente**, non dell'automazione.
- **Mai inventare un valore numerico o dimensionale** in una tabella tecnica.
  Un valore sbagliato sul sito di un produttore fa ordinare il pezzo sbagliato a
  un progettista. Dove un valore non è certo si dichiara come «tipico» invece
  che come minimo di norma, e si annota in `note_redazione` cosa deve verificare
  l'ufficio tecnico.

---

## 2. Dove siamo

**18 articoli scritti**, tutti in italiano (la traduzione nelle altre lingue
avviene dopo, lato sito). **15 in bozza, 3 già pubblicati.** Mappatura completa,
letta dal log del run 19 del 2 novembre:

| ID | Stato su WP | Categoria | Articolo | File in `content/` |
|---|---|---|---|---|
| 8787 | bozza | ok | Galling e Nitronic 60 | `2026-08-17-galling-grippaggio-filetti-nitronic-60.md` |
| 8789 | bozza | ok | Corrosione galvanica | `2026-08-17-corrosione-galvanica-accoppiamenti-bimetallici.md` |
| 8791 | **pubblicato** | ok | Alloy 800 / 800H / 800HT | `2026-08-17-alloy-800-800h-800ht-alte-temperature.md` |
| 8793 | bozza | ok | PREN: come si calcola | `2026-08-17-pren-come-si-calcola.md` |
| 8795 | **pubblicato** | ok | DFARS e specialty metals | `2026-08-17-dfars-specialty-metals-bulloneria.md` |
| 8798 | **pubblicato** | ok | ISO 3506 e ASTM F593/F594 | `2026-08-17-iso-3506-astm-f593-equivalenze.md` |
| 8800 | bozza | ok `[1, 123]` | A193 B8 Classe 1 e Classe 2 | `2026-09-01-a193-b8-classe-1-classe-2.md` |
| 8803 | bozza | **vuota** | Antigrippanti e fattore K | `2026-09-01-antigrippanti-fattore-k.md` |
| 8861 | bozza | **vuota** | ASTM A194: i gradi dei dadi | `2026-10-01-astm-a194-gradi-dadi.md` |
| 8863 | bozza | **vuota** | Werkstoff, AISI, UNS, ASTM | `2026-10-01-equivalenze-werkstoff-aisi-uns-astm.md` |
| 8865 | bozza | **vuota** | Coppia di serraggio dei tiranti | `2026-10-01-coppia-serraggio-tiranti-inox-leghe-nichel.md` |
| 8867 | bozza | **vuota** | Bulloneria per flange ASME B16.5 | `2026-10-01-flange-bolting-chart-asme-b16-5.md` |
| 8869 | bozza | **vuota** | Serraggio flange ASME PCC-1 | `2026-10-02-asme-pcc-1-serraggio-flange.md` |
| 8871 | bozza | **vuota** | Infragilimento da idrogeno | `2026-10-02-infragilimento-da-idrogeno-bulloneria.md` |
| 8877 | bozza | **vuota** | 316Ti e 1.4571 contro il 316L | `2026-11-02-316ti-1-4571-stabilizzazione-vs-316l.md` |
| 8879 | bozza | **vuota** | Nimonic 80A oltre i 700 °C | `2026-11-02-nimonic-80a-bulloneria-alte-temperature.md` |
| 8881 | bozza | **vuota** | Titanio Gr. 2, Gr. 5, Gr. 7 | `2026-11-02-titanio-gr2-gr5-gr7-bulloneria-quale-scegliere.md` |
| 8883 | bozza | **vuota** | UNC, UNF o 8-UN | `2026-11-02-unc-unf-8un-filettature-bulloneria-inox.md` |

Link di revisione: `https://mfinox.com/wp-admin/post.php?post=<ID>&action=edit`

I quattro di novembre valgono 7.510 parole in tutto (1.878 / 1.948 / 1.925 /
1.759). Il totale del blog è circa 29.400 parole.

---

## 3. L'automazione: cosa c'è e come si usa

Tutto gira su GitHub Actions. Nessuno script va lanciato a mano in locale.

| Workflow | Quando parte | Cosa fa |
|---|---|---|
| **Pubblica bozza su WordPress** (`publish-draft.yml`) | da sé a ogni push di un `.md` in `content/` su `main`; oppure a mano | Crea le bozze via REST API. Salta gli slug già presenti su WordPress, quindi **rilanciarlo non crea duplicati**. A mano accetta: un singolo file, la categoria, lo stato, e una prova a vuoto (`dry_run`). |
| **Diagnostica WordPress** (`diagnostica.yml`) | a mano | Stampa ID, stato, data, link e i meta Yoast esposti degli articoli indicati. Serve a capire cos'è andato storto senza toccare il sito. |
| **Title e meta** (`title-meta.yml`) | a mano | Riscrive title SEO e meta description di 20 pagine da `data/title-meta.csv`. **Prova a vuoto per default**: scrive solo con `applica=true`. Non tocca mai gli slug. |
| **Piano editoriale** (`piano-editoriale.yml`) | a mano | Sincronizza `data/piano-editoriale.csv` con il Google Sheet. |

### Come si aggiunge un articolo

1. Scrivi un file in `content/` con front matter + blocchi Gutenberg (copia la
   struttura di un file esistente; i campi obbligatori sono `titolo`, `slug`,
   `focus_keyword`, `meta_title`, `meta_description`, `categoria`, `stato`).
2. Fai girare il validatore (vedi sotto). **Non saltare questo passaggio.**
3. Commit e push su `main`. Il workflow fa il resto e la bozza compare in
   Bacheca → Articoli → Bozze.

### Il validatore

`python3 scripts/valida_articolo.py content/*.md` — esce con codice 1 se
trova un errore, così si può mettere in un hook o in CI. Controlla:

- front matter completo, `meta_title` ≤ 60 caratteri, `meta_description` ≤ 160;
- blocchi Gutenberg aperti e chiusi nell'ordine giusto (`<!-- wp:x -->` /
  `<!-- /wp:x -->`) — questo intercetta gli errori che rompono l'editor;
- tag HTML bilanciati;
- nel corpo, nessun commento che non sia un delimitatore di blocco `wp:`
  (serve: un commento spurio non rompe nulla all'apparenza e resta nel sito);
- link interni con lo slash finale (la convenzione del progetto è **assoluta**,
  `https://mfinox.com/...`, come nei 18 articoli esistenti);
- residui tipo `TODO`, `placeholder`, cercati a parola intera.

Quattro articoli di agosto e settembre hanno la `meta_description` fra 162 e
165 caratteri, cioè 2-5 caratteri oltre il limite. Sono già su WordPress:
modificare il `.md` non li aggiorna. Si correggono a mano in Yoast, oppure si
aggiungono a `data/title-meta.csv` e si lancia il workflow Title e meta.

---

## 4. Conclusioni corrette — cose che altrove sono scritte male

Queste tre rettificano analisi precedenti. Chi riprende il lavoro deve partire
da qui, non da `docs/analisi-seo.md` di agosto.

1. **Le circa 31.000 impressioni su «raccordi» non sono domanda reale.** Sono un
   rank tracker: 0,92 impressioni per query al giorno, cioè un controllo
   automatico giornaliero della SERP, e **zero clic in 16 mesi**. In
   `docs/analisi-seo.md` erano state lette come opportunità. Non lo sono. Nel
   complesso il 13,6% delle impressioni da query è traffico di bot.

2. **Il bug delle categorie NON è il firewall.** I sette articoli che restano
   senza categoria `News` falliscono anche quando il run passa senza un solo
   errore e senza un solo ritentativo (run 18: 14 articoli su 14, zero errori,
   e gli stessi sette sbagliati). La PATCH riceve una risposta JSON valida che
   dichiara `categories: []`. Sono **due guasti distinti** comparsi insieme.
   **Il run 19 ha affinato il quadro e il confine è netto: tutto quello che ha
   un ID fino a 8800 ha la categoria giusta, tutto quello da 8803 in su la ha
   vuota — comprese le quattro bozze appena create.** Quindi non è una
   proprietà del singolo articolo: ogni articolo nuovo *nasce* senza categoria
   e la PATCH successiva non riesce ad assegnarla, mentre un articolo che una
   categoria ce l'ha già la conserva. Si noti che 8800 ha `[1, 123]`, cioè
   porta anche «Senza categoria».
   *Ipotesi da verificare: un plugin lato WordPress — traduzione o tassonomie —
   riscrive le tassonomie al salvataggio. Il modo di confermarlo è lo stesso
   comando del §5 che elenca i plugin attivi.*
   **Aggiramento che funziona oggi:** spuntare `News` a mano nella bacheca. Una
   volta messa, resta.

3. **I dati strutturati `Product` non pagano.** Senza prezzo, disponibilità e
   recensioni Google non mostra nulla. L'unico markup che rende è
   `BreadcrumbList`. Il plugin `wordpress/mfinox-seo.php` lo fa e **esclude
   deliberatamente `Product`**.

---

## 5. Il firewall e l'indicizzazione

**Dove siamo arrivati, con le prove:**

- Lo strato di challenge **gira dentro WordPress come plugin**, non è l'hosting
  e non è un proxy. Prove: `server: Apache`, nessun header di WAF, DNS diretto
  su IP Hetzner senza proxy, e soprattutto un header
  `permissions-policy` che autorizza esplicitamente `challenges.cloudflare.com`,
  `recaptcha.net` e `hcaptcha.com`. **Si risolve dalla bacheca**, non con un
  ticket all'hosting. (Le ipotesi precedenti su Sucuri e sull'hosting erano
  sbagliate.)
- Intercetta le chiamate REST **in modo intermittente e selettivo**: risponde
  200 con `text/html` e una pagina di attesa che si ricarica dopo 5 secondi.
  Il run 16 è fallito su 7 articoli su 14, il run 15 su nessuno.
- **Mitigazione già in repository e collaudata:** tre tentativi con attesa 3 e
  9 secondi su errore di rete, 5xx e risposte non JSON; nessun ritentativo sui
  4xx. La creazione non passa dall'helper generico: prima di ogni nuovo
  tentativo **ricontrolla se l'articolo esiste**, perché un POST di creazione
  ritentato alla cieca produrrebbe un doppione. Collaudata su sei scenari
  contro un finto WordPress, compreso il caso pericoloso «challenge ma post
  creato comunque»: riconosciuto, nessun duplicato.
- **L'articolo DFARS è tecnicamente indicizzabile**: HTTP 200, nessun
  `x-robots-tag: noindex`, canonical autoreferenziale corretto, `robots.txt`
  completamente aperto, sitemap dichiarata. Quindi le zero impressioni **non**
  sono un blocco tecnico di pagina.

**Il prossimo passo, da fare:**

```bash
# 1. nomina il plugin responsabile (i plugin si tradiscono dai percorsi dei loro asset)
curl -sS https://mfinox.com/ | grep -oE 'wp-content/plugins/[^/]+' | sort -u
```

2. In **Search Console → Controllo URL** sull'articolo DFARS → *Testa URL
   pubblicato* → apri **HTML testato**. Se compare «One moment, please...»
   invece dell'articolo, Google vede la challenge e non il contenuto: è la
   spiegazione definitiva delle zero impressioni.
3. Nelle impostazioni del plugin individuato, escludere `/wp-json/` e
   verificare la whitelist di Googlebot.

---

## 6. Da fare lato cliente / lato Alberto

In ordine di impatto.

1. **Rigenerare la password applicativa WordPress** e aggiornare il Secret.
2. **Escludere `/wp-json/` nel plugin di sicurezza** (vedi §5) — sblocca
   l'automazione in modo definitivo.
3. **Spuntare la categoria `News`** sulle 11 bozze che ne sono rimaste senza:
   8803, 8861, 8863, 8865, 8867, 8869, 8871, 8877, 8879, 8881, 8883. Trenta
   secondi a bozza, e aggira un guasto non ancora risolto. Una volta messa a
   mano, la categoria resta.
4. **Verifica tecnica delle tabelle numeriche** dei nuovi articoli. Cosa
   guardare è elencato in `note_redazione` dentro ogni file: in sintesi, i
   limiti di composizione contro l'edizione in uso della norma, i minimi
   meccanici contro la sezione del prodotto, e per il Nimonic 80A il ciclo di
   trattamento termico.
5. **Decidere se pubblicare le bozze.** Sono 18 e aspettano il consenso del
   cliente.
6. **Installare i due plugin** in `wordpress/`: `mfinox-seo.php` (meta Yoast
   esposti alla REST API + `BreadcrumbList`) e `mfinox-performance.php`
   (alleggerimento JavaScript). Il secondo parte in modalità `report`, che non
   cambia nulla: va letto l'inventario su `?mfinox_assets=1` da utente
   amministratore prima di passare a `on`.
7. **Riscrivere title e meta di 20 pagine**: l'elenco pronto da incollare è in
   `docs/title-meta-da-riscrivere.md`, oppure si applica col workflow.

Rimandate dal cliente, da non riproporre senza che le chieda: consolidare le
pagine duplicate; pubblicare le bozze prima della sua revisione.

---

## 7. I numeri che contano

Dall'export di Search Console a 16 mesi (`docs/riepilogo-2026-10-01.md` ha
l'analisi completa).

- **95,9% delle impressioni è su `/en/`.** Il mercato è internazionale, non
  italiano. Gli articoli si scrivono in italiano e si traducono.
- **13,6% delle impressioni da query è traffico di bot** (rank tracker).
- **LCP mobile 25,4 secondi**, di cui 14,4 s di soli redirect. È il problema
  tecnico più grave del sito e non è stato ancora affrontato alla radice.
- **DA 16 con 138 domini referenti.** Una singola pagina di Extreme Bolt ne ha
  62. Per questo si evitano gli argomenti dove si competerebbe a posizione
  35-47: non c'è autorità per vincerli.
- **I contenuti migliori dei concorrenti sono tabelle di riferimento**, non
  schede prodotto. È il motivo per cui gli articoli del sito sono costruiti
  attorno a tabelle e criteri di scelta.

---

## 8. Argomenti già valutati e scartati, con il motivo

Da non riproporre senza un motivo nuovo.

- **Hastelloy C-276 contro C-22.** 16.600 impressioni, ma posizioni 35-47:
  troppo arretrate perché un sito con DA 16 le recuperi.
- **Classi dell'A453 Gr. 660.** La pagina converte già allo 0,99%, il
  guadagno marginale è il più basso fra le opzioni esaminate.

---

## 9. Mappa del repository

```
content/           i 18 articoli, Markdown con front matter e blocchi Gutenberg
data/
  piano-editoriale.csv    18 righe: titolo, key, stato
  title-meta.csv          20 righe: url, title_seo, meta_description, titolo_post, stato
scripts/
  publish_to_wordpress.py  il cuore: idempotente, con ritentativi, forza draft
  aggiorna_title_meta.py   riscrive title e meta, prova a vuoto per default
  diagnostica_wp.py        legge lo stato di un articolo senza modificarlo
  piano_editoriale.py      sincronizza il CSV col Google Sheet
  sheet.py                 accesso al Google Sheet
  valida_articolo.py       controlla front matter, blocchi Gutenberg, HTML, link
docs/
  riepilogo-2026-10-01.md       l'analisi di riferimento: parti da qui
  audit-tecnico-2026-10-01.md   Ubersuggest, PageSpeed, prove sul firewall
  title-meta-da-riscrivere.md   i 20 title e meta pronti
  aggiornamento-2026-09.md
  analisi-seo.md                agosto, in parte superato (vedi §4)
  dati-strutturati.md
  javascript-non-utilizzato.md
  GITHUB.md, SETUP.md
wordpress/
  mfinox-seo.php           meta Yoast esposti alla REST + BreadcrumbList
  mfinox-performance.php   alleggerimento JavaScript, parte in sola lettura
```

Google Sheet del piano editoriale: `1zuea9Uglp9JqQuGekrNwpMm0NE4nxX57F7h1wm9n2CE`
(colonne: titolo / key / stato). Non è ancora stato popolato con le righe nuove.
