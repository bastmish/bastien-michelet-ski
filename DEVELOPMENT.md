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
