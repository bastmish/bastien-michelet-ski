/* Ski Society — independent sample testimonials, no Trustpilot content scraping.
   All ten demo reviews are invented and labelled as such. Never publish as authentic.
   Real client quotes require source verification and consent.
   This is NOT an official Trustpilot widget, nor a live Trustpilot integration.
   Example record format:
   { quote: "Customer's exact approved quote", name: "First name or initials",
     context: "Cours privé · hiver 2025", date: "2025-02-01", sourceUrl: "https://...",
     consent: true }
   Keep sourceUrl only for directly attributable and permitted sources.
*/
(function () {
  'use strict';
  const testimonials = [
    { quote: "Une vraie différence sur la technique dès les premières descentes. Les conseils sont précis, faciles à appliquer et on repart avec des pistes de progression concrètes.", name: "Exemple 01", context: "Ski privé · Savoie", demo: true },
    { quote: "Superbe journée en montagne. Le programme a évolué avec notre niveau et les conditions, sans jamais nous presser.", name: "Exemple 02", context: "Journée privée · Haute-Savoie", demo: true },
    { quote: "J'avais envie de retrouver de la confiance sur les pistes plus engagées. L'accompagnement et les explications ont tout changé.", name: "Exemple 03", context: "Progression · Chamonix", demo: true },
    { quote: "Une expérience qui va bien au-delà d'un cours classique. On prend le temps de comprendre le terrain et de profiter de chaque descente.", name: "Exemple 04", context: "Expérience sur mesure", demo: true },
    { quote: "L'équilibre entre exigence technique et plaisir de skier était exactement ce que nous recherchions.", name: "Exemple 05", context: "Perfectionnement · Megève", demo: true },
    { quote: "Notre groupe n'avait pas le même niveau. La journée a pourtant fonctionné pour tout le monde, du premier au dernier virage.", name: "Exemple 06", context: "Ski en groupe", demo: true },
    { quote: "Des conseils clairs, aucune formule compliquée et de vrais progrès sur les appuis. Très bonne approche pédagogique.", name: "Exemple 07", context: "Technique alpine", demo: true },
    { quote: "Le choix des itinéraires et l'attention portée aux conditions ont rendu la découverte du domaine particulièrement agréable.", name: "Exemple 08", context: "Découverte · Alpes", demo: true },
    { quote: "J'ai particulièrement apprécié la capacité à ajuster les exercices. On comprend pourquoi on fait les choses, pas seulement comment.", name: "Exemple 09", context: "Coaching · Ski", demo: true },
    { quote: "Une demi-journée intense, conviviale et extrêmement utile. C'est le genre de moment qui redonne envie de skier davantage.", name: "Exemple 10", context: "Demi-journée privée", demo: true },
  ];
  const marquee = document.getElementById('ss-reviews-marquee');
  if (!marquee) return;
  const allowed = testimonials.filter(t =>
    t && (t.demo === true || t.consent === true) && typeof t.quote === 'string' && t.quote.trim() &&
    typeof t.name === 'string' && t.name.trim());
  if (!allowed.length) return;
  const cols = Array.from(marquee.querySelectorAll('[data-reviews-col]'));
  function makeCard(t) {
    const figure = document.createElement('figure');
    figure.className = 'ss-review-card';
    if (t.demo) {
      const tag = document.createElement('span');
      tag.className = 'ss-review-demo-tag';
      tag.textContent = 'AVIS FICTIF · DÉMONSTRATION';
      figure.appendChild(tag);
    }
    const quote = document.createElement('blockquote');
    quote.textContent = t.quote;
    figure.appendChild(quote);
    const cap = document.createElement('figcaption');
    cap.className = 'ss-review-person';
    const avatar = document.createElement('span');
    avatar.className = 'ss-review-avatar';
    avatar.setAttribute('aria-hidden','true');
    avatar.textContent = t.name.trim().charAt(0).toUpperCase();
    const details = document.createElement('span');
    details.className = 'ss-review-person-info';
    const author = document.createElement('strong');
    author.textContent = t.name;
    details.appendChild(author);
    if (t.context || t.date) {
      const meta = document.createElement('small');
      meta.textContent = [t.context, t.date].filter(Boolean).join(' · ');
      details.appendChild(meta);
    }
    cap.appendChild(avatar); cap.appendChild(details);
    figure.appendChild(cap);
    if (t.sourceUrl && /^https:\/\//.test(t.sourceUrl)) {
      const a = document.createElement('a');
      a.className = 'ss-review-source';
      a.href = t.sourceUrl; a.target = '_blank'; a.rel = 'noopener noreferrer';
      a.textContent = 'Voir la source ↗';
      figure.appendChild(a);
    }
    return figure;
  }
  // Three independent columns, lengths balanced; copies are visual only.
  cols.forEach((col,index) => {
    const items = allowed.filter((_,i) => i % cols.length === index);
    if (!items.length) { col.hidden = true; return; }
    const track = document.createElement('div');
    track.className = 'ss-review-track';
    items.forEach(t => track.appendChild(makeCard(t)));
    col.appendChild(track);
    if (items.length > 1 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      const clone = track.cloneNode(true);
      clone.setAttribute('aria-hidden','true');
      clone.querySelectorAll('a').forEach(a => { a.tabIndex = -1; });
      col.appendChild(clone);
      col.classList.add('ss-reviews-animate');
    }
  });
  marquee.dataset.reviewsState = 'ready';
  marquee.setAttribute('aria-label', allowed.length + ' exemples fictifs de témoignages, pour tester le design');
})();