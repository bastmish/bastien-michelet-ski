# LOT 1 — Fondations CSS

Branche : `refactor/css-foundations-lot1`, issue de `audit/design-refactor-plan` au commit audité `5bd9206` (site : parent `3da8cd1`). Périmètre : sources CSS, compilation et contrôles de non-régression. Aucun travail graphique du lot 2 n'est activé.

## Architecture livrée

- `styles/design-tokens.json` : registre unique des couleurs, familles typographiques, corps, graisses, espacements, conteneurs et conditions responsive. Les rôles sémantiques sont séparés des valeurs `compat-*` héritées. Les variantes anciennes restent présentes pour conserver le rendu ; ce lot ne normalise pas graphiquement les 867 anciennes nuances/alphas. Les quatre couleurs propres aux pages légales sont également référencées.
- `styles/entries.json` : ordre explicite des dépendances et classes injectées par les scripts. Neuf familles isolées : accueil, collectif, prestations, index prestations, catalogue, catalogue alternatif, fiches destinations, légal, erreur.
- `styles/components/` : ADN, expériences/formats, header accueil, réservation, bandeau Destinations, footer.
- `styles/themes/home.css` : thèmes existants des sections ; couleurs alimentées par le registre.
- `styles/layout/home.css` : largeur extérieure et conteneurs intérieurs existants.
- `styles/pages/` : collectif, destinations et légal. Le même bloc CSS auparavant intégré aux quatre pages légales est extrait une seule fois.
- `styles/compatibility/` : adaptations éditoriales, responsive hérité et anciennes transitions isolées. Leur suppression visuelle attend le lot 2.
- `styles/chapters.json` : contrat des cinq chapitres et invariants des futures transitions : fond sur wrapper extérieur, conteneur intérieur, aucune nouvelle photographie, aucune hauteur de raccord ajoutée, aucune géométrie dépendante du chargement d'image. Ce contrat n'active aucun nouveau rendu.
- `scripts/css_build.py` : compilation déterministe, suppression conservative de sélecteurs inapplicables à une famille et de déclarations supplantées pour le même sélecteur/propriété/condition. Les états dynamiques, pseudo-classes fonctionnelles et sélecteurs non interprétés sont conservés.
- `public/assets/css/` : deux liens CSS par page, tokens communs + bundle de famille portant une empreinte de contenu. `manifest.json` indique les dépendances, mesures et chaque règle écartée avec fichier/ligne/sélecteur. Ne pas éditer ces sorties.

L'ordre et les priorités historiques sont conservés. Une expérimentation de conversion des `!important` en couches de cascade a été **écartée** : les captures révélaient des bordures décalées d'un pixel malgré des valeurs calculées identiques. La version finale ne l'active pas. Aucun nouveau `!important` correctif n'a été ajouté.

Six feuilles historiques restent des **sources de compilation protégées**, sans lien direct HTML : `styles.css`, `white-theme.css`, `architecture-v21.css`, `site-nav.css`, `stations.css`, `manifesto.css`, dans `public/`. Leurs déclarations utiles sont sélectionnées par famille. Treize attributs `style` historiques restent inchangés (cinq fonds, huit marges), car des sélecteurs hérités dépendent de leurs chaînes littérales ; ce reliquat de compatibilité est explicite, pas un second système de thème. Leur découpage sémantique complet reste une dette explicite ; elles ne sont pas supprimées.

Huit autres feuilles sont remplacées dans le chemin actif par leurs modules sources : `adn-editorial.css`, `course-formats.css`, `home-system.css`, `booking-v3.css`, `editorial-content.css`, `premium-footer.css`, `story-home.css`, `integration.css`. Les huit fichiers originaux restent inchangés sur disque. Les huit feuilles déjà dormantes au moment de l'audit restent également inchangées. Aucun ancien fichier CSS n'est supprimé.

## Mesure de la cascade

Voir [les mesures détaillées](css-metrics.json) et le manifeste de compilation. Les listes de sélecteurs séparés par des virgules sont développées **des deux côtés** : les nombres sont comparables entre eux mais diffèrent du comptage brut du rapport d'audit (977 occurrences textuelles sur l'accueil).

