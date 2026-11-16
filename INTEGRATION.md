# Ski Society — design de bc9bb78 et nouveaux textes validés

Branche : feat/ski-society-complete. Référence graphique : main au commit bc9bb78.
main n’est pas modifiée ; PR #20 non fusionnée ; aucun déploiement en production.

## Séparation entre design et rédaction

- content/original-pages/ fournit les compositions de référence.
- content/pages.json fournit les 32 sections de rédaction approuvée ; ce fichier reste inchangé.
- scripts/editorial.py applique une correspondance explicite entre les champs éditoriaux et les composants originaux.
- scripts/build.py génère le site, les destinations et le footer. Il ne se contente plus de restaurer les anciens textes.
- public/editorial-content.css contient uniquement les adaptations des textes nouveaux dans les composants existants (espacement des introductions, palette native du chapitre Programmes réutilisé dans les offres, textes de réserve des avis, boutons et listes). Aucun nouveau système de mise en page pour les pages principales.
- Les feuilles de style d’origine, les photographies, leurs URLs et leurs règles de cadrage restent celles de bc9bb78.

L’audit a été effectué avant modification : docs/editorial-integration/audit.md.

## Correspondance des composants

| Page | Sections éditoriales | Composition réemployée |
|---|---:|---|
| Accueil | A01–A08 : 8 | Hero, diptyque photographique, galerie ADN, quatre cartes expériences, programmes, galerie destinations et bandeau catalogue, coque des avis, accordéons FAQ, formulaire et contact. |
| Le collectif | B01–B04 : 4 | À la demande suivante : hero, cartes photographiques, programmes éditoriaux et contact de la page d’accueil. Les quatre textes validés restent inchangés. |
| Cours particuliers | C01–C05 : 5 | Photo et hero propres à cette page, grille de points et listes, cartes other-offers, programmes de la home de référence, étapes et final-cta photographique d’origine. |
| Performance & technique | D01–D05 : 5 | Même méthode, à partir de son propre fichier de référence et de ses propres photos. |
| Freeride & milieu alpin | E01–E05 : 5 | Même méthode ; seuls les formats journée et sur mesure sont présentés. |
| Snowboard | F01–F05 : 5 | Même méthode, avec les composants et photos de sa page d’origine. |

Il n’y a aucune suppression des huit sections de la home ni d’une section validée. Les offres possèdent désormais leurs cinq sections complètes en réemployant les composants disponibles sur main. Les titres de certaines sections servent aussi de légendes aux emplacements photographiques existants ; aucun ancien slogan n’est réintroduit pour remplir ces emplacements.

Les identifiants hero-title, tiles-title, formules-title, destinations-title, reviews-title et contact-title sont conservés. En particulier, les déclencheurs de transition du chapitre noir et du retour au clair fonctionnent toujours.

## Contrôle des textes

Tableau détaillé : docs/editorial-integration/sections.md.
Résultats structurés : docs/editorial-integration/sections.json.

32/32 sections vérifiées, chaque bloc source recherché dans le HTML final de la section correspondante. Seuls les marqueurs Markdown et les annotations de préparation (« version V2 approuvée ») sont exclus du texte publié ; les mots, accents, apostrophes et ponctuations validés sont conservés. Les retours à la ligne de mise en page sont normalisés pour le contrôle.

Les anciens paragraphes marketing de main sont également contrôlés pour éviter leur réapparition. Les libellés fonctionnels conservés de la navigation et du formulaire ne sont pas des anciens textes marketing. Les nouveaux textes restent visibles sans JavaScript. La page intermédiaire offres/index.html réutilise également les extraits validés Expériences et Contact, dans ses propres compositions, afin de ne pas conserver une ancienne promesse de disponibilité.

## Avis et réservation

La coque graphique et les colonnes animées des avis sont conservées. Les témoignages fictifs de la maquette sont remplacés par les seuls textes de réserve approuvés ; aucun avis, auteur, score ou citation n’est inventé. Sur mobile, chaque colonne affichable contient le texte de réserve complet.

Le formulaire d’origine et le fonctionnement WhatsApp sont conservés. La demi-journée est désactivée pour le freeride ; une sélection de demi-journée préexistante est remplacée par la journée. Aucun message n’a été envoyé pendant les tests.

## Destinations et SEO

43 pages locales, métadonnées et 86 CTA spécifiques conservés. Les cartes de stations.html et la sélection de recherche ouvrent chaque fiche correspondante. Le second index destinations.html reste disponible.

Titres, H1 et descriptions des six pages principales utilisent la nouvelle rédaction. noindex,nofollow reste présent partout, avec les protections HTTP/robots existantes. Aucun domaine canonique n’est inventé ; aucun sitemap soumis ni indexation activée.

## Footer

Le footer est le seul composant avec une nouvelle direction graphique : grand pré-footer photographique utilisant une image sportive déjà présente sur main, CTA WhatsApp, navigation fonctionnelle et signature Ski Society. Le composant est isolé dans content/premium-footer.html et premium-footer.css. La photo reste une illustration, sans identification d’un membre du collectif ou d’une station.

## Recette visuelle

