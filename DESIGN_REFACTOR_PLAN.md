# Ski Society — Audit et plan de reprise du design

**Phase 1 : diagnostic soumis à validation, sans modification graphique.**

- Date : 17 novembre 2026, Europe/Zurich.
- Branche de cet audit : `audit/design-refactor-plan`, créée depuis `feat/ski-society-complete`.
- État audité : `3da8cd158c5bb40d07e04ba1ae3af4696bcbf750`.
- Référence historique : `bc9bb78e4214f8ddbede9321cef0771240f5025d`.
- Ce livrable ajoute uniquement ce document. Aucun fichier HTML, CSS, JavaScript, contenu éditorial ou configuration de publication n’est modifié.

## 1. Diagnostic principal

Le site ne manque pas d’un correctif supplémentaire. Il juxtapose plusieurs systèmes de présentation : composants historiques, anciennes palettes au scroll, nouvelles classes de thèmes, nouvelles compositions et corrections locales prioritaires.

La dette est en partie **antérieure à la mission** : les 14 feuilles CSS déjà présentes dans `bc9bb78` sont encore identiques à ce commit. Les ajouts récents n’ont pas remplacé ce socle ; ils l’ont surchargé. Cela explique pourquoi une modification locale nécessite fréquemment un sélecteur plus spécifique ou un nouvel `!important` et pourquoi les pages secondaires ne suivent pas les mêmes conventions que l’accueil.

Les problèmes à traiter en priorité sont :

1. Une cascade à propriétaires multiples : palettes, typographies et espacements définis dans plusieurs fichiers.
2. Des transitions de nature différente : thème historique au scroll, thèmes fixes, images conditionnelles et bande de dégradé autonome.
3. Des compositions dont la hauteur dépend du chargement de photographies décoratives.
4. Des largeurs et gouttières incohérentes entre composants, malgré un système pleine largeur désormais explicite.
5. Un générateur qui conserve les anciens composants puis les transforme/remplace, au lieu de rendre chaque composant depuis une source unique.
6. Une recette technique fragmentée par versions, qui ne constitue pas une validation de direction artistique.

**Point important :** à 1440 et 390 px, les wrappers de Destinations, Avis, FAQ et Réservation occupent effectivement toute la largeur dans l’instance locale auditée. Je n’ai pas reproduit de marge latérale blanche à ces tailles. Le diagnostic actuel ne doit donc pas réduire tous les défauts visuels à un problème de `max-width` : les raccords, la densité et les surcharges restent problématiques même avec des fonds pleine largeur.

## 2. Méthode et limites de l’audit

### Contrôles effectués sans modifier le site

- Inventaire et analyse syntaxique des **22 fichiers CSS** de `public/`, incluant les règles sous `@media` et `@supports`.
- Inventaire des chargements CSS dans les **61 pages HTML** générées, des imports CSS et des composants de l’accueil.
- Comparaison Git des fichiers et du DOM avec `bc9bb78`, sans modifier ni changer la branche `main`.
- Inspection Chromium de l’état courant et de la référence à **1440×900 et 390×844**, avec styles calculés, géométrie, états des médias et captures temporaires hors du dépôt.
- Vérification des empreintes éditoriales protégées : inchangées. Répartition des sections : **8 + 4 + 5 + 5 + 5 + 5 = 32** ; **43 destinations** dans les données.
- Exécution en lecture seule de `python tests/check_site.py` : liens, ancres, H1, robots, contenu/métadonnées des 43 destinations et 86 CTA locaux contrôlés avec succès.
- Aucun défaut syntaxique de règle/déclaration CSS détecté par le parseur utilisé. Le problème observé est surtout architectural ; cela ne certifie pas chaque comportement CSS sur tous les navigateurs.

### Limites à ne pas masquer

Les requêtes vers `images.pexels.com`, `fonts.googleapis.com` et `api.fontshare.com` échouent dans cette instance. Les deux calques immersifs restants sont `unavailable`, masqués, avec `naturalWidth=0`. Les mesures ci-dessous décrivent donc le **mode sans ces médias chargés**, avec les polices de repli ; elles ne valident ni les cadrages photographiques ni le rendu typographique final.

Aucune photographie de substitution et aucune simulation de succès de chargement n’ont été utilisées. L’audit de code et le plan sont réalisables ; la validation visuelle finale des futurs lots devra se faire avec les vraies ressources accessibles. Les rapports précédents de tests ne valent pas acceptation du design par le propriétaire.

## 3. Inventaire complet des feuilles CSS

Sur l’accueil, l’ordre effectif est :

`styles.css → white-theme.css → architecture-v21.css → site-nav.css → adn-editorial.css → course-formats.css → home-system.css → booking-v3.css → editorial-content.css → premium-footer.css`.

S’ajoutent la feuille Google Fonts et l’import Fontshare dans `site-nav.css:1`.

Le comptage statique des déclarations de règles de style donne **977 `!important` sur les 5 881 déclarations des dix feuilles locales chargées sur l’accueil**. `site-nav.css` en contient 621 et `architecture-v21.css` 265. Ces deux fichiers sont historiques, pas de nouveaux fichiers de la refonte. `home-system.css` ajoute à lui seul 70 déclarations prioritaires.

Méthode : commentaires exclus, règles conditionnelles incluses ; déclarations de keyframes/font-face et feuilles distantes non incluses. Ces nombres indiquent la complexité de la cascade, pas le nombre de défauts visibles ou de règles effectivement appliquées à un instant donné.