| Famille | Déclarations avant → après | `!important` avant → après | Répétitions exactes avant → après |
|---|---:|---:|---:|
| Accueil | 6654 → 2390 | 1372 → 563 | 542 → 0 |
| Collectif | 5693 → 1485 | 1241 → 478 | 538 → 0 |
| Prestations | 5674 → 1024 | 1238 → 259 | 538 → 0 |
| Index prestations | 5623 → 804 | 1235 → 203 | 533 → 0 |
| Catalogue | 3655 → 1175 | 1024 → 275 | 369 → 0 |
| Catalogue alternatif | 3948 → 1192 | 1075 → 283 | 370 → 0 |
| 43 fiches destinations | 6350 → 855 | 1288 → 201 | 544 → 0 |
| Légal | 2981 → 643 | 951 → 195 | 269 → 3 |
| Erreur | 6350 → 711 | 1288 → 197 | 544 → 0 |

Sur l'accueil : 1494 sélecteurs écartés de ce bundle et 219 déclarations explicitement supplantées supprimées, soit 64 % de déclarations et 59 % de priorités en moins, à méthode de comptage constante. Les 127 `!important` présents dans les modules extraits sont des priorités héritées, pas de nouveaux correctifs.

Une « répétition exacte » désigne la même propriété du même sélecteur dans la même condition. Cela ne mesure pas toutes les interactions entre sélecteurs de spécificités différentes ni entre raccourcis et propriétés détaillées. Les trois répétitions légales restantes conservent une priorité historique antérieure à une déclaration normale. Les priorités restantes ne sont pas prétendues toutes résolues.

## Build et sources réelles

```sh
python -m pip install -r requirements-build.txt
python scripts/build.py
python scripts/build.py --output-dir /tmp/ski-clean
python tests/check_css_contract.py
python tests/check_editorial.py
python tests/check_site.py
python tests/lot1_sources.py
python tests/lot1_build.py
python tests/lot1_css_metrics.py
```

`build.py` et `editorial.py` écrivent dans le dossier de sortie demandé. Un dossier vide est alimenté avec les ressources statiques sources conservées, puis les HTML et CSS sont reconstruits. Les anciens HTML générés et les bundles préexistants ne sont pas nécessaires. Les ressources statiques encore situées dans `public/` sont des entrées gelées et protégées par empreintes, explicitement conservées jusqu'à migration.

Résultat : **deux sorties vides et `public/` identiques, fichier par fichier, sur 109 fichiers**. Empreintes dans [build.json](build.json). Dépendances Python de build épinglées ; navigateur et dépendances QA séparés dans `requirements-qa.txt`. Le build n'exige aucun accès aux photographies ou polices distantes.

## Non-régression

- Vérification de 130 contrats de sources/ressources/HTML : tous les fichiers `content/`, les CSS originaux, JavaScript, URL des images, liens, formulaires et métadonnées restent inchangés. Les différences HTML autorisées concernent seulement les liens CSS et l'extraction du bloc `<style>` légal.
- Les six pages principales, 32 sections sources et 43 fiches destinations passent les contrôles existants. Les adaptations éditoriales/condensations déjà présentes dans l'état audité ne sont pas réécrites pendant ce lot.
- Tous les liens internes, ancres, H1, métadonnées destinations et 86 CTA locaux passent. `noindex,nofollow` reste présent sur les 61 HTML, y compris les quatre redirections inchangées. Aucun sitemap n'est créé ni soumis.
- Parcours WhatsApp : validations des deux étapes, erreurs associées aux champs, aller-retour avec conservation des valeurs, autre station, les 43 stations, préremplissage URL, participants entiers positifs sans maximum arbitraire, champs optionnels, encodage accents et caractères spéciaux. Demi-journée réellement retirée en freeride et rétablie pour les autres disciplines.
- L'ouverture WhatsApp est interceptée par le test : aucun message n'est envoyé. Le JavaScript métier est protégé octet pour octet.
- Navigation mobile, FAQ ouverte, recherche accent-insensible des deux catalogues, réinitialisation, filtres et navigation d'une suggestion vers Méribel : PASS. Le test respecte le comportement existant qui ouvre directement une fiche après choix d'une suggestion.
- Axe : quatre scans du bloc réservation (deux étapes × desktop/mobile), aucune violation dans ce périmètre. Ce résultat n'est pas un audit d'accessibilité complet du site.
- Cas de sécurité du compilateur : classes dynamiques, `:not`, `:is`, `:has`, focus, priorités face aux attributs inline et animations : PASS.

