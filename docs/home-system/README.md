# Système de fonds de l’accueil et réservation en deux étapes

Référence avant : 23821ca. Branche feat/ski-society-complete. La modification concerne les thèmes de l’accueil complet, le header de cette page et la section Réservation. Les autres pages et les sources éditoriales validées restent intactes.

## Fonds pleine largeur

- Hero et ADN : thème clair ; Expériences et Formats : #F7F6F2.
- Destinations : #111312 dès le dernier pixel de Formats, padding compris.
- Avis et FAQ : #FFFFFF dès la fin de Destinations, sans espace intermédiaire.
- Réservation, pré-footer photographique et footer : base #111312, sans bande blanche.
- Les classes de thème portent les fonds sur les wrappers à 100 % de largeur. Aucun 100vw susceptible de créer une barre horizontale, aucune marge de transition ni gradient entre sections.
- Les conteneurs de Destinations, Avis, FAQ, Réservation et footer sont plafonnés à 1320 px, avec padding horizontal 48 px desktop, 32 px tablette et 20 px mobile. Les compositions photographiques du hero et de l’ADN restent celles déjà validées.
- Le voile photographique existant du pré-footer est neutralisé en #111312, sans dégradé bleu, pour prolonger le fond sombre. La photographie, la navigation et toutes les informations du footer sont conservées.

Le test contrôle les boîtes de chaque wrapper et la contiguïté de leurs frontières aux sept tailles. Les pixels sur les deux bords du viewport sont aussi vérifiés de part et d’autre des trois transitions : ce contrôle ne se limite pas à la valeur CSS du conteneur.

## Header

Deux palettes explicites : fond clair rgba(247,246,242,.96) / texte sombre et fond sombre rgba(21,23,22,.96) / texte blanc, avec CTA inversé. Le thème est calculé à la position de la capsule flottante, indépendamment du titre des sections et du masquage lors du défilement. Une zone de tolérance de deux pixels limite les changements erratiques près d’une frontière.

Les transitions de couleur durent 200 ms, sont désactivées en réduction de mouvement et ne modifient aucune dimension. Les deux anciennes fonctions de thème dans app.js sortent immédiatement pour `.ss-home-themed` ; elles restent identiques sur les autres pages. Les interactions existantes de navigation et de menu sont conservées.

## Réservation

- Textes A08 conservés mot pour mot dans la colonne gauche : titre, introduction, processus, texte complémentaire et lien WhatsApp direct. Aucune section éditoriale supprimée.
- Grille desktop .85fr / 1.15fr, espace 72 px, panneau clair sans ombre. Tablette et mobile en une colonne, sans hauteur forcée. La photo latérale de l’ancien formulaire est retirée de l’accueil uniquement.
- Étape 1 : quatre expériences via radios natifs, recherche native par datalist parmi 43 stations et « Autre station », station libre conditionnelle et date/période libre. Aucun planning de disponibilité.
- Étape 2 : niveau, nombre entier positif de participants sans maximum arbitraire, format, prénom et précisions facultatifs.
- En freeride, l’option Demi-journée est retirée du DOM et la règle est explicitée sous le champ. Une ancienne sélection de demi-journée est effacée ; l’option réapparaît quand une autre expérience est choisie.
- Boutons Retour/Continuer sans rechargement, valeurs conservées, focus sur l’étape ou le premier champ erroné, erreurs spécifiques reliées aux champs. Les champs de l’étape inactive sont désactivés et masqués.
- La station transmise par le catalogue via ?station= est préremplie. Un nom hors catalogue active Autre station.
- Le seul envoi de formulaire valide prépare un lien wa.me avec encodeURIComponent et ouvre un brouillon dans un nouvel onglet protégé par noopener/noreferrer. L’utilisateur choisit lui-même l’envoi dans WhatsApp. Aucun paiement, confirmation de réservation ou stockage persistant.
- Sans JavaScript, une notice oriente vers le lien WhatsApp direct, conservé à côté du formulaire.

