/* Ski Society — independent first-party testimonials, no Trustpilot content scraping.
   Only add exact customer quotes for which display permission has been obtained.
   This is NOT an official Trustpilot widget, nor a live Trustpilot integration.
   Example record format:
   { quote: "Customer's exact approved quote", name: "First name or initials",
     context: "Cours privé · hiver 2025", date: "2025-02-01", sourceUrl: "https://...",
     consent: true }
   Keep sourceUrl only for directly attributable and permitted sources.
*/
(function () {
  'use strict';
  const testimonials = []; // Add real, approved firsthand testimonies here.
  const marquee = document.getElementById('ss-reviews-marquee');
  if (!marquee) return;
  const allowed = testimonials.filter(t =>
    t && t.consent === true && typeof t.quote === 'string' && t.quote.trim() &&
    typeof t.name === 'string' && t.name.trim());
  if (!allowed.length) return;
  const cols = Array.from(marquee.querySelectorAll('[data-reviews-col]'));
  const frag = document.createDocumentFragment();
  function makeCard(t) {
    const figure = document.createElement('figure');
    figure.className = 'ss-review-card';
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
  marquee.setAttribute('aria-label', allowed.length + ' témoignages clients');
})();