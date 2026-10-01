# JavaScript non utilizzato: come lo togliamo

PageSpeed misura **1,18 MB di JavaScript caricato e mai eseguito**: 10,8 s di
risparmio stimato su mobile, 1,2 s su desktop. Il file da installare è
`wordpress/mfinox-performance.php`.

## Perché serve un inventario prima delle regole

PageSpeed dà il totale, non l'elenco dei file. E il sito non è leggibile da
fuori: il firewall applicativo serve la pagina «One moment, please...» a
qualunque crawler (vedi `docs/audit-tecnico-2026-10-01.md`).

Indovinare quali plugin caricano cosa significherebbe rompere il sito. Quindi il
plugin parte **in sola lettura** e la prima cosa che fa è dirti cosa c'è.

## Passo 1 — installare e guardare

Copia il file in:

```
wp-content/mu-plugins/mfinox-performance.php
```

**Non serve configurare niente.** Senza la costante in `wp-config.php` la
modalità è `report`: il plugin non tocca una riga di quello che il visitatore
vede.

Poi, da amministratore, apri tre pagine aggiungendo `?mfinox_assets=1` all'URL:

```
https://mfinox.com/en/?mfinox_assets=1
https://mfinox.com/en/materials/stainless-steel-w-1-4529-aisi-926-uns-n08926-3/?mfinox_assets=1
https://mfinox.com/en/astm-a194-high-performance-nuts-for-high-and-low-temperature-industrial-applications/?mfinox_assets=1
```

In fondo a ogni pagina compare una tabella: ogni script e ogni foglio di stile
con **handle, peso in KB, dipendenze** e se ha codice inline attaccato. Ordinata
dal più pesante.

Tre pagine diverse perché è il confronto che smaschera gli sprechi: uno script
che compare sulla scheda materiale ma serve solo alla home è peso buttato su 154
pagine.

Mandami le tre tabelle e ti scrivo le regole del sito.

## Passo 2 — provare a vuoto

In `wp-config.php`, sopra la riga `/* That's all, stop editing! */`:

```php
define( 'MFINOX_PERF_MODE', 'dry' );
```

Il plugin scrive nel log degli errori di PHP cosa rimuoverebbe, senza rimuovere
niente. Controlla il log, poi passa a `'on'`.

## Passo 3 — applicare

```php
define( 'MFINOX_PERF_MODE', 'on' );
```

A questo punto il plugin fa tre cose.

**Rimuove gli sfridi certi.** Solo quelli che su qualunque installazione
WordPress si possono togliere senza conseguenze:

| Asset | Cos'è | Perché via |
|---|---|---|
| `wp-embed` | script oEmbed | serve solo se altri incorporano *questo* sito nelle loro pagine |
| `jquery-migrate` | ponte per codice jQuery pre-2016 | se il tema è recente non serve |
| script e CSS degli emoji | rilevamento emoji | i browser di oggi li gestiscono da sé |

Tutto il resto **non viene toccato**: la rimozione è una scelta esplicita, non
un comportamento predefinito. Le regole sui plugin del sito si aggiungono dopo
il passo 1, con il filtro `mfinox_perf_regole`. Nel file c'è l'esempio già
scritto per Contact Form 7, che è il caso tipico: il modulo sta su una pagina e
lo script si carica su tutte.

**Rinvia il resto con `defer`.** Gli script non critici smettono di bloccare il
rendering. È l'intervento con il rapporto fra effetto e rischio migliore:
nessuno script sparisce, cambia solo quando viene eseguito.

Due esclusioni, che sono il motivo per cui questo file è più lungo di tre righe:

- **jQuery non si rinvia mai.** Temi e plugin stampano codice inline che usa `$`
  subito dopo averlo caricato: rinviare jQuery romperebbe la pagina.
- **Nessuno script con codice inline attaccato si rinvia.** Se la libreria
  arriva dopo, l'inline gira su una libreria che non c'è ancora. Il plugin lo
  verifica con `get_data( $handle, 'after' )` e lo salta.

## Interruttore d'emergenza

Un amministratore può disattivare tutto per una singola richiesta:

```
https://mfinox.com/en/?mfinox_perf=off
```

Serve a capire in dieci secondi se un problema è colpa del plugin. Per spegnerlo
del tutto: cancella il file, o rimetti `'report'`.

Il plugin non scrive nel database, non modifica contenuti, non lascia tracce.

## Quanto aspettarsi

Meno di 10,8 s. Due motivi.

**Le stime di PageSpeed non si sommano.** I 14,4 s attribuiti ai redirect e i
10,8 s del JavaScript si sovrappongono: parte dell'attesa è la stessa, contata
due volte da due diagnosi diverse.

**I 10,8 s valgono su una 4G lenta simulata**, che è il profilo di test di
Lighthouse. Su una connessione reale il guadagno è minore, ma va nella stessa
direzione.

E resta il fatto che **il firewall pesa più del JavaScript**. Se si può
intervenire su una cosa sola, la whitelist del WAF vale più di questo. Ma sono
indipendenti e si possono fare in parallelo: questo non richiede di toccare la
sicurezza del sito.