| Fichier dans `public/` | Lignes | `!important` | Chargement courant | Diagnostic et destination proposée |
| --- | ---: | ---: | --- | --- |
| `styles.css` | 459 | 3 | Accueil et 56 autres pages | Socle historique utile, mais mêle reset, composants anciens, `.wrap`, boutons et `footer` générique. Extraire les fondations et scoper les composants. |
| `white-theme.css` | 51 | 1 | Accueil et 56 autres pages | Ancienne recoloration globale de body, hero, formulaires et pages secondaires. Remplacer ses effets actifs par des thèmes explicites ; ne plus charger une palette corrective. |
| `architecture-v21.css` | 1805 | 265 | Accueil et 50 autres pages | Plusieurs générations V21–V52. Réservoir de compositions utiles et de règles obsolètes. Extraire les composants retenus ; ne pas supprimer globalement avant migration des pages secondaires. |
| `site-nav.css` | 1199 | 621 | Accueil et 56 autres pages | Son nom masque un thème global V42–V76 : navigation, hero, typographie, palettes, sections, formulaires. Séparer navigation, typographie, thème et héritage. |
| `adn-editorial.css` | 45 | 3 | Accueil seulement | Composition autonome avec masque photographique et largeurs propres. Reprendre l’ADN dans le système commun ; conserver les textes et la photo pertinente. |
| `course-formats.css` | 51 | 8 | Accueil seulement | Ensemble compact Expériences/Formats plutôt bien isolé. Conserver sa compréhension et ses liens ; intégrer grille, boutons, typo et espacements au socle. |
| `home-system.css` | 132 | 70 | Accueil seulement | Mélange thèmes, header, réservation initiale, correctif pleine largeur et bandeau Destinations. Redistribuer dans les fichiers de responsabilité unique. |
| `booking-v3.css` | 71 | 4 | Accueil seulement | Surcharge la réservation et gère aussi les transitions globales. Séparer présentation du formulaire et raccords de chapitres ; retirer les calques photographiques parasites. |
| `editorial-content.css` | 24 | 2 | Six pages principales | Adaptations de copie et variantes d’offres. Plusieurs règles sont utiles, une couleur d’introduction Avis se contredit immédiatement. Intégrer les besoins réels aux composants. |
| `premium-footer.css` | 45 | 0 | 57 pages | Bonne base de composant isolé. Garder navigation, légal et signature ; consolider tokens, typo, photo et espacements. |
| `story-home.css` | 13 | 3 | `manifesto.html` | Colle le collectif à des anciens composants de home. Remplacer par un vrai gabarit collectif simple, sans couplage au DOM de l’accueil. |
| `integration.css` | 137 | 37 | 45 pages : 43 fiches, catalogue alternatif et 404 | Mélange règles d’anciennes intégrations et composants réellement utilisés par les fiches. Scinder destinations/404 et retirer les sélecteurs de home inutiles sur ces routes. |
| `manifesto.css` | 137 | 2 | 43 fiches destinations et 404 | Ancien manifeste, non chargé par le collectif actuel. Son `body` et son vocabulaire visuel servent de dépendance aux fiches. Retirer cette dépendance après extraction des styles nécessaires. |
| `stations.css` | 228 | 67 | `stations.html`, `destinations.html` | Catalogue et recherche utiles ; contient aussi des retouches de header. Garder la recherche, déplacer les styles de navigation et aligner les tokens. |
| `about-editorial.css` | 277 | 1 | Non chargé | Ancienne page histoire, candidate à archivage après vérification des références. Ne cause pas la cascade active de l’accueil. |
| `alpine-map.css` | 418 | 1 | Non chargé | Anciennes cartes interactives et nombreux breakpoints. Archiver si aucune réutilisation décidée. |
| `society-map.css` | 241 | 10 | Non chargé | Autre système de carte et pseudo-éléments. Même traitement, sans réintroduction décorative. |
| `territories.css` | 94 | 0 | Non chargé | Ancien chapitre territoires. Archiver les variantes inutilisées. |
| `scroll-story.css` | 31 | 0 | Non chargé | Ancienne timeline sticky. Garder éventuellement les principes de rythme, pas une dépendance morte. |
| `ridgeline-footer.css` | 20 | 0 | Non chargé | Ancien footer animé remplacé par le premium. Archiver ; ne pas restaurer automatiquement le canvas. |
| `palette-carbon-ice.css` | 73 | 61 | Non chargé | Expérience de palette, pas une cause active du rendu actuel. Archiver hors du chemin de production. |
| `palette-midnight-cobalt.css` | 77 | 67 | Non chargé | Expérience de palette cobalt. Ne pas réactiver ; contraire au cadre sobre retenu. |

« Non chargé » signifie absent des liens HTML générés et des imports CSS locaux ; aucun chargeur CSS dynamique correspondant n’a été détecté dans les scripts inspectés. Des références historiques restent dans les sources originales. **Archiver n’est pas supprimer maintenant.**

## 4. Problèmes précis : fichiers, sélecteurs et conséquences

### 4.1 Cascade, typographie et règles prioritaires

