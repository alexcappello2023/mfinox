---
titolo: "ASME PCC-1: perché una flangia progettata bene perde comunque, e cosa cambia la sequenza di serraggio"
slug: "asme-pcc-1-sequenza-serraggio-flange-bullonate"
focus_keyword: "asme pcc-1 serraggio flange"
keyword_secondarie:
  - "sequenza serraggio flangia a croce"
  - "interazione elastica bulloni flangia"
  - "passate serraggio pcc-1"
  - "stress di montaggio tiranti flangia"
  - "allineamento flange prima del serraggio"
meta_title: "ASME PCC-1: la sequenza di serraggio delle flange | MF Inox"
meta_description: "Perché serrare in croce non basta, cosa è l'interazione elastica, come si fissano le passate e lo stress di montaggio secondo ASME PCC-1."
categoria: "News"
lingua: it
stato: draft
autore_suggerito: "alberto.lupi"
riferimento_piano: 9
note_immagine: "Suggerimento per il cliente: flangia bullonata con numerazione dei tiranti visibile, oppure due operatori con chiavi dinamometriche su lati opposti della stessa flangia. Alt text proposto: \"Serraggio di una flangia bullonata secondo la sequenza ASME PCC-1\"."
note_redazione: |
  Terzo pilastro del cluster sul serraggio delle flange, insieme alla tabella
  B16.5 (bozza 8867) e al calcolo della coppia (bozza 8865). Non vale per
  volume di ricerca - zero query misurate in 16 mesi - ma come nodo tematico:
  tre pagine che si linkano fra loro su un argomento coerente si sostengono a
  vicenda meglio di tre pagine isolate.

  DA VERIFICARE dall'ufficio tecnico contro l'edizione di PCC-1 in uso:
  le lettere delle appendici citate (A per la qualificazione del personale,
  F per le sequenze alternative, O per la determinazione dello stress di
  montaggio) cambiano fra le edizioni della norma. Il contenuto e i principi
  non cambiano, i riferimenti sì: nel testo sono introdotti con "nell'edizione
  corrente" proprio per questo, ma vanno confermati prima della pubblicazione.
  Le percentuali delle passate sono quelle della sequenza legacy e sono
  stabili, ma vanno ricontrollate sulla copia della norma.
---

<!-- wp:paragraph -->
<p>Una flangia perde. Il progetto è corretto, la classe di pressione è giusta, la guarnizione è quella prescritta, i tiranti sono del grado richiesto e certificati. Non c'è nulla da rifare sulla carta, e però perde.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Nella maggior parte dei casi il difetto non sta in nessuno di quegli elementi: sta in <strong>come sono stati stretti i bulloni</strong>. È la ragione per cui ASME ha prodotto PCC-1, una linea guida che non parla di progettazione ma solo di montaggio — e che molti capitolati richiamano senza che chi serra l'abbia mai letta.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Cos'è PCC-1, e cosa non è</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Il titolo completo è <em>Guidelines for Pressure Boundary Bolted Flange Joint Assembly</em>. Tre parole vanno lette con attenzione.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li><strong>Guidelines.</strong> Non è un codice. Non impone nulla di per sé: diventa vincolante quando un capitolato o un contratto lo richiama, e allora lo è per intero.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><strong>Assembly.</strong> Riguarda il montaggio, non il dimensionamento. Il calcolo della giunzione resta ai codici di progetto.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><strong>Pressure boundary.</strong> Si applica alle giunzioni che contengono pressione, dove una perdita è un problema di sicurezza e non di manutenzione.</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>È quindi complementare ai codici, non alternativo. ASME Section VIII e, in Europa, la <strong>EN 1591-1</strong> dicono quanto carico serve; PCC-1 dice come ottenerlo davvero in cantiere. Una giunzione può essere conforme al codice di progetto e perdere, perché il codice assume un carico di montaggio che nessuno ha verificato di avere applicato.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Il problema che PCC-1 risolve: l'interazione elastica</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Questo è il punto da cui deriva tutto il resto, e quasi nessuno lo spiega.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Quando si serra un tirante, la flangia si flette localmente e la guarnizione si comprime in quel settore. Il risultato è che <strong>i tiranti già serrati si allentano</strong>: il carico che avevano si ridistribuisce. Serrare il bullone numero 5 significa togliere precarico ai numeri 1 e 3.</p>
<!-- /wp:paragraph -->

<!-- wp:quote -->
<blockquote class="wp-block-quote"><p>Si chiama <strong>interazione elastica</strong>. Su una flangia a venti tiranti, l'ultimo serrato può avere il doppio del carico del primo, pur avendo ricevuto la stessa coppia.</p></blockquote>
<!-- /wp:quote -->

