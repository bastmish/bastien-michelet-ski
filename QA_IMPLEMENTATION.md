# Recette Ski Society

## Périmètre

Branche dédiée basée sur main (bc9bb78). Six pages principales (32 sections) et 43 destinations HTML statiques générées depuis les sources éditoriales versionnées ; catalogue et recherche reliés aux fiches. Navigation, logo, pied de page et illustration alpine réutilisés. Les photos d’ambiance non identifiées des cartes sont remplacées par une illustration commune.

## Contrôles reproductibles

- `python scripts/build.py` : 6 pages principales, 43 destinations et page 404.
- `python tests/check_site.py` : textes validés, liens internes, ancres, un H1 par page, robots, 43 liens du catalogue, métadonnées locales distinctes, 86 CTA locaux et formats freeride.
- `git diff --check` : aucun problème.
- Playwright + Chromium : 50 pages à 375, 768 et 1440 px, absence de débordement horizontal, HTTP 200 et un H1. Menu mobile (ouverture/Escape), recherche clavier « Meribel » vers Méribel, inspection de l’URL WhatsApp.
- axe-core : règles WCAG 2 A/AA et 2.1 AA. Les contrastes insuffisants des composants existants ont été corrigés dans edition.css. Contrôle mobile supplémentaire sur accueil, catalogue et La Grave : aucune violation détectée.

Aucun message WhatsApp envoyé. Ces tests ne confirment pas la propriété du numéro ni la réception effective d’un message. Les contrôles automatisés d’accessibilité ne remplacent pas une recette humaine complète au clavier et avec lecteur d’écran.

## Performance et limites

Le nouveau contenu est disponible sans JavaScript. Pas de dépendance d’application ajoutée, pas d’API distante pour la recherche. HTML des pages principales : environ 9–16 ko hors compression. Les nouvelles pages utilisent un SVG local et ne nécessitent aucune photo distante. Aucun score Lighthouse ni mesure terrain n’a été établi : les feuilles de style historiques et l’animation du pied de page restent des pistes de mesure sur l’hébergement cible.

La page 404 est fournie pour éviter le repli automatique vers la page d’accueil sur l’hébergement statique. Les en-têtes Cloudflare _headers doivent être vérifiés sur une prévisualisation hébergée ; le serveur Python ne les applique pas. Les meta robots protègent déjà chaque page.

## Publication et éléments en attente

Aucun déploiement ni fusion. Aucun sitemap soumis. noindex,nofollow conservé dans les pages, complété par X-Robots-Tag et robots.txt.

Le domaine définitif doit être approuvé avant de générer les canoniques et le sitemap : voir DEVELOPMENT.md. Les titres et descriptions des six pages principales sont des propositions SEO à valider, distinctes des copies éditoriales approuvées.

Voir LOCAL_VERIFICATION.md pour les 43 références locales et les validations métier. Les avis restent un emplacement de réserve sans faux témoignage ; faire valider leur présentation avant publication.

La branche a été poussée. La création de PR via gh est bloquée par « Post https://api.github.com/graphql: Forbidden ». Le descriptif est disponible dans PR_DESCRIPTION.md. Ouvrir la PR vers main depuis :
https://github.com/bastmish/bastien-michelet-ski/pull/new/feat/ski-society-complete

Prévisualisation locale : http://localhost:3000 après lancement du serveur documenté. Aucun lien Cloudflare public n’a été généré.

## Résultat final automatisé

50 pages contrôlées aux trois largeurs (150 rendus), zéro violation axe-core sur les règles testées et zéro erreur JavaScript. Navigation mobile, recherche clavier et liens WhatsApp : PASS. Résultat machine : tests/browser-results.json. L’accueil a été recontrôlé après la dernière mise en forme des intitulés d’offres : PASS.