| Référence | Constat précis | Intervention prévue |
| --- | --- | --- |
| `styles.css:2`, `site-nav.css:435` | `--display` passe de Manrope à DM Sans. Les nouveaux composants choisissent souvent Clash Display en ajoutant des exceptions. Trois conventions de titre coexistent. | Deux rôles typographiques explicites : interface/texte et titres éditoriaux. Un seul propriétaire par rôle ; vérifier les licences avant éventuel auto-hébergement. |
| `site-nav.css:439`, `site-nav.css:445` | `body p`, `body button`, puis tous les `h1/h2/h3` reçoivent des familles, graisses et espacements `!important`. Les composants spécifiques et même les titres de footer doivent les combattre. | Retirer ces prescriptions globales du bundle migré, après extraction des styles nécessaires. Typographie définie au composant ou par classe de rôle. |
| `adn-editorial.css:10`, `course-formats.css:5`, `home-system.css:29` | Les titres ont besoin de nouveaux `!important` pour retrouver leur famille/poids face au sélecteur global. | Supprimer la cause et les contre-règles ensemble ; ne pas retirer seulement le `!important` local, ce qui rétablirait la mauvaise graisse. |
| `site-nav.css:647`, `site-nav.css:743`, `site-nav.css:1139` | `.ss-architecture .ss-reviews-v52` est blanc, puis blanc à nouveau, puis sombre via `background-color` et texte clair ; d’autres règles dépendent de `.ski-reviews-light`. `home-system.css:5` et `:12` réimposent ensuite le blanc. | Une seule surface de thème Avis/FAQ ; supprimer les définitions historiques concurrentes du bundle migré. |
| `editorial-content.css:5`, `:6`, `:7` | `.ss-reviews-heading>p` reçoit `color:inherit`, puis immédiatement `#c4c9c9`, puis une exception au scroll. Une autre exception de home corrige sa lisibilité. | Une seule couleur de texte secondaire dans un chapitre blanc ; conserver la rédaction. |
| `home-system.css:40`, `booking-v3.css:27` | Même barre : hauteur 2 puis 3 px, fond gris différent, progression noire puis verte. | Définition unique dans le composant réservation, avec les valeurs réellement retenues. |
| `home-system.css:27`, `booking-v3.css:15` | Deux grilles de réservation : `.85/1.15`, puis `.42/.58`, avec plusieurs règles tablette/mobile. | Un composant, une grille et ses adaptations ; garder les identifiants nécessaires au formulaire. |
| `home-system.css:39` | `#private-step-indicator` conserve `white-space:nowrap`, prévu pour « 01 / 02 », alors que V3 affiche une phrase. | Autoriser le retour à la ligne ; vérifier petite largeur, français et zoom 200 %. C’est un risque de reflow, pas un débordement démontré à 390 px. |
| `premium-footer.css:26`, `:29` | `.art-footer-signature` reçoit deux couleurs successives. | Supprimer la première déclaration devenue sans effet ; garder la couleur finalement validée. |
| `styles.css:180` | `footer` est stylé globalement avec fond/padding. Toute utilisation sémantique d’un footer de sous-section peut reprendre une boîte sombre involontaire. | Réserver ces styles à `.site-footer`/au composant premium, pas au nom de balise. |

#### Quels `!important` sont devenus inutiles ?

- **Doublon démontré :** le `background:#fafaf8!important` de `.ss-architecture .ss-reviews-v52` à `site-nav.css:647` est redéfini par le même sélecteur et la même valeur à `:743`, sans condition différente. La première déclaration est redondante ; ce constat n’autorise pas à supprimer tout le bloc.
- **Inutiles sur la home actuelle :** les règles visant `.ss-expertise-editorial`, `.ss-adn-photo-card`, `.ss-offers-v46`, `.ss-programmes-v72`, `.ss-station-index-v72` ou `.ss-contact-v29` ne trouvent plus ces anciens composants sur l’accueil. Elles doivent sortir du **bundle home**, pas être effacées aveuglément des fichiers partagés : certaines servent encore au collectif.
- **Restes récents sans élément correspondant :** `home-system.css:31–35` cible `.ss-reservation__process`, `.ss-reservation__invitation` et `.ss-reservation__direct`, retirés de la vue V3. Élaguer ces règles, y compris leurs exceptions de focus, quand la réservation est consolidée.
- **Contre-règles à retirer ensemble :** les `!important` typographiques et ceux des thèmes dans `home-system.css` servent aujourd’hui à gagner contre l’héritage. Ils sont évitables dans une architecture consolidée, mais leur suppression isolée casserait le rendu.
- **Exceptions à préserver si nécessaires :** `[hidden]{display:none!important}` et les protections de réduction de mouvement ont une justification fonctionnelle. Leur utilité doit être documentée ; elles ne sont pas du bruit équivalent aux recolorations successives.

### 4.2 Largeurs, hauteurs et espacements

| Référence | Problème | Reprise prévue |
| --- | --- | --- |
| `styles.css:11`, `site-nav.css:229`, `home-system.css:8`, `:100–112` | `.wrap`, retraits propres au hero, sélecteurs par ID et `.ss-container` répartissent la responsabilité des gouttières. Le système pleine largeur corrige les symptômes mais ajoute une deuxième famille de conteneurs. | Un conteneur texte commun, une exception explicite pour les médias bord à bord, aucune exception ajoutée par ID. |
| `adn-editorial.css:12`, `:20–28` | Grille secondaire en `content-box`, maximum 1320 px auquel s’ajoute le padding ; gouttières de 40/64 px. Le texte du haut commence à 63 % avec retrait droit de 64 px. Les alignements diffèrent des 48 px du reste. | Box-sizing commun et alignements intentionnels ; revoir le masque/ratio au lieu de compenser chaque breakpoint. |
| `adn-editorial.css:20` | La composition supérieure impose 540 à 720 px ; la copie est centrée dans une zone étroite. La section entière atteint environ 942 px desktop / 1466 px mobile dans le mode audité. | Conserver le contenu et une image forte, définir un rythme proportionné et une hauteur naturelle pour le texte. |
| `architecture-v21.css:1764–1805`, `scripts/editorial.py:152–155` | Les Avis gardent une structure animée de trois colonnes et deux tracks par colonne, avec répétition des mêmes textes de réserve. Environ 1133 px desktop sont consommés sans véritables avis nouveaux. | Présentation calme des seuls contenus approuvés, sans multiplier une réserve pour remplir un mur animé. Aucune invention de témoignage ni suppression de la section. |
| `home-system.css:118`, `:128` | Les dernières réductions du bandeau Destinations, 56/40 px, sont bien présentes. | Les conserver comme état de référence ; ajuster ensuite le rythme global, sans réintroduire le compteur 43. ni une nouvelle zone vide. |
| `premium-footer.css:2`, `:36` | Pré-footer avec hauteur minimale importante et grande signature ; c’est une base de marque intéressante mais elle doit être accordée au dernier chapitre. | Garder le composant et ses liens, vérifier son échelle et la pertinence de la photo ; ne pas recréer un deuxième tunnel de réservation. |

