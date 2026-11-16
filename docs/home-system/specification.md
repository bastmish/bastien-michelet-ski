# SKI SOCIETY — Système de fonds et refonte de la réservation

## Mission

Implémenter une alternance de fonds clairs et sombres à l'échelle de la page d'accueil complète, puis refondre graphiquement la section Réservation.

Références de direction artistique : l'élégance éditoriale de Moncler Grenoble et la précision sportive d'Arc'teryx.

Ne pas copier leurs identités visuelles.

## 1. Principe fondamental : les fonds couvrent toute la page

Les fonds ne sont pas appliqués aux conteneurs de contenu, mais aux sections pleine largeur.

Une transition claire/sombre doit couvrir exactement 100 % du viewport horizontal, de `x = 0` jusqu'à `x = window.innerWidth`.

Ne laisser aucune marge blanche extérieure, aucun bandeau parasite et aucun espace entre deux sections successives.

Le conteneur intérieur reste centré et limité à 1320 px.

### Structure

```html
<main>
  <section class="ss-theme-light">
    <!-- Hero + ADN -->
  </section>

  <section class="ss-theme-light-soft">
    <!-- Expériences + Formats -->
  </section>

  <section class="ss-theme-dark">
    <!-- Destinations -->
  </section>

  <section class="ss-theme-white">
    <!-- Avis + FAQ -->
  </section>

  <section class="ss-theme-dark">
    <!-- Réservation -->
  </section>
</main>

<footer class="ss-theme-dark">
  <!-- Footer premium -->
</footer>
```

Cette structure est conceptuelle. Conserver les sections sémantiques existantes si elles sont correctes et appliquer les fonds à leurs wrappers pleine largeur.

## 2. Position exacte des transitions

### Transition 01 : clair vers noir

**Déclenchement : immédiatement après le dernier pixel de la section Formats.**

À cet emplacement :

- La section Formats se termine.
- Le fond `#F7F6F2` s'arrête.
- La section Destinations commence.
- Le fond `#111312` occupe toute la largeur.

Aucun espace intermédiaire.

Ne pas effectuer cette transition entre Expériences et Formats.

### Transition 02 : noir vers blanc

**Déclenchement : immédiatement après la dernière ligne de la section Destinations, y compris son CTA et son padding inférieur.**

À cet emplacement :

- Le fond noir s'arrête.
- Le bloc Avis commence sur fond blanc.
- La FAQ reste sur le même fond blanc.

Couleur : `#FFFFFF`.

### Transition 03 : blanc vers noir

**Déclenchement : immédiatement après la dernière réponse de la FAQ et son padding inférieur.**

À cet emplacement :

- Le blanc s'arrête.
- La section Réservation commence en noir.
- Le footer conserve le même fond sombre.

Aucune rupture de fond entre Réservation et Footer.

## 3. Palette technique

```css
:root {
  --ss-light: #FFFFFF;
  --ss-light-soft: #F7F6F2;
  --ss-dark: #111312;
  --ss-dark-soft: #1B1D1C;

  --ss-on-light: #171A18;
  --ss-on-light-muted: #555B56;

  --ss-on-dark: #F7F6F2;
  --ss-on-dark-muted: #C7CCC8;

  --ss-border-light: #D4D4CF;
  --ss-border-dark: #454B47;
}
```

Utiliser des classes de thème au niveau des wrappers, sans modifier les styles globaux des autres pages.

Aucun gradient de transition entre les sections.

Les changements de fond doivent être nets et intentionnels.

## 4. Marges et contraintes

### Desktop

Viewport de référence : 1440 × 900 px.

Pour chaque grand chapitre :

- Largeur extérieure : 100vw, sans créer de débordement horizontal.
- Largeur maximale du contenu : 1320 px.
- Padding intérieur horizontal : 48 px.
- Centrage horizontal automatique.

### Mobile

- Largeur extérieure : 100 %.
- Padding horizontal intérieur : 20 px.
- Aucun débordement.
- Aucun espace blanc entre les fonds successifs.

Les marges verticales des premiers et derniers enfants ne doivent pas provoquer de fuite de marge entre sections. Utiliser `display: flow-root`, `display: grid` ou une gestion explicite des marges.

## 5. Header flottant

Le header doit rester lisible sur toutes les sections.

Ne pas laisser sa couleur dépendre directement du fond situé sous lui.

Créer deux apparences :

**Sur sections claires**

- Fond : `rgba(247,246,242,0.96)`.
- Texte : `#171A18`.
- CTA : fond `#171A18`, texte blanc.

**Sur sections sombres**

- Fond : `rgba(21,23,22,0.96)`.
- Texte : `#FFFFFF`.
- CTA : fond `#FFFFFF`, texte `#171A18`.

Détecter le thème de la section réellement située sous le header, en tenant compte de sa position dans le viewport.

