# Audit avant intégration

Référence : bc9bb78. État de départ : 21958de. Les main sont identiques à la référence ; seul le footer diffère. Les 32 sections sont présentes dans content/pages.json (8/4/5/5/5/5). Aucun contenu n’a encore été réinjecté à ce stade.

| Page | Sections validées | Composants originaux | Main identique au départ |
|---|---:|---|---|
| index.html | 8 | [['hero'], ['ss-expertise-editorial'], ['ss-section', 'ss-adn', 'ss-editorial-v41'], ['ss-section', 'ss-offers', 'ss-offers-v46'], ['ss-section', 'ss-formules', 'ss-journey-v49', 'ss-programmes-v72'], ['ss-section', 'ss-destinations'], ['ss-section', 'ss-testimonials', 'ss-reviews-v26', 'ss-reviews-v49', 'ss-reviews-v52'], ['ss-section', 'ss-questions'], ['ss-section', 'ss-contact', 'ss-contact-v29']] | True |
| manifesto.html | 4 | [['mf-hero'], ['mf-origin'], ['mf-turning'], ['mf-statement'], ['mf-translation'], ['mf-collective'], ['mf-final']] | True |
| offres/ski-prive.html | 5 | [['detail-hero'], ['section'], ['section'], ['final-cta']] | True |
| offres/performance-technique.html | 5 | [['detail-hero'], ['section'], ['section'], ['final-cta']] | True |
| offres/freeride-decouverte.html | 5 | [['detail-hero'], ['section'], ['section'], ['final-cta']] | True |
| offres/snowboard.html | 5 | [['detail-hero'], ['section'], ['section'], ['final-cta']] | True |

## Plan de correspondance

- Accueil : hero, diptyque et galerie ADN, cartes expériences, programmes, galerie destinations, coque des avis, accordéons FAQ, formulaire et contact. Tous les identifiants servant aux transitions de main seront conservés.
- Collectif : mf-hero pour B01 ; mf-origin et mf-turning pour B02 ; mf-statement et mf-translation pour B03 ; mf-collective et mf-final pour B04. Les sept compositions photographiques/éditoriales sont conservées et alimentent quatre sections éditoriales.
- Chaque offre : detail-hero pour 01 ; detail-points/detail-list pour 02 ; other-offers pour 03 ; composant programmes de main pour 04 ; final-cta et composant steps de main pour 05. Réemploi des composants d’origine, pas de nouveau système de cartes.
- Catalogue : mêmes cartes, images et recherche ; href et sélection reliés aux fiches.
- Footer : composant indépendant, seule nouvelle direction graphique.