Mesures de contrôle, à ne pas transformer en objectifs de hauteur fixe :

| Composant courant | 1440 px | 390 px |
| --- | ---: | ---: |
| Hero | 900 px | 844 px |
| ADN complet | ~942 px | ~1466 px |
| Expériences + Formats | ~850 px | ~2013 px |
| Destinations, hors bande de raccord suivante | ~1290 px | ~1231 px |
| Bande Destinations → Avis | 120 px | 72 px |
| Avis | ~1133 px | ~950 px |
| FAQ | ~601 px | ~774 px |
| Réservation | ~958 px | ~1342 px |

Ces relevés sont faits sans photos distantes chargées, avec FAQ fermée et formulaire à l’étape 1. Une page longue n’est pas automatiquement mauvaise ; ici, les changements de rythme et les répétitions comptent davantage que le seul total.

### 4.3 Pourquoi les transitions restent incohérentes

1. **Ancien moteur de thème conservé.** `app.js:198–234` pilote `.ski-dark-mode`, `.ski-reviews-light` et `data-scroll-tone` selon des positions de titres. Deux gardes empêchent son exécution sur `.ss-home-themed`, mais il reste actif sur certaines autres pages. Les CSS de ces états sont toujours chargées sur la home.
2. **Thème fixe ajouté par-dessus.** `home-system.css:2–14` et `:97–109` rétablissent des fonds par wrappers, neutralisent main et les pseudo-éléments, avec des priorités élevées. Les fonds calculés sont corrects dans l’état local ; l’empilement reste fragile.
3. **Photos d’entrée conditionnelles.** `scripts/editorial.py:189–197`, `booking-v3.css:2–14` et `home-system.js:30–43` ajoutent une couche à l’entrée de Destinations et une autre sur Réservation. Elles ne font pas partie des cartes et changent le chapitre quand elles chargent.
4. **Dépendance géométrique au réseau.** À 1440 px, Destinations passe d’un padding haut calculé de 95,04 px à 224 px quand la photo devient prête, soit ~129 px supplémentaires. Réservation passe de 112 à 312 px. Sur mobile, les deltas sont 92 et 110 px. Ce sont des déplacements prévisibles par le code ; un CLS réel n’a pas été mesuré puisque les images sont bloquées ici.
5. **Sortie différente des entrées.** `booking-v3.css:70–71` crée maintenant une bande de couleur indépendante de 120/72 px. Elle remplace bien la photo de sortie rejetée : celle-ci n’existe plus dans le DOM courant. Le dégradé peut néanmoins se lire comme un chapitre gris autonome. C’est un traitement volontaire de la correction précédente, pas une nouvelle photo cachée à cet endroit.
6. **Le header est un autre système.** `home-system.js:6–28` choisit sa palette au point situé sous la capsule, avec tolérance de deux pixels. La bande autonome n’a pas de thème déclaré : le script conserve son état précédent si aucune section ne correspond. Maintenir la lisibilité est acquis par le fond opaque, mais la sémantique du raccord doit être explicitée.

**À proposer dans la refonte :** une seule politique de raccord, intégrée à la respiration des sections, sans image ajoutée pour masquer une frontière, sans div de grande hauteur consacré à un effet et sans changement de géométrie déclenché par `img.load`. La forme et l’amplitude exactes seront validées visuellement au lot Accueil ; aucune nouvelle transition n’est implémentée pendant cet audit.

### 4.4 Photographies : distinguer patrimoine et ajouts parasites

| Média | Rôle actuel et origine | Décision proposée |
| --- | --- | --- |
| Hero, Pexels `31112554` | Déjà dans `bc9bb78`. `site-nav.css:311–321` masque le véritable `.hero-image` et réaffiche la photo en `::before`, avec voile en `::after`. | Garder la photo si les droits/cadrages sont confirmés ; unifier son rendu en un seul composant média. Ne pas maintenir deux sources de présentation pour le même hero. |
| ADN, `416805` | Ancienne photo de compétition du diptyque, réutilisée avec masque latéral dans `adn-editorial.css:24`. | Ressource sportive à conserver sous réserve de validation visuelle. Revoir la composition, pas inventer un nouveau visuel. |
| Quatre expériences | Sources historiques `20159351`, `31112554`, `12100585`, `6721020`. | Conserver les liens et les disciplines ; vérifier que chaque photo illustre effectivement son intitulé, en particulier snowboard, et diversifier les cadrages sans multiplier les images. |
| Quatre stations en avant | Photos historiques, désormais associées à Courchevel, Megève, Val d’Isère et Serre Chevalier avec avertissement de localisation non attestée. | Préserver les liens et la grille utile. Ne pas transformer une photo d’ambiance en preuve de localisation. |
| `.ss-photo-transition--entry` | Réemploi récent de `31112551`, ancien paysage de contact, comme bande à l’entrée de Destinations. | Supprimer cette utilisation décorative lors du lot Accueil, après validation. Ne pas toucher aux vraies cartes stations. |
| `.ss-booking-atmosphere` | Même `31112551` au-dessus de Réservation, hauteur 460/320 px. | Retirer l’effet de transition parasite ; si une photo est retenue pour le chapitre, elle doit avoir une place éditoriale, une boîte stable et un cadrage approuvé. Ce n’est pas acquis. |
| `.ss-photo-transition--exit` | Supprimée du rendu et des styles lors de la correction précédente. | Ne pas la réintroduire. |
| Pré-footer, `416805` | Réemploi récent de la photo sportive historique dans le nouveau footer. | Conserver le footer comme base ; arbitrer la photo et sa répétition avec l’ADN au lot Accueil, sans supprimer le footer. |

