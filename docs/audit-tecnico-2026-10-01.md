# Audit tecnico del 1 ottobre 2026 — e la causa comune di quattro problemi

Strumento: Ubersuggest, account `alex.cappello@gmail.com` (tier2). Crawl
forzato di `mfinox.com`, 771 pagine visitate su 770 previste. PageSpeed su
desktop e mobile. Nessuna modifica al sito.

## Il risultato dell'audit non è utilizzabile, e il motivo è la scoperta

Ubersuggest riporta **5.032 problemi** e un punteggio di salute di **39,4**
contro i **75** della scansione precedente. I conteggi:

| Problema | Pagine |
|---|---|
| Titoli duplicati | 718 |
| Contenuto troppo breve | 718 |
| Meta description assente | 718 |
| Titolo troppo corto | 718 |
| Compressione disattivata | 718 |
| URL non SEO-friendly | 717 |
| H1 assente | 715 |

Settecentodiciotto pagine su 771 con **tutti** gli stessi difetti, e
contemporaneamente zero titoli vuoti, zero meta description duplicate, zero
errori 4xx, zero redirect. Un sito non si rompe in questo modo. Ho chiesto
l'elenco degli URL colpiti e il titolo che il crawler ha letto su ognuno:

```
https://mfinox.com/        →  title: "One moment, please..."
... e lo stesso identico titolo su tutte le altre 717 pagine.
```

**Il crawler non ha mai visto il sito.** Su ogni URL ha ricevuto la pagina di
attesa di un firewall applicativo, servita con codice `200`. «One moment,
please...» è la schermata di challenge del *WebSite Firewall* di Sucuri; altri
WAF ne usano una analoga.

Quindi i 5.032 problemi non esistono: sono la radiografia della pagina del
firewall. Il punteggio passato da 75 a 39 non misura un peggioramento del sito,
misura il momento in cui il firewall è stato messo davanti.

## Perché questa è la notizia importante

Quel firewall spiega **quattro sintomi** che fino a oggi sembravano scollegati.

**1. Nessuno strumento SEO può analizzare il sito.** Non solo Ubersuggest:
Screaming Frog, SEMrush, Ahrefs, Sitebulb vedranno tutti la stessa pagina. Il
sito è cieco a ogni diagnostica esterna.

**2. I 14,4 secondi di redirect su mobile.** PageSpeed attribuisce ai redirect
14,4 s dei 25,4 s di Largest Contentful Paint su mobile, e 2,5 s dei 4,9 s su
desktop. La catena di challenge del firewall è esattamente il tipo di redirect
che produce quel profilo.

**3. La REST API che risponde `200` con un corpo non JSON.** Non è più
un'ipotesi: il **run 16 del 1 ottobre** ha catturato il corpo della risposta, e
sono queste dodici righe.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <script>
      (function(){
          setTimeout(function(){
              window.location.reload();
          }, 5000);
      }())
  </script>
  <link rel="icon"…
