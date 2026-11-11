# Ski Society — Refonte de l’architecture (v21) — Rapport de livraison

## Objectif et limites
Restructuration du site existant pour faire apparaître immédiatement l’offre privée de ski et snowboard, l’expertise sportive et la prise de contact personnelle. **Aucun rebranding** : logo, blanc dominant, rouge alpin, polices, navigation flottante et footer Ridgeline conservés.

## Architecture home — ordre implémenté
1. Hero immersive « Le ski, autrement. »
2. Bandeau de crédibilité (15 ans, 7 ans, tous niveaux, ski/snowboard)
3. Quatre expériences (ski privé, performance & technique, freeride & découverte, snowboard)
4. Expertise et transmission issues du sport de haut niveau
5. Expérience sur mesure (approche personnelle, technique, plaisir)
6. Destinations : Megève, Chamonix, autres stations sur demande
7. Avis historiques du fondateur — lien externe, sans avis inventé
8. Formules : demi-journée, journée, expérience personnalisée
9. FAQ (huit questions)
10. Contact WhatsApp direct, message prérempli

## Modifications principales
- `public/index.html` : réorganisation de la home, menu et footer révisés.
- `public/architecture-v21.css` : grilles, typographie, rythme éditorial et responsive (sans remplacer le design existant).
- `public/offres/index.html` : nouvelle sélection d’expériences.
- **Nouvelles pages** : `public/offres/ski-prive.html`, `public/offres/performance-technique.html`, `public/offres/freeride-decouverte.html`, `public/offres/snowboard.html`.
- **Anciennes pages** : `progresser.html`, `famille.html`, `amis.html`, `explorer.html` redirigent vers les nouvelles catégories.
- `public/manifesto.html` et `public/legal/*.html` : navigation et pied de page à jour. Confidentialité alignée sur le contact sans formulaire.
- Scripts GSAP et styles obsolètes de l’ancienne home retirés de la page d’accueil.

## Tests effectivement réalisés
- Audit GitHub du HTML/CSS/JS existant et comparaison avec l’architecture cible.
- Vérification de l’ordre des sections : neuf `<section>` et un bandeau de crédibilité = dix blocs.
- Vérification d’un seul H1 en home, de quatre cartes d’expériences avec pages dédiées, de huit questions de FAQ et du lien WhatsApp.
- Analyse statique des liens et ancres de la home et des pages d’expériences : **aucune erreur détectée dans les pages contrôlées**.
- Redirections des quatre anciennes URL et liens des pages légales vérifiés.
- Équilibre des accolades dans `architecture-v21.css` : OK.
- Confirmation des fichiers après fusion sur la branche de prévisualisation.
- **Non réalisé** : recette visuelle complète desktop/tablette/mobile, exécution du formulaire ou de WhatsApp sur appareil réel, audit accessibilité automatisé, contrôle de poids des images.

## Points à valider avant production
1. Rendu à 1440 px, 768 px, 390 px : cadrages, navigation mobile, CTA, footer animé et absence de débordement.
2. Disponibilités réelles et habilitations des moniteurs pour chaque discipline et zone.
3. Mentions obligatoires : immatriculation, assurance, carte professionnelle, conditions commerciales et contact professionnel.
4. Photos provisoires : les visuels des destinations sont **illustratifs, pas identifiés comme des photographies de Megève ou de Chamonix** ; droits à vérifier.
5. Avis Trustpilot historiques du fondateur à vérifier avant toute citation chiffrée.
6. Le flag `noindex,nofollow` est conservé pour la preview et doit faire l’objet d’un choix explicite avant production.

## Livraison et déploiement
PR #8 fusionnée sur la branche de prévisualisation `design/codrops-alpine-map-v12`, commit `53872f0e7197f241e663f4f9c3f630b6403634d2`. Production `main` inchangée.

URL habituelle de prévisualisation (à vérifier ; le déploiement Cloudflare n’est pas confirmé) :
https://design-codrops-alpine-map-v12-bastien-michelet-ski.bastienmichelet-pro.workers.dev/

La PR #5 vers `main` ne doit pas être fusionnée sans validation explicite.