Les calques récents sont des **réemplois artificiels dans la composition**, pas des images générées. Le fichier `content/home-immersive-media.json` indique lui-même que droits/attributions et validation photographique restent à vérifier. L’asset local `public/assets/experience-alpine.webp` est un petit visuel de 280×350 px avec avion et montagne : il ne constitue pas un remplacement haute définition pertinent pour ces transitions.

### 4.5 Génération, composants fantômes et tests

- `scripts/build.py:51–56` recharge les pages originales puis appelle `scripts/editorial.py`. Ce dernier remplace le contenu et certains composants par chaînes HTML et manipulations de DOM. Modifier directement `public/index.html` ne suffit pas : le prochain build le remplace.
- `content/templates/home.html`, `collective.html`, `offer.html`, ainsi que `content/header.html`/`footer.html`, ne sont pas le chemin de rendu des six pages principales dans le build courant. Leur nom peut induire une intervention au mauvais endroit. Les distinguer clairement des sources actives.
- `scripts/editorial.py:99–100`, `:176`, `:219`, `:231`, `:242` copie les anciens composants de home pour fabriquer le collectif. Un changement de l’accueil peut donc dériver vers Notre histoire si ces captures ne sont pas conservées correctement.
- `app.js:99–180` contient encore le traitement de `#ski-request-form`, alors qu’aucune des 61 pages générées n’a cet identifiant ni `#request-destination`/`#request-station`. Le vrai formulaire est `#private-request-form` dans `home-system.js`. Ce code mort doit sortir du chemin actif après vérification de build ; sa règle historique limitant Performance à une personne ne doit jamais revenir.
- `tests/adn_redesign.py:19` et `tests/course_formats.py:18` contournent une partie de leurs anciens contrôles de périmètre lorsque `.ss-home-themed` est présente. D’autres scripts comparent strictement un ancien commit et attendent des états devenus incompatibles avec la V3. Ils documentent des étapes de travail, pas une suite de régression unifiée.
- Plusieurs tests écrivent dans `docs/`, utilisent des ports locaux fixes et dépendent de chemins `/tmp` pour axe-core/BeautifulSoup. Séparer résultats d’exécution, archives de revue et assertions fonctionnelles durables. Ne pas réécrire un ancien contrôle pour appeler « validée » chaque nouvelle apparence.

## 5. Différences avec `main` au commit `bc9bb78`

| Zone | Design historique | État courant et conséquence |
| --- | --- | --- |
| Chargement CSS | Cinq feuilles locales, dont l’ancien footer ; déjà beaucoup de variantes accumulées. | Dix feuilles locales. Quatre socles historiques toujours chargés, six ajouts, ancien footer retiré. Un retour aveugle aux CSS historiques ne constituerait pas un nettoyage. |
| Navigation/hero | Capsule flottante, masquage au scroll, photo poudreuse plein cadre, titres Clash en accent. | Composition et photo largement conservées, nouveau moteur de palette de header. Détails de marque utiles à garder ; responsabilités à extraire. |
| ADN | Deux grandes photos, puis trois cartes photographiques avec texte en overlay. | Une image avec masque et texte à droite, deux prolongements textuels ; deux anciennes sections graphiques regroupées autour du contenu A02. Ne pas restaurer les anciens overlays par défaut. |
| Expériences | `.ss-offers-v46`, quatre cartes, paragraphes complets et chapitre pouvant devenir sombre. | `.ss-experiences-compact`, légendes courtes sur fond minéral. Compréhension plus immédiate, mais hiérarchie à accorder au reste. Sources complètes conservées par autorisation antérieure. |
| Formats | `.ss-programmes-v72`, lignes et grands index, titre scindé. | Trois catégories/durées compactes, titre continu et CTA. Garder la clarté, sans rétablir de grands chiffres décoratifs. |
| Destinations | Galerie photographique et ancien index « 43. », palette au scroll. | Quatre cartes conservées, bandeau éditorial explicite, noir statique, raccords hétérogènes autour du chapitre. Garder les cartes et le CTA contextualisé. |
| Avis | Démonstration de mur animé et thème piloté par titres. | Texte de réserve approuvé répété dans les tracks, fond blanc forcé. Ne réintroduire aucun faux avis de la maquette historique. |
| FAQ | Même famille de composant natif. | Questions/réponses validées réintégrées ; base saine à garder. |
| Réservation | Long formulaire, prénom requis, nombre de personnes limité, photo et texte annexe. | Deux étapes, 43 stations, prénom facultatif, nombre réel, règle freeride, brouillon WhatsApp. C’est un progrès fonctionnel à préserver malgré les reprises graphiques. |
| Footer | `.ss-ridge-footer`, scène animée/canvas. | Pré-footer photographique et footer premium fonctionnel. Base explicitement à conserver et améliorer. |
| Pages secondaires | Gabarits historiques avec leur vocabulaire visuel. | Nouveaux textes dans les anciens composants ; collectif couplé à la home ; 43 nouvelles fiches héritant aussi de styles de manifeste. Besoin d’un système commun de lecture. |

**La référence historique est une référence de composition et de détails, pas une autorisation de restaurer ses textes, ses témoignages illustratifs ou ses anciennes restrictions commerciales.**

## 6. Architecture visuelle proposée pour validation

### 6.1 Alternance fixe et responsabilités

