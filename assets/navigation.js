(() => {
  const button = document.getElementById('navigation-toggle');
  const navigation = document.getElementById('site-navigation');
  const header = button.closest('header');
  // Keep this breakpoint synchronized with styles.css.
  const compact = window.matchMedia('(max-width: 52rem)');
  let open = false;

  const render = () => {
    button.hidden = !compact.matches;
    navigation.hidden = compact.matches && !open;
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  };
  const close = (returnFocus = false) => {
    open = false;
    render();
    if (returnFocus) button.focus();
  };
  button.addEventListener('click', () => {
    open = !open;
    render();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && compact.matches && open) {
      event.preventDefault();
      close(true);
    }
  });
  document.addEventListener('click', event => {
    if (compact.matches && open && !header.contains(event.target)) {
      close(navigation.contains(document.activeElement));
    }
  });
  navigation.addEventListener('click', event => {
    if (compact.matches && event.target.closest('a')) close(true);
  });
  compact.addEventListener('change', () => {
    const focusInNavigation = navigation.contains(document.activeElement);
    const focusOnButton = document.activeElement === button;
    close(compact.matches && focusInNavigation);
    if (!compact.matches && focusOnButton) navigation.querySelector('a').focus();
  });
  render();
})();
