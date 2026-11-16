# Destinations → Avis : transition de couleur uniquement

Référence avant : a7719d8. Travail sur feat/ski-society-complete.

## Correctif

- Suppression complète du calque `.ss-photo-transition--exit`, de son image et de ses styles de fondu photographique. Aucun calque photo, pseudo-élément, texte ou filtre dans la nouvelle transition.
- Un seul div décoratif vide `.ss-destinations-to-reviews`, immédiatement après Destinations et avant Avis, sur toute la largeur.
- Gradient vertical exact : #111312 à 0 %, #333634 à 25 %, #8B8D8A à 55 %, #D9DAD7 à 80 %, #FFFFFF à 100 %.
- Hauteur 120 px desktop/tablette, 72 px jusqu’à 767 px. Aucune marge ni padding sur cette bande.
- Padding inférieur du bandeau « Votre station. Notre terrain de jeu. » : 56 px desktop, 40 px mobile. Alignement vertical du CTA neutralisant le petit espace de ligne sous le bouton : la distance mesurée entre le bas du CTA et le début du gradient est bien de 56/40 px, sans wrapper vide supplémentaire.
- Avis et FAQ restent sur fond blanc uniforme. Les autres transitions ne changent pas.

## Preuve visuelle et tests

[Desktop 1440 px](junction-1440.png) et [mobile 390 px](junction-390.png) montrent ensemble le bandeau final Destinations, le gradient entier et le début des Avis. Les captures brutes ne sont ni recolorées ni retouchées. Elles ont été inspectées visuellement.

| Contrôle | Résultat |
| --- | --- |
| 1440×900, 1280×800, 1024×768, 768×1024, 390×844, 375×812 | PASS |
| Aucune photo de sortie, aucun enfant dans le div de transition | PASS |
| Aucun pseudo-élément, blur ou texte dans la transition | PASS |
| Hauteur calculée 120 / 72 px, largeur du viewport | PASS |
| Arrêts de couleur exacts dans le style calculé | PASS |
| Padding inférieur 56 / 40 px, sans espace supplémentaire sous CTA | PASS |
| Fin Destinations = début gradient ; fin gradient = début Avis | PASS |
| Pixels gauche / centre / droite sur chaque ligne du gradient | PASS |
| Fond #111312 juste avant le gradient, #FFFFFF juste après | PASS |
| Avis et FAQ entièrement blancs | PASS |
| Aucun débordement horizontal ni erreur JavaScript | PASS |
| Textes, liens, quatre cartes, formulaire et autres pages | Inchangés |
| 32 sections sources, SEO, 43 destinations et 86 CTA locaux | PASS |

Le contrôle des pixels tolère au maximum deux unités RGB entre colonnes pour le tramage normal du navigateur sur les dégradés. Il ne tolère pas de photographie, de rupture latérale ou de couleur de fond extérieure différente. Les couleurs unies avant/après sont vérifiées exactement.

Le test compare tout le DOM avant/après après retrait des seuls ancien/nouveau bandeaux de transition et normalisation des révisions CSS. Les JavaScript, sources éditoriales, contenu du bandeau et template de réservation sont identiques octet par octet à la référence. Les quatre cartes destinations sont ainsi protégées.

Les photos/polices distantes restent sujettes au blocage réseau de l’environnement, mais cette transition n’en dépend plus et son contrôle visuel n’est plus bloqué par une photographie manquante.

Commandes : `PYTHONPATH=/tmp/ski-libs python scripts/build.py`, `PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py`, `python tests/check_site.py`, `PYTHONPATH=/tmp/ski-libs python tests/destinations_reviews_color.py`, `git diff --check`.

[Galerie](index.html), [résultats détaillés](results.json). Captures complémentaires aux six largeurs et pages complètes desktop/mobile incluses.

main inchangée, PR #20 non fusionnée, aucun déploiement en production, noindex,nofollow maintenu.