<!-- wp:paragraph -->
<p>Questa è la ragione — l'unica — per cui esistono le sequenze e le passate multiple. Non sono una buona pratica da cantiere: sono la risposta a un fenomeno meccanico che non si può evitare, solo gestire. Chi fa un solo giro alla coppia finale, anche seguendo lo schema a croce, ottiene una guarnizione caricata in modo molto disuniforme, che tiene finché l'impianto non va in temperatura.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">La sequenza tradizionale: croce più passate</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>La sequenza storica, quella che PCC-1 chiama <em>legacy</em>, ha due componenti che vanno applicate insieme.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">L'ordine: lo schema a stella</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Si numerano i tiranti e si serra ogni volta quello più lontano possibile dal precedente, in modo che la deformazione si distribuisca:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li>su <strong>4 tiranti</strong>: 1 — 3 — 2 — 4;</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>su <strong>8 tiranti</strong>: 1 — 5 — 3 — 7 — 2 — 6 — 4 — 8;</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>su <strong>12 tiranti</strong>: 1 — 7 — 4 — 10 — 2 — 8 — 5 — 11 — 3 — 9 — 6 — 12.</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Il criterio è sempre lo stesso: dopo ogni serraggio si passa al diametralmente opposto, poi si avanza di una posizione. Vale per qualunque numero pari di tiranti, e le flange ASME B16.5 ne hanno sempre un numero pari — la <a href="https://mfinox.com/bulloneria-flange-asme-b16-5-numero-bulloni-lunghezza-tiranti/">tabella per misura nominale e classe</a> dice quanti.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Le passate: mai una sola</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Lo schema a stella si ripete più volte, salendo di carico:</p>
<!-- /wp:paragraph -->

<!-- wp:table -->
<figure class="wp-block-table"><table><thead><tr><th>Passata</th><th>Carico</th><th>Scopo</th></tr></thead><tbody>
<tr><td>Preliminare</td><td>a mano, serraggio al contatto</td><td>portare le facce in appoggio e verificare l'allineamento</td></tr>
<tr><td>1ª</td><td>20–30% del valore finale</td><td>assestare la guarnizione senza deformare la flangia</td></tr>
<tr><td>2ª</td><td>50–70%</td><td>portare la giunzione verso il carico di lavoro</td></tr>
<tr><td>3ª</td><td>100%</td><td>raggiungere il valore di progetto</td></tr>
<tr><td>Rotazionale</td><td>100%, in senso orario continuo</td><td>recuperare l'interazione elastica</td></tr>
</tbody></table></figure>
<!-- /wp:table -->

