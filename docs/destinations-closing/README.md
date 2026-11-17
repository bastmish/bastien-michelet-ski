# Bandeau final Destinations

Branche feat/ski-society-complete. Référence avant : 528f726. Une modification limitée au bandeau de fin de Destinations.

## Composition

- Suppression de l’ancien lien-bandeau, du compteur géant 43., du point rouge et de la grille en trois zones.
- Nouveau bloc éditorial pleine largeur avec fond #111312 et bordure supérieure #424744. Son conteneur est limité à 1320 px, avec padding horizontal 48 px ; padding haut 64 px et bas 80 px sur desktop.
- Surtitre, titre et description repris exactement depuis la nouvelle formulation. Ils sont isolés dans content/destinations-closing.json pour conserver une trace claire de cette révision explicitement approuvée, sans altérer les sources éditoriales originales.
- Titre 48 px, graisse 500, ligne 1.08, largeur maximum 780 px. Paragraphe 17 px, ligne 1.65, maximum 720 px. CTA clair ajusté à son contenu, hauteur 52 px, flèche diagonale de 18 px.
- Mobile : padding horizontal 20 px et vertical 48 px, titre 34 px, paragraphe 16 px, CTA pleine largeur.
- Le bandeau est placé hors du conteneur des cartes, dans le wrapper sombre de Destinations. L’ancien padding inférieur redondant de cette section est supprimé pour que le nouveau padding de 80/48 px termine directement le chapitre ; les Avis commencent ensuite en blanc, sans espace intermédiaire.
- Les quatre cartes de stations et tout le reste du DOM de l’accueil restent identiques, hors bandeau et révision CSS. Aucun JavaScript ni élément de réservation modifié.

## Vérifications

| Contrôle | Résultat |
| --- | --- |
| 1440×900, 1280×800, 1024×768, 768×1024, 390×844, 375×812 | PASS |
| Textes du nouveau bandeau, mot pour mot | PASS |
| Ancien compteur et ancien bandeau retirés | PASS |
| Dimensions, paddings, tailles et graisse calculées | PASS |
| Fond #111312, pleine largeur, pixels gauche/centre/droite | PASS |
| Destinations → Avis : frontières contiguës | PASS |
| Pas de débordement horizontal | PASS |
| CTA vers stations.html, navigation réelle au clavier | PASS |
| Focus visible 2 px et axe WCAG A/AA ciblé desktop/mobile | Aucune violation détectée |
| Quatre stations mises en avant | HTML identique à 528f726 |
| Autres pages, 43 fiches, métadonnées, liens et 86 CTA locaux | PASS, inchangés |
| Formulaire, scripts, sources éditoriales et données stations | Identiques à la référence |
| Erreurs JavaScript | Aucune |

[Galerie avant/après](index.html), [desktop](after-1440.png), [mobile](after-390.png), [résultats détaillés](results.json).

Commandes : `PYTHONPATH=/tmp/ski-libs python scripts/build.py`, `PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py`, `python tests/check_site.py`, `PYTHONPATH=/tmp/ski-libs python tests/destinations_closing.py`, `git diff --check`.

Le test navigateur attend le serveur courant sur 3000, la référence 528f726 sur 3012, Chromium, Playwright et axe-core. Les contrôles de périmètre des tests antérieurs sont adaptés uniquement pour autoriser ce remplacement expressément demandé.

Le bandeau ne comporte aucune photographie. Les polices distantes restent bloquées par le proxy : les captures montrent le rendu réel avec la police de repli, sans substitution d’image ni recoloration. La famille typographique du projet est conservée dans les styles.

main inchangée, aucune fusion de la PR #20 ni publication en production ; noindex,nofollow conservé. Proposition en attente de validation visuelle.
