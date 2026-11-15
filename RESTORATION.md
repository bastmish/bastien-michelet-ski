# Restauration exacte de Ski Society

Référence : bc9bb78. Branche de travail : feat/ski-society-complete.
Aucune modification de main, aucune fusion de PR #20, aucun déploiement en production.

## Pages originales

Les 16 pages HTML présentes dans public/ au commit de référence sont restaurées depuis des snapshots exacts dans content/original-pages/. Les seuls changements autorisés sont le remplacement du footer et de ses propres liens CSS/JS. Les fichiers ne sont pas réécrits par un sérialiseur HTML.

Les 25 ressources originales (CSS, JavaScript, images, données) sont restaurées octet pour octet. Cela inclut app.js, stations-search.js, les animations, la palette et les composants de navigation. Aucun style de la refonte n’est chargé par les pages originales.

Les anciens textes, compositions et comportements sont intentionnellement restaurés, y compris le formulaire, les programmes, la FAQ et les libellés de navigation. Les textes éditoriaux validés restent inchangés dans content/pages.json, sans réinjection automatique.

## Exception : nouveau footer

Le pré-footer photographique, la signature et le CTA WhatsApp sont suivis d’une navigation à cinq rubriques, des liens légaux et d’un mot-symbole Ski Society.

Le HTML est isolé dans content/premium-footer.html ; premium-footer.css ne cible que ses propres classes. Aucun sélecteur de cette feuille ne redessine le body, le header, le main ou leurs composants. Le footer réutilise une photographie alpine déjà présente dans le site et les ressources typographiques existantes. Elle reste une illustration, pas une photo identifiée d’une destination ou d’un moniteur.

## Extension destinations

- Les 43 fiches, leurs textes locaux, métadonnées et deux CTA WhatsApp principaux sont conservés.
- /destinations.html est le nouvel index de l’extension, relié depuis le nouveau footer.
- /stations.html, ses anciennes cartes et sa recherche retrouvent exactement le comportement original. Elles ne sont pas modifiées pour exposer l’extension.
- destinations-search.js appartient à l’extension ; stations-search.js est l’original exact.
- La FAQ supplémentaire de la refonte est retirée : la FAQ originale est de nouveau sur la home.
- Aucun changement de noindex,nofollow ni soumission de sitemap.

## Vérification de l’identité

tests/check_site.py vérifie :
- identité littérale des 16 pages hors footer et ressources propres au footer ;
- SHA-256 des 25 ressources d’origine ;
- intégrité SHA-256 des deux fichiers sources éditoriaux ;
- liens, ancres, robots, H1, 43 contenus locaux et métadonnées, 86 CTA spécifiques.

Les comparaisons visuelles couvrent les six pages principales et stations.html à 1440 et 390 px :
**14 paires identiques pixel par pixel dans la zone main, hors footer.**
Les références proviennent d’un git archive de bc9bb78, sans checkout ni modification de main.

Rapport : docs/restoration/index.html.
Données : docs/restoration/comparison.json.
32 captures : 28 images avant/après et quatre détails du nouveau footer.

Les deux côtés sont capturés dans les mêmes conditions : mouvement réduit, animations/transitions figées pour le test, défilement automatique désactivé uniquement dans le navigateur de test. La capture reste strictement dans main afin de ne pas inclure une ligne arrondie du footer différent. Les styles et animations du site livré ne sont pas modifiés pour la comparaison.

**Limite :** le proxy refuse toujours les photos Pexels et les polices distantes. Les captures ne remplacent pas ces ressources. L’identité du code et des URLs est vérifiée ; les captures établissent l’identité du rendu disponible dans cet environnement, pas une validation complète avec les photos et polices chargées.

## Recette et suite

51 pages et 153 rendus responsive contrôlés, aucune erreur JavaScript ni débordement horizontal. Menu, FAQ, formulaire et recherche d’origine testés ; recherche de l’extension vers Méribel et URL WhatsApp testées sans envoyer de message. Aucune violation axe-core détectée dans le footer fonctionnel. Les observations d’accessibilité du reste du site sont consignées, pas corrigées sur les pages originales pour ne pas altérer la restauration.

La prévisualisation publique demeure dépendante d’un accès Cloudflare et des domaines réseau appliqués à la machine. Aucun lien public n’a été créé et aucune commande de production n’a été exécutée.

Les anciennes captures et notes DESIGN_PASS2.md sont des archives de la direction abandonnée. Le présent document, QA_IMPLEMENTATION.md et DEVELOPMENT.md décrivent l’état courant.
