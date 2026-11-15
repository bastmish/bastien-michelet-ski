# Étape 1 — accueil et footer uniquement

Brief de référence enregistré sans modification : docs/ARCHITECTURE_REQUIRED.md.

## Périmètre réalisé

La proposition est limitée à public/index.html et sa nouvelle feuille home-review.css.
Le générateur construit ensuite cette proposition via scripts/home_review.py, après les pages existantes, pour éviter toute propagation involontaire.

- Les huit sections A01–A08 restent présentes, sans suppression ni déplacement de FAQ.
- Toutes les copies validées restent mot pour mot ; le contrôle global des 32 sections passe.
- ADN : une grande photographie sur deux rangées, deux autres panneaux à droite ; sur mobile, trois hauteurs distinctes. Photos et composants historiques réutilisés.
- Expériences : quatre grandes cartes conservées ; Performance plus large et plus haute, badge validé conservé.
- Programmes : composition en lignes préservée ; les trois créneaux sont affichés à partir de la copie FAQ déjà approuvée, sans texte inventé.
- Destinations, avis réservés, six accordéons FAQ et contact WhatsApp conservés.
- Nouveau pré-footer : photographie sportive historique en grand format, signature et CTA.
- Nouveau footer fonctionnel : logo historique, navigation et liens indispensables, informations légales conservées.
- Aucune modification visuelle des autres pages publiques à cette étape.

Le nouveau footer n’est pas encore appliqué aux 49 pages : cette généralisation attend la validation de la proposition de l’accueil, conformément à la dernière instruction du brief.

## Contrôles passés

- tests/check_editorial.py : 32/32 sections et sources immuables.
- tests/check_site.py : liens, ancres, robots, H1, 43 destinations, métadonnées et 86 CTA spécifiques.
- tests/home_review.py : 375/768/1440 px, huit sections, compositions ADN distinctes, quatre offres, trois formats et trois créneaux, six questions, navigation mobile, transitions de chapitres, exclusion du freeride demi-journée, aucun débordement ni erreur JavaScript.
- Footer fonctionnel : aucune violation axe-core détectée pour les règles WCAG testées.
- git diff --check : PASS.
- main inchangée ; noindex,nofollow maintenu ; aucune fusion ni mise en production.

## Contrôle obligatoire bloqué

tests/home_review.py retourne volontairement **2** : les photographies ne sont pas chargées. La validation photographique obligatoire n’est donc pas réussie.

Résultat réel : 0 photographie chargée sur 16 pour chacune des trois largeurs. L’accès HTTPS à images.pexels.com échoue avec CONNECT 403 depuis le proxy. Les polices distantes sont également refusées.

Le brouillon de configuration, révision 2, contient déjà les domaines requis (images.pexels.com, fonts.googleapis.com, fonts.gstatic.com, api.fontshare.com, cdn.fontshare.com). La machine active n’a toujours aucun domaine personnalisé autorisé. Un enregistrement de brouillon ne constitue pas une application à la machine.

Les fichiers provisional-*.png et index.html sont des diagnostics identifiés comme tels. Ils ne satisfont pas et ne sont pas présentés comme le livrable « captures avec photographies correctement chargées ».

## Reprise

1. Appliquer/sauvegarder les domaines préparés dans les paramètres puis publier l’environnement de travail si l’interface l’exige. Cette opération ne déploie pas le site.
2. Vérifier l’accès réel aux photos et polices.
3. Relancer tests/home_review.py et produire les véritables captures chargées.
4. Soumettre l’accueil et le footer à validation visuelle.
5. Seulement après validation, appliquer les composants approuvés aux autres pages et généraliser le footer aux 49 pages, puis effectuer la recette globale.

Aucune approbation visuelle n’est présumée.
