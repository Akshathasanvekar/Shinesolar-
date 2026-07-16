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
