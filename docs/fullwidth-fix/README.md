# Correction des fonds pleine largeur

Branche : feat/ski-society-complete. Référence : bf42dea.

## Correctif limité aux fonds

- `ss-fullwidth` sur les wrappers Expériences/Formats, Destinations, Avis, FAQ, Réservation et les deux étages du footer : width 100 %, max-width none, position relative, marges et padding latéraux nuls, aucune bordure latérale.
- `ss-container` sur leurs conteneurs existants : contenu centré, max-width 1320 px, padding 48 px desktop, 32 px tablette et 20 px mobile. La réservation conserve son maximum tablette de 900 px.
- `main` neutralisé : largeur entière, aucun plafond de largeur, fond transparent et absence de padding latéral. Body sans marge ni padding. Aucun 100vw.
- Pseudo-éléments de canevas hérités neutralisés sur main et les sections concernées. Les overlays des photographies, le voile du pré-footer, les cartes et le panneau clair du formulaire restent inchangés.
- Fonds attribués explicitement aux wrappers : #F7F6F2, #111312, #FFFFFF, puis #111312 jusqu’au footer.
- La feuille est chargée avec la révision `/home-system.css?v=fullwidth-2` pour distinguer ce correctif d’une version mise en cache.

L’audit de la version locale précédente mesurait déjà des wrappers de 1440 px aux endroits contrôlés ; il n’a donc pas reproduit une marge latérale dans cette instance. Il identifiait toutefois un fond blanc sur main, l’absence d’architecture explicite ss-fullwidth/ss-container et des règles historiques de canevas. Le correctif verrouille cette architecture et retire ces couches concurrentes. Les preuves ci-dessous portent sur le rendu réel de la nouvelle version locale, sans prétendre diagnostiquer une autre preview non accessible.

## Mesures et pixels — 1440 px

Les prélèvements sont faits sur la capture PNG pleine page, dans le padding supérieur vide des sections (sans texte ou photographie), et confrontés aux styles calculés.

| Section | Y dans la capture complète | RGB aux x=0, 720, 1439 |
| --- | --- | --- |
| #destinations | 2703 | [17, 19, 18], [17, 19, 18], [17, 19, 18] |
| #avis | 3962 | [255, 255, 255], [255, 255, 255], [255, 255, 255] |
| #questions | 5095 | [255, 255, 255], [255, 255, 255], [255, 255, 255] |
| #contact | 5696 | [17, 19, 18], [17, 19, 18], [17, 19, 18] |
| .art-footer | 7208 | [17, 19, 18], [17, 19, 18], [17, 19, 18] |

Les wrappers ont tous x=0, width=1440 et max-width=none ; les conteneurs sont limités à 1320 px et ont un fond transparent. Les pseudo-éléments de canevas neutralisés ont content=none.

## Frontières — 1440 px

| Fin du chapitre / début du suivant | Fin Y | Début Y |
| --- | --- | --- |
| .ss-home-courses → #destinations | 2691.71875 | 2691.71875 |
| #destinations → #avis | 3950.796875 | 3950.796875 |
| #questions → #contact | 5684.875 | 5684.875 |

Les mêmes valeurs de fin et de début prouvent la contiguïté. Les pixels six positions avant et après chaque frontière sont également testés à gauche, au centre et à droite. La continuité Réservation → pré-footer → footer est vérifiée géométriquement.

## Résultats

- 1920×1080, 1536×960, 1440×900, 1280×800, 1024×768, 768×1024, 390×844 et 375×812 : PASS, aucun débordement horizontal.
- Fonds réellement peints à gauche/centre/droite, trois ruptures exactes, marges nulles, wrapper sans max-width : PASS.
- DOM identique à bf42dea après retrait des seules nouvelles classes et normalisation de la révision CSS : PASS. Aucun texte, image, champ, option ou interaction modifié.
- `public/app.js`, `public/home-system.js`, template du formulaire, sources éditoriales et stations : identiques octet par octet à la référence.
- Toutes les autres pages HTML : identiques à la référence.
- Contrôles des textes, 43 destinations, SEO, liens internes, H1, robots et 86 CTA locaux : PASS.
- Aucune erreur JavaScript pendant la recette.

Commandes : `PYTHONPATH=/tmp/ski-libs python scripts/build.py`, `PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py`, `python tests/check_site.py`, `PYTHONPATH=/tmp/ski-libs python tests/fullwidth_backgrounds.py`, `git diff --check`.

## Preuves

[Galerie](index.html), [capture complète brute à 1440 px](home-full-1440.png), [capture complète brute mobile](home-full-390.png), [feuille annotée des points de contrôle](pixel-evidence-1440.png), [mesures calculées et pixels JSON](results.json).

Les captures brutes ne sont ni retouchées ni recolorées ; la feuille de preuve annotée est un fichier séparé. Photos et polices distantes toujours bloquées par le réseau, sans substitution : les tests de couleur concernent les zones unies sans photographie demandées par le propriétaire. Cette limite ne modifie pas les valeurs des pixels des fonds testés.

Aucune modification de main, aucune fusion de PR #20, aucun déploiement de production ; noindex,nofollow maintenu.
