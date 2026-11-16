# Expériences & Formats — composition compacte de l’accueil

Une seule proposition, limitée aux sections 03 et 04. Référence avant : ccccbba. [Demande détaillée](specification.md).

## Résultat

La hauteur mesurée à 1440 px est de **849.5 px**. Le test navigateur vérifie que les deux H2, les quatre expériences, les trois formats et le CTA sont simultanément dans le viewport 1440×900 lorsque l’ensemble arrive en haut de l’écran. Aucune hauteur globale n’est fixée : le résultat vient de la condensation autorisée et des espacements.

- Une enveloppe `.ss-home-courses` et un conteneur de 1320 px maximum, avec 48 px de padding latéral : largeur utile de 1224 px à 1440 px. Fond unique #F7F6F2, aucune carte noire.
- Quatre expériences en une ligne dès 1280 px, images de 280 px à 1440 px, légendes de 19 px et CTA de 13 px. Le numéro accompagne le titre sur la même ligne pour éviter une rangée inutile. Les photos existantes et les quatre URLs sont conservées. Label Performance identique, dimensions de carte égales.
- Les descriptions longues sont retirées de cette vue compacte, conformément à la nouvelle autorisation. Ni les sources validées ni les pages prestations ne sont modifiées.
- Filet de séparation après 32 px, puis 25 px de respiration. Les formats sont trois colonnes égales : catégories, durées et règles métier lisibles sans interaction.
- Note horaire conservée et rappel « Freeride : journée complète ou sur mesure. » Le CTA « Parlons de votre projet » ouvre le parcours `#contact` existant ; aucun nouveau formulaire ni envoi automatique.
- Tablette : deux colonnes d’expériences, photos 4:3 ; mobile : une colonne et photos 16:10, formats empilés, CTA pleine largeur. Aucun contenu tronqué et aucun scroll horizontal.
- Styles exclusivement dans course-formats.css, chargée par la home. Les classes dédiées évitent les anciennes règles de cartes noires. Zoom de 1.025 au maximum, 300 ms ; supprimé en réduction de mouvement. Contours de focus de 2 px.
- Les anciens composants Expériences et Programmes nécessaires à Notre histoire sont conservés séparément par le générateur. Cette page reste identique à la référence.

## Traitement des textes

Les sources éditoriales content/pages.json sont inchangées et leur empreinte est vérifiée. Le contrôle des 32 sections distingue désormais la copie visible et les blocs conservés uniquement en source dans les vues compactes A03/A04 ; aucune suppression n’est masquée sous un résultat « tout présent dans le HTML ».

Les paragraphes de présentation des quatre expériences, les titres et descriptions des formats et l’introduction des formats restent dans les données. Les créneaux indicatifs de référence sont conservés dans content/course-format-ui.json. Les deux surtitres d’interface sont ceux expressément demandés dans cette spécification.

**Point à arbitrer séparément :** les pages prestations ont leur propre rédaction validée complète ; elles ne contiennent pas mot pour mot les quatre anciens résumés d’accueil. Elles sont conservées octet pour octet, conformément à l’interdiction de modifier ces pages. Aucun ajout de ces résumés n’est réalisé sans élargissement explicite du périmètre. Le texte de référence n’est pas perdu.

## Tests

| Vérification | Résultat |
| --- | --- |
| Sept viewports demandés | PASS |
| 1440×900 : tous les éléments requis simultanément visibles | PASS |
| Hauteur totale à 1440 px | 849.5 px |
| Quatre expériences desktop / deux tablette / une mobile | PASS |
| Trois formats immédiatement lisibles | PASS |
| Aucun fond de carte noir, troncature ou débordement horizontal | PASS |
| Sources éditoriales immuables, condensation explicite A03/A04 | PASS |
| Accueil hors sections 03/04 | HTML identique à ccccbba hors blancs inter-sections |
| Toutes les autres pages, footer, prestations et destinations | HTML identique octet par octet |
| Quatre URLs et CTA, navigation réelle au clavier, focus | PASS |
| 43 destinations, métadonnées, liens et 86 CTA locaux | PASS |
| Axe WCAG A/AA sur l’ensemble 03/04 | Aucune violation détectée |
| Erreurs JavaScript pendant la recette | Aucune |
| Photographies/polices réelles et URL HTTPS publique | BLOQUÉES |

Le contrôle axe est ciblé et n’est pas une certification de tout le site. Aucun formulaire ou message WhatsApp n’a été envoyé.

Commandes : `PYTHONPATH=/tmp/ski-libs python scripts/build.py`, `PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py`, `python tests/check_site.py`, `PYTHONPATH=/tmp/ski-libs python tests/course_formats.py`, `git diff --check`. Test navigateur : serveur courant 3000, référence ccccbba sur 3010, Chromium, Playwright et axe-core.

[Galerie avant/après](index.html) : vues complètes et viewports aux sept dimensions, références à 1440 et 390 px. [Résultats détaillés](results.json).

## Limites de livraison

Les photographies et polices sont refusées par le proxy ; les captures présentent donc la composition réelle avec ressources manquantes, pas une campagne photographique validée. Le choix définitif des photos et la lisibilité avec les polices projet chargées restent à contrôler. Aucun visuel n’est simulé ou téléchargé par contournement.

La prévisualisation HTTPS demandée reste indisponible : l’API Cloudflare est refusée avec CONNECT 403 par la politique réseau active. [Preuve et conditions de déblocage](preview-blocker.md). Aucune URL publique n’est inventée. Cette livraison fournit le code et la preuve du gabarit, mais ne présente pas la recette visuelle complète ni la preview comme terminées.

Branche feat/ski-society-complete uniquement, main inchangée, PR #20 non fusionnée, aucun déploiement en production. noindex,nofollow conservé partout. Attente de validation avant toute nouvelle refonte.
