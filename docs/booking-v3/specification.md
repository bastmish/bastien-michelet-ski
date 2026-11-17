# SKI SOCIETY — Refonte de la réservation et transitions immersives V3

## 1. Objectif

Corriger deux défauts majeurs du site actuel :

1. Les passages entre fonds blancs et noirs sont trop abrupts, sans transition immersive.
2. La section Réservation est surchargée de textes et le fonctionnement WhatsApp n'est pas suffisamment explicite.

La direction artistique reste celle validée : sport haut de gamme, sobriété, photographies puissantes, influences Moncler Grenoble, Arc'teryx et transitions photographiques immersives dans l'esprit Porsche.

Ne pas reconstruire toute la page et ne modifier aucun texte éditorial validé dans les sources.

## 2. Transitions photographiques clair / sombre

### Principe

Le changement de thème doit continuer à concerner 100 % de la largeur du navigateur.

Mais au lieu d'une frontière systématiquement nette entre deux grandes sections, utiliser une transition immersive lorsque l'on entre ou sort d'un chapitre sombre.

La transition doit être réalisée avec des calques photographiques et des gradients de transparence, **sans créer de bande grise artificielle**.

### Transition A — Formats vers Destinations

Fond de départ : `#F7F6F2`.

Fond d'arrivée : `#111312`.

La transition doit avoir lieu exactement à la frontière entre la fin des formats et le début des destinations.

Créer une zone de transition visuelle de 160 px sur desktop et 96 px sur mobile, faisant partie du padding supérieur de Destinations.

Le fond de Destinations reste noir sur toute la largeur.

Utiliser un calque pseudo-élément positionné à l'intérieur de Destinations :

```css
.ss-destinations {
  position: relative;
  isolation: isolate;
  background: #111312;
}

.ss-destinations::before {
  content: "";
  position: absolute;
  inset: 0 0 auto;
  height: 160px;
  pointer-events: none;
  background: linear-gradient(
    to bottom,
    #F7F6F2 0%,
    rgba(247,246,242,0.92) 18%,
    rgba(247,246,242,0.50) 48%,
    rgba(17,19,18,0.20) 76%,
    #111312 100%
  );
  z-index: 0;
}

.ss-destinations > * {
  position: relative;
  z-index: 1;
}
```

Cette interpolation n'est qu'une base technique à ajuster. Éviter les bandes ou teintes intermédiaires boueuses. La zone doit apparaître naturelle et continue.

Le contenu de Destinations commence sous la zone de transition ; il ne doit pas devenir illisible à cause du gradient.

### Transition B — Destinations vers Avis

Départ : `#111312`.

Arrivée : `#FFFFFF`.

Créer un fondu photographique descendant sur environ 160 px à l'intérieur de la fin de Destinations, vers un fond blanc.

Le blanc doit ensuite être parfaitement uniforme dans Avis et FAQ.

Il ne doit pas rester de fond noir derrière les paragraphes des avis.

### Transition C — FAQ vers Réservation

Départ : `#FFFFFF`.

Arrivée : `#111312`.

Créer une transition de 180 à 220 px sur desktop et 100 à 120 px sur mobile.

Cette transition doit être plus forte visuellement que les précédentes, car elle introduit le dernier chapitre de la page.

**Ajouter si possible une photographie alpine forte en arrière-plan de la partie haute de Réservation.**

Cette image doit être :
- sombre, avec une silhouette ou un paysage identifiable ;
- très peu contrastée derrière les textes ;
- recouverte d'un gradient vertical vers `#111312` ;
- limitée à la partie haute de la section.

### Fond photographique

Utiliser une vraie photographie autorisée et optimisée.

Exemple de traitement :

```css
.ss-booking-section {
  position: relative;
  isolation: isolate;
  background: #111312;
  color: #F7F6F2;
  overflow: clip;
}

.ss-booking-section::before {
  content: "";
  position: absolute;
  inset: 0 0 auto;
  height: 460px;
  background:
    linear-gradient(
      to bottom,
      rgba(17,19,18,0.12) 0%,
      rgba(17,19,18,0.72) 60%,
      #111312 100%
    ),
    url("/assets/booking-alpine.jpg") center 38% / cover no-repeat;
  opacity: 0.75;
  pointer-events: none;
  z-index: 0;
}

.ss-booking-section > * {
  position: relative;
  z-index: 1;
}
```

`booking-alpine.jpg` représente ici un emplacement à alimenter avec une image autorisée, et non un fichier dont l'existence est présumée.

