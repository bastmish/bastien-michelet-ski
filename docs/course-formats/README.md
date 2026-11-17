# UI SPEC 04 — Formats des cours privés

Proposition limitée à l’accueil, section 04 et sa liaison avec la section 03. Référence : 14df990. Les autres pages et sections restent identiques.

## Changements HTML et CSS

- Nouveau composant sémantique `section.ss-course-formats` avec header, trois articles et footer de section. Styles dans `public/course-formats.css`, chargé uniquement par la home.
- Les catégories DEMI-JOURNÉE, JOURNÉE COMPLÈTE et SUR MESURE sont les premiers repères des lignes. Titres éditoriaux et paragraphes validés restent intégralement visibles, suivis des créneaux indicatifs pour la demi-journée. Durées alignées à droite.
- Les lignes ne sont pas cliquables et n’ont pas de flèche. Le seul CTA « Parlons de votre projet » mène à `#contact`, le parcours existant, sans réservation immédiate ni nouvel envoi WhatsApp.
- Note horaire conservée mot pour mot. Rappel métier ajouté : « Freeride : journée complète ou sur mesure. »
- Le nouveau libellé d’interface « 04 / NOS FORMATS DE COURS PRIVÉS » ne remplace pas la copie approuvée : « 04 / VOTRE PROGRAMME » reste dans le pied compact. Le numéro, la catégorie et la durée issus des métadonnées sources sont répartis dans les colonnes ; aucun mot n’est remplacé.
- Fond #F7F6F2, titres graphite, filets fins, aucun visuel nouveau, ombre, carte flottante ou chiffre décoratif. Le titre ne contient plus de retour à la ligne forcé ni de deuxième ligne grise.
- Transition : entourage de la section 03 sur le même fond minéral, titres et introduction adaptés à ce fond, suppression du padding inférieur, distance de 88 px mesurée entre la grille des expériences et le H2 Formats à partir de 1200 px. Pour respecter ce rythme, le padding supérieur effectif est de 50 px sur desktop plutôt que 72 px : le label de 16 px et sa marge de 22 px complètent les 88 px.
- Les quatre cartes d’expériences conservent exactement leur HTML, leurs dimensions, typographies, cadrages et interactions. Leur canevas noir existant est maintenu derrière la grille pour conserver le contraste blanc sur noir ; il n’y a pas de bande noire supplémentaire entre les deux sections.
- Responsive : colonnes tablette et disposition mobile catégorie/durée, puis sous-titre/description. CTA pleine largeur sur mobile et aucun texte à hauteur fixe.
- Le pied sémantique de section est isolé des règles génériques de footer. Le générateur de footer global exclut désormais ce footer interne ; le footer du site et toutes les autres pages sont identiques à la référence. Le composant Programmes de Notre histoire est conservé séparément pour éviter toute généralisation.

## Ajustements nécessaires aux contraintes

- Les petits numéros utilisent #68716A, token muted de la spécification, plutôt que #8A918B : cette dernière valeur échoue au contrôle de contraste sur le fond minéral. La version livrée passe axe-core sur les règles WCAG A/AA testées.
- La hauteur réelle à 1440 px est d’environ 1107 px, supérieure à la cible indicative 680–790 px. L’intégralité de la copie, les sous-titres éditoriaux, les créneaux et les espacements de ligne imposés sont conservés. Aucune hauteur artificielle ni troncature n’est utilisée pour atteindre cette cible.

## Résultats

| Contrôle | Résultat |
| --- | --- |
| Tous les textes de la section 04 | PASS, sources immuables |
| 32 sections éditoriales | PASS |
| 43 destinations, métadonnées, liens et 86 CTA locaux | PASS |
| HTML des autres pages | Identique octet par octet à 14df990 |
| Accueil hors section 04 et classe de transition section 03 | Identique à la référence |
| Quatre cartes d’expériences | HTML, dimensions et typographies identiques |
| 1536×960, 1440×900, 1280×800, 1024×768, 768×1024, 390×844, 375×812 | PASS |
| Débordement horizontal, troncature | Aucun détecté |
| Catégories/durées alignées et visibles | PASS |
| Espacement desktop grille / H2 | 88 px |
| CTA au clavier et focus visible | PASS : ouverture de #contact, formulaire existant présent |
| Axe WCAG A/AA ciblé sur la section | Aucune violation détectée |
| Erreurs JavaScript | Aucune |
| Photos et polices distantes | BLOQUÉES par le proxy |

Le contrôle d’accessibilité est ciblé et ne constitue pas une certification globale. Aucun message ni formulaire n’a été envoyé. Les horaires sont clairement indicatifs et ne représentent pas des disponibilités confirmées.

## Captures et reproduction

[Galerie](index.html) : expériences et formats ensemble à 1440 px, comparaison avant/après, vues complètes et vues de viewport aux sept largeurs demandées. [Résultats détaillés](results.json).

Les photos Pexels et les polices distantes restent refusées par le proxy (ERR_TUNNEL_CONNECTION_FAILED). Les photos existantes des expériences ne sont pas remplacées. La section Formats ne contient aucune photographie. Les captures utilisent les polices de repli lorsque les polices projet ne sont pas chargées.

Commandes :

- `PYTHONPATH=/tmp/ski-libs python scripts/build.py`
- `PYTHONPATH=/tmp/ski-libs python tests/check_editorial.py`
- `python tests/check_site.py`
- `PYTHONPATH=/tmp/ski-libs python tests/course_formats.py`
- `git diff --check`

Le test navigateur utilise Chromium, Playwright et axe-core ; serveur courant sur 3000, référence 14df990 sur 3009. Leurs chemins sont indiqués dans le script. Les anciens rapports ADN restent des archives de leurs propositions respectives.

Branche feat/ski-society-complete uniquement, main inchangée, noindex,nofollow conservé, aucune fusion de PR ni mise en production. Proposition à valider avant toute généralisation.