```

`HTTP 200`, `Content-Type: text/html`, e una pagina che si ricarica da sola dopo
cinque secondi. È la stessa challenge che il crawler ha ricevuto su 718 URL su
718. Lo stesso meccanismo, catturato su due strumenti indipendenti: il firewall
intercetta anche le chiamate REST e il client crede di aver parlato con
WordPress.

Nel run 16 sono falliti **7 articoli su 14**, tutti con lo stesso
`JSONDecodeError`. Il run 15, quindici minuti prima, era passato senza errori
sulle stesse operazioni. Il rilancio immediato è andato a buon fine. È quindi
**intermittente e in peggioramento**: da zero fallimenti a sette.

Questo sposta la whitelist di `/wp-json/wp/v2/` da «utile» a **bloccante**:
senza, ogni pubblicazione è una scommessa su quale richiesta passa.

**Mitigazione in attesa della whitelist.** Dal 2 ottobre
`publish_to_wordpress.py` ritenta le chiamate che ricevono la challenge: tre
tentativi, attesa 3 e 9 secondi. Non si ritenta sui 4xx, che descrivono un
problema della richiesta. La creazione di un articolo è il caso delicato, perché
un POST ritentato alla cieca produrrebbe un doppione: lì, prima di ogni nuovo
tentativo, lo script ricontrolla se l'articolo è stato creato comunque — una
risposta non JSON non dice se la richiesta è arrivata a WordPress o è stata
intercettata prima.

Il meccanismo è stato collaudato contro un finto WordPress che imita la
challenge, su sei scenari:

| Scenario | Esito atteso | Verificato |
|---|---|---|
| Nessuna interferenza | pubblica al primo colpo | ✓ |
| Challenge sulle prime due letture | due ritentativi, poi pubblica | ✓ |
| Challenge sulla creazione, post non creato | ritenta e crea | ✓ |
| Challenge sulla creazione, **post creato comunque** | riconosce il post e **non lo duplica** | ✓ |
| Challenge sempre sulla creazione | si arrende, **zero post creati** | ✓ |
| Challenge su tutto | si arrende sulla verifica duplicati, prima di creare | ✓ |

Il quarto scenario è quello che conta: riconosce il post e non lo duplica.

### Il run 18 smentisce il legame fra firewall e categorie

Nel collaudo offline, dopo il riconoscimento del post l'allineamento delle
categorie era passato da `[]` a `[123]`, e ne avevo dedotto che il ritentativo
potesse sistemare anche quel bug. **Il run 18 sul sito reale dice che è
sbagliato.**

Quel run ha elaborato tutti e 14 gli articoli **senza un solo errore e senza un
solo ritentativo**: il firewall non è intervenuto nemmeno una volta. Eppure le
categorie restano non assegnate sugli stessi sette post. L'aggiornamento riceve
una risposta JSON valida, e quella risposta dichiara `categories: []`.

Conclusione: **il problema delle categorie non è il firewall.** WordPress accetta
la richiesta, risponde correttamente, e declina l'assegnazione del termine. Sono
due guasti distinti con la stessa data di comparsa, e la coincidenza temporale
mi aveva portato a unirli.

Resta un solo indizio utile, ed è riproducibile: **l'articolo 8800 è il solo su
cui l'aggiornamento abbia mai funzionato**, ed è anche il solo che prima
dell'aggiornamento avesse già un termine assegnato — `[1]`, Uncategorized. Su
quello l'unione `[1, 123]` è stata accettata. Su tutti gli altri, che partono da
`[]`, l'insieme `[123]` viene respinto.

L'esperimento decisivo è di una riga: assegnare via REST a uno dei sette post
l'insieme `[1, 123]` invece di `[123]`. Se resta, il blocco riguarda i post
senza termini e il rimedio è includere sempre la categoria predefinita
nell'unione. Se non resta, l'indizio cade e serve l'accesso admin per guardare i
filtri su `save_post` e i plugin di tassonomia.

**4. Le categorie scartate in silenzio.** La API accetta `categories: [123]`,
risponde `200`, e il post resta senza categoria. Un WAF che filtra il payload
della richiesta e la lascia passare svuotata produce esattamente questo.

### La cronologia regge

| Data | Evento |
|---|---|
| 17 agosto | Sei articoli pubblicati. Categorie assegnate **correttamente** |
| 1 settembre | Run 9 fallisce con risposta non JSON |
| 1 settembre | Dal run successivo le categorie **non si assegnano più** |
| 1 ottobre | Il crawler riceve la pagina di challenge su 718 URL su 718 |

Il firewall è stato quasi certamente attivato **fra il 17 agosto e il
1 settembre**. Fino al 17 agosto tutto funzionava.

Resta un dettaglio coerente: l'articolo 8800 è l'unico in cui l'aggiornamento
delle categorie è riuscito, passando da `[1]` a `[123, 1]`. Una regola di
filtraggio che si comporta diversamente a seconda del payload è più plausibile
di un problema di permessi WordPress, che sarebbe stato deterministico.

## Cosa fare, in ordine

**1. Scoprire quale firewall è, e chi l'ha messo.** Pannello di Sucuri o del
plugin di sicurezza, oppure l'hosting. Probabilmente non è una scelta fatta da
chi segue il sito.

**2. Mettere in whitelist i crawler SEO e la REST API.** Due regole:

- gli user agent e gli IP dei crawler di analisi, così il sito torna
  diagnosticabile;
- il percorso `/wp-json/wp/v2/` per l'utente dell'automazione, così le
  categorie si assegnano e le risposte tornano in JSON.

Con la seconda regola il punto 7 del piano (bug delle categorie) si chiude da
sé, e diventa utilizzabile anche `scripts/aggiorna_title_meta.py`.

**3. Verificare che Googlebot non riceva la challenge.** Search Console
registra 660.221 impressioni in 16 mesi, quindi Google indicizza: i firewall
mettono in whitelist i bot dei motori per impostazione predefinita. Ma vale la
pena controllare con `Controllo URL` → `Testa URL pubblicato` sui due articoli
pubblicati che hanno **zero impressioni** (DFARS e ISO 3506). Se Google li vede
come «One moment, please...», il problema di indicizzazione di quei due
articoli è spiegato.

**4. Rifare l'audit dopo la whitelist.** Solo allora i numeri avranno un senso,
e si potrà vedere quali problemi tecnici esistono davvero.

## Quello che si può concludere comunque

Due misure non dipendono dal crawler e restano valide.

### PageSpeed

| Metrica | Desktop | Mobile | Soglia «buono» |
|---|---|---|---|
| Largest Contentful Paint | 4,9 s | **25,4 s** | ≤ 2,5 s |
| Time to Interactive | 5,1 s | 26,4 s | — |
| First Contentful Paint | 0,7 s | 3,3 s | ≤ 1,8 s |
| Speed Index | 1,9 s | 7,7 s | ≤ 3,4 s |
| Cumulative Layout Shift | 0 | 0 | ≤ 0,1 ✓ |
| Total Blocking Time | 68 ms | 148 ms | ≤ 200 ms ✓ |

| Intervento | Desktop | Mobile |
|---|---|---|
| Eliminare i redirect | 2,5 s | **14,4 s** |
| JavaScript non utilizzato | 1,2 s (1.055 KB) | 10,8 s (1.180 KB) |
| JavaScript non minificato | 0 ms (8 KB) | 0 ms |

Oltre al firewall, **1,18 MB di JavaScript caricato e mai eseguito**: plugin
attivi su tutte le pagine anche dove non servono. Quello è un problema reale e
indipendente.

Due precisazioni per non attribuire troppo a questi numeri:

- **Non spiegano il CTR mobile più basso del desktop.** Il CTR si decide nella
  SERP, prima che la pagina carichi. La spiegazione resta il title troncato.
- **Non stanno danneggiando il posizionamento in modo visibile**: su mobile il
  sito è posizionato *meglio* che su desktop (13,49 contro 21,81). È un problema
  di esperienza e di conversione, non di ranking.

### Autorevolezza del dominio

| | |
|---|---|
| Domain Authority | **16** |
| Backlink | 4.746 da **138** domini referenti |
| Keyword organiche (USA) | 86, per 181 visite stimate al mese |

DA 16 con 138 domini referenti è un profilo debole per un sito di 770 pagine. È
il motivo per cui molte query restano in posizione 40–60 pur avendo una pagina
dedicata: non manca il contenuto, manca l'autorità. Nessuna riscrittura di title
compensa questo, e va detto prima di fissare aspettative sui punti 3 e 4 del
piano.

Un confronto che ridimensiona i dati di Search Console: Ubersuggest misura solo
gli Stati Uniti e dà `nace mr0175` (volume 390) in **posizione 53** e
`astm a262` (volume 140) in **posizione 53**, dove Search Console — che media su
tutti i paesi — dava 26,75 e 6,83. Dove il mercato è più grande, il
posizionamento è peggiore di quanto la media suggerisca.