Ne pas créer d'image de remplissage si aucune photographie pertinente n'est disponible.

Le footer reste uniformément noir, sans nouvelle transition.

## 3. Refonte de la colonne gauche de réservation

### Problème actuel

La colonne gauche présente trop d'informations :

- titre principal ;
- longue introduction ;
- déroulement en trois étapes ;
- deuxième titre ;
- deuxième paragraphe ;
- lien WhatsApp supplémentaire.

Cette répétition nuit à la hiérarchie.

### Nouvelle règle

**La colonne gauche doit contenir un seul message principal et au maximum un complément court visible au premier regard.**

Conserver dans les sources les textes validés, mais alléger leur présentation dans cette section.

### Desktop — Composition

Conteneur global :
- Max-width : 1320 px.
- Padding horizontal : 48 px.
- Padding vertical : 112 px.

Grille :
- Colonne gauche : 42 %.
- Colonne droite : 58 %.
- Gap : 72 px.
- Align-items : start.

### Colonne gauche

Surtitre :

`08 / CONTACT & RÉSERVATION`

- Font-size : 11 px.
- Letter-spacing : 0.18em.
- Color : `#C7CCC8`.

Titre principal validé :

`Parlons de votre prochaine journée de ski.`

- Font-size : clamp(42px, 4vw, 58px).
- Line-height : 1.07.
- Letter-spacing : -0.04em.
- Font-weight : 500.
- Couleur : #FFFFFF.
- Largeur maximale : 510 px.
- Margin-top : 26 px.

Texte d'introduction validé :

`Vous avez une station en tête, des dates ou simplement une envie particulière ? Parlez-nous de votre projet. Nous recherchons au sein du collectif le moniteur qui correspond à vos attentes et à vos disponibilités.`

- Font-size : 16 px.
- Line-height : 1.7.
- Max-width : 450 px.
- Couleur : #C9CECA.
- Margin-top : 28 px.

### À retirer de l'affichage principal

- La deuxième accroche « Votre prochaine expérience commence ici. »
- Le deuxième paragraphe répétitif.
- La liste verticale complète des trois étapes.
- Le lien WhatsApp supplémentaire sous le texte.

Ces contenus doivent rester conservés dans les sources validées, et peuvent être utilisés dans une aide contextuelle si nécessaire. Ne pas les supprimer définitivement.

### Information rassurante

Sous le paragraphe, afficher une courte ligne :

`Disponibilités et modalités confirmées avant toute réservation.`

Taille : 13 px.

Couleur : `#ABB5AE`.

Margin-top : 32 px.

Aucun pictogramme décoratif.

## 4. Refonte du panneau WhatsApp

### Objectif principal

Le visiteur doit comprendre immédiatement :

1. Qu'il remplit quelques informations.
2. Que ces informations préparent un message WhatsApp.
3. Qu'il envoie personnellement ce message à Ski Society.

### Panneau

- Background : #F7F6F2.
- Border-radius : 12 px.
- Padding : 36 px desktop.
- Padding : 22 px mobile.
- Width : 100 %.
- Max-width : 700 px.
- Box-shadow : none.

### Nouvel en-tête

Remplacer « Votre demande privée » seul par :

**Préparer votre message WhatsApp**

Sous-titre :

`Quelques informations pour organiser votre cours avec Ski Society.`

Ajouter une icône WhatsApp reconnaissable, avec nom accessible pour les lecteurs d'écran.

Dimensions :

- Icône : 28 × 28 px.
- Titre : 23 px.
- Line-height : 1.2.
- Couleur : #171A18.
- Sous-titre : 14 px.
- Couleur : #68716A.
- Espace titre/sous-titre : 8 px.

### Progression

Conserver les deux étapes existantes.

Afficher clairement :

`Étape 1 sur 2 — Votre projet`

puis

`Étape 2 sur 2 — Votre profil`

Barre de progression :
- Height : 3 px.
- Background : #DDE1DB.
- Progression : #1E6C4B.
- Border-radius : 3 px.
- Margin-top : 20 px.
- Margin-bottom : 28 px.

## 5. Formulaire : lisibilité

### Labels

- Font-size : 14 px.
- Font-weight : 600.
- Color : #252B26.
- Margin-bottom : 8 px.

### Champs

- Height : 54 px pour les champs simples.
- Background : #FFFFFF.
- Border : 1px solid #C9CEC8.
- Border-radius : 6 px.
- Font-size : 15 px.
- Color : #171A18.
- Padding horizontal : 16 px.

