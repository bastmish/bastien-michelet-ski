# Recette — design de référence et nouveaux textes

Le rapport courant est INTEGRATION.md. Les anciens rapports de restauration seule et de refonte sont archivés.

## Audit préalable et contenu

L’audit des composants est enregistré avant modification dans docs/editorial-integration/audit.md.

Les sources contiennent bien 32 sections : 8 accueil, 4 collectif, 5 cours particuliers, 5 performance, 5 freeride, 5 snowboard. Les fichiers sources ne sont pas réécrits.

tests/check_editorial.py vérifie chaque bloc source dans le HTML de la section correspondante. Il produit sections.md et sections.json. La normalisation porte sur les marqueurs Markdown de préparation et les blancs de mise en page ; aucun mot, accent, apostrophe ou signe de ponctuation validé n’est remplacé.

Résultat : 32/32 sections PASS. Le contrôle recherche également les anciens paragraphes marketing pour éviter leur réintroduction. Seuls les libellés fonctionnels de la navigation et du formulaire sont conservés lorsqu’ils restent pertinents.

## Fidélité graphique

- Chacune des six pages repart de son propre HTML bc9bb78.
- Toutes les photos de main conservent leurs URLs et leur ordre dans les six pages.
- Les feuilles de style de référence sont conservées et vérifiées par SHA-256.
- Les compositions de la home et les sept compositions du collectif sont conservées.
- Les offres réutilisent detail-hero, detail-points, detail-list, other-offers, les programmes et steps de main, ainsi que leur final-cta photographique d’origine.
- Aucune des six pages ne charge integration.css ou art-direction.css.
- editorial-content.css contient les adaptations nécessaires aux nouveaux blocs : introduction, réserve avis, boutons supplémentaires, listes et palette native du composant Programmes dans les offres.
- Les déclencheurs tiles-title et reviews-title sont préservés : chapitre sombre aux expériences, retour au clair aux avis. Le contrôle navigateur confirme ces états.
- Le nouveau footer photographique sportif est isolé dans son composant et sa feuille de style.

Deux scripts d’origine comportent des modifications fonctionnelles délimitées : stations-search.js ouvre les fiches ; app.js empêche une demande de freeride en demi-journée. Les autres interactions de référence sont conservées. Le script d’avis fictifs n’est plus chargé : seuls les textes de réserve validés sont affichés dans la coque et les colonnes du composant d’origine.

## Tests

Commandes utilisées :
- PYTHONPATH=/tmp/ski-libs python scripts/build.py
- PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py
- python tests/check_site.py
- AXE_SCRIPT=/tmp/ski-qa/node_modules/axe-core/axe.min.js python tests/browser_check.py
- python tests/booking_check.py
- python tests/editorial_visual.py
- git diff --check

Résultats :
- Copies 32/32 et sources immuables : PASS.
- Photos et ressources graphiques de référence : PASS.
- Liens, ancres, un H1 et noindex,nofollow : PASS.
- 43 fiches, tous leurs textes locaux et métadonnées : PASS.
- 86 CTA spécifiques : PASS.
- 52 pages, 156 rendus aux largeurs 375/768/1440 : aucun débordement horizontal ni erreur JavaScript.
- Menu mobile, FAQ approuvée, formulaire, catalogues et recherche vers Méribel : PASS.
- Formulaire : exclusion du freeride demi-journée et adaptation d’une sélection existante ; aucun message envoyé.
- Footer fonctionnel : aucune violation axe-core détectée sur les règles WCAG testées.
- Les observations d’accessibilité du reste du site sont consignées dans tests/browser-results.json ; ce résultat n’est pas présenté comme une conformité totale.

## Comparaison visuelle

docs/editorial-integration/visual/index.html présente 48 captures :
32 pages référence/nouveaux textes, 12 états de chapitres de la home en cours de navigation, 4 vues du nouveau footer, sur ordinateur et mobile.

Une capture complète prise tout en haut ne représente pas simultanément les palettes activées plus bas par le défilement : les états Expériences, Programmes et Avis sont donc capturés séparément. Aucun fond uniforme n’est forcé à la place des transitions de main.

Les textes nouveaux modifient volontairement certains retours à la ligne et la hauteur du contenu. Il ne s’agit pas d’une égalité des pixels ou des anciens textes : la référence porte sur les composants et les ressources graphiques.

