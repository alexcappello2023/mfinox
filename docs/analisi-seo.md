# mfinox.com — analisi SEO e piano editoriale

Periodo analizzato: **16 aprile 2025 – 15 agosto 2026** (16 mesi, export Google Search Console).
Data dell'analisi: 17 agosto 2026.

## Nota di metodo

Il confronto con i concorrenti **non** è un diff letterale dei tre file
`sitemap_index.xml`. L'ambiente di esecuzione ha la rete in uscita filtrata da
policy: `mfinox.com`, `www.pressbolt.com` e `www.extreme-bolt.com` rispondono
403 sul proxy di egress, così come qualunque altro dominio. L'unico canale
disponibile è l'indice di ricerca.

L'inventario dei contenuti è quindi stato ricostruito da due fonti:

- **mfinox**: le 352 URL presenti nell'export `Pagine.csv`, che coprono tutte le
  pagine con almeno un'impressione nei 16 mesi — di fatto un inventario completo
  del sito indicizzato, comprese le versioni `/en/`, `/es/`, `/fr/`, `/de/`.
- **concorrenti**: enumerazione tramite query `site:` sull'indice di ricerca.

Il limite da tenere presente: una pagina dei concorrenti non indicizzata o non
emersa dalle query può non essere stata rilevata. Per mfinox il rischio è nullo
sulle pagine che ricevono traffico, che sono quelle che contano per il confronto.

## 1. Il quadro quantitativo

| | Clic | Impressioni | CTR | Posizione media |
|---|---|---|---|---|
| Totale periodo | 4.864 | 635.878 | 0,76% | 24,6 |
| Primi 90 giorni | 755 | 94.162 | 0,80% | 39,5 |
| Ultimi 90 giorni | 876 | 115.031 | 0,76% | 16,8 |

### Andamento mensile

| Mese | Clic | Impressioni | CTR | Pos. |
|---|---|---|---|---|
| 2025-04 | 119 | 14.556 | 0,82% | 38,6 |
| 2025-05 | 301 | 31.676 | 0,95% | 38,8 |
| 2025-06 | 229 | 32.146 | 0,71% | 40,1 |
| 2025-07 | 233 | 33.737 | 0,69% | 40,7 |
| 2025-08 | 193 | 34.232 | 0,56% | 39,5 |
| 2025-09 | 331 | 33.749 | 0,98% | 27,7 |
| 2025-10 | 355 | 30.126 | **1,18%** | 23,8 |
| 2025-11 | 348 | 36.368 | 0,96% | 20,6 |
| 2025-12 | 276 | 44.295 | 0,62% | 20,9 |
| 2026-01 | 339 | 53.052 | 0,64% | 20,3 |
| 2026-02 | 350 | 53.227 | 0,66% | 15,8 |
| 2026-03 | **414** | 53.974 | 0,77% | 13,1 |
| 2026-04 | 326 | 42.756 | 0,76% | 13,4 |
| 2026-05 | 356 | 45.702 | 0,78% | 15,8 |
| 2026-06 | 273 | 38.365 | 0,71% | 16,8 |
| 2026-07 | 300 | 37.938 | 0,79% | 17,0 |
| 2026-08 (parziale) | 121 | 19.979 | 0,61% | 17,6 |

### Tre evidenze

**a) Il guadagno di ranking non si è tradotto in clic.** La posizione media è
passata da 39,5 a 16,8 e le impressioni sono cresciute del 22%, ma il CTR è
scivolato da 0,80% a 0,76%. Le posizioni guadagnate sono su query che non
generano clic: il sito è diventato più visibile senza diventare più cliccato.

**b) Il traffico è quasi tutto brand.** Sulle 1.000 query dell'export:

| | Clic | Impressioni | CTR |
|---|---|---|---|
| Brand (`mf inox`, `mfinox`, `mf screws`, `vimi`…) | 968 (66%) | 2.870 (0,9%) | 33,7% |
| Non brand | 497 (34%) | 322.075 (99,1%) | **0,15%** |

Il 66% dei clic arriva dallo 0,9% delle impressioni. Tutta la visibilità
informativa costruita converte allo 0,15%.

**c) 769 query su 1.000 hanno zero clic**, per 233.577 impressioni. Non è un
problema di volume: è un problema di posizione media su quelle query (spesso
oltre la 40) e di assenza di una pagina pensata per l'intento.

### Stagionalità

Due minimi ricorrenti — **agosto** (0,56% nel 2025, 0,61% nel 2026) e
**dicembre–gennaio** (0,62% / 0,64%), coerenti con le chiusure industriali. Il
massimo è **settembre–novembre** (0,98% / 1,18% / 0,96%). Un contenuto pubblicato
a metà agosto ha 4–6 settimane per essere indicizzato e maturare prima del picco.

### Geografia

