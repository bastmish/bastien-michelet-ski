# Recette — restauration exacte de bc9bb78

Le rapport courant est RESTORATION.md. Les captures de la refonte précédente sont des archives.

## Résultats

- 16 pages HTML : identité littérale hors footer et ressources propres au footer.
- 25 ressources originales : SHA-256 identique à bc9bb78.
- content/pages.json et content/stations.json : empreintes conservées, aucune réécriture.
- 43 destinations : tous les textes locaux et les métadonnées vérifiés ; 86 CTA spécifiques conservés.
- Liens et ancres internes, un H1, noindex,nofollow : PASS.
- 14 comparaisons visuelles originales/restaurées : pixels identiques avant le footer à 1440 et 390 px.
- 32 captures et rapport comparatif dans docs/restoration/.
- 51 pages, 153 rendus responsive : aucun débordement ni erreur JavaScript.
- Navigation, formulaire, FAQ et recherche originaux : PASS.
- Index et recherche de l’extension vers la bonne fiche : PASS.
- Footer fonctionnel : aucune violation axe-core sur les règles testées.
- Aucun message WhatsApp envoyé.

Le contrôle d’espaces Git peut signaler des espaces finaux provenant des fichiers de bc9bb78. Ils sont volontairement restaurés : le contrôle d’identité vérifie leur provenance exacte. Ils ne sont pas « corrigés » au prix d’une modification de la référence.

## Limites

Les photos et polices distantes restent refusées par le proxy. Aucune substitution n’est faite dans les captures. La comparaison est fiable pour le rendu disponible et complétée par les empreintes du code et des URLs ; elle ne constitue pas une recette complète des ressources distantes chargées.

Les animations sont figées uniquement pour le test visuel déterministe. Le JavaScript livré est exactement celui de bc9bb78.

Les observations d’accessibilité générales sont enregistrées dans tests/browser-results.json. Les imperfections de la référence ne sont pas corrigées sur les pages originales. Cela inclut les comportements et contenus de démonstration déjà présents dans la référence, qui restent étiquetés comme tels.

Les contrôles métier restent ceux de LOCAL_VERIFICATION.md : destinations, autorisations suisses, La Grave, qualifications/assurances, photos, numéro WhatsApp et modalités opérationnelles. Les nouveaux textes des six pages demeurent des sources non réinjectées.

Aucun déploiement en production, aucune fusion, aucune soumission de sitemap et aucune activation de l’indexation.
