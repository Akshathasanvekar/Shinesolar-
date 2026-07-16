// =====================
// SCROLL BEHAVIOR
// =====================
window.addEventListener('scroll', function () {
  const header = document.getElementById('mainHeader');
  if (header) {
    header.classList.toggle('scrolled', window.scrollY > 50);
  }
  const topBtn = document.getElementById('topBtn');
  if (topBtn) {
    topBtn.style.display = window.scrollY > 400 ? 'flex' : 'none';
  }
  const callFloat = document.getElementById('callFloat');
  if (callFloat) {
    callFloat.classList.toggle('show', window.scrollY > 400);
  }
});
 
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
 
// =====================
// HAMBURGER MENU
// =====================
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', function () {
    navLinks.classList.toggle('open');
    hamburger.classList.toggle('active');
  });
  document.addEventListener('click', function (e) {
    if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('open');
    }
  });
}
 
// =====================
// FAQ ACCORDION
// =====================
document.querySelectorAll('.faq-question').forEach(function (btn) {
  btn.addEventListener('click', function () {
    const answer = this.nextElementSibling;
    const isOpen = answer.style.display === 'block';
    document.querySelectorAll('.faq-answer').forEach(a => a.style.display = 'none');
    answer.style.display = isOpen ? 'none' : 'block';
  });
});
 
// =====================
// SOLAR CALCULATOR
// =====================
function calculateSolar() {
  const units = parseFloat(document.getElementById('units')?.value || 0);
  const rate = parseFloat(document.getElementById('rate')?.value || 7);
  const type = document.getElementById('sysType')?.value || 'grid';
 
  if (!units || units <= 0) {
    alert('Please enter your monthly electricity consumption.');
    return;
  }
 
  const systemSize = (units / 120).toFixed(2);
  const cost = type === 'offgrid' ? systemSize * 85000 : (type === 'hybrid' ? systemSize * 75000 : systemSize * 55000);
  const subsidy = type === 'grid' ? Math.min(cost * 0.30, 78000) : 0;
  const netCost = cost - subsidy;
  const savings = units * rate * 12;
  const payback = (netCost / savings).toFixed(1);
 
  document.getElementById('res-size').textContent = systemSize + ' kW';
  document.getElementById('res-cost').textContent = '₹' + Math.round(cost / 1000) + 'K';
  document.getElementById('res-subsidy').textContent = '₹' + Math.round(subsidy / 1000) + 'K';
  document.getElementById('res-netcost').textContent = '₹' + Math.round(netCost / 1000) + 'K';
  document.getElementById('res-saving').textContent = '₹' + Math.round(savings / 1000) + 'K/yr';
  document.getElementById('res-payback').textContent = payback + ' yrs';
 
  const result = document.getElementById('calcResult');
  if (result) {
    result.classList.add('show');
    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}
 
// =====================
// HERO STAT COUNTERS
// =====================
(function () {
  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const duration = 1800;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(function () {
      current += step;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = Math.floor(current);
    }, 16);
  }
  const counters = document.querySelectorAll('.stat-num[data-target]');
  if (!counters.length) return;
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animateCounter(e.target); obs.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { obs.observe(c); });
  } else {
    counters.forEach(animateCounter);
  }
})();
// =====================
// SCROLL REVEAL
// =====================
(function () {
  const items = document.querySelectorAll('.reveal');
  if (!items.length) return;
  if (!('IntersectionObserver' in window)) {
    items.forEach(el => el.classList.add('in-view'));
    return;
  }
  const obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  items.forEach(el => obs.observe(el));
})();

// =====================
// HERO BANNER — AUTO-SWAPPING SLIDER
// =====================
(function () {
  const heroSection = document.getElementById('heroSlider');
  if (!heroSection) return;

  const slides = heroSection.querySelectorAll('.hero-slide');
  const dots = heroSection.querySelectorAll('.hero-dot');
  if (slides.length <= 1) return; // nothing to rotate

  const AUTOPLAY_MS = 6000;
  let current = Math.max(0, [...slides].findIndex(s => s.classList.contains('active')));
  if (current === -1) current = 0;
  let timer = null;

  function goTo(index) {
    slides[current].classList.remove('active');
    dots[current] && dots[current].classList.remove('active');
    current = (index + slides.length) % slides.length;
    slides[current].classList.add('active');
    dots[current] && dots[current].classList.add('active');
  }

  function next() { goTo(current + 1); }

  function start() {
    stop();
    timer = setInterval(next, AUTOPLAY_MS);
  }
  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
  }

  dots.forEach(function (dot, i) {
    dot.addEventListener('click', function () {
      goTo(i);
      start(); // reset the autoplay timer after manual navigation
    });
  });

  // Pause on hover/focus so visitors can read the copy, resume on leave
  heroSection.addEventListener('mouseenter', stop);
  heroSection.addEventListener('mouseleave', start);

  // Pause when the tab isn't visible to save resources
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop(); else start();
  });

  start();
})();
