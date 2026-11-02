"""Controlla il markup Gutenberg e l'HTML di un articolo. Esce 1 se trova errori."""
import re, sys, html.parser

APERTURA = re.compile(r'<!--\s*wp:([a-z0-9-]+(?:/[a-z0-9-]+)?)(\s|\{|-->)')
CHIUSURA = re.compile(r'<!--\s*/wp:([a-z0-9-]+(?:/[a-z0-9-]+)?)\s*-->')
AUTOCHIUSO = re.compile(r'<!--\s*wp:[a-z0-9-]+(?:/[a-z0-9-]+)?\s*(\{.*?\})?\s*/-->')
VUOTI = {"br", "img", "hr", "input", "meta", "link", "source", "col"}

class Bilancia(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pila, self.errori = [], []
    def handle_starttag(self, tag, attrs):
        if tag not in VUOTI:
            self.pila.append((tag, self.getpos()[0]))
    def handle_endtag(self, tag):
        if tag in VUOTI:
            return
        if not self.pila:
            self.errori.append(f"riga {self.getpos()[0]}: </{tag}> senza apertura")
        elif self.pila[-1][0] != tag:
            atteso, r = self.pila[-1]
            self.errori.append(f"riga {self.getpos()[0]}: </{tag}> ma era aperto <{atteso}> (riga {r})")
            self.pila.pop()
        else:
            self.pila.pop()

def controlla(percorso):
    testo = open(percorso, encoding="utf-8").read()
    problemi = []

    # 1. front matter presente e campi obbligatori
    if not testo.startswith("---\n"):
        problemi.append("front matter assente")
        corpo = testo
    else:
        _, fm, corpo = testo.split("---", 2)
        for campo in ("titolo", "slug", "focus_keyword", "meta_title",
                      "meta_description", "categoria", "stato"):
            if not re.search(rf'^{campo}:', fm, re.M):
                problemi.append(f"front matter: manca «{campo}»")
        mt = re.search(r'^meta_title:\s*"(.*)"', fm, re.M)
        md = re.search(r'^meta_description:\s*"(.*)"', fm, re.M)
        if mt and len(mt.group(1)) > 60:
            problemi.append(f"meta_title di {len(mt.group(1))} caratteri (max 60)")
        if md and len(md.group(1)) > 160:
            problemi.append(f"meta_description di {len(md.group(1))} caratteri (max 160)")

    # 2. blocchi Gutenberg bilanciati, nell'ordine giusto
    pila = []
    for n, riga in enumerate(corpo.splitlines(), 1):
        if AUTOCHIUSO.search(riga):
            continue
        for m in APERTURA.finditer(riga):
            pila.append((m.group(1), n))
        for m in CHIUSURA.finditer(riga):
            nome = m.group(1)
            if not pila:
                problemi.append(f"riga {n}: chiusura /wp:{nome} senza apertura")
            elif pila[-1][0] != nome:
                atteso, r = pila.pop()
                problemi.append(f"riga {n}: chiusura /wp:{nome} ma era aperto wp:{atteso} (riga {r})")
            else:
                pila.pop()
    for nome, n in pila:
        problemi.append(f"riga {n}: blocco wp:{nome} mai chiuso")

    # 3. HTML bilanciato
    b = Bilancia()
    b.feed(corpo)
    problemi += b.errori
    problemi += [f"riga {r}: <{t}> mai chiuso" for t, r in b.pila]

    # 4. link interni: devono essere relativi e terminare con /
    for m in re.finditer(r'href="([^"]+)"', corpo):
        u = m.group(1)
        interno = u.startswith("/") or "mfinox.com" in u
        if interno and not u.endswith("/") and "#" not in u and "?" not in u:
            problemi.append(f"link interno senza slash finale: {u}")
        if u.startswith("/"):
            problemi.append(f"link interno relativo: {u} (la convenzione del progetto e' assoluta)")

    # 5. residui di segnaposto
    for sospetto in ("placeholder", "TODO", "XXX", "LOREM", "FIXME"):
        if re.search(rf'\b{sospetto}\b', corpo, re.I):
            problemi.append(f"residuo sospetto nel testo: «{sospetto}»")
    if "<!-- wp:list>" in corpo:
        problemi.append("blocco malformato: «<!-- wp:list>»")

    # 6. nel corpo l'unico commento ammesso e' un delimitatore di blocco wp
    for n, riga in enumerate(corpo.splitlines(), 1):
        for m in re.finditer(r'<!--(.*?)-->', riga, re.S):
            c = m.group(1).strip()
            if not re.match(r'^/?wp:[a-z0-9-]+(/[a-z0-9-]+)?', c):
                problemi.append(f"riga {n}: commento non valido «<!-- {c[:50]} -->»")

    return problemi

esito = 0
for percorso in sys.argv[1:]:
    p = controlla(percorso)
    nome = percorso.split("/")[-1]
    if p:
        esito = 1
        print(f"\n✗ {nome}")
        for x in p:
            print(f"    {x}")
    else:
        print(f"✓ {nome}")
sys.exit(esito)
