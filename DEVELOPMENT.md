# Développement Ski Society

Le site est statique : aucun build npm ni secret n’est nécessaire. Utiliser le checkout existant dans l’environnement isolé ; ne pas créer de worktree sauf demande explicite.

- Génération : `python scripts/build.py`.
- Validation statique : `python tests/check_site.py`.
- Prévisualisation locale : `python -m http.server 3000 --directory public`.
- Recette navigateur : installer Python Playwright et axe-core dans un emplacement local, puis `AXE_SCRIPT=/chemin/axe.min.js python tests/browser_check.py` avec Chromium disponible sous /usr/bin/chromium.

Les six pages principales sont rendues depuis `content/pages.json` (32 sections validées). Les destinations sont rendues depuis `content/stations.json` (43 propositions locales). Les composants communs se trouvent dans `content/header.html` et `content/footer.html`. Modifier les sources puis régénérer les fichiers HTML ; les textes validés nécessitent une validation éditoriale avant toute modification.

Le domaine définitif n’étant pas approuvé, aucune canonique n’est inventée. Après validation du domaine, `APPROVED_CANONICAL_ORIGIN=https://domaine-valide python scripts/build.py` génère les canoniques autoréférentes et sitemap.xml. Cette opération conserve noindex,nofollow et ne soumet rien. Ne pas exécuter cette variante avant validation du domaine.

Ne pas déployer ni fusionner sans autorisation explicite. Le push d’une branche peut déclencher une intégration GitHub/Cloudflare déjà configurée par le propriétaire ; aucun outil de déploiement n’est appelé ici.
