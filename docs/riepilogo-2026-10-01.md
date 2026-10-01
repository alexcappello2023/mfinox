# MF Inox — Riepilogo completo al 1 ottobre 2026

Export Search Console analizzato: **29/05/2025 – 28/09/2026** (16 mesi, ricerca
Web), pacchetto completo: Grafico, Query, Pagine, Paesi, Dispositivi, Aspetto
nella ricerca.

Questo documento sostituisce le conclusioni operative di `analisi-seo.md`
(export di agosto). L'analisi dei totali e della stagionalità resta in
`aggiornamento-2026-09.md`. Qui c'è tutto: stato del lavoro fatto, cosa dicono i
dati nuovi, e il piano rivisto.

---

## Parte 1 — Stato del lavoro

### Cosa è stato costruito

L'automazione di pubblicazione è completa e funzionante:

| Componente | File | Stato |
|---|---|---|
| Pubblicazione su WordPress | `scripts/publish_to_wordpress.py` | funziona |
| Workflow automatico al push | `.github/workflows/publish-draft.yml` | funziona |
| Diagnostica WordPress | `scripts/diagnostica_wp.py` | funziona |
| Piano editoriale | `data/piano-editoriale.csv` | aggiornato a mano |
| Google Sheet | — | non collegabile (restrizioni Google Cloud) |

Il flusso è: scrivo l'articolo → push su `main` → GitHub Actions crea la bozza
su WordPress. Niente passaggi manuali, idempotente (un secondo run non duplica),
e un articolo che fallisce non blocca gli altri.

### Cosa è stato scritto

Otto articoli, 13.056 parole, tutti in italiano, tutti in bozza:

1. Galling e grippaggio dei filetti — Nitronic 60 (UNS S21800)
2. Corrosione galvanica negli accoppiamenti bimetallici
3. PREN: come si calcola
4. Alloy 800, 800H e 800HT alle alte temperature
5. ISO 3506 e ASTM F593/F594: equivalenze
6. ASTM A193 B8 Classe 1 e Classe 2
7. Antigrippanti e fattore K
8. DFARS e specialty metals

### Due problemi tecnici irrisolti

**a) WordPress scarta la categoria assegnata via REST.** La API risponde 200 ma
il post resta senza categoria. Verificato che non è un problema di termini
multilingua (la lista delle categorie è identica con e senza `?lang=it`) né di
ID sbagliato (`News` = 123). La spunta manuale nell'admin funziona e resta.
Ipotesi residua: l'utente `alberto.lupi` non ha `assign_terms` sulla tassonomia
via REST, o un plugin di sicurezza filtra il campo restituendo comunque 200.
Serve qualcuno con accesso admin al sito per chiuderla. **Workaround attuale: la
spunta `News` a mano.**

**b) Una risposta non JSON da WordPress** ha fatto fallire il run #9. Lo script
adesso la gestisce e la segnala; il nuovo tentativo è andato a buon fine senza
modifiche, quindi era transitorio (WAF o cache). Da riverificare che non esista
una bozza ISO 3506 duplicata: gli ID dei post sono saltati da 8795 a 8798.

### In sospeso da parte tua

- spunta `News` sulle bozze 8798, 8800, 8803;
- **rotazione della password applicativa WordPress** (è passata nella chat, va
  rigenerata: WordPress → Utenti → Profilo → Password per applicazioni);
- la verifica (a) qui sopra, con accesso admin.

---

## Parte 2 — Le tre cose che i dati nuovi cambiano

### 1. Gli otto articoli non esistono per Google

`Pagine.csv` contiene 446 URL, fino a quelli con **una sola impressione**: non è
una lista troncata. Nessuno degli otto slug compare. Zero impressioni, zero
clic, in sei settimane dalla prima stesura.

**Aggiornamento del 1 ottobre, dai log del run 13.** Lo stato reale su
WordPress risolve l'ambiguità: non sono tutti bozze.

| ID | Articolo | Stato |
|---|---|---|
| 8787 | Galling / Nitronic 60 | draft |
| 8789 | Corrosione galvanica | draft |
| 8791 | Alloy 800 / 800H / 800HT | **future** (programmato) |
| 8793 | PREN | draft |
| 8795 | DFARS | **publish** |
| 8798 | ISO 3506 / F593 | **publish** |
| 8800 | A193 B8 Classe 1 e 2 | draft |
| 8803 | Antigrippanti / fattore K | draft |
| 8861 | ASTM A194 gradi | draft (nuovo) |
| 8863 | Equivalenze Werkstoff/AISI/UNS/ASTM | draft (nuovo) |

