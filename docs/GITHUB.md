# Configurare GitHub — percorso completo

Guida operativa dal repository vuoto alla prima bozza pubblicata.
Tempo realistico: 15 minuti, di cui 10 per il service account Google (opzionale).

Le tre trappole che bloccano tutti, in ordine di frequenza:

1. **`workflow_dispatch` compare solo se il file del workflow è sul branch
   predefinito.** Se i workflow restano su un branch di lavoro, il pulsante
   *Run workflow* non appare e sembra che l'automazione non funzioni.
2. **Le GitHub App non possono scrivere in `.github/workflows/`** senza il
   permesso *Workflows*, che è separato da quello sui contenuti. I file dei
   workflow conviene caricarli una volta a mano.
3. **Actions va abilitato** sui repository nuovi, e il criterio restrittivo
   sulle action di terze parti blocca `actions/checkout` se non si consente
   almeno quelle create da GitHub.

---

## Passo 1 — Portare i file su GitHub

Il repository è vuoto: nessun branch, nessun commit. Il modo più rapido è
partire dal bundle git allegato, che contiene già i commit fatti.

```bash
# Nella cartella dove hai scaricato mfinox-repo.bundle
git clone mfinox-repo.bundle mfinox
cd mfinox

git remote remove origin
git remote add origin https://github.com/alexcappello2023/mfinox.git

# Branch di lavoro
git push -u origin claude/mfinox-seo-content-analysis-fv1x9h

# Stesso contenuto anche su main: è ciò che rende visibili i workflow
git push origin claude/mfinox-seo-content-analysis-fv1x9h:main
```

In alternativa, partendo dallo zip:

```bash
unzip mfinox-seo-contenuti.zip -d mfinox && cd mfinox
git init -b main
git add -A
git commit -m "Analisi SEO, piano editoriale e automazione bozze WordPress"
git remote add origin https://github.com/alexcappello2023/mfinox.git
git push -u origin main
```

Verifica su GitHub: `Settings` → `General` → `Default branch` deve indicare
**main**. Se indica altro, cambialo qui.

## Passo 2 — Abilitare Actions

`Settings` → `Actions` → `General`:

- **Actions permissions**: `Allow all actions and reusable workflows`.
  Se preferisci il criterio restrittivo, scegli l'opzione che consente le tue
  action e **spunta `Allow actions created by GitHub`**: i workflow usano solo
  `actions/checkout` e `actions/setup-python`, entrambe di GitHub.
- **Workflow permissions**: lascia `Read repository contents and packages permissions`.
  I workflow non scrivono nel repository, quindi il permesso di scrittura non
  serve. Non concederlo.

Salva. Nella scheda `Actions` devono comparire due workflow:
*Pubblica bozza su WordPress* e *Piano editoriale (Google Sheet)*.

Se non compaiono, il problema è quasi sempre il Passo 1: i file non sono sul
branch predefinito.

## Passo 3 — Secrets

`Settings` → `Secrets and variables` → `Actions` → scheda **Secrets** →
`New repository secret`.

| Nome | Valore |
|---|---|
| `WP_USER` | `alberto.lupi` |
| `WP_APP_PASSWORD` | la application password **rigenerata** |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | contenuto integrale del JSON (solo per il foglio) |

Rigenera l'application password prima di inserirla: in WordPress
`Utenti` → profilo → `Application Passwords`, revoca la precedente e creane una
nuova chiamata `github-actions`. Gli spazi che WordPress mostra sono decorativi,
lo script li rimuove: incolla il valore così come lo vedi.

## Passo 4 — Variables

Stessa pagina, scheda **Variables** → `New repository variable`.

| Nome | Valore |
|---|---|
| `WP_BASE_URL` | `https://mfinox.com` |
| `SHEET_ID` | `1zuea9Uglp9JqQuGekrNwpMm0NE4nxX57F7h1wm9n2CE` |

Su `WP_BASE_URL` conta la forma canonica del dominio: se il sito risponde su
`www`, mettilo, altrimenti il redirect fa perdere l'autenticazione e si ottiene
un 401 che sembra un problema di password.

## Passo 5 — Prima esecuzione

`Actions` → *Pubblica bozza su WordPress* → `Run workflow`:

1. Prima volta con **`dry_run` = true**. Non tocca né il sito né il foglio:
   verifica solo che il file si legga e le dipendenze si installino.
2. Poi con **`dry_run` = false**. La bozza compare in WordPress sotto
   `Articoli` → `Bozze`, e il riepilogo dell'esecuzione contiene l'ID
   dell'articolo, il link di modifica e i tre campi per Yoast.

## Passo 6 — Popolare il foglio (opzionale)

Solo se hai configurato `GOOGLE_SERVICE_ACCOUNT_JSON`:
`Actions` → *Piano editoriale* → `semina`. Aggiunge i dieci titoli in stato
`DA FARE` senza duplicare quelli già presenti.

Senza service account, importa `data/piano-editoriale.csv` nel foglio a mano.
Il resto dell'automazione funziona comunque: al posto dell'aggiornamento
automatico, il workflow segnala che lo stato va messo a mano.

---

## Se vuoi che Claude possa fare push da sé

Oggi la sessione ha accesso in **sola lettura**: sia `git push` sia le API
rispondono `403 Resource not accessible by integration`. Per abilitare la
scrittura serve concedere il permesso alla GitHub App di Claude sul repository,
dalle impostazioni GitHub di Claude (https://claude.ai/admin-settings/claude-in-slack)
o dalla pagina di installazione della app.

Anche dopo, i file sotto `.github/workflows/` restano un caso a parte: servono
i permessi *Workflows*. Per questo il Passo 1 li fa caricare a te una volta
sola — dopodiché Claude può aggiornare articoli, script e documentazione senza
toccare i workflow.

## Diagnosi rapida degli errori

| Sintomo | Causa |
|---|---|
| Il pulsante *Run workflow* non c'è | Workflow non presenti sul branch predefinito (Passo 1) |
| `401 non autorizzato` | Password non rigenerata, o `WP_BASE_URL` con `www` sbagliato |
| `403 vietato` | L'utente non ha i permessi per creare articoli, oppure un WAF filtra la richiesta |
| `404` sull'endpoint | REST API disattivate da un plugin di sicurezza, o URL base errato |
| Foglio non aggiornato | Manca la condivisione del foglio con l'email del service account |
| `Resource not accessible by integration` | Permessi della GitHub App (vedi sezione sopra) |
