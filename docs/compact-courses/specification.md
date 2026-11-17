# SKI SOCIETY — Refonte des sections Expériences & Formats

## 1. Mission

Refondre les sections 03 « Nos expériences » et 04 « À chacun son rythme » de la page d'accueil pour les présenter comme un ensemble visuel unique.

Le rendu actuel est insatisfaisant : quatre cartes noires avec des textes trop petits, suivies d'une section de formats trop imposante.

Je veux une interface plus élégante, plus claire, plus sportive et plus facile à comprendre.

**Références : Moncler Grenoble pour l'élégance éditoriale et Arc'teryx pour la photographie sportive.**

Ne pas copier leur identité visuelle, leurs logos ou leurs composants.

## 2. Résultat attendu

Sur un viewport desktop de 1440 × 900 px, afficher simultanément :

- Le titre « La montagne se vit à votre manière. »
- Quatre expériences illustrées, sur une seule ligne.
- Les intitulés et liens des expériences.
- Le titre « À chacun son rythme. »
- Les trois formats : demi-journée, journée complète et sur mesure.

Le visiteur doit comprendre en moins de trois secondes :

1. Quels cours Ski Society propose.
2. Quelle durée il peut choisir.
3. Où cliquer pour en savoir davantage ou réserver.

Cette contrainte concerne **l'ensemble des deux sections dans un écran de 900 px de haut**, une fois arrivé à leur début. Elle ne signifie pas que toute la page d'accueil doit tenir dans un seul écran.

## 3. Architecture

Créer un ensemble éditorial commun :

```text
┌─────────────────────────────────────────────────────────────┐
│ 03 / NOS EXPÉRIENCES                                        │
│ La montagne se vit à votre manière.                         │
│ Introduction courte                                        │
│                                                             │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │
│ │            │ │            │ │            │ │            │ │
│ │  IMAGE 1   │ │  IMAGE 2   │ │  IMAGE 3   │ │  IMAGE 4   │ │
│ │            │ │            │ │            │ │            │ │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘ │
│ Ski privé     Performance    Freeride      Snowboard        │
│ Découvrir ↗   Découvrir ↗    Découvrir ↗   Découvrir ↗     │
│                                                             │
│ ─────────────────────────────────────────────────────────── │
│                                                             │
│ 04 / FORMATS DE COURS PRIVÉS                                │
│ À chacun son rythme.                                        │
│                                                             │
│ DEMI-JOURNÉE        JOURNÉE COMPLÈTE       SUR MESURE       │
│ 2 h 30              09h30 – 17h00          Sur demande      │
│                                                             │
│                      Organiser mon expérience ↗             │
└─────────────────────────────────────────────────────────────┘
```

Ne pas créer deux sections avec des fonds différents.

## 4. Dimensions desktop

### Viewport de référence

1440 × 900 px.

### Conteneur global

- `width: 100%`
- `max-width: 1320px`
- `margin-inline: auto`
- `padding-inline: 48px`
- `padding-top: 48px`
- `padding-bottom: 40px`
- `box-sizing: border-box`
- `background: #F7F6F2`

Utiliser une largeur utile de 1224 px à 1440 px.

### Budget vertical cible

| Élément | Hauteur |
|---|---:|
| En-tête expériences | 100 px |
| Espacement avant images | 22 px |
| Photographies | 280 px |
| Titres et liens expériences | 78 px |
| Séparation et respiration | 32 px |
| En-tête formats | 83 px |
| Trois formats | 110 px |
| CTA inférieur | 48 px |
| Marges et ajustements | 87 px |
| **Total maximal cible** | **840 px** |

Les valeurs sont des cibles de conception. Le contenu ne doit jamais être coupé pour atteindre artificiellement cette hauteur.

La hauteur totale de l'ensemble à 1440 px doit idéalement être comprise entre 780 et 850 px.

## 5. En-tête expériences

### Surtitre

`03 / NOS EXPÉRIENCES`

- Font-size : 11 px.
- Font-weight : 600.
- Letter-spacing : 0.16em.
- Line-height : 16 px.
- Couleur : `#626761`.

### H2

`La montagne se vit à votre manière.`

- Font-size : 48 px.
- Font-weight : 500.
- Line-height : 1.08.
- Letter-spacing : -0.04em.
- Couleur : `#171A18`.
- Margin-top : 12 px.
- Margin-bottom : 10 px.

Conserver le paragraphe d'introduction validé, mais l'afficher de manière discrète et lisible, avec une largeur maximale de 850 px.