Le panneau de l’étape 1 mesure environ 712 px à 1440 px dans cet environnement, au-delà de l’objectif indicatif de 500–620 px. Les labels, aides et notes restent lisibles, sans réduction artificielle de la copie ou hauteur fixe. Le formulaire mobile utilise le défilement vertical normal.

## Résultats des contrôles

| Contrôle | Résultat |
| --- | --- |
| 1536×960, 1440×900, 1280×800, 1024×768, 768×1024, 390×844, 375×812 | PASS |
| Fonds x=0 à x=largeur viewport et absence de débordement | PASS |
| Frontières Formats/Destinations, Destinations/Avis, FAQ/Réservation | PASS, positions contiguës et pixels aux deux bords |
| Continuité Avis/FAQ et Réservation/pré-footer/footer | PASS |
| Header : bon thème, hauteur stable desktop/mobile, menu lisible | PASS |
| Deux étapes, progression 50/100 %, retour, données conservées | PASS |
| Quatre expériences et 43 destinations + Autre station | PASS |
| Validation par champ et coordonnées des erreurs | PASS |
| Nombre de participants 0 / 2,5 refusé, 27 accepté | PASS |
| Prénom et commentaires facultatifs | PASS |
| Freeride : retrait réel de la demi-journée et explication | PASS |
| Brouillon WhatsApp, accents, &, +, retours à la ligne et encodage | PASS |
| Aucune ouverture WhatsApp avant soumission explicite valide | PASS |
| Aucun message ni formulaire envoyé à un tiers | Confirmé, window.open intercepté dans les tests |
| Axe WCAG A/AA : deux étapes et header clair/sombre, desktop/mobile | Aucune violation détectée |
| Axe complémentaire : Destinations, Avis, FAQ et footer, desktop/mobile | Aucune violation détectée |
| Erreurs JavaScript accueil et échantillon des autres pages | Aucune |
| 32 sections éditoriales, sources approuvées immuables | PASS, condensation A03/A04 précédemment autorisée maintenue |
| Autres pages HTML, prestations et 43 destinations | Identiques octet par octet à 23821ca |
| SEO, liens internes, H1, robots et 86 CTA locaux | PASS |
| Photographies et polices distantes | BLOQUÉES par le proxy |

Les tests axe sont ciblés sur les composants modifiés ; ils ne constituent pas une certification de toute la page. Les témoignages restent les textes de réserve validés. Aucune disponibilité, qualification, prestation locale ou limite de groupe n’est inventée.

## Livrables et reproduction

[Galerie](index.html) : pages complètes desktop/mobile ; trois transitions à 1440 et 390 px ; panneau des deux étapes aux sept tailles ; Réservation entière à l’étape 1. [Résultats JSON](results.json), [contrôle complémentaire des thèmes](theme-accessibility.json), [liste des fichiers](FILES.md), [spécification](specification.md).

Commandes :

- `PYTHONPATH=/tmp/ski-libs python scripts/build.py`
- `PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py`
- `python tests/check_site.py`
- `PYTHONPATH=/tmp/ski-libs python tests/home_system.py`
- `node --check public/app.js`
- `node --check public/home-system.js`
- `git diff --check`

Le test utilise Chromium, Playwright, Pillow et axe-core. Les chemins sont indiqués dans le script. Le serveur courant tourne sur 3000 ; la référence 23821ca est vérifiée via Git, aucune publication n’est nécessaire pour exécuter ces contrôles.

## Limites et publication

Les photos Pexels et les polices distantes restent bloquées par le proxy avec ERR_TUNNEL_CONNECTION_FAILED. Les captures montrent le gabarit réel avec ressources manquantes ; aucune image n’est simulée. La recette photographique et typographique complète reste à effectuer avec ces ressources chargées. La limite Cloudflare déjà documentée dans docs/compact-courses/preview-blocker.md reste inchangée ; aucune URL publique n’est inventée.

main inchangée, PR #20 non fusionnée, aucun déploiement en production. noindex,nofollow maintenu. La proposition est livrée pour validation visuelle.
