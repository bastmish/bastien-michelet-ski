# Développement Ski Society — restauration bc9bb78

Le site servi reste statique sous public/. Utiliser le checkout existant ; aucun worktree n’est nécessaire.

## Sources

- content/original-pages/ : snapshots exacts des 16 pages originales.
- content/original-manifest.json : empreintes des pages, des ressources de bc9bb78 et des sources éditoriales conservées.
- content/pages.json : rédaction validée, conservée pour une intégration ultérieure explicitement autorisée. Elle n’est plus injectée dans les pages originales.
- content/stations.json : contenus et SEO des 43 extensions destinations.
- content/premium-footer.html et public/premium-footer.css : seul composant graphique nouveau sur les pages originales.
- content/destinations-index.html : index distinct de l’extension.
- public/integration.css : exclusivement pour les extensions ; interdit sur les pages originales.

## Génération

`python -m venv /tmp/ski-build-venv`
`/tmp/ski-build-venv/bin/pip install -r requirements-build.txt`
`/tmp/ski-build-venv/bin/python scripts/build.py`

La génération restaure littéralement les pages depuis leurs snapshots, applique uniquement le footer, puis rend les 43 destinations et leur index. Elle ne réinterprète pas le design original et ne modifie pas les ressources CSS/JS d’origine.

Ne pas lancer les anciens générateurs d’intégration éditoriale. Les scripts de comparaison de la refonte ont été retirés ; leurs anciens rapports sont archivés.

## Contrôles

- `python tests/check_site.py` : identité exacte hors footer, SHA-256, liens et extension.
- `python -m http.server 3000 --directory public` pour les contrôles locaux.
- `AXE_SCRIPT=/chemin/axe-core/axe.min.js python tests/browser_check.py`, avec Python Playwright et Chromium /usr/bin/chromium.
- `python tests/booking_check.py` pour le formulaire d’origine, sans envoi.
- `python tests/restoration_visual.py` avec Playwright et Pillow ; servir une archive originale de bc9bb78 sur 3004, le site restauré sur 3000. Aucun changement de branche requis.

Les espaces de fin de ligne présents dans les snapshots sont volontairement conservés pour l’identité littérale. Ne pas formatter les pages originales pendant cette étape.

## Publication

noindex,nofollow doit rester actif partout. Ne pas fusionner PR #20 ni déployer en production sans autorisation explicite.

Une éventuelle prévisualisation autorisée utilise `wrangler versions upload --preview-alias review-pr20` et nécessite des accès Cloudflare et réseau effectifs. Ne jamais présenter une adresse locale ou une URL inventée comme lien public.

APPROVED_CANONICAL_ORIGIN reste réservé à un domaine validé ; il ne modifie pas les pages originales et ne soumet aucun sitemap.