<!-- wp:paragraph -->
<p>L'ultima riga è quella che viene saltata più spesso ed è la più importante. La <strong>passata rotazionale</strong> non segue la stella: si gira attorno alla flangia bullone per bullone, al valore finale, e si continua finché <strong>nessun dado ruota più</strong>. Se un dado gira ancora, significa che aveva perso precarico per effetto dei vicini: finché ne gira uno, la giunzione non è completa. Possono servire due o tre giri.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Nell'edizione corrente PCC-1 propone anche <strong>sequenze alternative</strong>, pensate per ridurre il numero di passate lavorando su più tiranti contemporaneamente o cambiando l'ordine. Costano attrezzatura e coordinamento, e hanno senso su flange grandi dove le passate complete sono lunghe. Il principio non cambia: più passate a carico crescente, e un controllo finale rotazionale.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Qual è il «100%»</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Tutta la sequenza ruota attorno a un numero che va deciso prima: lo <strong>stress di montaggio</strong> dei tiranti. PCC-1 dedica un'appendice al metodo, e la logica è quella di una forbice fra due limiti.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li><strong>Il minimo</strong> lo impone la guarnizione: sotto una certa pressione di contatto non sigilla, e il valore dipende dal tipo — una spirometallica chiede molto più di una piatta in grafite.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><strong>Il massimo</strong> è il più basso fra tre: lo snervamento del tirante, la resistenza della flangia alla flessione, e il carico che schiaccerebbe la guarnizione oltre il suo limite.</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Il target si colloca dentro quella forbice, tipicamente fra il 50% e il 70% dello snervamento del tirante quando il serraggio è a coppia controllata. E qui c'è il collegamento che molti non fanno: <strong>lo snervamento non è una costante del grado.</strong> Su un A193 B8 Classe 2 cala al crescere del diametro, perché l'incrudimento a freddo non arriva al cuore delle barre grosse. Il calcolo del precarico e della coppia corrispondente, con i valori per fascia di diametro, è in <a href="https://mfinox.com/coppia-serraggio-tiranti-inox-leghe-nichel-tabella/">coppia di serraggio dei tiranti in inox e lega di nichel</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Un avvertimento che PCC-1 rende esplicito: il controllo della coppia ha una dispersione nell'ordine del <strong>±25-30%</strong> sul precarico effettivo. Significa che un target al 70% dello snervamento, con quella dispersione, può portare qualche tirante oltre il limite. È il motivo per cui si sta più bassi, o si usano metodi che misurano il risultato invece di stimarlo: tensionamento idraulico, misura dell'allungamento, serraggio ad angolo.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Prima di toccare una chiave: l'allineamento</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>PCC-1 insiste su una verifica che in cantiere viene considerata una perdita di tempo, e che invece decide l'esito: le due flange devono essere <strong>parallele, concentriche e a distanza corretta</strong> prima che si cominci a serrare.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>La regola è che il disallineamento <strong>non si corregge coi bulloni</strong>. Usare i tiranti per tirare in posizione due flange non parallele produce tre effetti insieme: una parte del precarico viene consumata per deformare la tubazione invece di caricare la guarnizione, i tiranti lavorano a flessione anziché a trazione pura, e la guarnizione riceve un carico asimmetrico che non sigilla da un lato. La perdita arriva poi, in esercizio, e viene attribuita alla guarnizione.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Il controllo è semplice: le facce devono combaciare a mano, con i tiranti inseriti e i dadi solo appoggiati. Se serve forza per far entrare i tiranti nei fori, il problema è a monte.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">La qualificazione di chi serra</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>È la parte di PCC-1 che ha cambiato più cose nella pratica industriale. Un'appendice dedicata stabilisce un quadro per la <strong>formazione e la qualificazione del personale</strong> che monta giunzioni bullonate in pressione: conoscenze richieste, prove pratiche, mantenimento della qualifica.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Il ragionamento dietro è questo: per saldare un giunto in pressione serve un saldatore qualificato, e nessuno lo discute. Una giunzione bullonata contiene la stessa pressione e fallisce più spesso, ma storicamente la monta chiunque abbia una chiave. Sempre più capitolati, soprattutto in <em>oil &amp; gas</em>, richiedono oggi personale qualificato secondo questo schema.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Cosa dipende dalla bulloneria, e non dal montatore</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>PCC-1 assume che la bulloneria sia corretta e ripetibile. Quando non lo è, la sequenza più rigorosa non recupera niente. Quattro cose stanno a monte del montaggio:</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol class="wp-block-list">
<!-- wp:list-item -->
<li><strong>Un attrito ripetibile.</strong> La coppia produce precarico attraverso il fattore K, e K dipende dalla lubrificazione. Tiranti lubrificati in modo disomogeneo danno precarichi diversi a coppia uguale, e la passata rotazionale non lo rileva: vedi <a href="https://mfinox.com/antigrippanti-rivestimenti-tiranti-fattore-k-serraggio/">antigrippanti e fattore K</a>.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><strong>Proprietà meccaniche omogenee nel lotto.</strong> Lo stesso grado e la stessa fascia di diametro, con lo stesso certificato: un tirante dello stesso lotto ma di fascia diversa ha uno snervamento diverso.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><strong>La lunghezza giusta.</strong> Un tirante corto non impegna completamente i filetti del dado e cede a un carico più basso di quello calcolato, senza che si veda da fuori.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><strong>Dadi che non grippano.</strong> Un dado che si blocca a metà della passata rotazionale interrompe la sequenza, e il problema è l'accoppiamento di materiali: <a href="https://mfinox.com/galling-grippaggio-filetti-nitronic-60-uns-s21800/">galling e grippaggio dei filetti</a>.</li>
<!-- /wp:list-item -->
</ol>
<!-- /wp:list -->

<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">In sintesi</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li>PCC-1 è una <strong>linea guida di montaggio</strong>, non un codice di progetto: vincola quando un capitolato la richiama.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>Esiste per un motivo meccanico preciso, l'<strong>interazione elastica</strong>: serrare un tirante allenta quelli già serrati.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>Schema a stella più <strong>quattro passate</strong>, e una <strong>passata rotazionale finale</strong> ripetuta finché nessun dado ruota.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>Il «100%» si calcola fra il minimo imposto dalla guarnizione e il più basso fra tre massimi.</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><strong>L'allineamento si verifica prima</strong>, e non si corregge coi bulloni.</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Forniamo tiranti e dadi per flange in pressione con certificato EN 10204 3.1, omogenei di lotto e fascia di diametro, con la lunghezza calcolata sulla configurazione reale e, su richiesta, il valore di coppia corrispondente allo stress di montaggio voluto.</p>
<!-- /wp:paragraph -->