Due articoli sono **pubblicati** e hanno **zero impressioni** fino al 28
settembre. Non è quindi un problema di pubblicazione: è un **problema di
indicizzazione**. Vanno controllati tre punti: che non siano `noindex`, che
compaiano nella sitemap, e che l'URL sia stato sottoposto a Search Console con
"Richiedi l'indicizzazione".

Uno (8791) è in stato `future`, cioè programmato per una data futura: nessuno
sembra averlo deciso intenzionalmente e va verificato.

In ogni caso la conclusione sull'attribuzione non cambia: **il salto di
posizione di settembre non è attribuibile ai contenuti.** Pagine con zero
impressioni non possono spostare la posizione media del sito.

Resta un fatto buono — settembre 2026 è il mese migliore dei 16 per posizione
media (12,52) e il secondo per clic (378 in 28 giorni, +29% sul settembre 2025)
— ma la causa è altrove: stagionalità documentata più, con ogni probabilità, un
aggiornamento dell'algoritmo.

### 2. Il 95,9% della visibilità del sito è in inglese. Gli articoli sono in italiano.

| Lingua | Pagine | Clic | Impressioni | CTR | % impr. |
|---|---|---|---|---|---|
| `/en/` | 154 | 3.413 | 685.243 | 0,50% | **95,9%** |
| home `/` | 1 | 1.390 | 11.889 | 11,69% | 1,7% |
| `/` italiano | 90 | 76 | 5.699 | 1,33% | **0,8%** |
| `/es/` | 75 | 71 | 6.516 | 1,09% | 0,9% |
| `/fr/` | 54 | 50 | 2.161 | 2,31% | 0,3% |
| `/de/` | 61 | 47 | 2.235 | 2,10% | 0,3% |

Novanta pagine italiane producono **5.699 impressioni in 16 mesi**, contro le
685.243 delle 154 pagine inglesi. E dove esiste la coppia, il divario è brutale:

| Contenuto | `/en/` | italiano |
|---|---|---|
| ASTM A194 dadi | 22.616 impr | 201 impr |
| CRC classi di corrosione | 21.202 impr | 14 impr |
| La cultura dei materiali | 17.209 impr | 20 impr |
| NACE MR0175/MR0103 | 14.761 impr | 18 impr |
| ISO 3506 | 14.825 impr | 185 impr |
| Monel 400 guida completa | 9.840 impr | 1.400 impr |

I 1.500 clic italiani di `Paesi.csv` sono quasi tutti brand: la sola home fa
1.390 clic e le query brand ne fanno 969. **Il traffico organico italiano non
brand è praticamente zero.**

Conclusione scomoda ma netta: scrivere in italiano è stato un errore di
impostazione mio. Gli otto articoli valgono comunque — il contenuto tecnico è
buono e il piano è costruito su cluster di domanda reali — ma **vanno pubblicati
in inglese, su `/en/`, con l'italiano come traduzione secondaria**, non il
contrario.

### 3. Il 13,6% delle impressioni non sono utenti

Nell'export delle query ci sono 122 query con una struttura che non è umana:

| Famiglia | Query | Impressioni | Clic | Impr./query/giorno |
|---|---|---|---|---|
| `caps / fondelli / pezzi a t / riduzioni / curve / tubi / raccordi / flange` + lega | 74 | 33.236 | **0** | 0,92 |
| `screw / bolt / washer / nuts` + lega | 39 | 9.488 | 3 | 0,50 |
| `duplex super duplex nickel alloy fastener distributor buyer <paese>` | 4 | 846 | 0 | 0,43 |
| `thyssenkrupp materials uk datasheet 1.4301 … 400°c` | 4 | 331 | 0 | 0,17 |
| **totale** | **122** | **43.993** | **3** | |
| confronto: query normali sopra 400 impressioni | 174 | — | 1.006 | 2,22 |

Il dato che decide: **0,92 impressioni per query al giorno** sulla prima
famiglia. Una impressione al giorno, per 488 giorni, su 74 combinazioni che
formano un prodotto incrociato perfetto (8 tipi di raccordo × 9 leghe), con zero
clic in 16 mesi. È la firma di un **rank tracker che controlla una lista di
keyword una volta al giorno**, non di un mercato.

Questo **corregge una mia conclusione precedente**: in `analisi-seo.md` avevo
letto quelle ~31.000 impressioni come domanda reale di carpenteria per tubazioni
e avevo scritto che erano "impressioni già acquisite senza una pagina prodotto a
cui atterrare". Non lo sono. Sono controlli automatici.