## Limites et sécurité

Le proxy refuse toujours les photos Pexels et polices distantes. Aucune image n’est simulée ou substituée dans les captures ; les échecs et chargements en attente sont enregistrés. Une recette photographique et typographique complète reste à effectuer lorsque ces accès seront actifs.

Aucun prix, avis, score, qualification, disponibilité ou établissement local inventé. Les textes de réserve des avis restent clairement identifiés ; aucun témoignage fictif de main n’est réintroduit dans la version livrée.

Voir LOCAL_VERIFICATION.md pour la couverture réelle, les qualifications/assurances, la Suisse, La Grave, les photos, le numéro WhatsApp et l’organisation du questionnaire après confirmation.

main inchangée, PR #20 non fusionnée, aucun déploiement en production, aucune soumission de sitemap et noindex,nofollow maintenu.

## Mise à jour Notre histoire

À la demande du propriétaire, cette page adopte maintenant les composants de l’accueil plutôt que son ancienne composition manifeste. Les tests photo/styles de cette page vérifient donc ses ressources par rapport à la home. Les quatre sections validées sont intactes. tests/story_home.py passe à 375, 768 et 1440 px : aucun débordement, aucune erreur JavaScript et transitions sombre/clair confirmées. Les autres pages publiques ne sont pas modifiées par cette mise à jour. Comparatif : docs/story-home/index.html.

## Mise à jour : ADN de l’accueil

Seules les deux zones ADN de la home sont recomposées : introduction asymétrique claire avec une photo, puis trois cartes avec textes sous les images. Textes validés conservés intégralement ; autres sections, pages et destinations inchangées. Comparatif ordinateur/mobile et rapport : docs/adn-redesign/index.html et docs/adn-redesign/README.md. Contrôles éditoriaux, SEO, liens, responsive 375/768/1440 et axe ciblé : PASS. Le chargement des photos et polices distantes reste bloqué par le proxy ; la validation photographique complète reste à faire.

## ADN — composition alpine à une image

Cette demande remplace la précédente proposition de trois cartes : une photo dominante, les textes exacts de LA COMPÉTITION à droite, puis NOTRE APPROCHE et L’EXPÉRIENCE sans photo en dessous. L’introduction empruntée au collectif et son lien sont retirés de cette zone. Aucune autre section ni page ne change. Recette à 1440/1280/1024/768/390 px, contrôle littéral des neuf textes, comparaison du HTML hors zone, liens/SEO et axe ciblé : PASS. Captures, limites réseau et détails : docs/adn-alpine/index.html et docs/adn-alpine/README.md. Les photos/polices restent refusées par le proxy ; la validation photographique complète reste à faire.

## ADN — direction artistique V2

La proposition V2 remplace la composition précédente : sommet photographique pleine largeur avec fondu neutre vers la zone de texte, puis bande de deux contenus avec filet vertical. Trois contenus exacts, styles isolés sous .ss-adn-editorial-v2, aucune autre zone ni page modifiée. Recette aux cinq viewports demandés, vues entières et comparaison : docs/adn-v2/index.html. Rapport : docs/adn-v2/README.md. Contrôles de texte, périmètre, responsive, liens/SEO et axe ciblé réussis. Validation photographique (silhouette/fondu/cadrage) et typographique bloquée par le proxy ; ces contrôles ne sont pas déclarés réussis. Proposition livrée pour validation avant toute autre modification.

## UI SPEC 04 — Formats des cours privés

La section 04 devient une liste éditoriale de trois formats sur fond minéral. Catégories et durées immédiatement visibles, textes validés intégraux, créneaux indicatifs, note et CTA vers #contact. Transition section 03 limitée au fond, aux textes de son en-tête et à son espacement ; quatre cartes inchangées. Les autres pages, le footer et les destinations sont identiques. Recette sept viewports, textes, liens, CTA clavier, axe ciblé et comparaison des cartes : PASS. Numéros assombris pour le contraste ; hauteur naturelle supérieure à la cible indicative afin de préserver tous les contenus. Captures et rapport : docs/course-formats/index.html et docs/course-formats/README.md. Photos/polices distantes toujours bloquées.
