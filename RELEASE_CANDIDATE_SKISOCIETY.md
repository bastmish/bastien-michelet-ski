# Ski Society — Release candidate premium — 11 novembre 2026

## État
- **Branche candidate intégrée au preview** : `design/codrops-alpine-map-v12`
- **Commit de fusion** : `76c239c5a0d32ae9468dc1051bfa448f8df33859`
- **Production `main` : non modifiée**
- **PR de production existante** : #5 (draft)
- **Version visuelle navigateur : non certifiée**, déploiement Cloudflare non vérifié depuis cette session.

## Page d'accueil
Hero photographique; bandeau preuve; galerie asymétrique 4 expériences; différence technique et pédagogique; méthode à 3 temps; carte des Alpes en deux colonnes; parcours du fondateur; avis historiques; FAQ courte; CTA WhatsApp direct + formulaire facultatif.

## Préparation
- 11 pages harmonisées avec `public/site-premium.css`
- Asset `public/assets/alpes-atlas-society.svg` adouci, contours existants conservés
- Menu, footer Ridgeline et liens internes maintenus
- Scripts GSAP / timeline obsolètes retirés de la page d'accueil
- `noindex,nofollow` maintenu sur la preview
- Formulaire existant conservé, avec message WhatsApp prérempli

## Contrôles techniques effectivement réalisés
- 11/11 pages : liens CSS, menu, footer, main, H1, fermeture HTML présents.
- Home : une seule occurrence du formulaire ; 9 sections avec identifiants d'ancrage ; 8 images.
- CSS : nombre d'accolades ouvrantes et fermantes égal.
- Comparaison GitHub avant intégration : branche candidate 20 commits devant sa base, aucune divergence en retrait.
- PR #7 fusionnée dans la branche de preview.

## Recette indispensable (à réaliser dans le navigateur)
1. **Desktop 1440px** : hero, menu, galerie, sections asymétriques, carte à droite, pied de page.
2. **Tablette 768px** : absence d'overflow horizontal, titres sans collision, navigation.
3. **Mobile 390px** : ouverture/fermeture menu ; galerie et contact ; hauteur footer ; lisibilité de la carte.
4. **Interaction** : boutons offres, formulaire WhatsApp, numéro et message, liens footer, FAQ et ancres.
5. **Réseau** : vérifier toutes les photos Pexels, le SVG, les feuilles CSS, la bonne version Cloudflare.

## Bloqueurs commerciaux/éditoriaux avant mise en production officielle
- Informations légales encore préparatoires (forme juridique, adresse professionnelle, identifiants légaux, carte professionnelle, assurance, email et CGV à finaliser).
- Vérifier droits/attributions et remplacer si possible les photos d'ambiance par des photos réelles de Ski Society.
- Revérifier la note/quantité d'avis Trustpilot historiques avant diffusion.
- Valider les conditions réelles d'activité des moniteurs et destinations.
- Retirer `noindex` au moment de l'ouverture publique et après validation juridique.

## Publication
La PR #5 vers `main` reste **draft** et ne doit être fusionnée qu'après recette visuelle et validation des points ci-dessus. La présence du code dans GitHub ne confirme pas que Cloudflare affiche déjà ce commit.
