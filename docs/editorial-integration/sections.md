# Vérification des 32 sections

Contrôle du texte dans le HTML final de chaque section, sans modification des sources. Les retours à la ligne sont normalisés. Les blocs non condensés sont contrôlés mot pour mot dans le HTML. Pour A03/A04 de l’accueil, la condensation expressément autorisée est détaillée dans sections.json ; les textes complets restent dans les sources immuables.

| Page | Section | Blocs sources | Composants rendus | Résultat |
|---|---|---:|---|---|
| index.html | A01 | 5 | hero | PASS |
| index.html | A02 | 9 | ss-adn-editorial-v2 | PASS |
| index.html | A03 | 16 | ss-experiences-compact | PASS — vue compacte autorisée |
| index.html | A04 | 14 | ss-formats-compact | PASS — vue compacte autorisée |
| index.html | A05 | 8 | ss-section ss-destinations | PASS |
| index.html | A06 | 8 | ss-section ss-testimonials ss-reviews-v26 ss-reviews-v49 ss-reviews-v52 | PASS |
| index.html | A07 | 17 | ss-section ss-questions | PASS |
| index.html | A08 | 10 | ss-section ss-contact ss-contact-v29 | PASS |
| manifesto.html | B01 | 4 | hero | PASS |
| manifesto.html | B02 | 9 | ss-section ss-offers ss-offers-v46 | PASS |
| manifesto.html | B03 | 12 | ss-section ss-formules ss-journey-v49 ss-programmes-v72 | PASS |
| manifesto.html | B04 | 6 | ss-section ss-contact ss-contact-v29 | PASS |
| offres/ski-prive.html | C01 | 5 | detail-hero | PASS |
| offres/ski-prive.html | C02 | 15 | section | PASS |
| offres/ski-prive.html | C03 | 12 | section | PASS |
| offres/ski-prive.html | C04 | 15 | ss-section ss-formules ss-journey-v49 ss-programmes-v72 | PASS |
| offres/ski-prive.html | C05 | 11 | section steps, final-cta | PASS |
| offres/performance-technique.html | D01 | 5 | detail-hero | PASS |
| offres/performance-technique.html | D02 | 15 | section | PASS |
| offres/performance-technique.html | D03 | 15 | section | PASS |
| offres/performance-technique.html | D04 | 15 | ss-section ss-formules ss-journey-v49 ss-programmes-v72 | PASS |
| offres/performance-technique.html | D05 | 11 | section steps, final-cta | PASS |
| offres/freeride-decouverte.html | E01 | 5 | detail-hero | PASS |
| offres/freeride-decouverte.html | E02 | 13 | section | PASS |
| offres/freeride-decouverte.html | E03 | 15 | section | PASS |
| offres/freeride-decouverte.html | E04 | 11 | ss-section ss-formules ss-journey-v49 ss-programmes-v72 | PASS |
| offres/freeride-decouverte.html | E05 | 11 | section steps, final-cta | PASS |
| offres/snowboard.html | F01 | 5 | detail-hero | PASS |
| offres/snowboard.html | F02 | 15 | section | PASS |
| offres/snowboard.html | F03 | 12 | section | PASS |
| offres/snowboard.html | F04 | 15 | ss-section ss-formules ss-journey-v49 ss-programmes-v72 | PASS |
| offres/snowboard.html | F05 | 11 | section steps, final-cta | PASS |