Come verificarlo in dieci minuti: controlla se il sito (o l'agenzia che lo
seguiva) ha un progetto in SEMrush/Ahrefs/Ubersuggest con esattamente quelle
liste di keyword. Il formato `screw|bolt|washer × materiale` e
`caps|fondelli|pezzi a t × lega` è tipico di una lista costruita a tabella.

Conseguenza pratica: il CTR del sito è **strutturalmente sottostimato**. Togliendo
i pattern automatici il CTR non-brand passa da 0,16% a 0,19%. Poco in assoluto,
ma vuol dire che una fetta del "problema CTR" non è recuperabile perché non c'è
nessun umano da convertire.

---

## Parte 3 — Il problema vero, misurato

### Brand contro non brand

| | Query | Clic | Impressioni | CTR |
|---|---|---|---|---|
| Brand (`mf inox`, `mfinox`, `mf screws`, `vimi`…) | 14 | 969 (65%) | 2.999 (0,9%) | 32,31% |
| Non brand | 986 | 522 (35%) | 320.149 (99,1%) | **0,16%** |

Identico ad agosto. Il 65% dei clic arriva dallo 0,9% delle impressioni.

**756 query su 1.000 hanno zero clic**, per 237.461 impressioni.

### Dove i clic sono recuperabili e dove no

Le query a zero clic si dividono in due gruppi che richiedono interventi opposti:

**Gruppo A — ben posizionate, zero clic (139 query, 24.608 impressioni, pos ≤ 10).**
Qui non serve ranking, serve far cliccare. Ma attenzione: una parte di queste è
irrecuperabile per natura dell'intento.

| Query | Impr. | Pos. | Tipo di intento |
|---|---|---|---|
| `astm a262` | 1.117 | 6,83 | norma — recuperabile |
| `caps inox` | 840 | 7,43 | pattern automatico |
| `uns n06625 material` | 693 | 7,32 | lookup di specifica |
| `astm a193 b8ma` | 599 | 7,10 | norma — recuperabile |
| `astm a193 b8t` | 563 | 8,08 | norma — recuperabile |
| `din 6334` | 513 | 6,66 | norma — recuperabile |
| `astm a193 b8a` | 425 | 7,08 | norma — recuperabile |
| `astm a182 f55` | 422 | 9,20 | norma — recuperabile |
| `duplex 2507 chemical composition` | 316 | 4,26 | lookup di specifica |
| `ss 2507 chemical composition` | 298 | 1,82 | lookup di specifica |

Il caso `2507 chemical composition` va guardato da vicino: **1.258 impressioni
in posizione 1,70 e un clic in 16 mesi.** Posizione 1 con CTR 0,08% non è un
titolo sbagliato: è Google che risponde nella SERP, con un featured snippet o
un'AI Overview. Su una query che chiede un numero, l'utente legge il numero e
non clicca. Lo stesso vale per la famiglia `w.nr 2.4668`, `werkstoff 1.4301`,
`1.4828 material equivalent`: sono lookup di tabella.

Su queste la visibilità vale come presidio del marchio, non come traffico. **Non
le conterei nel potenziale di recupero.**

**Gruppo B — posizione 11–20, zero clic (120 query, 39.123 impressioni).**
Qui il problema è il ranking, e il rimedio è il contenuto. Le prime:

| Query | Impr. | Pos. |
|---|---|---|
| `1.4571 material` | 2.119 | 17,98 |
| `alloy 2507` | 1.793 | 11,23 |
| `n06625` | 1.749 | 16,74 |
| `uns no6625` | 1.556 | 18,84 |
| `inconel 625 key features` | 1.275 | 10,82 |
| `monel werkstoff` | 1.193 | 17,34 |
| `r56400` (titanio Gr. 5) | 1.180 | 13,36 |
| `1.4980 / a286 / 660` | 1.078 | 12,06 |
| `1.4057 atmos / 431 / apx` | 950 | 12,30 |
| `astm a194 8m` | 877 | 16,17 |

### I cluster di domanda reale, per dimensione