Comparatif : docs/editorial-integration/visual/index.html.
48 captures :
- 32 vues des huit pages (six principales + deux catalogues), référence et nouvelle copie, à 1440 et 390 px ;
- 12 vues des chapitres Expériences, Programmes et Avis pendant la navigation, des deux versions aux deux largeurs ;
- 4 vues du nouveau pré-footer et du footer fonctionnel.

Les textes et certains retours à la ligne changent volontairement : cette recette ne prétend donc pas à une égalité pixel par pixel. Elle vérifie la reprise des composants, photos, styles, palettes et interactions avec les textes nouveaux.

Les photos et polices distantes restent refusées par le proxy de l’environnement. Elles ne sont ni simulées ni remplacées dans les captures. Les URLs et les styles sont contrôlés, mais une recette photographique et typographique complète reste nécessaire lorsque les ressources seront accessibles.

Voir QA_IMPLEMENTATION.md pour les résultats et observations d’accessibilité. Les rapports de restauration seule et de refonte antérieure sont des archives, pas les spécifications de l’état courant.

## Mise à jour : style de l’accueil sur Notre histoire

La page manifesto.html reprend désormais les composants, photos, typographies et transitions de l’accueil. Les trois points de l’héritage sont présentés dans ses cartes ; les trois étapes de la philosophie dans ses lignes de programme ; la conclusion dans son bloc de contact. Aucun formulaire supplémentaire n’est ajouté. L’accueil et les autres pages ne changent pas. Les tests dédiés sont dans tests/story_home.py ; captures et résultats dans docs/story-home/.

## Mise à jour : ADN de l’accueil

Seules les deux zones ADN de la home sont recomposées : introduction asymétrique claire avec une photo, puis trois cartes avec textes sous les images. Textes validés conservés intégralement ; autres sections, pages et destinations inchangées. Comparatif ordinateur/mobile et rapport : docs/adn-redesign/index.html et docs/adn-redesign/README.md. Contrôles éditoriaux, SEO, liens, responsive 375/768/1440 et axe ciblé : PASS. Le chargement des photos et polices distantes reste bloqué par le proxy ; la validation photographique complète reste à faire.

## ADN — composition alpine à une image

Cette demande remplace la précédente proposition de trois cartes : une photo dominante, les textes exacts de LA COMPÉTITION à droite, puis NOTRE APPROCHE et L’EXPÉRIENCE sans photo en dessous. L’introduction empruntée au collectif et son lien sont retirés de cette zone. Aucune autre section ni page ne change. Recette à 1440/1280/1024/768/390 px, contrôle littéral des neuf textes, comparaison du HTML hors zone, liens/SEO et axe ciblé : PASS. Captures, limites réseau et détails : docs/adn-alpine/index.html et docs/adn-alpine/README.md. Les photos/polices restent refusées par le proxy ; la validation photographique complète reste à faire.

## ADN — direction artistique V2

La proposition V2 remplace la composition précédente : sommet photographique pleine largeur avec fondu neutre vers la zone de texte, puis bande de deux contenus avec filet vertical. Trois contenus exacts, styles isolés sous .ss-adn-editorial-v2, aucune autre zone ni page modifiée. Recette aux cinq viewports demandés, vues entières et comparaison : docs/adn-v2/index.html. Rapport : docs/adn-v2/README.md. Contrôles de texte, périmètre, responsive, liens/SEO et axe ciblé réussis. Validation photographique (silhouette/fondu/cadrage) et typographique bloquée par le proxy ; ces contrôles ne sont pas déclarés réussis. Proposition livrée pour validation avant toute autre modification.

## UI SPEC 04 — Formats des cours privés

La section 04 devient une liste éditoriale de trois formats sur fond minéral. Catégories et durées immédiatement visibles, textes validés intégraux, créneaux indicatifs, note et CTA vers #contact. Transition section 03 limitée au fond, aux textes de son en-tête et à son espacement ; quatre cartes inchangées. Les autres pages, le footer et les destinations sont identiques. Recette sept viewports, textes, liens, CTA clavier, axe ciblé et comparaison des cartes : PASS. Numéros assombris pour le contraste ; hauteur naturelle supérieure à la cible indicative afin de préserver tous les contenus. Captures et rapport : docs/course-formats/index.html et docs/course-formats/README.md. Photos/polices distantes toujours bloquées.

## Expériences & Formats — vue compacte autorisée

Les sections 03/04 forment désormais un ensemble minéral unique de 849,5 px à 1440 px. Quatre expériences sur une ligne, trois formats en dessous : visibilité simultanée à 1440×900 vérifiée. Descriptions longues retirées de cette vue avec autorisation explicite ; sources intactes, pages prestations et destinations inchangées. Contrôle éditorial adapté pour distinguer blocs affichés et blocs conservés uniquement en source. Sept viewports, liens/clavier, absence de débordement et axe ciblé : PASS. Galerie et rapport : docs/compact-courses/index.html et README.md. Les pages prestations conservent leurs propres textes complets, distincts des résumés d’accueil. Preview HTTPS et recette photographique restent bloquées par le proxy ; voir preview-blocker.md.
