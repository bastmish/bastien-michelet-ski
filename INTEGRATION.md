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
| Le collectif | B01–B04 : 4 | mf-hero ; mf-origin et mf-turning ; mf-statement et mf-translation ; mf-collective et mf-final. Les sept compositions visuelles restent présentes. |
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