| Cluster | Query | Impressioni | Clic | CTR | Pos. |
|---|---|---|---|---|---|
| Equivalenze (`equivalent`, `w.nr`, `werkstoffnummer`, `X / Y / Z`) | 54 | 15.052 | 33 | 0,22% | 31,2 |
| ASTM A194 — suffissi di grado (8, 8M, 8T, 8C, 8MLCuN, 3) | 32 | 10.113 | 17 | 0,17% | 16,1 |
| ASTM A193 B8x — suffissi di grado | 31 | 6.416 | 28 | 0,44% | 11,3 |
| A453 Gr. 660 / 1.4980 / A286 | 30 | 6.408 | 26 | 0,41% | 18,2 |
| NACE MR0175 vs MR0103 | 19 | 5.664 | 4 | 0,07% | 27,5 |
| Alloy 2507 / composizione | 15 | 5.742 | 5 | 0,09% | 10,6 |
| CRC / classi di resistenza a corrosione | 17 | 4.762 | 11 | 0,23% | 37,1 |
| ISO 3506 (incl. classi A2-70 / A4-80) | 15 | 4.714 | 25 | 0,53% | 20,6 |
| ASTM A320 / criogenico | 10 | 4.086 | 4 | 0,10% | 6,9 |

Due osservazioni su questa tabella.

**Le equivalenze sono il cluster più grande e il meno presidiato.** 54 query,
15.052 impressioni, posizione media 31. Quando convertono, convertono sopra la
media del sito (`1.4529 material equivalent` 1,03%, `astm a453 grade 660
equivalent material` 2,24%, `x19crmonbvn11-1 equivalent astm` 27,27%). Il sito
non ha **nessuna pagina hub di equivalenze**: ogni scheda materiale cita i propri
numeri, ma non esiste la tabella di conversione Werkstoff ↔ EN ↔ AISI ↔ UNS ↔
ASTM che la query chiede. Le varianti `w.nr 2.4668`, `w nr 2.4668`, `w.nr. 2.4668`
da sole fanno 3.249 impressioni in posizione 46–56.

**I suffissi di grado sono il secondo.** `astm a194` sta in posizione 9,42 con
2.931 impressioni e 6 clic; tutta la famiglia 8/8M/8T/8C/8MLCuN/3 è ben
posizionata e a zero clic. Nessuna pagina del sito risponde alla domanda vera,
che è «quale suffisso mi serve»: ci sono le schede dei singoli gradi, non il
decoder.

### CTR mobile sotto il desktop, con 8 punti di posizione in più

| Dispositivo | Clic | Impressioni | CTR | Pos. |
|---|---|---|---|---|
| Computer | 4.435 | 572.243 | 0,78% | 21,81 |
| Mobile | 566 | 85.746 | 0,66% | 13,49 |
| Tablet | 12 | 2.232 | 0,54% | 12,57 |

Su mobile il sito è posizionato otto punti meglio e converte peggio. Non è
ranking: è lo snippet. I title delle schede materiale sono lunghissimi
(`Stainless steel Werkstoff 1.4571 AISI 316Ti UNS S31635` e simili) e su mobile
vengono troncati prima di arrivare all'informazione utile.

### Nessun dato strutturato

`Aspetto nella ricerca` contiene una sola riga: **Risultati tradotti**, 634
impressioni, 8 clic, posizione 7,6. Nessun breadcrumb, nessun risultato
prodotto, nessuna FAQ. Google non riconosce **nessun markup strutturato** sul
sito. Per un catalogo tecnico è un'anomalia, e `Product` + `BreadcrumbList`
agiscono proprio sul CTR.

I risultati tradotti dicono anche un'altra cosa: Google traduce attivamente le
pagine per utenti stranieri. Il mercato anglofono vede il sito e non lo
riconosce come pertinente.

### Pagine duplicate: 21.388 impressioni disperse

Nove gruppi di URL `/en/` con lo stesso slug e un suffisso numerico:

| Impr. totali | Clic | Gruppo | URL |
|---|---|---|---|
| 21.598 | 33 | `1.4401 / AISI 316` | `-2` (13.614, pos 15,8) + base (7.984, pos 25,5) |
| 13.717 | 161 | `1.4529 / AISI 926` | `-3` (10.176) + `-2` (3.214) + base (327) |
| 12.439 | 37 | `1.4571 / AISI 316Ti` | `-2` (10.925) + base (1.514) |
| 9.519 | 75 | `1.4841 / AISI 314` | `-2` (5.587) + base (3.931) |
| 7.847 | 32 | `904L / 1.4539` | base + `-3` + `-2` |
| 5.482 | 35 | `1.4828 / AISI 309` | base + `-2` |
| 3.167 | 18 | `1.4845 / AISI 310S` | base + `-2` |

Più i doppioni tematici, che il filtro automatico non vede:

- **Alloy 625 su tre pagine**: `/en/alloy-625-heres-why…` (15.525 impr),
  `/en/uns-n06625-the-ideal-superalloy…` (11.535 impr, 9 clic), scheda materiale
  (13.678 impr). Oltre 40.000 impressioni divise in tre, 77 clic in totale.
