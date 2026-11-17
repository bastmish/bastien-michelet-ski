# Réservation et transitions immersives V3

Référence avant : 8653c75. Branche feat/ski-society-complete. [Spécification](specification.md).

**État : réservation implémentée et testée ; validation photographique des transitions BLOQUÉE. La V3 n’est pas déclarée visuellement terminée.**

## Réservation

- Colonne gauche limitée au surtitre, au titre et à l’introduction exacts validés. Une seule ligne rassurante ajoutée selon la spécification : « Disponibilités et modalités confirmées avant toute réservation. »
- Les textes A08 secondaires restent intégralement dans content/pages.json, inchangé. Le contrôle éditorial enregistre explicitement la condensation autorisée de cette vue.
- Grille desktop 42/58 après déduction du gap de 72 px ; conteneur 1320 px et marges internes 48 px. Sur mobile, lecture dans l’ordre surtitre/titre/introduction/formulaire/note, marges de 20 px et padding vertical de 72 px.
- Nouveau panneau : icône WhatsApp vectorielle nommée pour les lecteurs d’écran, titre « Préparer votre message WhatsApp », sous-titre demandé et progression « Étape 1 sur 2 — Votre projet » / « Étape 2 sur 2 — Votre profil ».
- Progression verte de 3 px, labels de 14 px, champs simples de 54 px, aides courtes et regroupement des précisions de groupe/horaires à la fin de la deuxième étape.
- CTA vert uniquement dans ce contexte fonctionnel : « Ouvrir mon message dans WhatsApp », icône de 20 px, flèche de 16 px, hauteur minimale 56 px et focus visible. Retour reste une action secondaire, après le CTA dans l’ordre visuel et clavier.
- Notice sous l’action, exactement selon la nouvelle formulation. Elle ne prétend jamais qu’un message a été envoyé ou une réservation confirmée.
- Les 43 stations, Autre station, la validation, les valeurs conservées et le retrait réel de la demi-journée en freeride restent opérationnels. Les champs facultatifs ne deviennent pas obligatoires.

## Éléments retirés ou masqués de la vue principale

| Élément antérieur | Traitement |
| --- | --- |
| « Votre prochaine expérience commence ici. » | Retiré de l’affichage, conservé en source |
| Deuxième paragraphe éditorial | Retiré de l’affichage, conservé en source |
| Processus complet en trois étapes à gauche | Retiré de l’affichage, conservé en source |
| Deuxième lien WhatsApp sous la colonne gauche | Retiré de l’affichage principal, texte conservé en source |
| « Votre demande privée » seul | Remplacé par le nouvel en-tête fonctionnel explicite |
| « 01 / 02 » / « 02 / 02 » | Remplacés par les étapes nommées |
| Légendes de fieldset dupliquant les étapes | Visuellement masquées, conservées pour la sémantique accessible |
| Aides longues répétées sous participants et format | Regroupées dans une note concise ; règle freeride explicitée au champ concerné |
| « Préparer mon WhatsApp » | Remplacé par l’action explicite demandée |

Sans JavaScript, un lien WhatsApp direct est proposé dans une notice noscript du panneau ; il n’ajoute pas de deuxième CTA visible dans le parcours normal.

## Transitions photographiques préparées

- Trois calques décoratifs réutilisent la photographie alpine déjà référencée dans le contact du projet original : photo Pexels 31112551, variante de 1600 px. Configuration dans content/home-immersive-media.json. Aucun nouveau fournisseur ni fichier de remplissage inventé.
- A, à l’intérieur du haut de Destinations : 160 px desktop / 96 px mobile ; fond de départ minéral, arrivée #111312, contenu en dessous.
- B, à l’intérieur de la fin de Destinations : 160 px desktop / 96 px mobile, vers le blanc uniforme des Avis et FAQ.
- C, au sommet de Réservation : entrée de 200 px desktop / 110 px mobile avec photographie limitée à 460/320 px de haut et voile sombre derrière les textes. Le reste du chapitre garde #111312. Le footer n’est pas modifié.
- Les fonds restent pleine largeur. Calques isolés et non interactifs, photographies en object-fit:cover, gradients de transparence sur les images ; pas de bande grise opaque ni d’animation de défilement.
- Les effets ne s’activent qu’après un chargement réel de l’image (naturalWidth > 0). En cas d’échec, le calque reste masqué et le site conserve ses couleurs unies et ses champs lisibles. Les captures de cet environnement montrent **ce mode de repli**, pas les fondus photographiques validés.

