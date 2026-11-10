# Carte animée — Jura, Haute-Savoie et Suisse (V12.2)

## Inspiration

Animation inspirée du principe de Codrops : carte SVG vectorielle et révélation visuelle liée au défilement.

- Codrops, Tom Miller, « Creating Scroll-Driven SVG Map Animations with GSAP » (21 mai 2026) : https://tympanus.net/codrops/2026/05/21/creating-scroll-driven-svg-map-animations-with-gsap/
- Démonstration : https://tympanus.net/Tutorials/ScrollMap/

Le code de cette carte est une adaptation originale, et non une copie de la démo. GSAP/ScrollTrigger est facultatif, pour une légère animation de caméra. La révélation des stations fonctionne en JavaScript natif, sans API cartographique ni clé payante.

## Géographie et licences

La carte s'appuie sur de vrais contours vectoriels, simplifiés uniquement pour le rendu web.

**France — IGN Admin Express COG, millésime 2018, Licence Ouverte**, via les fichiers départementaux de `gregoiredavid/france-geojson` :

- Jura (39)
- Doubs (25)
- Ain (01)
- Haute-Savoie (74)
- Savoie (73)

Source et licence : https://github.com/gregoiredavid/france-geojson

**Suisse — Office fédéral de la statistique (OFS), frontières cantonales 2025**, via les GeoJSON de `samkhavandi/Swiss_Geography_Look_Ups` :

- GE, VD, VS, FR, NE, JU et BE.

Source : https://github.com/samkhavandi/Swiss_Geography_Look_Ups

Vérifier les éventuelles conditions d'attribution spécifiques de l'OFS avant diffusion publique commerciale. Les traits de relief fins sont décoratifs et ne constituent pas des courbes de niveau réelles.

## Mise en page V12.3 et lac Léman

La section est devenue une composition **éditoriale à deux colonnes** sur ordinateur : titre, six massifs, station sélectionnée et informations à gauche ; carte plus compacte à droite. Sous 1 060 px, les blocs se superposent et la carte reste panoramique/déplaçable horizontalement afin de ne pas réduire les 40 noms à une taille illisible.

Le lac Léman (« lac de Genève ») est représenté en bleu pâle, avec son nom au cœur de la carte. Sa silhouette est **stylisée**, obtenue depuis des points de rive approximatifs : il ne s'agit pas d'une extraction directe d'un contour officiel. Le jeu de données public de référence, à consulter pour une future version géométriquement plus précise, est celui du **Système d'information du territoire à Genève (SITG)**, « GEO_LAC_LEMAN » : https://vector.sitg.ge.ch/arcgis/rest/services/GEO_LAC_LEMAN/FeatureServer/0

Cette représentation d'ambiance reste indicative et ne doit pas être utilisée pour la navigation. Le tracé rouge de découverte des stations est distinct du lac ; il ne représente pas un déplacement réel.

## 40 points de stations et six ensembles

- Jura (8) : Les Fourgs, Métabief, Les Rousses, Saint-Cergue, La Dôle, Lamoura, Mijoux – La Faucille, Lélex. Le groupe regroupe les stations du massif du Jura côté français et suisse.
- Portes du Soleil, Haute-Savoie (7) : Les Gets, Morzine, Avoriaz, Châtel, Abondance, Bernex, Thollon-les-Mémises.
- Grand Massif, Haute-Savoie (5) : Praz de Lys, Samoëns, Morillon, Les Carroz, Flaine.
- Aravis, Haute-Savoie (4) : Le Grand-Bornand, La Clusaz, Manigod, Le Semnoz.
- Pays du Mont-Blanc, Haute-Savoie (8) : Praz-sur-Arly, Megève, Combloux, Saint-Gervais, Les Contamines, Les Houches, Chamonix, Argentière.
- Alpes suisses (8) : Champéry, Les Crosets, Morgins, Leysin, Villars-sur-Ollon, Les Diablerets, Verbier, Crans-Montana.

Références de domaines et d'implantation :

- Jura Tourisme : https://www.jura-tourism.com/vivre-le-jura/pratiquer/ski-sports-hiver/ski-alpin-et-snowboard/
- Suisse Tourisme : https://www.myswitzerland.com/fr-ch/decouvrir/hiver/winter-sport-destinations-search/regions/
- Haute-Savoie Mont-Blanc : https://hautesavoiemontblanc-tourisme.com/notre-destination/hautement-blanche/les-stations/

**Précision :** les coordonnées WGS84 des points de station sont approximatives et indiquent le village/le secteur, pas l'emplacement d'un départ de remontée, de cours ou d'une piste. Le tracé rouge passe par les 40 points et constitue un **chemin graphique de lecture seulement**. Ce n'est pas un itinéraire skiable, de randonnée, routier ou une recommandation de sécurité.

## Interaction V12.2

- La carte apparaît dans le déroulé normal de la page ; un scroll court (~0,74 hauteur d'écran) révèle les 40 points.
- Le tracé SVG progresse jusqu'à chaque point en synchronisation avec les apparitions.
- Les noms révélés restent en permanence sur la carte, même lors du scroll inverse. Le système de liste « Stations découvertes » a été supprimé.
- Les étiquettes sont positionnées pour limiter les superpositions ; les traits fins relient le texte au point si nécessaire.
- En dessous de 950 pixels de large, la carte reste grande et **peut être parcourue horizontalement** au doigt ou à la souris : les noms ne sont pas réduits à une taille illisible.
- Les six boutons de zone dévoilent et sélectionnent les stations correspondantes.
- Clic sur un point ou un nom : la destination est présélectionnée dans le formulaire WhatsApp existant.
- La préférence utilisateur de réduction du mouvement est respectée.
- Le menu, le hero, les offres, les avis et le formulaire restent inchangés.

## Fichiers de la PR

- `public/index.html` — carte SVG, positions et tracé intégral (40 sommets)
- `public/alpine-map.css` — mise en page et animation responsive
- `public/alpine-map.js` — révélation, positionnement des étiquettes et préremplissage du formulaire

**Production :** la PR V12.2 reste en brouillon sur `design/codrops-alpine-map-v12` ; ne pas fusionner automatiquement.
