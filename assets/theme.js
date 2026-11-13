(() => {
  const query = window.matchMedia('(prefers-color-scheme: dark)');
  let choice;
  try { choice = localStorage.getItem('theme'); } catch (_) { /* Storage is optional. */ }
  if (choice !== 'light' && choice !== 'dark') choice = null;
  const root = document.documentElement;
  const apply = () => {
    const dark = choice ? choice === 'dark' : query.matches;
    root.dataset.theme = dark ? 'dark' : 'light';
    const button = document.getElementById('theme-toggle');
    if (button) {
      button.hidden = false;
      button.textContent = dark ? 'Light mode' : 'Dark mode';
      button.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} mode`);
    }
  };
  apply();
  query.addEventListener('change', apply);
  document.addEventListener('DOMContentLoaded', () => {
    apply();
    document.getElementById('theme-toggle').addEventListener('click', () => {
      choice = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('theme', choice); } catch (_) { /* Keep session choice. */ }
      apply();
    });
  });
})();