| Chapitre | Fond extérieur | Contenu et intention |
| --- | --- | --- |
| Hero + ADN | Clair, `#FFFFFF` | Photo hero conservée, voile local pour la lisibilité ; ADN éditorial, sans bande noire autonome. Une photo peut être sombre sans rendre tout le chapitre « thème sombre ». |
| Expériences + Formats | Minéral, `#F7F6F2` | Ensemble unique, informations immédiatement lisibles, photos propres aux disciplines et pas de cartes noires. |
| Destinations | Noir, `#111312`, bord à bord | Galerie et découverte des 43 destinations ; pas de photographie ajoutée comme raccord. |
| Avis + FAQ | Blanc, `#FFFFFF`, bord à bord | Réassurance lisible, vrais contenus autorisés seulement, questions natives accessibles. |
| Réservation + Footer | Noir, `#111312`, bord à bord | Message émotionnel court, action WhatsApp explicite et navigation de marque. Pas de répétition du parcours dans trois blocs. |

Principes :

- Les fonds appartiennent à des wrappers extérieurs sans `max-width`. Les conteneurs de texte, eux seuls, sont limités à 1320 px, avec des gouttières cohérentes 48/32/20 px. Le bord à bord photographique est une exception explicite, pas une autre définition de `.wrap`.
- La fluidité vient d’abord de l’alignement, du rythme, du cadrage et des espacements entre chapitres. Proposition de raccords tonaux courts **intégrés à leur padding**, à valider avec images réelles ; pas d’ajout automatique d’une bande indépendante de 120–220 px pour chaque frontière.
- Pas de photo de transition dédiée, pas de blur pour masquer une coupe, pas de déclenchement d’une hauteur supplémentaire après chargement réseau.
- Moncler Grenoble : peu d’éléments, grands espaces utiles et typographie maîtrisée. Arc’teryx : sujets sportifs crédibles, détails précis et lisibilité. Porsche : continuité de lecture, placement juste et transitions discrètes. Aucun logo, palette ou composant copié de ces marques.
- Réserver les mouvements au feedback utile et à de légers effets d’image ; conserver `prefers-reduced-motion`. Ne pas rendre le thème de toute la page dépendant du défilement.
- Conserver le footer premium : ses liens, le légal et sa signature sont la base ; proportionner la clôture photographique au dernier chapitre, sans refaire une deuxième réservation.

### 6.2 Pages secondaires

- **Collectif :** identité, histoire et méthode compréhensibles dès l’introduction ; quatre sections validées conservées, composants éditoriaux propres plutôt qu’une copie de la home.
- **Quatre prestations :** discipline, promesse validée, formats compatibles, contact immédiatement repérables ; cinq sections sources par page conservées. Les paragraphes détaillés restent accessibles dans un rythme plus simple, sans même grande photo répétée à chaque étape.
- **Fiches destinations :** nom de station, contexte local distinct et CTA contextualisé visibles rapidement ; garder leurs URL, H1, Title, descriptions, canonicals éventuels et liens. Réduire le hero actuellement défini avec `min-height:780px` dans `integration.css:31`, sans homogénéiser les textes locaux ni prétendre que les photos d’ambiance sont des prises de vue locales.
- **Catalogue :** préserver recherche et accès aux 43 fiches. `stations.html` et `destinations.html` forment deux entrées différentes à rationaliser. Ne supprimer ni rediriger une route avant validation d’une stratégie d’URL.
- **Routes anciennes :** `offres/amis.html`, `famille.html`, `explorer.html`, `progresser.html` existent encore, sans lien entrant détecté dans le HTML courant. Décider leur rôle, leur contenu ou leurs alias séparément ; aucune suppression automatique.
- Garder les pages légales simples et lisibles, sans leur faire charger des composants décoratifs de home.

## 7. Proposition de structure CSS consolidée

Structure de travail proposée, **non créée pendant cet audit** :

```text
styles/
  tokens.css                  couleurs, typo, espacements, rayons, durées
  reset.css                   normalisation minimale
  base.css                    document, texte, liens, médias
  layout.css                  wrapper, conteneur, grilles, sections
  themes.css                  light / mineral / dark et contraste associé
  components/
    header.css
    buttons.css
    media.css
    experience-card.css
    formats.css
    destination-gallery.css
    reviews.css
    faq.css
    booking.css
    footer.css
  pages/
    home.css
    collective.css
    offer.css
    destinations-index.css
    destination.css
    legal.css
  utilities.css               hidden, sr-only, réduction de mouvement
  entries/                    composition explicite par famille de page
```

Sorties visées : **un socle commun et une feuille de page**, générés de façon déterministe dans `public/assets/`. Le mécanisme peut rester dans le build statique existant ; aucun besoin de réécrire le site dans un framework JavaScript.

Règles de consolidation :

1. Une propriété structurante a un propriétaire : thème pour les fonds, layout pour les conteneurs, composant pour son padding interne et sa typo. Le header ne définit plus le style de tous les paragraphes de la page.
2. Conventions de classes stables, sans suffixes de version comme contrat permanent ; conserver les IDs et ancres publics nécessaires à la navigation et au formulaire.
3. Définir une échelle de titres, de texte, de gutters et d’espacement ; pas de nouvelles couleurs quasi identiques dispersées dans les composants. Le vert WhatsApp reste fonctionnel, dans la réservation.
4. Utiliser éventuellement un ordre de couches `reset, tokens, base, layout, components, pages, utilities`, mais **pas comme correctif magique** : du CSS historique non stratifié peut dominer les nouvelles couches, et l’ordre des couches s’inverse pour les déclarations `!important`. Éliminer les conflits nécessaires avant de promettre leur résolution par `@layer`.
5. Garder les exceptions d’accessibilité nécessaires, documentées. Interdire les nouveaux sélecteurs par ID pour gagner une bataille de couleurs et les ajouts « correctif de correctif » en fin de fichier.
6. Charger uniquement les composants de la route. Ne pas charger `manifesto.css` pour une fiche station ni les palettes expérimentales pour une page courante.
7. Maintenir un chemin legacy séparé pour les pages non encore migrées. Ne jamais faire cohabiter, sans contrôle, tout `site-nav.css` non stratifié et un nouveau design system supposé prioritaire. Extraire dans un paquet legacy borné les règles effectivement nécessaires à la route en migration.
8. Rendre les composants depuis des sources explicites. Garder `content/pages.json` et `content/stations.json` comme données ; préserver aussi `booking-ui.json`, `destinations-closing.json` et les décisions de condensation. Les templates actifs doivent porter des noms sans ambiguïté ; `public/` reste une sortie reproductible.