Éviter un changement de couleur erratique à proximité des frontières.

Transition de couleur : 180 à 220 ms maximum.

Ne pas modifier la hauteur du header pendant le changement de thème.

## 6. Réservation — Objectif UX

La section actuelle est trop longue et trop proche d'un formulaire administratif.

La nouvelle version doit donner la sensation d'un accompagnement privé, simple et personnalisé.

Le client doit pouvoir préparer une demande WhatsApp en deux étapes.

Aucun paiement en ligne.

Aucune disponibilité fictive.

Aucune confirmation automatique de réservation.

## 7. Layout Réservation desktop

### Section extérieure

- Background : `#111312`.
- Width : 100 %.
- Padding-top : 104 px.
- Padding-bottom : 112 px.

### Conteneur

- Max-width : 1320 px.
- Padding-inline : 48 px.
- Margin-inline : auto.

### Grille

Deux colonnes :

- Colonne gauche : `minmax(0, 0.85fr)`.
- Colonne droite : `minmax(0, 1.15fr)`.
- Gap : 72 px.
- Align-items : start.

La colonne gauche accueille les textes éditoriaux validés et une explication courte du fonctionnement.

La colonne droite accueille le formulaire.

### Colonne gauche

Label :

`08 / CONTACT & RÉSERVATION`

- Font-size : 11 px.
- Letter-spacing : 0.18em.
- Color : `#C7CCC8`.

Titre :

`Parlons de votre prochaine journée de ski.`

- Font-size : `clamp(42px, 4.2vw, 62px)`.
- Line-height : 1.06.
- Letter-spacing : -0.035em.
- Color : `#FFFFFF`.
- Max-width : 520 px.
- Margin-top : 28 px.

Texte d'introduction :

Conserver exactement le texte validé dans les sources.

- Font-size : 17 px.
- Line-height : 1.7.
- Color : `#C7CCC8`.
- Max-width : 470 px.
- Margin-top : 28 px.

Afficher ensuite le processus de réservation validé, sous une forme discrète et lisible.

## 8. Panneau formulaire

### Apparence

- Background : `#F7F6F2`.
- Border-radius : 12 px.
- Padding : 40 px.
- Couleur du texte : `#171A18`.
- Largeur : 100 % de la colonne droite.
- Border : none.
- Box-shadow : none.

### Hauteur

Aucune hauteur fixe.

Objectif indicatif : 500 à 620 px à l'étape 1 sur desktop, selon le contenu réel.

### En-tête du panneau

Titre :

`Votre demande privée`

- Font-size : 24 px.
- Font-weight : 600.
- Line-height : 1.2.

Indicateur d'étape :

`01 / 02` ou `02 / 02`

- Font-size : 12 px.
- Color : `#667069`.

Afficher une barre de progression discrète, hauteur 2 px, avec progression à 50 % puis 100 %.

## 9. Étape 1 — Votre projet

Champs :

### A. Expérience

Quatre options :

- Leçons particulières
- Performance & technique
- Freeride & milieu alpin
- Snowboard

Utiliser des boutons de sélection de type radio, accessibles au clavier.

Disposition :

- Grille 2 × 2.
- Gap : 12 px.
- Hauteur minimale : 56 px par option.
- Padding : 14 px.
- Border-radius : 6 px.
- Border : 1 px solid `#CBCFC9`.

État sélectionné :

- Background : `#E8EBE5`.
- Border : 1.5 px solid `#171A18`.
- Texte : `#171A18`.

État non sélectionné :

- Background : `#FFFFFF`.

### B. Station

Champ avec recherche parmi les 43 destinations référencées.

Prévoir également :

`Autre station`

La sélection d'une station ne doit pas constituer une promesse de disponibilité.

Hauteur du champ : 52 px.

### C. Date ou période

Accepter une date précise ou une période exprimée librement.

Ne pas afficher de créneaux comme disponibles en temps réel.

Hauteur du champ : 52 px.

### Navigation

Bouton principal :

`Continuer`

- Height : 52 px.
- Width : 100 %.
- Background : `#171A18`.
- Color : `#FFFFFF`.
- Border-radius : 6 px.
- Font-size : 15 px.
- Font-weight : 600.

Valider les champs requis avant de passer à l'étape 2.

## 10. Étape 2 — Votre profil et votre format

Champs :

- Niveau.
- Nombre de participants.
- Format souhaité.
- Prénom, facultatif.
- Informations complémentaires, facultatives.

### Format

Choix :

- Demi-journée — 2 h 30.
- Journée complète — 09h30 à 17h00.
- Sur mesure.

**Règle métier : si l'expérience sélectionnée est Freeride & milieu alpin, supprimer l'option Demi-journée.**

Ne pas simplement la rendre visuellement inactive sans explication.

### Nombre de participants

Permettre d'indiquer le nombre réel de personnes, sans imposer un nombre arbitraire non validé.

