# Prévisualisation HTTPS — blocage constaté

La configuration active du fournisseur indique `network_policy.mode = restricted`, `state = enforced` et `allowed_hosts = []`. Les domaines de paquets autorisés par défaut ne comprennent pas Pexels, Google Fonts, Fontshare ni Cloudflare. Les autorisations évoquées plus tôt dans la conversation ne sont donc toujours pas appliquées à cette instance.

Vérification de l’API d’ouverture d’un tunnel de prévisualisation : `curl -I -m 10 https://api.trycloudflare.com` échoue dès CONNECT avec HTTP 403. L’image Pexels échoue également. Les échecs du navigateur sont conservés dans results.json.

Les outils disponibles ne proposent pas d’exposition publique de port ou de création de preview. Un brouillon de configuration ne change pas la politique réseau en cours. Aucun contournement du proxy n’est utilisé.

Pour débloquer une URL Cloudflare, l’environnement doit autoriser l’API et les connexions de tunnel Cloudflare nécessaires ; pour une recette photographique, il doit aussi autoriser les photos et polices du projet. Une fois les accès effectifs, le tunnel et son URL HTTPS pourront être créés et vérifiés. Un tunnel de prévisualisation est distinct d’un déploiement de production.

Aucune adresse localhost n’est présentée comme une URL publique. Aucune URL HTTPS de prévisualisation n’a été créée ou annoncée comme fonctionnelle. La validation finale du rendu photographique et de la preview reste bloquée.
