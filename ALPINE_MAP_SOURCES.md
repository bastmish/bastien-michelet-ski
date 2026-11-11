# SKI SOCIETY — Carte alpine relief 3D (V15)

## Décision éditoriale
Référence visuelle : Harris Mountains Heli-Ski, étude de design Fluid (https://fluid.co.nz/work/harris-mountains-heli-ski/). Inspiration graphique : relief spectaculaire, cartographie hivernale épurée, quelques zones cuivrées et points de stations. **Aucun code, visuel, marque, logo ou photographie appartenant au site Harris Mountains n'a été copié.** L'implémentation est originale.

Message à côté de la carte : « Nous venons à vous. Dans la station où vous passez vos vacances. » Le texte reste accompagné des réserves sur la disponibilité des moniteurs, les autorisations professionnelles et l'organisation concrète des demandes.

## Pile technique gratuite

- **MapLibre GL JS 6.16.0**, moteur WebGL open source, licence BSD-3-Clause. https://github.com/maplibre/maplibre-gl-js
- **Maptoolkit.org Community**, style **Winter 3D** : https://styles.maptoolkit.org/winter-3d.json et https://docs.maptoolkit.org/map-styles/3d-terrain/
- Fond de carte de type hivernal, relief Mapterhorn, hillshade et terrain 3D configurés par la feuille de style.
- Aucune clé API ni abonnement requis tant que les critères du Community License s'appliquent.
- Documentation du service et licence : https://www.maptoolkit.org/ et https://www.maptoolkit.org/tos

**Conditions à surveiller avant publication et ensuite :**
1. Utilisation commerciale gratuite limitée aux entreprises dont le CA consolidé annuel est strictement inférieur à 1 M€ **et** qui emploient moins de 10 équivalents temps plein, selon les termes en vigueur en novembre 2026.
2. Le logo Maptoolkit doit rester visible dans la carte, à au moins **24 px de hauteur**. Le vrai logo officiel est chargé depuis `https://www.maptoolkit.org/assets/maptoolkit-attribution.png` et affiché à 26 px (25 px mobile).
3. Les crédits © Maptoolkit et © OpenStreetMap doivent être affichés en permanence et cliquables : `attributionControl: {compact:false}`, sans masque ou superposition.
4. Service à disponibilité « best effort », sans SLA ; ne pas utiliser pour navigation de sécurité.
5. Si les conditions commerciales sont dépassées, négocier une licence Enterprise ou migrer vers une autre source.

## Relief et précision
Maptoolkit Winter 3D emploie les données Mapterhorn (https://mapterhorn.com/) dont les sources sont mixtes, publiées selon leurs licences d'origine (https://mapterhorn.com/attribution/). L'affichage topographique est une représentation graphique et **n'est pas une carte d'itinéraires hors-piste ou un outil de décision de sécurité**.

Contour d'emphase : GeoJSON `public/ski-regions.geojson` créé à partir des géométries réelles du référentiel **IGN Admin Express COG 2018**, Licence Ouverte, via :
https://github.com/gregoiredavid/france-geojson/blob/master/departements-version-simplifiee.geojson

Codes : 39 = Jura, 25 = Doubs (pour inclure Métabief), 74 = Haute-Savoie, 73 = Savoie, 05 = Hautes-Alpes.

## 4 territoires et 15 stations repères

Jura (massif, avec Doubs) : Les Rousses, Métabief.
Haute-Savoie : Megève, Chamonix, La Clusaz, Avoriaz.
Savoie : Courchevel, Méribel, Les Arcs, Tignes, Val d'Isère, Val Thorens.
Hautes-Alpes : Serre Chevalier, Montgenèvre, Vars.

Les coordonnées sont indicatives (point de village / zone de station) : ce ne sont ni des rendez-vous ni une preuve de couverture commerciale. **Ne jamais promettre qu'un membre est disponible partout tant que le réseau n'est pas constitué.**

## UX
- Vue panoramique initiale et vraie carte interactive 3D.
- Choix d'une région : recentrage animé et relief dans le territoire choisi.
- Marqueurs cuivrés ; les stations marquantes reçoivent un nom visible dans la zone active ; les autres noms apparaissent au survol/focus.
- Clic sur un marqueur : destination préremplie dans le formulaire WhatsApp existant. **Pas de réservation, paiement, ni envoi automatique.**
- CTA principal pour les stations non affichées dans la sélection.
- Sous 850 px, la carte reste dans le cadre et se manipule au toucher ; aucune grande image panoramique à faire défiler horizontalement.
- `prefers-reduced-motion` : pas d'animation obligatoire.
- Chargement différé via IntersectionObserver ; message alternatif si WebGL indisponible.

## Fichiers actifs
- `public/index.html` : cadrage et cadre MapLibre 3D, logo Maptoolkit, crédits.
- `public/society-map.js` : import de MapLibre, carte hiver, affichage des stations, navigation entre territoires, interactions.
- `public/society-map.css` : interface éditoriale et surcharge graphique autour du canvas.
- `public/ski-regions.geojson` : contours réels IGN simplifiés (5 départements).
- `public/app.js` : le formulaire WhatsApp déjà en place ; aucune modification en V15.

Les anciens `alpine-map.js` et les anciennes règles de carte CSS ne sont pas exécutés ; le CSS global `alpine-map.css` reste lié temporairement car il contient des styles encore nécessaires à la section « Notre approche ».

**Validation restante** : test navigateur réel (chargement du CDN, style 3D, adaptation mobile, WebGL, crédits visibles), contrôle performance et validation graphique. Ne pas fusionner ou déployer sur les domaines acquis sans accord explicite.