- **ISO 3506 su due pagine**: `/en/iso-3506/` (14.825, 110 clic, pos 13,52) e
  `/en/iso-3506-1-standards-for-male…` (3.064, 9 clic, pos 8,00).
- **Monel K500 su due pagine quasi identiche**:
  `/en/why-choose-monel-k500-for-your-fasteners/` e
  `/en/when-to-use-fixing-systems-in-monel-k500/`.
- **1.4301 su due URL con un errore nel titolo**: lo slug
  `stainless-steel-w-1-4301-aisi-304l-uns-s30400` associa 1.4301 a 304**L**.
  1.4301 è AISI 304; 304L è 1.4307. La pagina ha 29.592 impressioni e 26 clic.

Il consolidamento di questi gruppi (301 verso l'URL migliore) è l'intervento
tecnico a ritorno più alto e più rapido, e non richiede di scrivere nulla.

---

## Parte 4 — Il piano rivisto

In ordine di ritorno sullo sforzo.

**1. Pubblicare le otto bozze. In inglese.** (sforzo: traduzione + pubblicazione)
Sono scritte, sono buone, e oggi valgono zero perché nessuno le vede. La
traduzione in inglese e la pubblicazione su `/en/` è il passo che trasforma il
lavoro già fatto in qualcosa di misurabile. Italiano come versione secondaria.

**2. Consolidare i duplicati.** (sforzo: redirect, nessuna scrittura)
Nove gruppi tecnici più quattro tematici. 21.388 impressioni sugli URL
secondari, più le 40.000 di Alloy 625 divise in tre. Da fare prima di qualunque
contenuto nuovo: pubblicare su un sito che si cannibalizza significa diluire
anche il nuovo.

**3. Riscrivere title e meta description delle venti pagine a maggiore
impressione.** (sforzo: un'ora, zero sviluppo)
La lista pronta è in `docs/title-meta-da-riscrivere.md`. Priorità alle pagine
già in top 10 con intento decisionale, non ai lookup di specifica.

**4. Correggere il titolo di 1.4301.** (sforzo: cinque minuti)
29.592 impressioni su una pagina che confonde 304 e 304L.

**5. Aggiungere `Product` e `BreadcrumbList`.** (sforzo: tecnico, basso)
Zero dati strutturati riconosciuti oggi. Agisce sul CTR su tutte le 154 pagine
inglesi insieme.

**6. Due contenuti nuovi, in inglese, sui cluster non presidiati:**

| # | Titolo | Keyword | Perché |
|---|---|---|---|
| 1 | Material equivalence table: Werkstoff / EN / AISI / UNS / ASTM for corrosion-resistant fasteners | material equivalent | 54 query, 15.052 impr, pos 31, nessuna pagina hub. Cluster più grande del sito |
| 2 | ASTM A194 grades decoded: 8, 8M, 8T, 8A, 8C, 8MLCuN — which nut do you need | astm a194 8m | 32 query, 10.113 impr, pos 16,1, 17 clic. Il decoder manca |

**7. Chiudere il bug delle categorie**, per non dover più spuntare a mano.

### Cosa resta del piano vecchio

Tre titoli non ancora scritti. Dei tre, **uno va tolto**:

| Titolo | Verdetto |
|---|---|
| Infragilimento da idrogeno | tenere — adiacente al cluster NACE (5.664 impr) |
| Serraggio flange ASME PCC-1 | tenere con riserva — zero query misurate, ma intento di servizio |
| Bulloneria amagnetica | **togliere** — zero query in 16 mesi su 1.000, nessun segnale |

---

## Parte 5 — Limiti di questa analisi

- `Query.csv` è limitato a 1.000 righe dalla UI di Search Console: copre 323.148
  impressioni su ~660.000 totali, cioè il 49%. Le conclusioni sui cluster valgono
  sulla metà più visibile della domanda.
- La somma di `Pagine.csv` (714.188 impressioni) non coincide con `Grafico.csv`
  (660.221). È normale: Search Console usa pipeline diverse e anonimizza parte
  delle query. Lo scostamento è dell'8% e non cambia nessuna conclusione.
- Le due finestre di export (agosto e ottobre) non coincidono: i confronti
  mensili sono omogenei, i totali di periodo no.
- L'attribuzione dei pattern automatici a un rank tracker è un'inferenza
  fondata su struttura e frequenza, non una prova. Va verificata come scritto
  sopra.
