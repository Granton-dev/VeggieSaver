// Auto-dismiss toasts
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.toast').forEach(el => {
    setTimeout(() => el.classList.remove('show'), 4000);
  });
});