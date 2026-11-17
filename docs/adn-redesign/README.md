# ADN — nouvelle composition de la home

Modification limitée aux zones `#expertise` et `#adn` de l’accueil, par rapport au commit f321a69. Le HTML de l’accueil hors de ces zones et du lien vers sa nouvelle feuille CSS a été comparé : identique. Les autres pages publiques ne changent pas.

## Choix de design

- Une seule grande photo de compétition ouvre la séquence, face à un bloc éditorial clair. L’asymétrie, le titre plus affirmé et les espaces donnent une hiérarchie nette.
- L’introduction réutilise mot pour mot le surtitre et le paragraphe validés du collectif (B01) et le titre validé B02. Elle évite de répéter les textes des trois cartes.
- Les trois contenus ADN A02 restent intégralement présents : labels, titres et paragraphes inchangés. Les photos sont au-dessus ; les textes sont dans le flux, jamais en superposition.
- Les trois colonnes ont des cadrages et hauteurs décalés sur ordinateur ; elles deviennent une séquence verticale sur mobile. Pas d’ombre ni d’arrondi décoratif ; filets fins, couleurs papier/encre et typographies existantes.
- Les ressources photographiques existantes sont réutilisées. La seconde grande photo du diptyque n’est plus dupliquée : elle reste dans la carte transmission. Les transitions de couleur des chapitres suivants, le footer et la navigation restent identiques.

## Vérifications

| Contrôle | Résultat |
| --- | --- |
| 32 sections éditoriales et intégrité des sources | PASS |
| 43 destinations, métadonnées, liens et 86 CTA locaux | PASS |
| noindex,nofollow, titres H1, liens internes | PASS |
| Largeurs 375 / 768 / 1440 : aucun débordement | PASS |
| Trois cartes, textes hors image, espacement image/label | PASS |
| Transitions des chapitres suivants | PASS |
| Erreurs JavaScript pendant la recette | Aucune |
| Axe WCAG A/AA sur les deux sections ADN | Aucune violation détectée |
| git diff --check | PASS |
| Photos et polices distantes | BLOQUÉ par le proxy réseau |

Recette : `tests/adn_redesign.py`, `tests/check_editorial.py`, `tests/check_site.py`. Les contrôles axe sont limités à cette zone et ne constituent pas une certification de tout le site.

[Comparaison ordinateur/mobile](index.html), captures brutes avant/après à 1440 et 390 px, [résultats détaillés](results.json).

Les captures ne remplacent pas la validation avec photos et polices chargées : Pexels, Google Fonts et Fontshare échouent avec ERR_TUNNEL_CONNECTION_FAILED. Aucun remplacement artificiel n’est utilisé. Aucun lien public Cloudflare n’a été créé dans cet environnement. Aucun déploiement de production, aucune fusion, aucune modification de main.
