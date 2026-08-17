# Configurazione

Da fare una volta sola. Dopo, ogni articolo si pubblica lanciando un workflow.

## 1. Secrets del repository

`Settings` → `Secrets and variables` → `Actions` → scheda **Secrets** → `New repository secret`.

| Nome | Valore | Obbligatorio |
|---|---|---|
| `WP_USER` | `alberto.lupi` | sì |
| `WP_APP_PASSWORD` | l'application password di WordPress | sì |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | contenuto integrale del file JSON del service account | solo per l'aggiornamento automatico del foglio |

> **Rigenera l'application password.** Quella usata in fase di analisi è transitata
> in una conversazione, quindi va considerata compromessa. In WordPress:
> `Utenti` → il proprio profilo → `Application Passwords` → revoca la vecchia,
> creane una nuova con nome `github-actions`, e incolla solo quella nel secret.
> Gli spazi mostrati da WordPress sono decorativi: lo script li rimuove da sé,
> puoi incollare il valore così come lo vedi.

## 2. Variables del repository

Stessa pagina, scheda **Variables** → `New repository variable`.

| Nome | Valore |
|---|---|
| `WP_BASE_URL` | `https://mfinox.com` (aggiungi `www` solo se è il dominio canonico) |
| `SHEET_ID` | `1zuea9Uglp9JqQuGekrNwpMm0NE4nxX57F7h1wm9n2CE` |

## 3. Service account Google (per il foglio)

Serve solo se vuoi che lo stato passi da `DA FARE` a `INSERITO` da sé. Senza
questo, tutto il resto funziona e lo stato lo aggiorni a mano.

1. Su [console.cloud.google.com](https://console.cloud.google.com) crea o seleziona un progetto.
2. `API e servizi` → `Libreria` → abilita **Google Sheets API**.
3. `IAM e amministrazione` → `Account di servizio` → `Crea account di servizio`.
4. Aprilo → `Chiavi` → `Aggiungi chiave` → `Crea nuova chiave` → **JSON**.
5. Copia **tutto** il contenuto del JSON scaricato nel secret `GOOGLE_SERVICE_ACCOUNT_JSON`.
6. Nel JSON trovi il campo `client_email` (del tipo `nome@progetto.iam.gserviceaccount.com`).
   Apri il Google Sheet, `Condividi`, e dai a quell'indirizzo il permesso di **Editor**.

Il passaggio 6 è quello che viene dimenticato più spesso: senza la condivisione
il service account riceve un errore di permessi anche con le credenziali corrette.

## 4. Verifica

`Actions` → **Pubblica bozza su WordPress** → `Run workflow`, lasciando
`dry_run` su `true`. Non tocca né il sito né il foglio: valida solo che il file
si legga e che le dipendenze si installino.

Poi rilancia con `dry_run` su `false`: la bozza compare in WordPress sotto
`Articoli` → `Bozze`, e il riepilogo dell'esecuzione contiene i tre campi da
incollare in Yoast SEO.

## Perché i campi Yoast non si compilano da soli

Yoast registra `_yoast_wpseo_title` e `_yoast_wpseo_metadesc` come post meta
non esposti alle REST API. Renderli scrivibili richiede una `register_post_meta`
in un plugin o nel `functions.php` del tema — una modifica al sito che va
decisa dal cliente, non introdotta di nascosto da un'automazione. Finché non
c'è, lo script stampa titolo SEO, meta description e focus keyword nel riepilogo
del workflow, da incollare in fase di revisione.

Se il cliente vuole automatizzarlo, il frammento è questo:

```php
// functions.php del tema child, oppure plugin dedicato
add_action( 'init', function () {
    foreach ( [ '_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw' ] as $chiave ) {
        register_post_meta( 'post', $chiave, [
            'show_in_rest'  => true,
            'single'        => true,
            'type'          => 'string',
            'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
        ] );
    }
} );
```

Con quel frammento attivo si può estendere `publish_to_wordpress.py` per
inviare anche il dizionario `meta`.

## Pubblicare l'articolo successivo

1. Scrivi il file in `content/`, con `titolo` nel front matter **identico** alla
   riga del foglio (è la chiave con cui lo script trova la riga da aggiornare).
2. Commit e push.
3. `Actions` → `Pubblica bozza su WordPress` → `Run workflow`, indicando il percorso del file.

Lo stato passa a `INSERITO` solo dopo che WordPress ha confermato la creazione
della bozza, quindi il foglio non può dire `INSERITO` per un articolo che non
esiste.