### Blocage restant

Le proxy refuse toujours images.pexels.com avec CONNECT HTTP 403 / ERR_TUNNEL_CONNECTION_FAILED. Les trois calques ont donc l’état `unavailable`, sont masqués et possèdent naturalWidth=0. Une demande d’application des autorisations réseau déjà convenues a été adressée au propriétaire pendant le travail.

L’unique image locale disponible est un petit visuel déjà présent dans le projet ; elle n’est pas substituée à la photo alpine pour fabriquer une preuve visuelle. Aucune image simulée, requête contournant le proxy ou capture recolorée n’est utilisée.

**Restent à vérifier avec les vraies images chargées :** pertinence du cadrage, silhouette ou paysage identifiable, qualité des trois fondus, absence de zones boueuses, contraste photographique et droits/attributions déjà signalés dans LOCAL_VERIFICATION.md. Le simple référencement de la photo existante ne remplace pas ce contrôle. La V3 n’est pas considérée terminée sur ces points.

## Résultats des tests

| Contrôle | Résultat |
| --- | --- |
| 1440×900, 1280×800, 1024×768, 768×1024, 390×844, 375×812 | PASS pour réservation et mode de repli |
| Colonne gauche sans répétition, en-tête WhatsApp et icône accessible | PASS |
| Ordre mobile formulaire puis note rassurante | PASS |
| CTA vert, hauteur ≥56 px, progression 3 px | PASS |
| Deux étapes, progression nommée, retour et données conservées | PASS |
| 43 stations + Autre station et préremplissage depuis le catalogue | PASS |
| Erreurs spécifiques, nombre entier positif, aucun plafond arbitraire | PASS |
| Freeride : retrait de la demi-journée et suppression de la valeur périmée | PASS |
| Prénom et commentaires facultatifs | PASS |
| URL WhatsApp, accents, &, + et retours à la ligne | PASS |
| Ouverture seulement après soumission valide explicite | PASS |
| Aucun message envoyé automatiquement | Confirmé : ouverture externe interceptée pendant les tests |
| Axe WCAG A/AA ciblé, deux étapes et header, desktop/mobile | Aucune violation détectée |
| Débordement horizontal ou erreur JavaScript | Aucun détecté |
| Textes sources des 32 sections, SEO et 43 destinations | Préservés |
| Autres pages HTML et footer | Identiques à la référence |
| Chargement des photos et contrôle visuel des fondus | BLOQUÉ — non validé |

Le résultat axe est ciblé ; il ne certifie pas toute la page ni le contraste avec des photos qui n’ont pas pu charger.

[Galerie avant/après](index.html), [réservation desktop](reservation-step1-1440.png), [réservation mobile](reservation-step1-390.png), [résultats détaillés](results.json), [fichiers](FILES.md).

Commandes : `PYTHONPATH=/tmp/ski-libs python scripts/build.py`, `PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py`, `python tests/check_site.py`, `PYTHONPATH=/tmp/ski-libs python tests/booking_v3.py`, `node --check public/home-system.js`, `git diff --check`. Le navigateur de test est Chromium avec Playwright/axe-core ; la référence est servie sur 3013 et la version courante sur 3000.

main inchangée, PR #20 non fusionnée, aucun déploiement en production. noindex,nofollow maintenu. Les preuves fonctionnelles sont livrées ; la validation finale des photographies reste en attente.
