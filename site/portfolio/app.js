'use strict';

// Public copy only. Rendering uses textContent; no credentials or remote requests.
const allowedLanguages = new Set(['zh', 'en']);
const copy = new Map([
  ['zh', {
    title: 'Lei Zhang / Liozza — 云平台与 AI 工作流',
    description: 'Lei Zhang（Liozza）的个人空间。云平台技术负责人，分享 AI 工作流、平台工程、安全交付与个人探索。',
    count: (number) => `显示 ${number} 个工程案例。`,
  }],
  ['en', {
    title: 'Lei Zhang / Liozza — Cloud Engineering & AI Workflows',
    description: 'A personal space by Lei Zhang, also known as Liozza. Cloud engineering, practical AI workflows, secure delivery, publicly shared tools, and creative exploration.',
    count: (number) => `Showing ${number} engineering ${number === 1 ? 'case' : 'cases'}.`,
  }],
]);

const projects = careerProjects;

const languageButton = document.querySelector('#language-toggle');
const languageLabel = document.querySelector('#language-label');
const filterButtons = [...document.querySelectorAll('[data-filter]')];
const cards = [...document.querySelectorAll('[data-project]')];
const status = document.querySelector('#filter-status');
const dialog = document.querySelector('#project-dialog');
let language = 'zh';
let currentProject = null;

function rememberLanguage(value) {
  try {
    localStorage.setItem('liozza-language', value);
  } catch {
    // The language switch also works when browser storage is unavailable.
  }
}

function updateCount() {
  status.textContent = copy.get(language).count(cards.filter((card) => !card.hidden).length);
}

function appendList(list, values) {
  const fragment = document.createDocumentFragment();
  for (const value of values) {
    const item = document.createElement('li');
    item.textContent = value;
    fragment.append(item);
  }
  list.replaceChildren(fragment);
}

function populateDialog(projectId) {
  if (!projects.has(projectId)) return;
  const project = projects.get(projectId);
  const text = project[language];
  document.querySelector('#dialog-kicker').textContent = project.category;
  document.querySelector('#dialog-title').textContent = typeof project.name === 'string' ? project.name : project.name[language];
  document.querySelector('#dialog-summary').textContent = text.summary;
  document.querySelector('#dialog-context').textContent = text.context;
  appendList(document.querySelector('#dialog-points'), text.points);
  appendList(document.querySelector('#dialog-tags'), project.tags);
  const roleBlock = document.querySelector('#dialog-role-block');
  const outcomeBlock = document.querySelector('#dialog-outcome-block');
  roleBlock.hidden = !text.role;
  outcomeBlock.hidden = !text.outcome;
  document.querySelector('#dialog-role').textContent = text.role || '';
  document.querySelector('#dialog-outcome').textContent = text.outcome || '';

}

function applyLanguage(value, persist = false) {
  language = allowedLanguages.has(value) ? value : 'zh';
  document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
  document.title = copy.get(language).title;
  document.querySelector('meta[name="description"]').content = copy.get(language).description;
  for (const element of document.querySelectorAll('[data-zh][data-en]')) {
    element.textContent = element.getAttribute(`data-${language}`);
  }
  for (const element of document.querySelectorAll('[data-label-zh][data-label-en]')) {
    element.setAttribute('aria-label', element.getAttribute(`data-label-${language}`));
  }
  languageLabel.textContent = language === 'zh' ? 'EN' : '中文';
  languageButton.setAttribute('aria-label', language === 'zh' ? 'Switch to English' : '切换为中文');
  languageButton.setAttribute('aria-pressed', String(language === 'en'));
  updateCount();
  if (currentProject) populateDialog(currentProject);
  if (persist) rememberLanguage(language);
}

languageButton.addEventListener('click', () => applyLanguage(language === 'zh' ? 'en' : 'zh', true));
for (const button of filterButtons) {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    for (const candidate of filterButtons) {
      const isActive = candidate === button;
      candidate.classList.toggle('is-active', isActive);
      candidate.setAttribute('aria-pressed', String(isActive));
    }
    for (const card of cards) card.hidden = filter !== 'all' && card.dataset.category !== filter;
    updateCount();
  });
}

for (const button of document.querySelectorAll('[data-detail]')) {
  button.addEventListener('click', () => {
    const projectId = button.dataset.detail;
    if (!projects.has(projectId)) return;
    currentProject = projectId;
    populateDialog(projectId);
    dialog.showModal();
    document.body.classList.add('dialog-open');
  });
}

document.querySelector('#dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (event) => {
  // Only clicks outside the dialog rectangle dismiss the modal.
  if (event.target !== dialog) return;
  const bounds = dialog.getBoundingClientRect();
  const outside = event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom;
  if (outside) dialog.close();
});
dialog.addEventListener('close', () => {
  document.body.classList.remove('dialog-open');
  currentProject = null;
});

let savedLanguage;
try {
  savedLanguage = localStorage.getItem('liozza-language');
} catch {
  savedLanguage = null;
}
applyLanguage(savedLanguage);
document.querySelector('#year').textContent = String(new Date().getFullYear());
document.documentElement.classList.remove('no-js');
