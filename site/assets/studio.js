'use strict';

// Static UI only; all copy is local, and stored language values are allowlisted.
const studioLanguages = new Set(['zh', 'en']);
const studioToggle = document.querySelector('[data-language-toggle]');
let studioLanguage = 'zh';
function setStudioLanguage(value, persist = false) {
  studioLanguage = studioLanguages.has(value) ? value : 'zh';
  document.documentElement.lang = studioLanguage === 'zh' ? 'zh-CN' : 'en';
  for (const element of document.querySelectorAll('[data-zh][data-en]')) {
    element.textContent = element.getAttribute(`data-${studioLanguage}`);
  }
  const title = document.documentElement.getAttribute(`data-title-${studioLanguage}`);
  if (title) document.title = title;
  if (studioToggle) {
    studioToggle.setAttribute('aria-label', studioLanguage === 'zh' ? 'Switch to English' : '切换为中文');
    studioToggle.querySelector('[data-language-label]').textContent = studioLanguage === 'zh' ? 'EN' : '中文';
  }
  for (const element of document.querySelectorAll('[data-placeholder-zh][data-placeholder-en]')) {
    element.setAttribute('placeholder',element.getAttribute(`data-placeholder-${studioLanguage}`));
  }
  for (const element of document.querySelectorAll('[data-label-zh][data-label-en]')) {
    element.setAttribute('aria-label',element.getAttribute(`data-label-${studioLanguage}`));
  }
  window.dispatchEvent(new Event('studio-languagechange'));
  if (persist) {
    try { localStorage.setItem('liozza-language', studioLanguage); } catch { /* Navigation works without browser storage. */ }
  }
}
if (studioToggle) studioToggle.addEventListener('click', () => setStudioLanguage(studioLanguage === 'zh' ? 'en' : 'zh', true));
let studioSavedLanguage;
try { studioSavedLanguage = localStorage.getItem('liozza-language'); } catch { studioSavedLanguage = null; }
setStudioLanguage(studioSavedLanguage);
for (const element of document.querySelectorAll('[data-year]')) element.textContent = String(new Date().getFullYear());

document.documentElement.classList.remove('no-js');