- Font-size : 15 px.
- Line-height : 1.5.
- Couleur : `#555B56`.

## 6. Galerie des quatre expériences

### Grille

- Display : grid.
- Grid-template-columns : repeat(4, minmax(0, 1fr)).
- Column-gap : 16 px.
- Margin-top : 22 px.

### Images

- Hauteur : 280 px à 1440 px.
- Largeur : 100 %.
- Object-fit : cover.
- Border-radius : 0.
- Pas de bordure.
- Pas d'overlay noir.
- Pas de texte superposé.

Chaque image doit être différente et directement liée à la discipline.

**01 — Leçons particulières**

Photographie d'un cours de ski avec un moniteur et un élève. Authenticité et transmission.

**02 — Performance & technique**

Photographie de carving engagé ou de compétition alpine. Mouvement puissant et précision technique.

**03 — Freeride & milieu alpin**

Photographie d'un skieur dans un terrain de neige naturelle, avec une forte présence de la montagne.

**04 — Snowboard**

Photographie d'un snowboardeur en action. Ne pas utiliser une photographie de skieur.

Privilégier les photographies existantes lorsqu'elles conviennent. Ne pas introduire de nouvelles images sans droits d'utilisation adaptés.

### Sous chaque photographie

Afficher :

- Le numéro discret `01 /`, `02 /`, etc.
- Le nom de l'expérience.
- Un lien de découverte.

La description complète validée ne doit pas être affichée dans cette vue compacte, afin de préserver la lisibilité.

Elle doit rester conservée intégralement dans les fichiers sources éditoriaux et disponible sur la page dédiée à la prestation.

**Cette condensation est autorisée uniquement pour la présentation compacte de l'accueil. Ne supprimer aucun texte des pages prestations.**

### Titres

- Font-size : 19 px.
- Font-weight : 600.
- Line-height : 1.2.
- Letter-spacing : -0.02em.
- Couleur : `#181D19`.
- Margin-top : 12 px.

### Liens

- Font-size : 13 px.
- Font-weight : 500.
- Couleur : `#333B35`.
- Margin-top : 8 px.

Conserver les quatre CTA déjà validés et leurs destinations exactes.

Ne pas créer de bouton blanc sur fond noir.

### Mise en avant Performance

Conserver le label `NOTRE SPÉCIALITÉ`.

Placer ce label discrètement en haut de la photographie Performance, sur un fond blanc cassé opaque.

- Font-size : 10 px.
- Padding : 7 px 10 px.
- Border-radius : 2 px.

Ne pas augmenter la taille de cette carte par rapport aux trois autres.

## 7. Interaction des cartes

Chaque photographie et son titre peuvent pointer vers la page de prestation correspondante.

Hover desktop :

- Zoom image maximal : `scale(1.025)`.
- Durée : 300 ms.
- Easing : ease-out.
- Image contenue dans un wrapper avec `overflow: hidden`.

Le titre et le lien restent fixes.

Respecter `prefers-reduced-motion`.

Clavier :

- Chaque carte doit être accessible.
- Focus visible avec contour de 2 px.
- Aucun élément interactif imbriqué dans un autre lien.

## 8. Transition vers les formats

Après les quatre expériences :

- Margin-top : 32 px.
- Border-top : 1 px solid `#D4D4CF`.
- Padding-top : 25 px.

Aucun fond différent.

Aucune section noire.

Aucun chiffre géant en arrière-plan.

## 9. En-tête formats

### Surtitre

`04 / FORMATS DE COURS PRIVÉS`

- Font-size : 11 px.
- Font-weight : 600.
- Letter-spacing : 0.16em.
- Couleur : `#626761`.

### Titre

`À chacun son rythme.`

- Font-size : 34 px.
- Font-weight : 500.
- Line-height : 1.12.
- Letter-spacing : -0.035em.
- Couleur : `#171A18`.
- Margin-top : 8 px.

Le titre doit tenir sur une seule ligne à 1440 px.

La clarification « Formats de cours privés » doit être visible immédiatement.

## 10. Présentation des trois formats

Créer une grille en trois colonnes de largeur égale.

- Grid-template-columns : repeat(3, minmax(0, 1fr)).
- Column-gap : 24 px.
- Margin-top : 22 px.

Chaque format est un bloc éditorial sans fond de carte.

### Contenu

**01 — DEMI-JOURNÉE**

Durée : `2 h 30`

Créneaux indicatifs conservés dans le contenu de référence :

- 09h30 – 12h00
- 12h00 – 14h30
- 14h30 – 17h00

