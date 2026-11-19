'use strict';

const catalogCards = [...document.querySelectorAll('.catalog-card')];
const catalogButtons = [...document.querySelectorAll('[data-category-button]')];
const catalogSearch = document.querySelector('#catalog-search');
const catalogClear = document.querySelector('#clear-search');
const catalogCount = document.querySelector('#catalog-result-count');
const catalogEmpty = document.querySelector('#catalog-empty');
let catalogCategory = 'all';

function applyCatalogFilters() {
  const query = catalogSearch.value.normalize('NFKC').trim().toLocaleLowerCase('en');
  let visible = 0;
  for (const card of catalogCards) {
    const inCategory = catalogCategory === 'all' || card.dataset.category === catalogCategory;
    const matchesSearch = !query || card.dataset.search.normalize('NFKC').toLocaleLowerCase('en').includes(query);
    card.hidden = !inCategory || !matchesSearch;
    if (!card.hidden) visible += 1;
  }
  const english = document.documentElement.lang === 'en';
  catalogCount.textContent = english ? `Showing ${visible} of ${catalogCards.length} projects` : `显示 ${visible} / ${catalogCards.length} 个项目`;
  catalogClear.hidden = !catalogSearch.value;
  catalogEmpty.hidden = visible !== 0;
}

for (const button of catalogButtons) {
  button.addEventListener('click', () => {
    catalogCategory = button.dataset.categoryButton;
    for (const item of catalogButtons) {
      const active = item === button;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-pressed', String(active));
    }
    applyCatalogFilters();
  });
}
catalogSearch.addEventListener('input', applyCatalogFilters);
catalogSearch.addEventListener('search', applyCatalogFilters);
catalogClear.addEventListener('click', () => {
  catalogSearch.value = '';
  applyCatalogFilters();
  catalogSearch.focus();
});
window.addEventListener('studio-languagechange', applyCatalogFilters);
applyCatalogFilters();