### Espacement vertical

Entre deux groupes de champs : 22 px.

Entre deux champs côte à côte : 16 px.

### Focus

- Outline : 2 px solid #1E6C4B.
- Outline-offset : 2 px.

### Aides de saisie

- Font-size : 12 px.
- Line-height : 1.5.
- Color : #69736B.
- Margin-top : 6 px.

Ne pas afficher une aide longue sous chaque champ. Seules les informations réellement nécessaires doivent être visibles.

Pour les règles de groupe et d'horaires, regrouper les précisions dans une note concise à la fin de l'étape.

## 6. Bouton WhatsApp

### Problème actuel

« Préparer mon WhatsApp » ne dit pas clairement ce qui va se passer.

### Nouveau libellé

**Ouvrir mon message dans WhatsApp**

Le bouton doit être l'action dominante du panneau.

### Desktop

- Height : 56 px.
- Width : 100 %.
- Background : #1E6C4B.
- Color : #FFFFFF.
- Font-size : 15 px.
- Font-weight : 600.
- Border-radius : 6 px.
- Icône WhatsApp de 20 px à gauche du texte.
- Flèche externe de 16 px à droite.

Hover : #17573D.

Focus visible : contour contrasté de 3 px.

Le bouton peut devenir vert WhatsApp, car cette couleur possède ici une fonction claire. Ne pas étendre ce vert à l'identité générale du site.

### Comportement

Au clic :

- Valider les données.
- Préparer un message complet.
- Ouvrir WhatsApp avec le texte prérempli.
- Laisser le visiteur relire et envoyer lui-même son message.

Ne pas afficher de message prétendant que WhatsApp a été envoyé.

### Message d'information

Sous le bouton :

`Votre message s'ouvrira dans WhatsApp. Vous pourrez le relire avant de l'envoyer. Aucune réservation n'est confirmée à cette étape.`

- Font-size : 12 px.
- Line-height : 1.55.
- Color : #657068.
- Margin-top : 14 px.
- Align : center.

## 7. Réduire les répétitions

Ne plus afficher à la fois :

- le processus complet à gauche ;
- une progression en deux étapes dans le formulaire ;
- un deuxième appel WhatsApp à gauche ;
- une nouvelle explication sous le bouton.

La progression du formulaire devient l'élément principal de pédagogie.

La colonne gauche apporte l'émotion et la confiance.

La colonne droite permet l'action.

## 8. Responsive

### Mobile — 390 px de référence

Ordre :

1. Surtitre.
2. Titre principal.
3. Paragraphe.
4. Formulaire.
5. Note de réservation.

Aucun processus en trois étapes intercalé avant le formulaire.

Dimensions :
- Padding horizontal de section : 20 px.
- Padding vertical : 72 px.
- Titre : 36 px.
- Paragraphe : 15 px.
- Panneau : padding 20 à 22 px.
- Champs pleine largeur.
- Bouton WhatsApp : hauteur 56 px, pleine largeur.

La colonne gauche ne doit pas occuper plus d'espace vertical que nécessaire.

## 9. Tests

Tester :
- 1440 × 900.
- 1280 × 800.
- 1024 × 768.
- 768 × 1024.
- 390 × 844.
- 375 × 812.

Vérifier :
- Transition photographique visible entre les zones claires et sombres.
- Absence de bordure blanche parasite.
- Colonne gauche lisible et non répétitive.
- Titre WhatsApp immédiatement identifiable.
- Champs et labels bien contrastés.
- Bouton dominant.
- Ouverture effective d'une URL WhatsApp correctement encodée.
- Conservation des données entre les deux étapes.
- Absence de demi-journée en freeride.
- Aucune réservation annoncée comme confirmée automatiquement.

## 10. Contraintes

Conserver les 32 sections éditoriales validées dans les sources.

Ne pas altérer les 43 destinations, les textes SEO ni les autres pages.

Travailler exclusivement sur la branche de développement existante.

Ne pas modifier `main`.

Ne pas fusionner la PR #20.

Ne pas déployer en production.

Maintenir `noindex,nofollow`.

## 11. Livrables

Fournir :
- Une capture complète de la zone Réservation à 1440 px.
- Une capture mobile à 390 px.
- Une capture pleine page montrant les transitions.
- Une comparaison avant/après.
- Les résultats des tests WhatsApp.
- Une liste des éléments visuels supprimés ou masqués.

Ne pas considérer le travail comme terminé sans contrôle visuel des photographies et des transitions.