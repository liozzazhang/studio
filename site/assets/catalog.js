'use strict';

const cards = [...document.querySelectorAll('.catalog-card')];
const categoryButtons = [...document.querySelectorAll('[data-category-button]')];
const searchInput = document.querySelector('#catalog-search');
const clearButton = document.querySelector('#clear-search');
const countLabel = document.querySelector('#catalog-result-count');
const emptyState = document.querySelector('#catalog-empty');
const visibilitySelect = document.querySelector('#visibility-filter');
let activeCategory = 'all';
function applyFilters() {
  const query = searchInput.value.normalize('NFKC').trim().toLocaleLowerCase('en');
  let visible = 0;
  for (const card of cards) {
    const categoryMatch = activeCategory === 'all' || card.dataset.category === activeCategory;
    const visibilityMatch = visibilitySelect.value === 'all' || card.dataset.visibility === visibilitySelect.value;
    const searchMatch = !query || card.dataset.search.normalize('NFKC').toLocaleLowerCase('en').includes(query);
    card.hidden = !(categoryMatch && visibilityMatch && searchMatch);
    if (!card.hidden) visible += 1;
  }
  const template = countLabel.getAttribute(document.documentElement.lang === 'en' ? 'data-filtered-en' : 'data-filtered-zh');
  countLabel.textContent = template.replace('{visible}', String(visible)).replace('{total}', String(cards.length));
  clearButton.hidden = !searchInput.value;
  emptyState.hidden = visible !== 0;
}
for (const button of categoryButtons) {
  button.addEventListener('click', () => {
    activeCategory = button.dataset.categoryButton;
    for (const item of categoryButtons) {
      const active = item === button;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-pressed', String(active));
    }
    applyFilters();
  });
}
searchInput.addEventListener('input', applyFilters);
searchInput.addEventListener('search', applyFilters);
visibilitySelect.addEventListener('change', applyFilters);
clearButton.addEventListener('click', () => { searchInput.value = ''; applyFilters(); searchInput.focus(); });
document.querySelector('[data-reset-filters]').addEventListener('click', () => {
  searchInput.value = '';
  visibilitySelect.value = 'all';
  categoryButtons.find(button => button.dataset.categoryButton === 'all').click();
  searchInput.focus();
});
window.addEventListener('studio-languagechange', applyFilters);
applyFilters();