Les groupes restent soumis aux possibilités d'encadrement.

### Validation

Vérifier que les données nécessaires à la demande sont présentes.

Ne pas exiger le prénom ni les informations facultatives.

### Boutons

Bouton secondaire :

`Retour`

Bouton principal :

`Préparer mon WhatsApp`

Au clic, générer le message prérempli et ouvrir WhatsApp.

Le message doit contenir :

- Expérience.
- Station.
- Date ou période.
- Niveau.
- Nombre de participants.
- Format.
- Prénom si renseigné.
- Commentaires si renseignés.

Ne jamais envoyer automatiquement de message.

L'utilisateur doit rester maître de l'envoi.

## 11. États et interactions

### Navigation entre étapes

Conserver les données lorsqu'on revient à l'étape précédente.

Ne pas recharger la page.

Mettre à jour l'indicateur de progression.

### Erreurs

Afficher les messages de validation directement sous le champ concerné.

- Font-size : 13 px.
- Couleur : `#A43F32`.
- Margin-top : 6 px.

Ne pas afficher de message d'erreur générique sans indiquer le champ concerné.

### Focus

Contour visible de 2 px minimum.

Contraste WCAG AA.

### Animations

Durée : 180 à 250 ms maximum.

Pas de glissement horizontal spectaculaire.

Respecter `prefers-reduced-motion`.

## 12. Responsive tablette

De 768 à 1199 px :

- Colonnes empilées.
- Conteneur max-width : 900 px.
- Padding horizontal : 32 px.
- Espace entre texte et formulaire : 48 px.
- Formulaire max-width : 720 px.
- Titre : 48 px.

## 13. Responsive mobile

Jusqu'à 767 px :

### Section

- Padding-top : 64 px.
- Padding-bottom : 72 px.
- Padding-inline : 20 px.

### Titre

- Font-size : 36 px.
- Line-height : 1.1.

### Formulaire

- Padding : 24 px.
- Border-radius : 8 px.
- Margin-top : 36 px.

### Options de prestations

Grille deux colonnes lorsque chaque option conserve une largeur lisible.

À moins de 360 px de largeur, une seule colonne si nécessaire.

### Champs

Tous les champs occupent 100 % de la largeur.

Hauteur minimale : 48 px.

### Boutons

Hauteur : 52 px.

CTA principal pleine largeur.

Ne jamais forcer un formulaire complet dans la hauteur d'un seul écran mobile.

## 14. Transition Réservation vers Footer

Le fond reste `#111312` jusqu'à la fin du footer.

Ne pas créer de rupture blanche.

Séparer éventuellement le formulaire et les liens du footer par une ligne :

`border-top: 1px solid #454B47`.

Conserver les informations légales, la navigation et les liens existants.

## 15. Tests obligatoires

Tester aux viewports :

- 1536 × 960
- 1440 × 900
- 1280 × 800
- 1024 × 768
- 768 × 1024
- 390 × 844
- 375 × 812

### Contrôles visuels

- Les fonds couvrent toute la largeur de la page.
- Les trois ruptures sont au bon endroit.
- Aucune bande blanche parasite.
- Le header reste lisible au-dessus de chaque thème.
- Le formulaire conserve une hiérarchie claire.
- Les champs sont correctement alignés.
- Les états sélectionnés sont visibles.
- Le footer prolonge correctement le fond noir.

### Contrôles fonctionnels

- Les deux étapes fonctionnent.
- Les données sont conservées entre étapes.
- Les validations fonctionnent.
- Les messages d'erreur sont explicites.
- Le freeride ne propose pas de demi-journée.
- Les 43 stations sont sélectionnables.
- L'option Autre station fonctionne.
- WhatsApp reçoit les informations correctement encodées.
- Aucun message n'est envoyé automatiquement.
- Aucune réservation n'est présentée comme confirmée.

## 16. Livrables

Fournir :

1. Une capture pleine page de l'accueil montrant les trois ruptures clair/sombre.
2. Une capture de la transition Formats → Destinations.
3. Une capture de la transition Destinations → Avis.
4. Une capture de la transition FAQ → Réservation.
5. Les deux étapes du formulaire sur desktop.
6. Les deux étapes sur mobile.
7. Un rapport de tests fonctionnels.
8. Une liste des fichiers modifiés.

## 17. Contraintes

Travailler uniquement sur la branche de développement en cours.

Ne pas modifier `main`.

Ne pas fusionner la PR #20.

Ne pas déployer en production.

Conserver `noindex,nofollow`.

Ne pas modifier les textes éditoriaux validés, sauf les nouveaux libellés fonctionnels explicitement définis dans cette spécification.

Ne pas supprimer les autres sections.

**Le résultat attendu est une expérience premium cohérente sur toute la page, pas une collection de composants indépendants.**