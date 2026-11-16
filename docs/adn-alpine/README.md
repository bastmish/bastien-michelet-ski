# ADN — composition alpine éditoriale

Cette version remplace la proposition à trois cartes du commit 33fb77c. Elle applique la nouvelle demande détaillée du propriétaire : une image dominante, le bloc compétition à droite, puis deux prolongements textuels.

## Composition

- Fond ivoire #F8F7F3, noirs et gris neutres, sans vert, dégradé, ombre, bouton, pictogramme ni animation.
- Une seule photo de compétition, réutilisée dans les ressources originales : centrée, sans texte en superposition. Les photos de musculation, coaching et télésiège sont retirées de cette zone.
- Desktop dès 1280 px : wrapper de 1440 px maximum, marges internes 56 / 96 / 104 px, grille 1.1fr / 0.9fr, gouttière 48 px et intervalle vertical 44 px. Deux textes secondaires de même largeur en deuxième rangée, séparés de 36 px.
- Titre principal à 78 px, graisse 400, dans la famille Clash Display déjà utilisée par le projet ; aucune nouvelle famille n’est ajoutée. La règle est strictement limitée à la zone ADN pour neutraliser la graisse 600 imposée globalement aux titres.
- Le label NOTRE ADN avec son filet est complété par le label validé 01 / LA COMPÉTITION. Ils restent distincts pour préserver chaque texte demandé. L’ancien titre « Le haut niveau laisse une empreinte », son introduction du collectif et le lien ajoutés par la proposition précédente ne figurent plus dans cette zone.
- Tablette : image horizontale au-dessus, titre 58 px, deux blocs secondaires côte à côte au-delà de 980 px, empilés sinon.
- Mobile : NOTRE ADN, image haute de 420 px, compétition, approche, expérience ; titre principal 44 px, paragraphes 17 px et marges latérales de 20 px.
- L’image conserve une préférence de ratio 4/5 avec une hauteur plafonnée à la cible de 760 px sur desktop, puis 16/10 plafonné à 520 px sur tablette. Sa largeur occupe la colonne et le recadrage reste centré.

## Recette

| Contrôle | Résultat |
| --- | --- |
| 9 labels, titres et paragraphes A02, chacun exactement une fois | PASS |
| 32 sections éditoriales et sources immuables | PASS |
| Autres sections et en-tête de la home, hors blancs inter-sections | HTML identique à 33fb77c |
| Autres pages, footer, destinations | HTML identique octet par octet à 33fb77c |
| Liens internes, robots, H1, 43 destinations, 86 CTA locaux | PASS |
| Responsive 1440 / 1280 / 1024 / 768 / 390 px | PASS, sans débordement |
| Ordre mobile, image unique, absence de superposition éditoriale | PASS |
| Deux blocs secondaires et bascules de colonnes | PASS |
| Transitions des chapitres suivants | PASS |
| Graisse réelle du titre : 400 | PASS |
| Erreurs JavaScript | Aucune |
| Axe WCAG A/AA ciblé sur ADN | Aucune violation détectée |
| Ressources photographiques et typographiques distantes | BLOQUÉES |

Commandes : `PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py`, `python tests/check_site.py`, `PYTHONPATH=/tmp/ski-libs python tests/adn_redesign.py`, `git diff --check`. Le test navigateur nécessite un serveur courant sur 3000, la référence 33fb77c sur 3007, Chromium et axe-core. Les chemins de dépendances temporaires sont documentés dans le script.

[Comparaison desktop, tablette, mobile](index.html) et [résultats détaillés](results.json). Les captures constituent une recette de structure ; la validation photographique et typographique finale reste à effectuer lorsque Pexels et les polices seront accessibles. Vérification réseau : CONNECT refusé HTTP 403 / ERR_TUNNEL_CONNECTION_FAILED. Aucun substitut artificiel ni contournement utilisé.

Travail sur feat/ski-society-complete uniquement. noindex,nofollow conservé, aucune fusion de PR, aucun déploiement en production. Aucun lien public Cloudflare créé par cette tâche.
