# SKI SOCIETY — Carte des territoires (V14)

## Objet et positionnement
À la demande du fondateur, l'ancienne carte de 40 stations couvrant Jura, Haute-Savoie et Suisse est remplacée par une carte **focalisée sur les quatre territoires français** et **15 stations emblématiques**.

Message commercial : **« Nous venons à vous. Dans la station où vous passez vos vacances. »**

La présence effective d'un moniteur partenaire dans une station n'est pas encore vérifiée. La mention sur site indique que les interventions dépendent des disponibilités, qualifications et autorisations professionnelles. **Aucune garantie de couverture ou d'implantation partout n'est exprimée.**

## Contours réels et droits d'usage

La carte utilise les contours départementaux IGN Admin Express COG (2018), simplifiés à 5 %, diffusés dans le dépôt open source de Grégoire David sous Licence Ouverte :

- https://github.com/gregoiredavid/france-geojson
- https://github.com/gregoiredavid/france-geojson/blob/master/departements-version-simplifiee.geojson

Codes sources : **39 Jura**, **25 Doubs**, **74 Haute-Savoie**, **73 Savoie**, **05 Hautes-Alpes**.

**Précision géographique** : « Jura » désigne ici le *massif du Jura* et inclut une portion du Doubs, puisque **Métabief est situé dans le Doubs (25)**. La carte utilise une projection affine du WGS84 pour un rendu éditorial ; ce n'est pas une carte de navigation. Les traits de relief en arrière-plan sont purement graphiques et ne sont pas de vraies courbes de niveau.

## Quinze stations (coordonnées WGS84 indicatives)

### Massif du Jura — 2
- Les Rousses — 46.484 / 6.063 (Jura)
- Métabief — 46.774 / 6.350 (Doubs)

### Haute-Savoie — 4
- Megève — 45.857 / 6.618
- Chamonix — 45.922 / 6.869
- La Clusaz — 45.907 / 6.425
- Avoriaz — 46.192 / 6.774

### Savoie — 6
- Courchevel — 45.415 / 6.634
- Méribel — 45.394 / 6.566
- Les Arcs — 45.573 / 6.830
- Tignes — 45.469 / 6.915
- Val d’Isère — 45.448 / 7.000
- Val Thorens — 45.298 / 6.580

### Hautes-Alpes — 3
- Serre Chevalier — 44.940 / 6.587 (point indicatif du domaine)
- Montgenèvre — 44.931 / 6.723
- Vars — 44.572 / 6.689

Les coordonnées localisent des secteurs/villages et **ne garantissent pas un point de rendez-vous**, l'emplacement exact d'une école, d'une remontée ou d'une piste. Les lieux affichés sont des *stations de référence*, pas des implantations commerciales déjà vérifiées.

## Interaction
- Quatre boutons de territoire sélectionnent les stations correspondantes.
- Les stations principales ont une étiquette visible ; les autres apparaissent au survol, au focus ou dans la carte d'information.
- Les étiquettes visibles sont repositionnées en JavaScript pour réduire les collisions.
- Un clic sur une station renseigne « J'ai une station en tête » et le nom de la station dans **le formulaire WhatsApp existant**. L'utilisateur vérifie et envoie lui-même sa demande : aucune réservation ni paiement automatique.
- Le bouton principal permet également de demander une station **non affichée**.
- Sous 850 px, la carte est horizontalement déplaçable. Les préférences de réduction des animations sont respectées.

## Fichiers actifs
- `public/index.html` : carte, contours SVG, 15 points et wording.
- `public/society-map.css` : style premium indépendant, responsive.
- `public/society-map.js` : interactions accessibles et présélection du formulaire.

L'ancien fichier `public/alpine-map.css` reste chargé uniquement pour ses styles historiques de la section « Notre approche ». L'ancien JavaScript de la carte `public/alpine-map.js` n'est plus chargé et peut être nettoyé plus tard après recette complète.

## Restrictions
Ne pas fusionner cette branche sans recette navigateur et validation de la couverture commerciale réelle. Production, DNS et `main` inchangés.
