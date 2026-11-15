# Recette de la correction graphique — PR #20

## Référence et contenu

Référence visuelle : main au commit bc9bb78, sans modification de cette branche.
Correction sur feat/ski-society-complete uniquement.

- Accueil : hero, diptyque photographique, galerie ADN, cartes expériences, programmes, cartes destinations, FAQ en accordéons, formulaire et animations de main réutilisés.
- Collectif : hero photographique du manifeste et composition éditoriale ; aucun profil individuel.
- Offres : hero photographique existant, cartes illustrées, méthode, formats en lignes éditoriales et panneau de réservation.
- Destinations : 43 pages avec hero photographique, portrait en deux colonnes, cartes disciplines et panneau WhatsApp. Les photos d’ambiance sont identifiées comme telles, sans attribution locale non vérifiée.
- edition.css supprimé ; les styles historiques sont conservés. integration.css contient des adaptations ciblées.
- Copies validées, métadonnées locales et messages WhatsApp conservés ; noindex,nofollow inchangé.

## Captures et comparaison

20 captures desktop (1440 px) et mobile (390 px), dans docs/visual :
référence main, proposition rejetée et intégration corrigée. L’index HTML permet de les parcourir et captures.json consigne les erreurs de chargement.

**Limite majeure :** le proxy de l’environnement refuse images.pexels.com et les polices externes. Les captures montrent donc la composition réelle avec les ressources non chargées ; aucune photographie n’a été simulée ou remplacée pour masquer ce blocage. Une validation photographique et typographique complète reste nécessaire après application des autorisations réseau. Les captures ne constituent pas une validation graphique du propriétaire.

## Contrôles

Les tests statiques vérifient les textes des 32 sections, les liens et ancres, les 43 liens de destinations, les métadonnées distinctes, les 86 CTA locaux et les formats freeride. La recherche clavier et le menu mobile sont testés par Playwright. Le formulaire ne permet plus la demi-journée en freeride et ne présume plus un nombre de participants imposé pour le coaching.

Les résultats navigateur de la correction sont dans tests/browser-results.json. Les tests automatisés ne remplacent pas la recette humaine et ne prouvent pas les droits photographiques, la propriété du numéro WhatsApp ni la disponibilité des prestations. Aucun message envoyé.

## Prévisualisation HTTPS : blocage constaté

Wrangler 4.162.0 :
- whoami : non authentifié ; aucune session locale ni variable CLOUDFLARE_API_TOKEN utilisable.
- versions upload --preview-alias review-pr20 : échec avant téléversement, jeton requis en mode non interactif.
- API Cloudflare : connexion refusée par le proxy (CONNECT 403).
- Aucun lien de prévisualisation Cloudflare obtenu ; aucune URL inventée.

Les domaines photos/polices/Cloudflare ainsi que les champs CLOUDFLARE_API_TOKEN et CLOUDFLARE_ACCOUNT_ID sont enregistrés dans le brouillon de l’environnement. La sauvegarde du brouillon ne les applique pas à la machine. L’interface exige de sauvegarder et publier l’environnement de travail, puis de renseigner les accès dans ses paramètres sécurisés. Cela ne publie pas le site.

Après application : recharger les photos, refaire les captures et les contrôles, téléverser une version de prévisualisation sans activation production, vérifier son URL HTTPS et la transmettre au propriétaire.

## Points métier

Voir LOCAL_VERIFICATION.md pour les contrôles station par station, les autorisations suisses, La Grave, les qualifications/assurances, le numéro WhatsApp et la procédure du questionnaire. Domaine canonique et photos locales restent à valider.

Aucun déploiement en production ni fusion. PR #20 conservée ouverte.

## Résultat final de la correction

- Tests statiques : PASS, y compris absence d’edition.css et présence des 43 templates photographiques.
- Playwright : 50 pages, 150 rendus à 375/768/1440 px, aucun débordement horizontal, aucune erreur JavaScript.
- axe-core : aucune violation détectée pour les règles WCAG 2 A/AA et 2.1 AA testées. Résultat final dans tests/browser-results.json.
- Formulaire : tests/booking_check.py PASS pour l’exclusion du freeride demi-journée et l’adaptation d’une sélection existante.
- Captures : 20 vues à 390/1440 px, aucun débordement ; 266 occurrences d’images non chargées dans l’ensemble des captures (plusieurs vues réutilisent les mêmes photos).
- Wrangler versions upload --dry-run : PASS. Ce contrôle ne téléverse rien et ne fournit aucune URL publique.
- git diff --check : PASS.

Les résultats d’accessibilité et de géométrie restent limités au rendu disponible sans les photos et polices externes. Il faut refaire la validation visuelle complète une fois l’accès appliqué.