Pour reproduire les captures, servir le `public/` de `5bd9206` dans un serveur local de référence et le `public/` courant dans un deuxième serveur, puis :

```sh
python -m pip install -r requirements-qa.txt
python tests/lot1_visual.py --before http://127.0.0.1:3090 --after http://127.0.0.1:3091 --output /tmp/ski-comparison
python tests/lot1_functional.py --url http://127.0.0.1:3091 --output /tmp/ski-functional --axe /chemin/axe.min.js
python tests/lot1_css_safety.py
```

Chromium doit être disponible à `/usr/bin/chromium`. Axe est facultatif dans le script ; la recette livrée l'a exécuté avec axe-core installé dans l'environnement. Ces URL sont des points d'entrée de test locaux, pas des prévisualisations publiques.

Rapport fonctionnel : [functional.json](functional.json). Les contrôles fonctionnels ont également été exécutés sur la référence avant modification.

## Comparaisons visuelles et limites

Les comparaisons couvrent les **57 routes habillées × 1440 et 390 px**, soit 114 paires, dont les six principales et les 43 destinations. Même Chromium, même taille, mouvement réduit, défilement préalable pour déclencher le lazy loading. Aucun remplacement des photographies ni substitution de polices dans le test. Les quatre redirections sont contrôlées par les contrats de sources.

**Résultat final : 113/114 paires strictement identiques, aucune différence dans les vecteurs de géométrie/styles contrôlés, aucun débordement horizontal, aucune erreur JavaScript. Les 98 cas des six pages principales et des 43 destinations sont tous identiques pixel par pixel.** Le seul écart résiduel concerne `stations.html` à 390 px : 246 pixels dans la zone `[21, 3221, 369, 3590]`, écart maximal de 2/255 par canal, sans décalage de géométrie. Cet écart de peinture est consigné, pas masqué. Les six comparaisons supplémentaires de FAQ ouverte et de formulaire aux deux étapes sont strictement identiques ([rapport](interaction-visual.json)).

Les résultats définitifs et empreintes des captures sont dans [visual-results.json](visual-results.json). Les captures pleine page conservées couvrent les six pages principales et trois destinations représentatives (Méribel, La Grave, La Dôle), dans les deux tailles, avant/après. Les autres captures ont été analysées ; leurs empreintes et mesures sont conservées dans le rapport.

[Planche desktop](comparison-1440.jpg) · [Planche mobile](comparison-390.jpg) · [Captures détaillées](CAPTURES.md).

**Limite bloquante pour la recette photographique et typographique** : `images.pexels.com`, `fonts.googleapis.com` et `api.fontshare.com` ne sont pas accessibles dans cet environnement. Les captures montrent les états de repli réellement obtenus, avec des photographies absentes et des polices système. Les cadrages, masques, fondus conditionnés au succès des médias et métriques des polices distantes ne sont donc **pas validés**. Aucun résultat avec ces médias chargés n'est revendiqué. La liste exacte des requêtes en échec figure dans le rapport visuel. Les polices servies par `fonts.gstatic.com` ne peuvent pas être évaluées lorsque leur feuille Google Fonts est bloquée.

La comparaison est effectuée sur Chromium uniquement. Le mouvement réduit neutralise les animations pendant les captures ; leur comportement temporel complet et les autres moteurs de navigateur restent à vérifier. Les ressources historiques et scripts d'interaction sont conservés.

## Fin du lot

Inventaire exact : [FILES.md](FILES.md). Aucun changement de `main`, aucune fusion de la PR #20, aucun déploiement. L'architecture des futurs chapitres est préparée, mais les compositions actuelles, y compris les transitions héritées, sont conservées. Le lot 2 attend une nouvelle autorisation.