**02 — JOURNÉE COMPLÈTE**

Horaire : `09h30 – 17h00`

**03 — SUR MESURE**

Indication : `Sur demande`

### Style

Noms :

- Font-size : 19 px.
- Font-weight : 600.
- Couleur : `#181D19`.

Durées :

- Font-size : 15 px.
- Font-weight : 500.
- Couleur : `#555D56`.
- Margin-top : 6 px.

Chaque format possède une fine bordure supérieure :

`1px solid #D4D4CF`

Padding-top : 14 px.

Conserver tous les titres, descriptions, notes et horaires validés dans les données éditoriales.

Sur les pages prestations, continuer à afficher les descriptions complètes.

Ne pas faire disparaître les règles métier : le freeride reste uniquement proposé à la journée ou sur mesure.

## 11. CTA inférieur

Créer une zone d'action discrète, alignée à droite sous les formats.

Texte :

`Parlons de votre projet`

- Hauteur : 48 px.
- Padding horizontal : 22 px.
- Fond : `#171C19`.
- Couleur : `#FFFFFF`.
- Border-radius : 4 px.
- Font-size : 13 px.
- Font-weight : 600.

Lien vers le parcours de contact existant.

Ne pas ajouter de nouveau formulaire.

## 12. Responsive

### Desktop large : 1280 px et plus

- Quatre expériences sur une ligne.
- Trois formats sur une ligne.
- Hauteur totale cible inférieure ou égale à 850 px à 1440 × 900 px.

### Tablette : 768 à 1279 px

- Deux colonnes d'expériences.
- Trois formats en colonnes si la largeur le permet, sinon empilés.
- Aucune hauteur fixe globale.
- Padding horizontal : 32 px.
- Photos au ratio 4:3.
- Titre principal : 40 px.

### Mobile : 767 px et moins

- Expériences en une colonne.
- Images au ratio 16:10 ou 4:3.
- Padding horizontal : 20 px.
- Titre principal : 34 px.
- Format de cours empilés.
- CTA pleine largeur.

Sur mobile, accepter le défilement vertical. Ne pas sacrifier la lisibilité pour tenir sur un écran.

## 13. Palette

- Fond : `#F7F6F2`
- Titres : `#171A18`
- Texte secondaire : `#555B56`
- Lignes : `#D4D4CF`
- Fond des labels : `#F7F6F2`
- CTA sombre : `#171C19`

Ne pas utiliser de fond noir pour les cartes ou les formats.

Ne pas introduire de vert vif, de bleu de marque ou de dégradé décoratif.

## 14. Intégration dans le code existant

Ne pas recréer toute la page d'accueil.

Identifier les composants existants responsables des sections 03 et 04.

Conserver leur contenu source et leurs URLs.

Modifier uniquement leur HTML/CSS de présentation.

Encapsuler les nouveaux styles avec des classes dédiées, par exemple :

- `.ss-experiences-compact`
- `.ss-experiences-compact__grid`
- `.ss-experiences-compact__item`
- `.ss-formats-compact`
- `.ss-formats-compact__grid`

Ne pas modifier les styles globaux qui pourraient casser les autres pages.

## 15. Validation obligatoire

Tester aux dimensions :

- 1536 × 960
- 1440 × 900
- 1280 × 800
- 1024 × 768
- 768 × 1024
- 390 × 844
- 375 × 812

### Critères d'acceptation

- Les quatre expériences et les trois formats sont visibles simultanément sur le viewport de référence, lorsque l'utilisateur arrive au début de cet ensemble.
- Aucune carte noire.
- Aucun texte minuscule.
- Chaque discipline est identifiable.
- Le titre « À chacun son rythme » est clairement associé aux formats de cours privés.
- Les durées sont visibles sans interaction.
- Les liens sont fonctionnels.
- Aucune régression responsive.
- Aucun débordement horizontal.
- Aucune modification des pages prestations ou destinations.

### Livrables

1. Capture complète desktop à 1440 px.
2. Capture mobile à 390 px.
3. Comparaison avec la version précédente.
4. Rapport des modifications.
5. Résultats des tests.
6. URL HTTPS de prévisualisation.

Ne pas considérer le travail terminé sans preuve visuelle du résultat.

## 16. Contraintes de publication

Travailler uniquement sur la branche de design actuellement utilisée pour la PR #20.

Ne pas modifier `main`.

Ne pas fusionner la Pull Request.

Ne pas déployer en production.

Maintenir `noindex,nofollow`.

Attendre la validation du propriétaire avant toute nouvelle refonte.
