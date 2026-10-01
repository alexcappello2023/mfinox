<?php
/**
 * Plugin Name: MF Inox — performance degli asset
 * Description: Inventario degli script caricati, rimozione di quelli non necessari e defer dei non critici. Parte in sola lettura.
 * Version:     1.0.0
 * Author:      MF Inox
 *
 * PageSpeed misura 1,18 MB di JavaScript caricato e mai eseguito, pari a 10,8 s
 * su mobile e 1,2 s su desktop. Questo file serve a eliminarlo, in tre tempi.
 *
 * MODALITÀ — si imposta in wp-config.php, prima della riga «That's all»:
 *
 *   define( 'MFINOX_PERF_MODE', 'report' );   // default: NON cambia niente
 *   define( 'MFINOX_PERF_MODE', 'dry' );      // scrive nel log cosa rimuoverebbe
 *   define( 'MFINOX_PERF_MODE', 'on' );       // applica le regole
 *
 * Senza la costante la modalità è 'report': installare il file non cambia
 * nulla di quello che il visitatore vede. È voluto.
 *
 * COME SI USA
 *
 *   1. Installa in wp-content/mu-plugins/ e lascia la modalità 'report'.
 *   2. Da amministratore, apri una pagina qualsiasi aggiungendo ?mfinox_assets=1
 *      all'URL. In fondo alla pagina compare la tabella di tutti gli script e
 *      fogli di stile caricati, con handle, peso e dipendenze.
 *      Fallo su tre pagine diverse: la home, una scheda materiale, un articolo.
 *   3. Manda le tre tabelle: da quelle si scrivono le regole specifiche del
 *      sito, che oggi non si possono indovinare.
 *   4. Passa a 'dry', controlla il log, poi a 'on'.
 *
 * INTERRUTTORE D'EMERGENZA: un amministratore può disattivare le regole per una
 * singola richiesta con ?mfinox_perf=off. Per spegnere tutto, cancella il file.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! defined( 'MFINOX_PERF_MODE' ) ) {
	define( 'MFINOX_PERF_MODE', 'report' );
}

/**
 * Modalità effettiva per questa richiesta.
 */
function mfinox_perf_modalita() {
	if ( isset( $_GET['mfinox_perf'] ) && 'off' === $_GET['mfinox_perf'] && current_user_can( 'manage_options' ) ) {
		return 'report';
	}
	$modalita = MFINOX_PERF_MODE;
	return in_array( $modalita, array( 'report', 'dry', 'on' ), true ) ? $modalita : 'report';
}

/**
 * Le regole non si applicano mai dove romperebbero qualcosa.
 */
function mfinox_perf_contesto_escluso() {
	if ( is_admin() || is_customize_preview() ) {
		return true;
	}
	if ( defined( 'DOING_AJAX' ) && DOING_AJAX ) {
		return true;
	}
	if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
		return true;
	}
	// In anteprima serve tutto quello che il tema usa.
	if ( is_preview() ) {
		return true;
	}
	return false;
}

/* =========================================================================
 * 1. INVENTARIO — sola lettura, visibile solo a un amministratore
 * ====================================================================== */

/**
 * Peso in byte di un asset, se il file sta su questo server.
 *
 * @return int|null Byte, oppure null se il file è esterno o non trovato.
 */
function mfinox_perf_peso( $src ) {
	if ( ! $src ) {
		return null;
	}
	$src = strtok( $src, '?' );
	$base_url = site_url();
	$contenuti_url = content_url();

	if ( 0 === strpos( $src, $contenuti_url ) ) {
		$percorso = WP_CONTENT_DIR . substr( $src, strlen( $contenuti_url ) );
	} elseif ( 0 === strpos( $src, $base_url ) ) {
		$percorso = ABSPATH . ltrim( substr( $src, strlen( $base_url ) ), '/' );
	} elseif ( 0 === strpos( $src, '/' ) ) {
		$percorso = ABSPATH . ltrim( $src, '/' );
	} else {
		return null; // asset su un altro dominio
	}

	$percorso = wp_normalize_path( $percorso );
	if ( ! file_exists( $percorso ) || ! is_readable( $percorso ) ) {
		return null;
	}
	$byte = filesize( $percorso );
	return false === $byte ? null : (int) $byte;
}

function mfinox_perf_formato_peso( $byte ) {
	if ( null === $byte ) {
		return 'esterno';
	}
	if ( $byte < 1024 ) {
		return $byte . ' B';
	}
	return number_format_i18n( $byte / 1024, 1 ) . ' KB';
}

/**
 * Raccoglie l'inventario di una coda (script o stili).
 */
