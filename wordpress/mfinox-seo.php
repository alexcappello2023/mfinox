<?php
/**
 * Plugin Name: MF Inox — SEO helper
 * Description: Espone i campi Yoast alle REST API e stampa il markup BreadcrumbList. Nessuna modifica visibile in pagina.
 * Version:     1.0.0
 * Author:      MF Inox
 *
 * Installazione: copiare questo file in wp-content/mu-plugins/ (si attiva da
 * solo, non compare fra i plugin disattivabili), oppure in
 * wp-content/plugins/mfinox-seo/mfinox-seo.php e attivarlo dalla bacheca.
 *
 * Fa due cose indipendenti:
 *
 *  1. register_post_meta sui campi Yoast, su TUTTI i tipi di contenuto
 *     pubblici. Serve perché l'automazione possa scrivere title SEO e meta
 *     description via REST API: senza questo WordPress risponde 200 e scarta
 *     i valori. Non cambia nulla per chi lavora dalla bacheca.
 *
 *  2. BreadcrumbList in JSON-LD sulle pagine singole. È il markup che in SERP
 *     trasforma la riga dell'URL da
 *       mfinox.com/en/materials/stainless-steel-w-1-4529-aisi-926-uns-n08926-3/
 *     in
 *       mfinox.com › Materials › 1.4529 AISI 926
 *     Non influisce sul posizionamento: agisce sul CTR.
 *     Se i breadcrumb di Yoast sono già attivi questa parte si disattiva da
 *     sola, per non stampare due volte lo stesso markup.
 *
 * NOTA sul markup Product: deliberatamente non incluso. Google mostra un
 * risultato arricchito di prodotto solo se il markup contiene prezzo,
 * disponibilità o recensioni. Il sito non espone nessuno dei tre, quindi il
 * markup verrebbe letto e ignorato. Da aggiungere solo quando ci sarà almeno
 * la disponibilità.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/* -------------------------------------------------------------------------
 * 1. Campi Yoast scrivibili via REST API
 * ---------------------------------------------------------------------- */

add_action(
	'init',
	function () {
		$chiavi = array(
			'_yoast_wpseo_title',
			'_yoast_wpseo_metadesc',
			'_yoast_wpseo_focuskw',
		);

		$tipi = get_post_types( array( 'public' => true ), 'names' );

		foreach ( $tipi as $tipo ) {
			if ( 'attachment' === $tipo ) {
				continue;
			}
			foreach ( $chiavi as $chiave ) {
				register_post_meta(
					$tipo,
					$chiave,
					array(
						'show_in_rest'  => true,
						'single'        => true,
						'type'          => 'string',
						'default'       => '',
						'auth_callback' => function () {
							// Solo chi può già modificare i contenuti dalla bacheca.
							return current_user_can( 'edit_posts' );
						},
					)
				);
			}
		}
	},
	20 // dopo la registrazione dei custom post type del tema
);

/* -------------------------------------------------------------------------
 * 2. BreadcrumbList in JSON-LD
 * ---------------------------------------------------------------------- */

/**
 * I breadcrumb di Yoast sono già attivi?
 *
 * In quel caso Yoast stampa il proprio BreadcrumbList e il nostro sarebbe un
 * duplicato.
 */
function mfinox_yoast_breadcrumb_attivi() {
	if ( ! function_exists( 'YoastSEO' ) && ! class_exists( 'WPSEO_Options' ) ) {
		return false;
	}
	if ( class_exists( 'WPSEO_Options' ) ) {
		return (bool) WPSEO_Options::get( 'breadcrumbs-enable', false );
	}
	return false;
}

/**
 * Costruisce la scala dei breadcrumb per il contenuto corrente.
 *
 * @return array Elenco di array( 'nome' => string, 'url' => string ).
 */
function mfinox_scala_breadcrumb() {
	$post = get_queried_object();
	if ( ! $post instanceof WP_Post ) {
		return array();
	}

	// home_url() restituisce la home della lingua corrente: con WPML o
	// Polylang la scala parte da /en/, /de/, /fr/ come deve.
	$scala = array(
		array(
			'nome' => __( 'Home' ),
			'url'  => home_url( '/' ),
		),
	);

	$tipo = get_post_type_object( $post->post_type );

	// Archivio del tipo di contenuto, se ne ha uno proprio e navigabile.
	if ( $tipo && ! empty( $tipo->has_archive ) ) {
		$archivio = get_post_type_archive_link( $post->post_type );
		if ( $archivio ) {
			$scala[] = array(
				'nome' => $tipo->labels->name,
				'url'  => $archivio,
			);
		}
	}

	// Pagine gerarchiche: la catena dei genitori, dal più alto al più basso.
	if ( is_post_type_hierarchical( $post->post_type ) ) {
		$antenati = array_reverse( get_post_ancestors( $post ) );
		foreach ( $antenati as $id_antenato ) {
			$scala[] = array(
				'nome' => get_the_title( $id_antenato ),
				'url'  => get_permalink( $id_antenato ),
			);
		}
	} else {
		// Contenuti non gerarchici: la prima categoria utile come livello
		// intermedio. 'Uncategorized' non dice niente a nessuno, si salta.
		foreach ( get_object_taxonomies( $post->post_type, 'objects' ) as $tassonomia ) {
			if ( empty( $tassonomia->public ) || empty( $tassonomia->hierarchical ) ) {
				continue;
			}
			$termini = get_the_terms( $post, $tassonomia->name );
			if ( is_wp_error( $termini ) || empty( $termini ) ) {
				continue;
			}
			$termine = $termini[0];
			if ( 'uncategorized' === $termine->slug ) {
				continue;
			}
			$collegamento = get_term_link( $termine );
			if ( ! is_wp_error( $collegamento ) ) {
				$scala[] = array(
					'nome' => $termine->name,
					'url'  => $collegamento,
				);
			}
			break;
		}
	}

	$scala[] = array(
		'nome' => get_the_title( $post ),
		'url'  => get_permalink( $post ),
	);

	return $scala;
}

add_action(
	'wp_head',
	function () {
		if ( ! is_singular() || is_front_page() ) {
			return;
		}
		if ( mfinox_yoast_breadcrumb_attivi() ) {
			return;
		}
		/**
		 * Permette di disattivare il markup senza rimuovere il file.
		 */
		if ( ! apply_filters( 'mfinox_breadcrumb_jsonld', true ) ) {
			return;
		}

		$scala = mfinox_scala_breadcrumb();
		// Con meno di due livelli il breadcrumb non aggiunge informazione.
		if ( count( $scala ) < 2 ) {
			return;
		}

		$elementi = array();
		$posizione = 1;
		foreach ( $scala as $livello ) {
			$nome = trim( wp_strip_all_tags( (string) $livello['nome'] ) );
			if ( '' === $nome ) {
				continue;
			}
			$elementi[] = array(
				'@type'    => 'ListItem',
				'position' => $posizione,
				'name'     => $nome,
				'item'     => esc_url_raw( $livello['url'] ),
			);
			$posizione++;
		}

		if ( count( $elementi ) < 2 ) {
			return;
		}

		$grafo = array(
			'@context'        => 'https://schema.org',
			'@type'           => 'BreadcrumbList',
			'itemListElement' => $elementi,
		);

		printf(
			"<script type=\"application/ld+json\">%s</script>\n",
			wp_json_encode( $grafo, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
		);
	},
	20
);
