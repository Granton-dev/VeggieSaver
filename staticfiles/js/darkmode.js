// Dark mode toggle
const DARK_KEY = 'veggieguard_theme';

function initDarkMode() {
  const saved = localStorage.getItem(DARK_KEY) || 'light';
  applyTheme(saved);
}

function toggleDarkMode() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  localStorage.setItem(DARK_KEY, next);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const btn = document.getElementById('darkToggle');
  if (btn) {
    btn.innerHTML = theme === 'dark'
      ? '<i class="bi bi-sun-fill"></i>'
      : '<i class="bi bi-moon-fill"></i>';
    btn.title = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
  }
}

document.addEventListener('DOMContentLoaded', initDarkMode);
