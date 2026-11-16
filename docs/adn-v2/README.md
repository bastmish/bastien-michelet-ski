# ADN — direction artistique V2

Une seule proposition, conforme à la demande V2. Cette version remplace la composition alpine précédente (0c1bfaf). Le périmètre reste exclusivement la zone ADN de l’accueil.

## Composition et finitions

- Sommet pleine largeur : 620 px à 1440 px, entre 540 et 720 px sur desktop dès 1280 px. Le texte occupe les 37 % de droite, avec 64 px de marge droite et un décalage optique vertical de -10 px.
- La photographie existante de compétition est réutilisée, avec une variante responsive demandée à 2400 px. Aucun nouveau fournisseur ni nouveau visuel n’est introduit. Sa définition effective, ses droits déjà associés au projet et son cadrage restent à confirmer avec l’image accessible.
- La boîte photographique déborde jusqu’à 75 % de la largeur ; le masque neutre s’efface entre 45 % et 63 % du viewport (18 %), avant le début du texte. Il ne s’agit ni d’un filtre appliqué à toute la photo ni d’une séparation géométrique. La silhouette ne peut pas être contrôlée dans cet environnement car la photo est bloquée.
- Le bloc principal contient seulement le label compétition, le titre validé et son paragraphe. Le label supplémentaire NOTRE ADN est retiré, comme le prévoit la V2. Aucun mot des trois contenus validés ne change.
- Fond #F8F7F4, titres Clash Display déjà présents dans le projet, graisse 400. Titre principal clamp(42px,3.9vw,62px), paragraphe 17px/1.65. Aucune famille supplémentaire, carte, bordure autour du texte, ombre, pictogramme ou animation.
- Bande inférieure : contenu maximum 1320 px, marges horizontales 64 px sur desktop, 56 px au-dessus et 72 px en dessous, colonnes égales séparées par 96 px et un filet vertical discret. Labels et titres sont alignés ; la copie conserve sa hauteur naturelle.
- Tablette : image 16:9 plafonnée à 520 px, texte en dessous avec 40 px de padding. Les colonnes secondaires se replient lorsque les deux largeurs utiles de 320 px et la gouttière ne tiennent plus (moins de 816 px).
- Mobile : photo seule en premier, hauteur entre 340 et 420 px, puis compétition, approche et expérience. Aucun masque latéral. Textes avec 24 px de padding horizontal, 48 px entre les blocs, filet horizontal entre les deux derniers. Aucune hauteur fixe de texte.
- Les styles sont isolés sous `.ss-adn-editorial-v2`.

## Recette

| Vérification | Résultat |
| --- | --- |
| 9 labels/titres/paragraphes validés, exactement une fois chacun | PASS |
| 32 sections éditoriales et sources immuables | PASS |
| HTML de l’accueil hors ADN | Identique à 0c1bfaf, hors blancs inter-sections |
| Toutes les autres pages HTML, y compris footer et destinations | Identiques octet par octet à 0c1bfaf |
| SEO, liens internes, robots, 43 destinations et 86 CTA locaux | PASS |
| Viewports 1440×900, 1280×800, 1024×768, 768×1024, 390×844 | PASS |
| Débordement horizontal et troncature | Aucun détecté |
| Hauteur desktop, alignements, ordre mobile, colonnes secondaires | PASS |
| Texte hors de la partie opaque du masque photographique | PASS géométrique |
| Transitions des sections suivantes | PASS |
| Erreurs JavaScript | Aucune |
| Axe WCAG A/AA ciblé sur ADN | Aucune violation détectée |
| Photographie, silhouette, qualité du fondu et polices réelles | BLOQUÉ par le réseau |

Les tests automatiques ne constituent pas une certification de tout le site. Le contrôle de silhouette et de coupe du sportif n’est pas présenté comme réussi : la photo distante est inaccessible. La position `42% 50%` est préparée sur la ressource existante, sans prétendre l’avoir validée photographiquement.

## Captures et reproduction

[Galerie](index.html) : cinq captures aux dimensions exactes des viewports, cinq captures de la section entière et trois références avant modification. Les captures de viewport représentent la navigation réelle, avec son header flottant conservé. Les vues de section entière sont cadrées dans le document sans masquer ni modifier le header.

Commandes :

- `PYTHONPATH=/tmp/ski-libs python scripts/build.py`
- `PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py`
- `python tests/check_site.py`
- `PYTHONPATH=/tmp/ski-libs python tests/adn_redesign.py`
- `git diff --check`

Le test navigateur attend le serveur courant sur 3000, la référence 0c1bfaf sur 3008, Chromium et axe-core. Les chemins de dépendances temporaires sont explicités dans le script.

## Limite de validation

Pexels, Google Fonts et Fontshare échouent avec ERR_TUNNEL_CONNECTION_FAILED. Une requête directe vers l’image 2400 px est également refusée par le proxy (CONNECT HTTP 403). Aucune image simulée ni aucun contournement réseau. Une recette complète avec les photos/polices chargées est nécessaire avant validation visuelle définitive.

Aucune autre direction n’est appliquée : cette proposition est livrée pour validation. Branche feat/ski-society-complete uniquement, noindex,nofollow préservé, aucune fusion ni mise en production.