function mfinox_perf_inventario( $coda ) {
	$righe = array();
	$totale = 0;

	foreach ( (array) $coda->done as $handle ) {
		if ( ! isset( $coda->registered[ $handle ] ) ) {
			continue;
		}
		$oggetto = $coda->registered[ $handle ];
		$src = $oggetto->src;
		if ( is_string( $src ) && '' !== $src && 0 === strpos( $src, '/' ) && 0 !== strpos( $src, '//' ) ) {
			$src = site_url( $src );
		}
		$peso = mfinox_perf_peso( is_string( $src ) ? $src : '' );
		if ( null !== $peso ) {
			$totale += $peso;
		}
		// Uno script con codice inline aggiunto non si può rinviare senza
		// rinviare anche l'inline: va segnalato.
		$inline = (bool) ( $coda->get_data( $handle, 'after' ) || $coda->get_data( $handle, 'before' ) );

		$righe[] = array(
			'handle' => $handle,
			'src'    => is_string( $src ) ? $src : '(inline / senza file)',
			'peso'   => $peso,
			'deps'   => implode( ', ', (array) $oggetto->deps ),
			'inline' => $inline,
		);
	}

	usort(
		$righe,
		function ( $a, $b ) {
			return (int) $b['peso'] <=> (int) $a['peso'];
		}
	);

	return array( 'righe' => $righe, 'totale' => $totale );
}

add_action(
	'wp_footer',
	function () {
		if ( empty( $_GET['mfinox_assets'] ) || ! current_user_can( 'manage_options' ) ) {
			return;
		}

		$script = mfinox_perf_inventario( wp_scripts() );
		$stili  = mfinox_perf_inventario( wp_styles() );

		echo '<div style="all:initial;display:block;font:13px/1.5 ui-monospace,monospace;background:#fff;color:#111;padding:24px;margin:24px;border:2px solid #111">';
		echo '<h2 style="font:700 16px/1.3 sans-serif;margin:0 0 4px">Inventario asset — MF Inox</h2>';
		printf(
			'<p style="margin:0 0 16px">URL: <code>%s</code><br>Modalità: <strong>%s</strong></p>',
			esc_html( add_query_arg( array() ) ),
			esc_html( mfinox_perf_modalita() )
		);

		foreach ( array( 'JAVASCRIPT' => $script, 'CSS' => $stili ) as $etichetta => $dati ) {
			printf(
				'<h3 style="font:700 14px/1.3 sans-serif;margin:16px 0 6px">%s — %d file, %s in totale</h3>',
				esc_html( $etichetta ),
				count( $dati['righe'] ),
				esc_html( mfinox_perf_formato_peso( $dati['totale'] ) )
			);
			echo '<table style="border-collapse:collapse;width:100%;font:12px/1.4 ui-monospace,monospace">';
			echo '<tr style="text-align:left;border-bottom:1px solid #111">'
				. '<th style="padding:4px 8px">handle</th>'
				. '<th style="padding:4px 8px">peso</th>'
				. '<th style="padding:4px 8px">inline</th>'
				. '<th style="padding:4px 8px">dipende da</th>'
				. '<th style="padding:4px 8px">file</th></tr>';
			foreach ( $dati['righe'] as $r ) {
				printf(
					'<tr style="border-bottom:1px solid #ddd">'
					. '<td style="padding:4px 8px"><strong>%s</strong></td>'
					. '<td style="padding:4px 8px;white-space:nowrap">%s</td>'
					. '<td style="padding:4px 8px">%s</td>'
					. '<td style="padding:4px 8px">%s</td>'
					. '<td style="padding:4px 8px;word-break:break-all">%s</td></tr>',
					esc_html( $r['handle'] ),
					esc_html( mfinox_perf_formato_peso( $r['peso'] ) ),
					$r['inline'] ? 'sì' : '',
					esc_html( $r['deps'] ),
					esc_html( str_replace( site_url(), '', $r['src'] ) )
				);
			}
			echo '</table>';
		}

		echo '<p style="margin:16px 0 0">Copia questa tabella e mandala: da qui si scrivono le regole specifiche del sito.</p>';
		echo '</div>';
	},
	9999
);

/* =========================================================================
 * 2. REGOLE DI RIMOZIONE
 * ====================================================================== */

/**
 * Le regole: handle => callable che restituisce true se l'asset SERVE.
 *
 * Tutto ciò che non è elencato qui non viene toccato: la rimozione è una
 * scelta esplicita, non un default.
 *
 * Qui dentro ci sono solo gli sfridi che su qualunque installazione WordPress
 * si possono togliere senza conseguenze. Le regole sui plugin specifici del
 * sito si aggiungono con il filtro 'mfinox_perf_regole' dopo aver guardato
 * l'inventario — indovinarle a priori significherebbe rompere qualcosa.
 */
