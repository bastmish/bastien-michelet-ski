# Développement Ski Society

Le site livré reste statique. Utiliser le checkout existant dans l’environnement isolé ; ne pas créer de worktree sans demande explicite.

## Génération

Installer les dépendances du générateur dans un environnement Python local :
`python -m venv /tmp/ski-build-venv`
`/tmp/ski-build-venv/bin/pip install -r requirements-build.txt`
`/tmp/ski-build-venv/bin/python scripts/build.py`

Les copies validées sont dans content/pages.json ; les 43 fiches sont dans content/stations.json. Les fichiers content/templates conservent les compositions de main (bc9bb78). Le générateur remplace les contenus au sein des composants de référence et construit les déclinaisons offres/destinations. Ne pas modifier les copies validées sans accord éditorial.

styles.css, architecture-v21.css, site-nav.css, manifesto.css et les animations historiques sont conservés. integration.css ne traite que l’intégration des textes longs, les nouveaux composants et les corrections de contraste. La couche graphique edition.css a été supprimée.

## Vérification

- `python tests/check_site.py`
- `python -m http.server 3000 --directory public`
- `AXE_SCRIPT=/chemin/axe-core/axe.min.js python tests/browser_check.py` avec Python Playwright et Chromium /usr/bin/chromium.
- `python tests/visual_compare.py` : serveurs de référence sur 3001, proposition rejetée sur 3002, correction sur 3000. Les snapshots de comparaison proviennent de git archive, sans modifier main.

## Prévisualisation Cloudflare uniquement

Avec un accès Cloudflare valide et les domaines réseau autorisés :
`npx wrangler versions upload --preview-alias review-pr20 --message "Visual correction PR20 - preview only"`

Cette commande téléverse une version de prévisualisation sans activer la version en production. Vérifier l’URL HTTPS effectivement retournée, le contenu et les en-têtes robots avant de la transmettre. Ne pas employer une commande de déploiement de production, ne pas modifier main et ne pas fusionner la PR #20.

Les canoniques et le sitemap attendent toujours un domaine définitif approuvé. APPROVED_CANONICAL_ORIGIN permet leur génération ultérieure ; ne pas soumettre le sitemap ni retirer noindex,nofollow.

## Deuxième passe design

art-direction.css porte la composition resserrée de la home et le footer partagé en deux étages. integration.css reste chargé pour les pages intérieures. Le générateur prend en charge le nouveau footer pour toutes les pages non redirigées ; les scripts et styles de l’ancien footer ne sont plus chargés.

La FAQ est déplacée sans réécriture vers questions.html, alimentée par la section a07 de content/pages.json. Les programmes de la home et le formulaire de demande utilisent des éléments details/summary natifs, fermés par défaut. Le formulaire doit être ouvert avant de tester ses champs.

Pour les captures avant/après de cette passe : servir un git archive de 5a9cc1f sur le port 3003 et le site courant sur 3000, puis exécuter tests/design_pass2.py. Il n’est pas nécessaire de créer un worktree ni de modifier main.
