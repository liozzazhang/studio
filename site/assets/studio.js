'use strict';

// The website never receives GitHub credentials. Access is decided on GitHub.
const allowedLanguages = new Set(['zh', 'en']);
const languageToggle = document.querySelector('[data-language-toggle]');
let language = 'zh';
function setLanguage(value, persist = false) {
  language = allowedLanguages.has(value) ? value : 'zh';
  document.documentElement.lang = language === 'en' ? 'en' : 'zh-CN';
  for (const element of document.querySelectorAll('[data-zh][data-en]')) {
    element.textContent = element.getAttribute(`data-${language}`);
  }
  for (const element of document.querySelectorAll('[data-content-language]')) {
    element.hidden = element.dataset.contentLanguage !== language;
  }
  for (const element of document.querySelectorAll('[data-placeholder-zh][data-placeholder-en]')) {
    element.setAttribute('placeholder', element.getAttribute(`data-placeholder-${language}`));
  }
  for (const element of document.querySelectorAll('[data-label-zh][data-label-en]')) {
    element.setAttribute('aria-label', element.getAttribute(`data-label-${language}`));
  }
  const title = document.documentElement.getAttribute(`data-title-${language}`);
  if (title) document.title = title;
  if (languageToggle) {
    languageToggle.querySelector('[data-language-label]').textContent = language === 'zh' ? 'EN' : '中文';
    languageToggle.setAttribute('aria-label', language === 'zh' ? 'Switch to English' : '切换为中文');
  }
  if (persist) {
    try { localStorage.setItem('liozza-language', language); } catch { /* Reading does not require browser storage. */ }
  }
  window.dispatchEvent(new Event('studio-languagechange'));
}
if (languageToggle) languageToggle.addEventListener('click', () => setLanguage(language === 'zh' ? 'en' : 'zh', true));
let savedLanguage;
try { savedLanguage = localStorage.getItem('liozza-language'); } catch { savedLanguage = null; }
setLanguage(savedLanguage);
for (const element of document.querySelectorAll('[data-year]')) element.textContent = String(new Date().getFullYear());
for (const button of document.querySelectorAll('[data-print]')) button.addEventListener('click', () => window.print());

const accessDialog = document.querySelector('#access-dialog');
let lastAccessTrigger;
if (accessDialog) {
  for (const trigger of document.querySelectorAll('[data-private-repo]')) {
    trigger.addEventListener('click', (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || typeof accessDialog.showModal !== 'function') return;
      const slug = trigger.dataset.privateRepo;
      const repositoryUrl = trigger.dataset.repositoryUrl;
      const requestEmail = trigger.dataset.requestEmail;
      // Build-time validation is repeated before assigning link destinations.
      if (!/^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$/.test(slug) || repositoryUrl !== `https://github.com/liozzazhang/${slug}` || !requestEmail.startsWith('mailto:')) return;
      event.preventDefault();
      accessDialog.querySelector('[data-access-name]').textContent = slug;
      accessDialog.querySelector('[data-access-github]').href = repositoryUrl;
      accessDialog.querySelector('[data-access-email]').href = requestEmail;
      lastAccessTrigger = trigger;
      accessDialog.showModal();
    });
  }
  accessDialog.querySelector('[data-close-access]').addEventListener('click', () => accessDialog.close());
  accessDialog.addEventListener('click', (event) => {
    const rect = accessDialog.getBoundingClientRect();
    if (event.target === accessDialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) accessDialog.close();
  });
  accessDialog.addEventListener('close', () => { if (lastAccessTrigger) lastAccessTrigger.focus(); });
}
document.documentElement.classList.remove('no-js');

// Include expanded engineering notes in the printable profile, then restore the UI.
let printExpandedDetails = [];
window.addEventListener('beforeprint', () => {
  printExpandedDetails = [...document.querySelectorAll('details:not([open])')];
  for (const detail of printExpandedDetails) detail.open = true;
});
window.addEventListener('afterprint', () => {
  for (const detail of printExpandedDetails) detail.open = false;
  printExpandedDetails = [];
});