function mfinox_perf_regole() {
	$regole = array(
		// oEmbed: serve solo se qualcuno incorpora QUESTO sito altrove.
		'wp-embed' => '__return_false',

		// jQuery Migrate: ponte per codice jQuery anteriore al 2016. Se il
		// tema è recente non serve. Da verificare in 'dry' prima di 'on'.
		'jquery-migrate' => '__return_false',
	);

	/**
	 * Regole aggiuntive, da compilare con i dati dell'inventario.
	 *
	 * Esempio — Contact Form 7 solo dove c'è davvero un modulo:
	 *
	 *   add_filter( 'mfinox_perf_regole', function ( $regole ) {
	 *       $serve_modulo = function () {
	 *           $post = get_post();
	 *           return $post && (
	 *               has_shortcode( $post->post_content, 'contact-form-7' )
	 *               || has_block( 'contact-form-7/contact-form-selector', $post )
	 *           );
	 *       };
	 *       $regole['contact-form-7'] = $serve_modulo;
	 *       $regole['swv']            = $serve_modulo;
	 *       return $regole;
	 *   } );
	 */
	return apply_filters( 'mfinox_perf_regole', $regole );
}

add_action(
	'wp_enqueue_scripts',
	function () {
		$modalita = mfinox_perf_modalita();
		if ( 'report' === $modalita || mfinox_perf_contesto_escluso() ) {
			return;
		}

		$rimossi = array();

		foreach ( mfinox_perf_regole() as $handle => $serve ) {
			if ( ! is_callable( $serve ) ) {
				continue;
			}
			if ( call_user_func( $serve ) ) {
				continue; // l'asset serve su questa pagina
			}
			$presente = wp_script_is( $handle, 'enqueued' ) || wp_script_is( $handle, 'registered' )
				|| wp_style_is( $handle, 'enqueued' ) || wp_style_is( $handle, 'registered' );
			if ( ! $presente ) {
				continue;
			}
			$rimossi[] = $handle;
			if ( 'on' === $modalita ) {
				wp_dequeue_script( $handle );
				wp_deregister_script( $handle );
				wp_dequeue_style( $handle );
				wp_deregister_style( $handle );
			}
		}

		if ( $rimossi && 'dry' === $modalita ) {
			error_log(
				sprintf(
					'[mfinox-perf] PROVA A VUOTO su %s — rimuoverei: %s',
					add_query_arg( array() ),
					implode( ', ', $rimossi )
				)
			);
		}
	},
	999
);

/**
 * Script degli emoji: WordPress li stampa fuori dalla coda, quindi si tolgono
 * staccando le azioni.
 */
add_action(
	'init',
	function () {
		if ( 'on' !== mfinox_perf_modalita() || mfinox_perf_contesto_escluso() ) {
			return;
		}
		remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
		remove_action( 'wp_print_styles', 'print_emoji_styles' );
		remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
		remove_action( 'admin_print_styles', 'print_emoji_styles' );
		add_filter( 'emoji_svg_url', '__return_false' );
	}
);

/* =========================================================================
 * 3. DEFER DEI NON CRITICI
 * ====================================================================== */

/**
 * Handle che NON si rinviano.
 *
 * jquery-core sta qui perché temi e plugin stampano codice inline che usa $
 * subito dopo averlo caricato: rinviarlo rompe la pagina.
 */
function mfinox_perf_mai_differiti() {
	return apply_filters(
		'mfinox_perf_mai_differiti',
		array( 'jquery', 'jquery-core', 'jquery-migrate' )
	);
}

add_filter(
	'script_loader_tag',
	function ( $tag, $handle ) {
		if ( 'on' !== mfinox_perf_modalita() || mfinox_perf_contesto_escluso() ) {
			return $tag;
		}
		if ( in_array( $handle, mfinox_perf_mai_differiti(), true ) ) {
			return $tag;
		}
		// Già differito o asincrono, oppure è un modulo: non toccare.
		if ( false !== strpos( $tag, ' defer' ) || false !== strpos( $tag, ' async' )
			|| false !== strpos( $tag, 'type="module"' ) ) {
			return $tag;
		}
		// Uno script con inline attaccato non si rinvia: l'inline girerebbe
		// prima della libreria da cui dipende.
		$coda = wp_scripts();
		if ( $coda->get_data( $handle, 'after' ) || $coda->get_data( $handle, 'before' ) ) {
			return $tag;
		}
		return str_replace( ' src=', ' defer src=', $tag );
	},
	10,
	2
);
