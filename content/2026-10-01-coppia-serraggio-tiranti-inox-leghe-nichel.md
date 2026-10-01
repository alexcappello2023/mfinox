---
titolo: "Coppia di serraggio dei tiranti in inox e lega di nichel: perché le tabelle che trovi online sono sbagliate"
slug: "coppia-serraggio-tiranti-inox-leghe-nichel-tabella"
focus_keyword: "coppia serraggio tiranti inox"
keyword_secondarie:
  - "bolt torque chart"
  - "tabella coppia serraggio a193 b8"
  - "precarico tirante calcolo"
  - "snervamento b8 classe 2 diametro"
  - "coppia serraggio acciaio inossidabile"
meta_title: "Coppia di serraggio tiranti inox: il calcolo | MF Inox"
meta_description: "Le tabelle di coppia in circolazione valgono per il B7 in acciaio legato. Su un tirante austenitico portano oltre lo snervamento: come si calcola davvero."
categoria: "News"
lingua: it
stato: draft
autore_suggerito: "alberto.lupi"
riferimento_piano: 15
note_immagine: "Suggerimento per il cliente: chiave dinamometrica in uso su un tirante di flangia, con il quadrante leggibile. Oppure tirante strumentato per misura diretta dell'allungamento. Alt text proposto: \"Serraggio a coppia controllata di un tirante in acciaio inossidabile\"."
note_redazione: |
  Intercetta il cluster 'bolt torque chart' (2.400 ricerche/mese negli USA,
  difficolta' SEO 26) ma riformulato sul pubblico giusto: la keyword generica
  porta hobbisti e meccanici, questa versione parla a chi serra flange in
  materiali speciali, che e' il cliente di MF Inox.

  I VALORI DELLA TABELLA SONO CALCOLATI, NON COPIATI: snervamento da ASTM A193
  per B8 Classe 2, area resistente del filetto UNC, precarico al 50% dello
  snervamento, fattore K = 0,16. Tutte le ipotesi sono dichiarate nel testo
  sopra la tabella, cosi' il lettore puo' rifare il conto.
  DA VERIFICARE dall'ufficio tecnico prima della pubblicazione: i valori di
  snervamento per fascia di diametro e le aree resistenti. Il metodo e'
  corretto, ma su una tabella di coppia pubblicata da un produttore serve il
  controllo di chi ha la norma in mano.

  Completa il cluster sul serraggio: galling, antigrippanti/fattore K,
  B8 Classe 1 e 2, e ora il calcolo. Quattro link interni.
---

<!-- wp:paragraph -->
<p>Cerca «tabella coppia serraggio bulloni» e trovi decine di tabelle. Sono quasi tutte corrette, e quasi tutte inapplicabili alla bulloneria che serra una flangia in acciaio inossidabile o in lega di nichel. Il motivo è che sono calcolate su <strong>ASTM A193 B7</strong>, acciaio legato bonificato, che è il materiale più diffuso e il meno simile a un austenitico.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Applicare una coppia da tabella B7 a un tirante B8 Classe 2 dello stesso diametro significa, nella maggior parte dei casi, <strong>portarlo oltre lo snervamento</strong> mentre la chiave dinamometrica segna il valore «giusto». Questo articolo spiega perché, e come si fa il calcolo corretto.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Due differenze, non una</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>La coppia non è una proprietà del bullone. È il mezzo con cui si ottiene il <strong>precarico</strong>, che è la grandezza che tiene chiusa la giunzione. La relazione è:</p>
<!-- /wp:paragraph -->

<!-- wp:quote -->
<blockquote class="wp-block-quote"><p><strong>T = K · D · F</strong><br>dove T è la coppia, K il fattore di serraggio, D il diametro nominale e F il precarico voluto.</p></blockquote>
<!-- /wp:quote -->

<!-- wp:paragraph -->
<p>Fra un B7 e un austenitico cambiano <strong>entrambi</strong> i termini che contano.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">1. Il precarico ammissibile è più basso</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Il precarico si fissa come frazione dello snervamento, e gli snervamenti non sono paragonabili:</p>
<!-- /wp:paragraph -->

<!-- wp:table -->
<figure class="wp-block-table"><table><thead><tr><th>Grado</th><th>Materiale</th><th>Snervamento minimo</th></tr></thead><tbody>
<tr><td>A193 B7</td><td>acciaio legato bonificato</td><td>724 MPa (105 ksi) fino a 2 1/2"</td></tr>
<tr><td>A193 B8 Classe 2</td><td>tipo 304 incrudito</td><td>690 MPa (100 ksi) fino a 3/4"</td></tr>
<tr><td>A193 B8 Classe 2</td><td>tipo 304 incrudito</td><td>552 MPa (80 ksi) da 3/4" a 1"</td></tr>
<tr><td>A193 B8 Classe 2</td><td>tipo 304 incrudito</td><td>448 MPa (65 ksi) da 1" a 1 1/4"</td></tr>
<tr><td>A193 B8 Classe 1</td><td>tipo 304 solubilizzato</td><td>205 MPa (30 ksi) tutti i diametri</td></tr>
</tbody></table></figure>
<!-- /wp:table -->

<!-- wp:paragraph -->
<p>Due cose salgono agli occhi. La prima: un <strong>B8 Classe 1 ha uno snervamento pari a meno di un terzo di un B7</strong>. Serrarlo con la coppia del B7 non lo porta vicino al limite: lo porta ben oltre.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>La seconda, meno conosciuta: nel <strong>B8 Classe 2 lo snervamento cala al crescere del diametro.</strong> L'incrudimento si ottiene per deformazione a freddo, e su una barra di diametro maggiore la deformazione non arriva al cuore. A 1 1/4" il vantaggio sul Classe 1 si è più che dimezzato. È il motivo per cui una tabella di coppia per austenitici deve avere una riga per fascia di diametro, e non un valore unico per grado. Il fenomeno è spiegato in <a href="https://mfinox.com/astm-a193-b8-classe-1-classe-2-incrudimento-carichi/">A193 B8 Classe 1 e Classe 2</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">2. Il fattore K è più alto e più disperso</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>K aggrega tutti gli attriti della giunzione. Su un B7 lubrificato vale tipicamente 0,15–0,18. Su un austenitico <strong>a secco</strong> sale, e soprattutto si disperde: superfici dello stesso materiale che strisciano l'una sull'altra tendono a saldarsi a freddo, con valori di K che variano da pezzo a pezzo sulla stessa flangia.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Questo è il legame con il grippaggio, che non è un problema separato: è la stessa fisica. Un filetto che gripperà allo smontaggio è un filetto il cui K al montaggio era imprevedibile. I valori tipici e l'errore più frequente — applicare un antigrippante senza ricalcolare la coppia — sono in <a href="https://mfinox.com/antigrippanti-rivestimenti-tiranti-fattore-k-serraggio/">antigrippanti e fattore K</a>, mentre la soluzione a monte, cioè l'accoppiamento che non grippa, è in <a href="https://mfinox.com/galling-grippaggio-filetti-nitronic-60-uns-s21800/">galling e grippaggio dei filetti</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">La tabella, con le ipotesi dichiarate</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Una tabella di coppia senza le sue ipotesi non è verificabile, e quindi non è utilizzabile. Queste sono le nostre:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li>grado <strong>A193 B8 Classe 2</strong>, filettatura <strong>UNC</strong>;</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>precarico fissato al <strong>50% dello snervamento minimo</strong> della fascia di diametro;</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>fattore <strong>K = 0,16</strong>, corrispondente a filetti lubrificati con antigrippante;</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>precarico calcolato sull'<strong>area resistente del filetto</strong>, non sulla sezione del gambo.</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:table -->
<figure class="wp-block-table"><table><thead><tr><th>Diametro</th><th>Area resist. (in²)</th><th>Snerv. (ksi)</th><th>Precarico al 50%</th><th>Coppia</th></tr></thead><tbody>
<tr><td>1/2-13</td><td>0,1419</td><td>100</td><td>31,6 kN</td><td>64 N·m (47 ft·lbf)</td></tr>
<tr><td>5/8-11</td><td>0,226</td><td>100</td><td>50,3 kN</td><td>128 N·m (94 ft·lbf)</td></tr>
<tr><td>3/4-10</td><td>0,334</td><td>100</td><td>74,3 kN</td><td>226 N·m (167 ft·lbf)</td></tr>
<tr><td>7/8-9</td><td>0,462</td><td>80</td><td>82,2 kN</td><td>292 N·m (216 ft·lbf)</td></tr>
<tr><td>1-8</td><td>0,606</td><td>80</td><td>107,8 kN</td><td>438 N·m (323 ft·lbf)</td></tr>
<tr><td>1 1/8-7</td><td>0,763</td><td>65</td><td>110,3 kN</td><td>504 N·m (372 ft·lbf)</td></tr>
<tr><td>1 1/4-7</td><td>0,969</td><td>65</td><td>140,1 kN</td><td>712 N·m (525 ft·lbf)</td></tr>
</tbody></table></figure>
<!-- /wp:table -->

<!-- wp:paragraph -->
<p>Il salto fra 3/4" e 7/8" merita attenzione: il precarico cresce solo del 10% mentre l'area cresce del 38%, perché nel frattempo lo snervamento è sceso da 100 a 80 ksi. Fra 1" e 1 1/8" è ancora più netto — l'area cresce del 26% e il precarico del 2%. <strong>Oltre il pollice, aumentare il diametro di un tirante austenitico incrudito rende molto poco.</strong> A quel punto conviene cambiare grado o aumentare il numero di tiranti, che è esattamente la strategia che ASME B16.5 adotta passando dalla Classe 150 alla 300: raddoppia i bulloni invece di ingrossarli. Il legame con la tabella delle flange è in <a href="https://mfinox.com/bulloneria-flange-asme-b16-5-numero-bulloni-lunghezza-tiranti/">bulloneria per flange ASME B16.5</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Come si adatta la tabella al caso reale</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>I numeri sopra valgono per le ipotesi dichiarate. Fuori da quelle, si rifà il conto — ed è un conto di due passaggi.</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol class="wp-block-list">
<!-- wp:list-item -->
<li><strong>Precarico</strong>: F = frazione scelta × snervamento minimo × area resistente. La frazione va da 0,4 a 0,7 secondo quanto si controlla il serraggio: 0,5 con una chiave dinamometrica, si può salire con il tensionamento idraulico o la misura dell'allungamento.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><strong>Coppia</strong>: T = K × D × F, con D il diametro nominale e K scelto sulla lubrificazione effettiva. Attenzione alle unità: con D in pollici e F in libbre si ottengono libbre-pollice, da dividere per 12 per avere le libbre-piede.</li>
<!-- /wp:list-item -->
</ol>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Due casi che cambiano il risultato più di quanto si pensi. Se si passa a un <strong>B8 Classe 1</strong>, lo snervamento scende a 205 MPa per tutti i diametri: la coppia crolla a circa <strong>un terzo</strong> di quella in tabella. Se si monta <strong>a secco</strong> invece che con antigrippante, K sale e la stessa coppia produce un precarico molto inferiore, con dispersione alta: è la ragione per cui conviene lubrificare e ricalcolare, non lasciare a secco e sperare.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Il limite del metodo, detto chiaramente</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Il controllo della coppia è il metodo meno preciso fra quelli disponibili. Su una giunzione serrata a chiave dinamometrica la dispersione del precarico effettivo è nell'ordine del <strong>±25-30%</strong>, e su un austenitico a secco può essere peggiore. Non è un difetto della formula: è che il 90% della coppia applicata viene consumato dagli attriti, e l'attrito non si misura, si stima.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Dove la tenuta è critica — una flangia in servizio <em>sour</em>, una giunzione criogenica, uno scambiatore ad alta pressione — si usano metodi che misurano direttamente il risultato: <strong>tensionamento idraulico</strong>, controllo dell'<strong>allungamento</strong> del tirante, o <strong>serraggio ad angolo</strong> oltre il punto di contatto. Costano più tempo e danno una dispersione di qualche punto percentuale invece di trenta.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">In sintesi</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li>Le tabelle di coppia in circolazione sono per <strong>B7</strong>: su un austenitico portano oltre lo snervamento.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>Nel <strong>B8 Classe 2 lo snervamento scende col diametro</strong>: serve una riga per fascia, non un valore per grado.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>Un <strong>B8 Classe 1</strong> vuole circa un terzo della coppia di un Classe 2 di pari diametro.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><strong>Cambiare lubrificazione è cambiare il calcolo</strong>, non un dettaglio di montaggio.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>Una tabella senza le sue ipotesi dichiarate non è verificabile: <strong>chiedile sempre</strong>.</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Su richiesta forniamo il calcolo del precarico e della coppia per la configurazione specifica — grado, diametro, lubrificazione e metodo di serraggio — insieme alla bulloneria e al certificato EN 10204 3.1.</p>
<!-- /wp:paragraph -->