L'Italia porta 1.517 clic su 81.309 impressioni (CTR 1,87%, pos. 13,9) ma è
dominata dal brand. I mercati con la visibilità maggiore e la resa peggiore:

| Paese | Clic | Impressioni | CTR | Pos. |
|---|---|---|---|---|
| Stati Uniti | 236 | 126.870 | 0,19% | 21,7 |
| Regno Unito | 256 | 70.448 | 0,36% | 29,9 |
| India | 237 | 37.254 | 0,64% | 15,8 |
| Germania | 278 | 29.950 | 0,93% | 38,1 |
| Brasile | 55 | 24.367 | 0,23% | 31,5 |

Gli Stati Uniti sono il primo mercato per impressioni con il CTR più basso in
assoluto. È il dato che giustifica il tema #7 del piano (equivalenze ISO/ASTM).

## 2. I cluster con domanda non intercettata

| Cluster | Query | Impressioni | Clic |
|---|---|---|---|
| Alloy 800 / 800H / 800HT | 32 | 24.452 | 3 |
| Monel 400 / K500 | 26 | 11.996 | 2 |
| Nitronic 60 / S21800 / alloy 218 | 32 | 10.458 | 2 |
| Nitronic 50 / XM-19 | 14 | 2.201 | 3 |
| Raccordi (caps, fondelli, riduzioni, pezzi a T) | 56 | ~31.000 | 0 |

Sull'ultima riga una precisazione: sono query di **carpenteria per tubazioni**,
non di bulloneria (`caps alloy 825`, `fondelli monel 400`, `riduzioni
concentriche alloy 800h`, `pezzi a t uns n06625`). Sono intento sbagliato e non
vanno inseguite con contenuti di blog. Restano un segnale utile: se il gruppo
tratta anche raccordi, sono ~31.000 impressioni già acquisite senza una pagina
prodotto a cui atterrare.

Le pagine che perdono più valore, tutte con impressioni alte e posizione oltre
la 25:

| Pagina | Impressioni | Clic | CTR | Pos. |
|---|---|---|---|---|
| `/en/materials/nitronic-60-a193-b8s-uns-s21800-alloy-218/` | 16.744 | 34 | 0,20% | 44,5 |
| `/en/materials/alloy-800-nickel-alloy-alloy-800h-and-alloy-800ht/` | 26.523 | 24 | 0,09% | 37,8 |
| `/en/materials/stainless-steel-w-1-4301-aisi-304l-uns-s30400/` | 29.999 | 26 | 0,09% | 14,9 |
| `/en/materials/monel-400-w-2-4360-uns-n04400/` | 19.520 | 8 | 0,04% | 53,6 |
| `/en/materials/super-duplex-a182-f53-uns-s32750-w-1-4410-saf-2507/` | 22.670 | 71 | 0,31% | 24,0 |
| `/en/materials/nimonic-80a-…-werkstoff-2-4952/` | 21.607 | 46 | 0,21% | 27,1 |

Sono schede materiale: rispondono a una query di consultazione, non a una
domanda. Un articolo che spiega *un problema* e linka la scheda intercetta un
intento diverso e le trasferisce autorità interna.

## 3. Confronto con i concorrenti

### Pressbolt (www.pressbolt.com — Turate, CO)

**Non ha un blog.** Solo pagine prodotto e specifica: ASTM A193 B7 / B7M / B16 /
B8 / B8M, A320 L7 / L7M / L43, A453 660, A182 F55 / F51, A437 B4B, X12Cr13,
AISI 904L, A182 F44, Inconel 718, Nitronic XM-19, Incoloy 925. Più `studbolts`,
`anchor bolts`, `hexagonal nuts`, `screws`, `hex plugs`, `our plant`,
`production` e una pagina **`coatings`** (zincatura a caldo, elettrolitica,
PTFE, nichelatura). Range dimensionale dichiarato 1/4"–7" (M6–M180).

Compete sulle specifiche, non sull'editoriale. Presidia due aree che mfinox non
tocca: **acciai al carbonio e legati (B7, B16, L7)** e **rivestimenti**.

### Extreme Bolt & Fastener (www.extreme-bolt.com)

È l'avversario editoriale vero: blog WordPress maturo, con tassonomia per
applicazione (`corrosion-resistance`, `high-strength`,
`high-temperature-resistance`, `non-conductive`) e per tag di materiale.

Articoli rilevati:

- *Fastener Thread Galling: What Is It & How to Prevent It?*
- *Materials Prone to Thread Galling*
- *Galling Issues with Inconel and Hastelloy*
- *Will A286 Fasteners Gall with Titanium or Stainless*
- *Inconel Bolts: Preventing Galling/Seize & Over-Torque*
- *Choosing a Non-Magnetic Fastener*
- *Nylon vs All Metal Lock Nuts*
- *Understanding Bolt Lengths*
- *A286 Cryogenic Usage*
- *Inconel vs Hastelloy for High Strength Corrosion*
- *Overview of Extreme High Strength Fasteners*
- *Military Fasteners: Materials, Specs & DFARS*
- *Nickel Alloys Part 1: Moderate Corrosion*
- *Technical Questions – FAQ's*

