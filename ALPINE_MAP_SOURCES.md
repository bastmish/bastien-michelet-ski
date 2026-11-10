# Carte Haute-Savoie — sources et implémentation

## Inspiration Codrops

Cette section est une implémentation originale inspirée du tutoriel de Tom Miller, « Creating Scroll-Driven SVG Map Animations with GSAP », publié par Codrops le 21 mai 2026 :

- https://tympanus.net/codrops/2026/05/21/creating-scroll-driven-svg-map-animations-with-gsap/
- https://tympanus.net/Tutorials/ScrollMap/

Le principe repris : une carte vectorielle, un tracé dessiné au scroll, une légère animation de caméra et un récit cartographique piloté par le défilement. Il ne s'agit pas d'une copie de la démo ni d'un réemploi de ses images/cartes. Le site charge GSAP 3.13.0 et ScrollTrigger par CDN, avec une solution de repli native si le CDN est indisponible.

## Source géographique

Le contour SVG du département de la Haute-Savoie est généré à partir du GeoJSON :

https://github.com/gregoiredavid/france-geojson/blob/master/departements/74-haute-savoie/departement-74-haute-savoie.geojson

Origine : IGN Admin Express COG, millésime 2018 (Licence Ouverte). Les coordonnées de points de stations sont indicatives et projetées depuis la latitude/longitude. Les fins traits de terrain sont décoratifs, **non** des courbes de niveau réelles. Le tracé rouge ne représente **aucun itinéraire routier, piéton, de piste ou hors-piste**.

## Stations et périmètre

24 stations de Haute-Savoie réparties en quatre massifs : Portes du Soleil, Grand Massif, Aravis et Pays du Mont-Blanc. Vérification de la dénomination des stations à l'aide de la liste officielle de Haute-Savoie Mont-Blanc :

https://hautesavoiemontblanc-tourisme.com/notre-destination/hautement-blanche/les-stations/

La présence d'une station sur la carte n'est **pas** une garantie de disponibilité, d'autorisation professionnelle ou de capacité à effectuer une prestation sur place. La destination est discutée avant toute prestation.

## Interaction

- Cartographie affichée sans API de cartographie payante, sans dépôt de cookies, sans géolocalisation du visiteur.
- **V12.1 : scroll accéléré** sur ordinateur : la carte reste visible environ 176vh au total, et les 24 stations se révèlent sur les 76vh de défilement disponibles.
- Chaque point s'active et **son nom reste affiché** sur la carte ; l'affichage ne repart jamais à zéro en remontant le scroll. Placement automatique des étiquettes pour éviter les chevauchements.
- Plus de carrousel temporisé de 2,6 s : la progression du scroll est la source de vérité, avec fonctionnement natif même si GSAP n'est pas téléchargé. GSAP apporte uniquement une subtile mise à l'échelle.
- Clic sur un massif : dévoile rapidement ses stations sans effacer celles déjà apparues.
- Clic sur un point, sur un nom ou sur « Imaginer une journée ici » : le nom de la station est renseigné dans le formulaire du site.
- Écrans étroits : noms cumulés dans un catalogue lisible sous la carte ; carte et marqueurs partagent maintenant exactement le même ratio SVG 1000:650 afin que les points ne soient pas décalés.
- Préférence « réduire les animations » respectée : la carte est immédiatement complètement visible et les transitions sont neutralisées.
- Le titre « Une bonne journée de ski commence par vous » est dorénavant centré et disposé sur deux lignes, sans toucher au contenu de la frise.
- Prévisualisation uniquement avant validation du fondateur.

## Fichiers

- `public/index.html` : structure carte, station pins, SVG géographique
- `public/alpine-map.css` : mise en forme responsive
- `public/alpine-map.js` : interactions, animation et préremplissage de demande
