// Mobile nav toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const isOpen = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach((a) =>
      a.addEventListener('click', () => links.classList.remove('open'))
    );
  }

  // Newsletter signup -> mailto fallback (no backend wired up yet)
  const signupForm = document.querySelector('.signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = signupForm.querySelector('input[type="email"]').value.trim();
      if (!email) return;
      window.location.href =
        'mailto:hello@thegreenhousesheshed.com' +
        '?subject=' + encodeURIComponent('Join the Grove newsletter') +
        '&body=' + encodeURIComponent('Please add me to the newsletter list: ' + email);
    });
  }

  // Contact form -> mailto fallback (no backend wired up yet)
  const contactForm = document.querySelector('.contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = contactForm.querySelector('#name')?.value.trim() || '';
      const email = contactForm.querySelector('#email')?.value.trim() || '';
      const message = contactForm.querySelector('#message')?.value.trim() || '';
      window.location.href =
        'mailto:hello@thegreenhousesheshed.com' +
        '?subject=' + encodeURIComponent('Message from ' + (name || 'the website')) +
        '&body=' + encodeURIComponent(message + '\n\n— ' + name + ' (' + email + ')');
    });
  }
});
