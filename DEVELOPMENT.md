# Développement Ski Society

Le site servi est statique sous public/. Utiliser le checkout existant, sans créer de worktree sauf demande explicite.

## Sources et génération

- content/original-pages/ : référence de composition bc9bb78.
- content/pages.json : 32 sections validées ; ne pas réécrire sans autorisation.
- scripts/editorial.py : intégration explicite dans les composants d’origine, page par page.
- content/stations.json : 43 destinations et leurs métadonnées.
- content/premium-footer.html / public/premium-footer.css : footer indépendant.
- public/editorial-content.css : adaptations limitées aux nouveaux contenus.
- public/integration.css : pages extensions uniquement ; non chargé par les six pages principales.

Installer les dépendances de génération dans un environnement local :
`python -m venv /tmp/ski-build-venv`
`/tmp/ski-build-venv/bin/pip install -r requirements-build.txt`
`/tmp/ski-build-venv/bin/python scripts/build.py`

Le générateur charge la référence graphique, y intègre les textes approuvés, remplace le footer puis rend les destinations. Ne pas rétablir une génération qui ignore content/pages.json ni réintroduire un template graphique générique.

## Vérifications

- `PYTHONPATH=/chemin/bs4 python tests/check_editorial.py` : 32 sections, sources immuables, photos/styles d’origine et absence d’anciens paragraphes marketing.
- `python tests/check_site.py` : liens, ancres, robots, H1, destinations, métadonnées et WhatsApp.
- `python -m http.server 3000 --directory public`.
- `AXE_SCRIPT=/chemin/axe.min.js python tests/browser_check.py` avec Python Playwright et Chromium.
- `python tests/booking_check.py` : formulaire et formats, sans envoi.
- `python tests/editorial_visual.py` : référence bc9bb78 servie sur 3004 et site courant sur 3000 ; aucune modification de branche nécessaire. Les ressources externes en échec sont consignées.

## Publication

Conserver noindex,nofollow. Ne pas modifier main, fusionner PR #20 ni déployer en production sans autorisation explicite. Aucune URL publique de prévisualisation ne doit être annoncée sans avoir été obtenue et vérifiée.

APPROVED_CANONICAL_ORIGIN demeure réservé à un domaine approuvé ; aucun sitemap n’est soumis automatiquement.
