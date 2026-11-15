# Recette Ski Society — deuxième passe design

## Périmètre

Référence artistique : main (bc9bb78), sans modification de cette branche.
Branche corrigée : feat/ski-society-complete.
Avant/après de cette passe : commit 5a9cc1f et nouvelle composition.
Détail des décisions et des sections : DESIGN_PASS2.md.

Six pages principales et 43 destinations conservées. Les copies validées restent dans content/pages.json et content/stations.json, sans changement. La FAQ validée est désormais pré-rendue dans public/questions.html et accessible depuis le footer. Les programmes restent intégralement dans un volet de la home. Les textes ne sont pas injectés par JavaScript.

## Contrôles reproductibles

- `PYTHONPATH=/tmp/ski-libs python scripts/build.py` dans cette machine ; installation reproductible dans DEVELOPMENT.md.
- `python tests/check_site.py` : copie des 32 sections (dont la FAQ déplacée), liens/ancres, robots, un H1 par page, 43 destinations, métadonnées locales distinctes, 86 CTA locaux, formats freeride et nouveau footer unique sur chaque page non redirigée.
- `AXE_SCRIPT=/chemin/axe.min.js python tests/browser_check.py` : 51 pages à 375/768/1440 px ; menu mobile, volet Programmes, recherche clavier « Meribel », URL WhatsApp et règles axe-core WCAG 2 A/AA, 2.1 AA.
- `python tests/booking_check.py` : ouverture du formulaire facultatif, exclusion du freeride demi-journée, correction d’une sélection précédente et demande de coaching sans restriction de participants inventée.
- `python tests/design_pass2.py` : 20 captures avant/après et détails aux largeurs 1440 et 390 px.
- `git diff --check`.

Le test de navigation remet la page en haut après utilisation des programmes : la navigation de référence se masque volontairement pendant la descente et se révèle à la remontée. Aucun changement de ce comportement n’a été introduit pour faire passer le test.

Les résultats finaux sont dans tests/browser-results.json et docs/visual-pass2/captures.json.

## Captures et comparaison

Ouvrir docs/visual-pass2/index.html.
Trois types de pages comparés : accueil, collectif et destination Courchevel, sur ordinateur/mobile. Captures complémentaires du pré-footer, du footer fonctionnel, des programmes dépliés et de la FAQ.

Mesures de la home, volets fermés :
- 1440 px : 9100 → 7215 px (environ −21 %).
- 390 px : 13235 → 9402 px (environ −29 %).

Limite : le proxy refuse encore les photographies Pexels et les polices externes. Les captures montrent la vraie composition avec les ressources absentes ; elles ne constituent pas une validation photographique/typographique complète. Les défauts de chargement sont enregistrés, pas masqués. Les droits et la pertinence locale des photos restent à vérifier.

## Prévisualisation Cloudflare

Tentative réelle avec Wrangler 4.162.0 :
`wrangler versions upload --preview-alias review-pr20 --message "Design pass 2 - preview only"`

Échec avant téléversement : variable CLOUDFLARE_API_TOKEN absente en mode non interactif ; aucune session Wrangler disponible. Le réseau de la machine ne dispose toujours pas des domaines photos/polices/Cloudflare. La configuration enregistrée précédemment est un brouillon et n’est pas appliquée.

Aucune URL HTTPS publique obtenue ou inventée. Reprise après application des accès et connexion Cloudflare : refaire la recette avec les photos/polices, téléverser une version de prévisualisation, puis vérifier l’URL retournée et les en-têtes robots. Ne pas utiliser un déploiement de production.

## Garanties et validations restantes

Aucun envoi de message WhatsApp, aucun paiement, aucune soumission de sitemap, aucune activation de l’indexation. noindex,nofollow conservé partout. Aucun déploiement en production ni fusion de PR.

Les contrôles automatisés ne remplacent pas une recette humaine au lecteur d’écran ni la validation graphique du propriétaire. Voir LOCAL_VERIFICATION.md : couverture réelle des destinations, qualifications/assurances, autorisations suisses, La Grave, numéro WhatsApp, questionnaire après confirmation et domaine canonique restent à vérifier.

## Résultat final

- Intégrité éditoriale et contrôles statiques : PASS ; fichiers sources pages.json et stations.json inchangés.
- 51 pages, 153 rendus à trois largeurs : PASS, aucun débordement.
- axe-core : zéro violation détectée sur les règles testées ; zéro erreur JavaScript.
- Volet Programmes, menu mobile, recherche clavier et lien WhatsApp contextualisé : PASS.
- Formulaire facultatif et formats freeride : PASS.
- 20 captures comparatives et de détail enregistrées.
- Vérification des espaces et du patch Git : PASS.
- Prévisualisation Cloudflare : bloquée avant téléversement ; aucune URL publique obtenue.
