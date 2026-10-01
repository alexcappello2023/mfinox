# Dati strutturati: cosa installare e come verificarlo

Search Console, scheda `Aspetto nella ricerca`, export del 1 ottobre 2026:
**una sola riga**, Risultati tradotti. Nessun breadcrumb, nessun risultato
prodotto. Google non riconosce nessun markup strutturato sul sito.

Il file da installare è `wordpress/mfinox-seo.php`.

## Cosa fa

**1. Rende scrivibili i campi Yoast via REST API.** Serve all'automazione dei
title e delle meta description (`scripts/aggiorna_title_meta.py`). Senza questo
WordPress risponde `200` e scarta i valori: l'automazione crederebbe di aver
scritto qualcosa. Registra `_yoast_wpseo_title`, `_yoast_wpseo_metadesc` e
`_yoast_wpseo_focuskw` su **tutti** i tipi di contenuto pubblici — le schede
materiale non sono dei normali `post` e il frammento in `SETUP.md` copriva solo
quelli. La scrittura resta riservata a chi ha già `edit_posts`.

**2. Stampa il BreadcrumbList in JSON-LD** sulle pagine singole. In SERP la riga
dell'URL passa da

```
mfinox.com/en/materials/stainless-steel-w-1-4529-aisi-926-uns-n08926-3/
```

a

```
mfinox.com › Materials › 1.4529 AISI 926
```

Non cambia nulla in pagina e non influisce sul posizionamento: agisce sul CTR,
ed è l'unico markup fra quelli disponibili che produca un effetto visibile su
questo sito.

Si disattiva da solo se i breadcrumb di Yoast sono già attivi, per non stampare
il markup due volte.

## Cosa NON fa, e perché

**Niente markup `Product`.** Google mostra un risultato arricchito di prodotto
solo se il markup contiene prezzo, disponibilità o recensioni. Il sito non
espone nessuno dei tre. Il markup verrebbe letto, comparirebbe in Search
Console nel rapporto "Prodotti" con degli avvisi, e in SERP non cambierebbe
niente. Da aggiungere quando ci sarà almeno la disponibilità.

Questa è una correzione a quanto avevo scritto nel riepilogo: avevo messo
`Product` e `BreadcrumbList` sullo stesso piano. Non lo sono.

**Niente `FAQPage`.** Dal 2023 Google mostra i risultati arricchiti FAQ solo
per siti istituzionali e sanitari. Su un sito commerciale non produce nulla.

## Installazione

Due modi, equivalenti.

**Come mu-plugin** (si attiva da solo, nessuno può disattivarlo per sbaglio):

```
wp-content/mu-plugins/mfinox-seo.php
```

Se la cartella `mu-plugins` non esiste, va creata.

**Come plugin normale** (compare in bacheca e si può disattivare):

```
wp-content/plugins/mfinox-seo/mfinox-seo.php
```

poi `Plugin` → `Plugin installati` → attiva "MF Inox — SEO helper".

Il file non tocca il tema, quindi un aggiornamento del tema non lo cancella.

## Verifica, in quest'ordine

1. **Prima di tutto, controlla se serve.** `Yoast SEO` → `Impostazioni` →
   `Avanzate` → `Breadcrumb`. Se sono già attivi, Yoast stampa il markup da sé e
   del punto 2 non c'è bisogno: resta utile solo il punto 1.

2. **Il markup c'è?** Apri una scheda materiale e cerca `BreadcrumbList` nel
   codice sorgente della pagina (`Ctrl+U`, poi `Ctrl+F`).

3. **Google lo legge?** Incolla l'URL in
   `search.google.com/test/rich-results`. Deve comparire "Percorsi di
   navigazione" senza errori.

4. **I campi Yoast sono scrivibili?** `Actions` → `Aggiorna title e meta
   description` → `Run workflow` **senza** spuntare `applica`. È una prova a
   vuoto: se i campi non sono esposti lo dice e non scrive niente.

5. **Fra una e due settimane**, Search Console → `Percorsi di navigazione`. Il
   rapporto compare solo dopo che Google ha ripassato le pagine.

## Se qualcosa va storto

Il file si rimuove cancellandolo: non scrive nel database, non modifica
contenuti, non lascia tracce. Il markup si può anche disattivare senza
rimuoverlo, aggiungendo nel `functions.php` del tema:

```php
add_filter( 'mfinox_breadcrumb_jsonld', '__return_false' );
```