Il modello editoriale è per **problema applicativo** (grippaggio, amagnetismo,
criogenia, alta resistenza), non per materiale.

### L'incrocio

mfinox copre con profondità i **materiali** (oltre 60 schede) e le **norme**
(ISO 3506, EN 10269, A193, A194, A320, NACE MR0175/MR0103, Eurocode 3
EN 1993-1-4, ASTM G48/A262, classi CRC). Non copre quasi nulla dei **modi di
guasto e dei problemi di montaggio**, che è esattamente il terreno di Extreme
Bolt.

Il caso più netto è il galling. Extreme Bolt ha cinque articoli sul tema.
mfinox ha la scheda materiale del Nitronic 60 — il materiale che il problema lo
risolve — ferma in posizione 44,5 con 16.744 impressioni e 34 clic, e 10.458
impressioni di query `nitronic 60` che portano 2 clic. Domanda presente,
prodotto presente, contenuto che li collega assente.

## 4. Piano editoriale

Tutti e dieci i temi sono stati verificati contro le 352 URL di `Pagine.csv`:
nessuno duplica un contenuto esistente. Ordinamento per rapporto tra domanda
dimostrata e difendibilità.

| # | Titolo | Key | Motivazione |
|---|---|---|---|
| 1 | Galling e grippaggio dei filetti: perché il Nitronic 60 (UNS S21800) risolve un problema che il 316 non risolve | nitronic 60 | 10.458 impressioni / 2 clic; scheda materiale a pos. 44,5; gap diretto sui 5 articoli di Extreme Bolt |
| 2 | Corrosione galvanica nei sistemi di fissaggio: come gestire gli accoppiamenti bimetallici | corrosione galvanica bulloneria | scoperto da entrambi i concorrenti; trasversale a tutti i settori serviti |
| 3 | PREN: come si calcola e perché conta più della sigla AISI | pren super duplex | completa l'articolo esistente sulle classi CRC senza sovrapporsi |
| 4 | Sistemi di fissaggio amagnetici: permeabilità magnetica e scelta del materiale | bulloneria amagnetica | Extreme Bolt lo presidia, mfinox non ha nulla; aggancia Nitronic 50/60 e 316 |
| 5 | Infragilimento da idrogeno: il rischio nascosto su acciai ad alta resistenza e 17-4 PH | infragilimento da idrogeno bulloneria | estende il posizionamento NACE già acquisito |
| 6 | Alloy 800, 800H e 800HT: quale scegliere alle alte temperature | alloy 800h 800ht | 24.452 impressioni / 3 clic, il cluster più grande non intercettato |
| 7 | ISO 3506 e ASTM F593/F594: equivalenze per il mercato americano | iso 3506 astm f593 | USA = 126.870 impressioni con CTR 0,19%; già in pos. 12,3 su `iso 3506` |
| 8 | ASTM A193 B8 Classe 1 e Classe 2: incrudimento, carichi e quando serve | astm a193 b8 classe 2 | già posizionato su `a193 b8`, manca la pagina che spiega le classi |
| 9 | Serraggio delle flange secondo ASME PCC-1: sequenza, coppia e precarico | asme pcc-1 serraggio flange | terreno naturale di Pressbolt (studbolt), scoperto da entrambi |
| 10 | Antigrippanti e rivestimenti sui tiranti: effetto sul fattore K di serraggio | antigrippante fattore k | risposta diretta alla pagina `coatings` di Pressbolt |

### Raccomandazioni oltre i contenuti

1. **Le schede materiale hanno un problema di CTR, non di ranking.** `1.4301`
   è in posizione 14,9 con 29.999 impressioni e 26 clic. Prima di produrre
   altri contenuti vale la pena rivedere title tag e meta description delle
   dieci schede a più alta impressione: è l'intervento con il ritorno più
   rapido su tutto il dataset.
2. **Verificare cosa è successo tra il 12 e il 15 settembre 2025.** Le
   impressioni crollano a 255 il 13 settembre e la posizione media passa da 27,7
   a 22,9 in tre giorni. Sembra una migrazione o un cambio di proprietà GSC: se
   è una migrazione, va controllato che i redirect siano tutti a posto.
3. **Duplicati da consolidare.** Ci sono coppie di URL sullo stesso materiale
   (`…werkstoff-1-4841-aisi-314…` e `…werkstoff-1-4841-aisi-314…-2`,
   `…aisi-904l…` in tre varianti, `…1-4529-aisi-926…` in tre varianti). Si
   cannibalizzano: da unificare con canonical o redirect.