## 8. Plan de reprise en quatre lots

Aucun lot n’est engagé par ce document. Chaque lot produira une version revue avant le suivant.

### Lot 1 — Fondations et maîtrise de la cascade

**But :** rendre les responsabilités prévisibles avant de dessiner à nouveau les sections.

Travaux :

- Figer les références de contenu, métadonnées, routes et états de formulaire ; distinguer référence graphique historique et invariants métier actuels.
- Cartographier puis extraire les tokens, conteneurs, thèmes, navigation, utilitaires et styles réellement employés. Retirer les doublons démontrés et l’héritage sans composant de la route migrée.
- Préparer les entrées CSS par famille de page et leur génération déterministe ; maintenir les autres routes sur leur chemin existant.
- Séparer logique de header, thèmes, médias et formulaire ; préparer le retrait du handler de formulaire devenu mort sans toucher au moteur fonctionnel actuel.
- Remplacer le couplage de copie de composants entre home et collectif par des composants explicites, progressivement et avec comparaison de contenu.
- Rendre les tests exécutables avec un répertoire de résultats temporaire, une URL de test configurable et des dépendances identifiées.

Livrables : carte des responsabilités, bundles de fondation, manifeste des routes migrées, mesures de cascade avant/après et preuve d’absence de changement éditorial.

**Acceptation :** aucune fuite de styles vers les pages non migrées ; ancres et navigation intactes ; aucun nouveau `!important` cosmétique ; pas de promesse qu’un nettoyage technique équivaut déjà à la nouvelle direction artistique. Validation du propriétaire avant lot 2.

### Lot 2 — Accueil et rythme des chapitres

**But :** une composition cohérente de Hero à FAQ et une continuité maîtrisée vers le footer.

Travaux :

- Recomposer les alignements Hero/ADN avec la photo historique pertinente et la copie approuvée ; ne pas restaurer les longs overlays anciens par défaut.
- Accorder Expériences et Formats au même système typographique et minéral, en conservant les quatre destinations de liens et les données de référence.
- Garder Destinations en noir bord à bord, la galerie des quatre stations et le nouveau bandeau explicite. Supprimer les calques photographiques d’entrée parasites.
- Remplacer les trois stratégies de transition par une seule politique de raccord validée sur l’ensemble de la page ; traiter explicitement le gradient autonome actuel au lieu d’empiler un nouvel effet dessus.
- Donner aux Avis une hauteur justifiée par le contenu réel ; conserver les textes de réserve tant qu’aucun témoignage autorisé n’existe. Garder la FAQ native et sa copie.
- Améliorer la base du footer premium et sa relation au chapitre de réservation, sans supprimer les informations ni changer ses liens.
- Préparer/valider un petit catalogue de médias : rôle, droits, définition, sujet, crop desktop/mobile, dimensions et alt. Ne pas ajouter des images pour remplir de la hauteur.

Livrables : captures complètes desktop/mobile, trois raccords dans leur contexte, comparaison historique centrée sur composition/ressources et inventaire des composants retirés.

**Acceptation :** alternance exacte des cinq chapitres ; fonds réellement bord à bord ; pas de bande photo parasite ni grande zone vide ; validation des vraies photographies et polices chargées ; aucune disparition de section. Ne pas conclure sur des captures de ressources manquantes.

### Lot 3 — Réservation et continuité jusqu’au footer

**But :** une action privée simple et explicite, sans régression de parcours.

Travaux :

- Consolider `home-system.css`/`booking-v3.css` en un seul composant de réservation ; supprimer les anciennes règles de processus retirés et les doubles définitions de grille/progression.
- Garder le titre/introduction approuvés et la hiérarchie WhatsApp explicite ; alléger les répétitions selon les autorisations existantes, sans modifier les sources validées.
- Retirer le calque `.ss-booking-atmosphere` en tant que transition artificielle ; toute réutilisation photographique éventuelle nécessite une composition et un cadrage validés, avec boîte réservée stable.
- Préserver la machine à deux étapes, radios natifs, recherche des 43 stations/Autre station, période libre, champs facultatifs, nombre réel de participants et règle freeride.
- Régler reflow des étapes nommées, focus, erreurs par champ, zone de saisie mobile et éventuel recouvrement par le bouton WhatsApp flottant. Garder la réduction de mouvement.
- Préserver l’ouverture d’un brouillon et la maîtrise de l’envoi par l’utilisateur ; aucun changement de numéro ou de parcours métier sans demande explicite.

Livrables : deux étapes, erreurs et état freeride sur desktop/mobile ; messages encodés vérifiés sans envoi ; continuité sombre jusqu’au bas du footer.

**Acceptation :** données conservées au Retour, tous les champs nécessaires validés, prénom/commentaires facultatifs, demi-journée réellement absente en freeride, aucun plafond de groupe inventé, aucun paiement ni confirmation automatique. Validation du propriétaire avant lot 4.

### Lot 4 — Pages secondaires, destinations et retrait de l’héritage

**But :** informations essentielles visibles rapidement et cohérence avec le système consolidé.

Travaux :

- Migrer collectif, quatre prestations, catalogues, fiches stations et légal par familles, avec comparaison de contenu et de navigation à chaque étape.
- Simplifier les premières vues et répétitions de médias sans modifier les 4/5 sections validées de chaque page principale.
- Détacher les fiches de `manifesto.css`, isoler leurs composants locaux et conserver le texte distinct des 43 stations, leurs métadonnées et leurs CTA contextualisés.
- Préserver les résumés d’accueil dans les sources : le propriétaire a choisi de conserver les pages prestations actuelles, pas d’y recopier ces résumés automatiquement.
- Arbitrer les deux catalogues et les quatre anciennes routes sans lien entrant ; aucune suppression/redirection non validée.
- Quand toutes les routes sont migrées, retirer les imports legacy et archiver les feuilles non utilisées. Mettre à jour le registre des sources actives et la documentation, sans réécrire les archives comme si elles étaient des validations graphiques.

Livrables : matrice des routes, premières vues par famille, contrôle des 43 fiches, bilan des styles chargés et fichiers archivés, rapport de non-régression.

**Acceptation :** 32 sections sources intactes, 43 URL et contenus SEO protégés, recherche et liens fonctionnels, navigation/légal préservés, absence de styles de home sur les pages secondaires. Aucune mise en ligne ni fusion automatique.

## 9. Risques de régression et tests à prévoir

| Risque | Protection / preuve attendue |
| --- | --- |
| Retrait d’une règle partagée qui habille encore le collectif ou une prestation | Graphe de chargement par route, captures des familles, extraction avant déchargement. Ne pas confondre zéro match sur home et code globalement mort. |
| Une édition de `public/` disparaît au rebuild | Rendre depuis les sources actives ; build reproductible ; comparer les sorties de deux builds. |
| Perte de copie lors d’une simplification | Empreintes des données approuvées, contrôle par bloc/section et registre explicite des condensations autorisées A03/A04/A08 et de la révision A05. Pas de nettoyage par recherche/remplacement sur le texte. |
| Styles de couches et anciens `!important` prennent une priorité inattendue | Vérifier les styles calculés des éléments clés et les règles gagnantes ; pas seulement le nombre de fichiers. Tester normal, hover, focus, menu ouvert, champ invalide et étape 2. |
| Masquage accessible brisé en supprimant les règles prioritaires | Vérifier `[hidden]`, fieldsets inactifs, ordre clavier, lectorat écran, focus d’erreur et réduction de mouvement. |
| Photographies coupées, non chargées ou déplacement au chargement | Validation des assets réels, dimensions/ratio réservés, tests réseau froid/chaud/lent/échec et deux tailles de crop. Pas de test avec image de remplacement présenté comme une validation photographique. |
| Raccord gris autonome, marge blanche ou débordement masqué | Mesures de wrappers, tests de pixels dans les zones unies aux bords et au centre, captures de chaque raccord et de la page entière. Mesurer scrollWidth : `overflow-x:hidden` seul ne prouve pas l’absence de débordement. |
| Header change de palette au mauvais endroit ou couvre un titre | Tester montée/descente du scroll, ancres, retour navigateur, frontières, menu mobile et focus ; contrôler hauteur stable et contraste dans les deux palettes. |
| Régression WhatsApp | Tester les quatre expériences, 43 stations + Autre station, période libre, nombre entier réel, Retour, options facultatives, retrait/réapparition de demi-journée et valeurs périmées. Intercepter l’ouverture de l’URL pour décoder accents, &, + et retours ligne. Vérifier zéro ouverture avant soumission valide et zéro envoi automatique. |
| Altération du SEO et de la navigation locale | Figer URL, Title, H1, descriptions, canonicals existants et liens des 43 fiches ; conserver les 86 CTA locaux et leurs messages. Ne pas inventer un domaine canonique. |
| Publication ou indexation accidentelle | Maintenir meta robots, `public/_headers` et `robots.txt` ; aucun changement de `main`, fusion PR #20, déploiement ou soumission de sitemap dans ces lots sans autorisation explicite distincte. |
| Tests anciens passent en contournant des assertions devenues gênantes | Séparer archives de versions et tests durables. Toute modification d’un contrat de test doit correspondre à une décision approuvée, pas à un simple nouvel état du rendu. |

Matrice minimale de recette :

- 1536×960, 1440×900, 1280×800, 1024×768, 768×1024, 390×844 et 375×812 ; 320 px et zoom 200 % pour le reflow et l’accessibilité.
- Chromium, puis WebKit/Firefox lorsque disponibles ; ne pas présenter une seule exécution Chromium comme une validation de tous les navigateurs.
- Contrôle clavier et axe ciblé sur les composants changés, complété par inspection humaine ; pas de conclusion « site conforme » à partir d’un résultat axe vide.
- Images et polices réellement chargées pour la recette de direction artistique ; état sans réseau testé séparément pour la robustesse.
- Cibles de performance proposées : LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 sur profil documenté. Ce sont des objectifs futurs à mesurer, pas des résultats de cet audit.

## 10. Décision attendue avant intervention

Valider d’abord le diagnostic, l’alternance des cinq chapitres, la consolidation par responsabilités et les quatre lots. Les cadrages, amplitudes exactes des raccords et proportions finales feront l’objet de preuves visuelles au lot Accueil ; ils ne sont pas implicitement approuvés par ce plan.

À cette étape : **seul `DESIGN_REFACTOR_PLAN.md` est ajouté sur la branche dédiée.** Le rendu actuel reste inchangé, les données des 32 sections et des 43 destinations sont préservées, `noindex,nofollow` reste actif. Aucune fusion de la PR #20 et aucun déploiement n’ont été effectués.
