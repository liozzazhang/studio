#!/usr/bin/env python3
"""Generate Studio from independently discoverable, reviewed content modules."""
import argparse
import hashlib
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
SITE = ROOT / 'site'
SLUG = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}')
DOWNLOAD_FILE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}\.(pdf|docx)')
DOWNLOAD_SIGNATURES = {'pdf': b'%PDF-', 'docx': b'PK\x03\x04'}
MAX_DOWNLOAD_BYTES = 5 * 1024 * 1024
HOME_SECTIONS = ('highlights', 'focus', 'experience', 'evolution', 'selected', 'resume', 'beyond', 'contact')
STALE_OUTPUT = re.compile(r'projects/[A-Za-z0-9_.-]+/(?:access/)?index\.html|downloads/[A-Za-z0-9][A-Za-z0-9_.-]*\.(?:pdf|docx)')

# Shared copy for the current build; filled by build() before any page is rendered.
UI = {}
PROFILE = {}
DOWNLOADS = []
LANGUAGE = {'default': 'zh'}


def read_json(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'Expected regular content file: {path.name}')
    return json.loads(path.read_text(encoding='utf-8'))


def esc(value):
    return escape(str(value), quote=True)


def bi(value, en=None, tag='span', attrs=''):
    if en is not None:
        value = {'zh': value, 'en': en}
    if not isinstance(value, dict) or not all(isinstance(value.get(lang), str) for lang in ('zh', 'en')):
        raise ValueError('Bilingual copy needs zh and en text')
    return f'<{tag} data-zh="{esc(value["zh"])}" data-en="{esc(value["en"])}"{(" " + attrs) if attrs else ""}>{esc(value[LANGUAGE["default"]])}</{tag}>'


def txt(value, tag='span', attrs=''):
    """Render language-neutral text or bilingual copy."""
    if isinstance(value, str):
        return f'<{tag}{(" " + attrs) if attrs else ""}>{esc(value)}</{tag}>'
    return bi(value, tag=tag, attrs=attrs)


def asset(name):
    digest = hashlib.sha256((SITE / 'assets' / name).read_bytes()).hexdigest()[:10]
    return f'/studio/assets/{name}?v={digest}'


def pick(value):
    return value[LANGUAGE['default']] if isinstance(value, dict) else value


def fill(value, **values):
    def apply(text):
        for key, replacement in values.items():
            text = text.replace('{' + key + '}', str(replacement))
        return text
    if isinstance(value, dict):
        return {lang: apply(value[lang]) for lang in ('zh', 'en')}
    return apply(value)


def url(value):
    parsed = urlsplit(value)
    if parsed.scheme == 'https' and parsed.netloc and not parsed.username and not parsed.password:
        return value
    raise ValueError('External links must use HTTPS without credentials')


def load_content():
    config = read_json(CONTENT / 'site.json')
    if config['owner'] != 'liozzazhang' or config['base_path'] != '/studio/' or config['origin'] != 'https://liozzazhang.github.io':
        raise ValueError('Unexpected publication destination')
    if config.get('default_language', 'zh') not in ('zh', 'en'):
        raise ValueError('default_language must be zh or en')
    profile = read_json(CONTENT / 'profile.json')
    categories = read_json(CONTENT / 'categories.json')
    category_ids = set()
    for item in categories:
        if not re.fullmatch(r'[a-z][a-z0-9-]*', item['id']) or item['id'] in category_ids:
            raise ValueError('Invalid or duplicate category')
        category_ids.add(item['id'])
    projects, seen = [], set()
    for directory in sorted((CONTENT / 'projects').iterdir()):
        if directory.is_symlink():
            raise ValueError('Symlink project directories are not supported')
        if not directory.is_dir() or not (directory / 'project.json').exists():
            continue
        item = read_json(directory / 'project.json')
        slug = item['slug']
        if not SLUG.fullmatch(slug) or '..' in slug or slug != directory.name or slug.casefold() in seen:
            raise ValueError('Invalid, duplicate, or mismatched project directory')
        seen.add(slug.casefold())
        if item['category'] not in category_ids or item.get('group') not in ('engineering', 'wow'):
            raise ValueError(f'Unknown project category/group: {slug}')
        if item['url'] != f'https://github.com/{config["owner"]}/{slug}':
            raise ValueError('Project repository must belong to the configured owner')
        if item.get('visibility') not in ('public', 'private'):
            raise ValueError('Repository visibility must be explicit')
        if item['visibility'] == 'private' and item.get('disclosure') != 'summary-only':
            raise ValueError('Private projects require explicit summary-only disclosure')
        for field in ('title', 'summary'):
            bi(item[field])
        if not isinstance(item.get('tags'), list) or not all(isinstance(tag, str) for tag in item['tags']):
            raise ValueError('Project tags must be text')
        for flag in ('fork', 'archived', 'legacy'):
            if flag in item and not isinstance(item[flag], bool):
                raise ValueError('Project flags must be boolean')
        for field in ('order', 'featured'):
            if field in item and (type(item[field]) is not int or item[field] < 0):
                raise ValueError('Project order must be a nonnegative integer')
        item['_directory'] = directory
        projects.append(item)
    projects.sort(key=lambda item: (item.get('order', 1000), item['slug'].casefold()))
    if not projects:
        raise ValueError('No project modules found')
    return config, profile, categories, projects


def load_ui():
    ui = read_json(CONTENT / 'ui.json')
    if not isinstance(ui.get('home_sections'), list) or not set(ui['home_sections']) <= set(HOME_SECTIONS) or len(set(ui['home_sections'])) != len(ui['home_sections']):
        raise ValueError('ui.json home_sections must list known sections once')
    return ui


def load_downloads():
    """Read the reviewed resume manifest; files not listed there are never published."""
    manifest = CONTENT / 'downloads' / 'downloads.json'
    if not manifest.exists():
        return []
    groups, ids, names = [], set(), set()
    for group in read_json(manifest):
        if not re.fullmatch(r'[a-z][a-z0-9-]*', str(group.get('id', ''))) or group['id'] in ids:
            raise ValueError('Invalid or duplicate download group')
        ids.add(group['id'])
        bi(group['title'])
        bi(group['description'])
        if 'order' in group and (type(group['order']) is not int or group['order'] < 0):
            raise ValueError('Download order must be a nonnegative integer')
        files = []
        for entry in group.get('files', []):
            name = str(entry.get('file', ''))
            match = DOWNLOAD_FILE.fullmatch(name)
            if not match or '..' in name or entry.get('format') != match.group(1) or entry.get('lang') not in ('zh', 'en') or name.casefold() in names:
                raise ValueError(f'Invalid download entry: {name}')
            names.add(name.casefold())
            path = CONTENT / 'downloads' / 'files' / name
            if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_DOWNLOAD_BYTES:
                raise ValueError(f'Download must be a regular file within the size limit: {name}')
            data = path.read_bytes()
            if not data.startswith(DOWNLOAD_SIGNATURES[entry['format']]):
                raise ValueError(f'Download content does not match its format: {name}')
            files.append({**entry, 'data': data})
        if not files:
            raise ValueError('Download groups need at least one file')
        groups.append({**group, 'files': files})
    groups.sort(key=lambda group: (group.get('order', 1000), group['id']))
    return groups


def inline_markdown(text):
    """Render a small Markdown subset; raw HTML and external images stay inert."""
    pattern = re.compile(r'`([^`]+)`|\*\*([^*]+)\*\*|(?<!!)\[([^\]]+)\]\(([^\s)]+)\)')
    output, last = [], 0
    for match in pattern.finditer(text):
        output.append(esc(text[last:match.start()]))
        if match.group(1):
            output.append('<code>' + esc(match.group(1)) + '</code>')
        elif match.group(2):
            output.append('<strong>' + esc(match.group(2)) + '</strong>')
        else:
            try:
                target = url(match.group(4))
                output.append(f'<a href="{esc(target)}" target="_blank" rel="noopener noreferrer">{esc(match.group(3))}</a>')
            except ValueError:
                output.append(esc(match.group(0)))
        last = match.end()
    output.append(esc(text[last:]))
    return ''.join(output)


def markdown(path):
    if not path.exists():
        return ''
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 100000:
        raise ValueError('Invalid project Markdown file')
    output, paragraph, listing = [], [], []
    def flush():
        if paragraph:
            output.append('<p>' + inline_markdown(' '.join(paragraph)) + '</p>')
            paragraph.clear()
        if listing:
            output.append('<ul>' + ''.join('<li>' + inline_markdown(line) + '</li>' for line in listing) + '</ul>')
            listing.clear()
    for line in path.read_text(encoding='utf-8').splitlines():
        heading = re.match(r'^(#{1,4})\s+(.+)$', line)
        if heading:
            flush()
            level = min(len(heading.group(1)) + 1, 4)
            output.append(f'<h{level}>' + inline_markdown(heading.group(2)) + f'</h{level}>')
        elif line.startswith('- '):
            if paragraph:
                flush()
            listing.append(line[2:])
        elif not line.strip():
            flush()
        else:
            if listing:
                flush()
            paragraph.append(line.strip())
    flush()
    return '\n'.join(output)


def header(active='home'):
    copy = UI['header']
    links = ''.join(f'<a href="{esc(link["href"])}"' + (' aria-current="page"' if link['key'] == active else '') + '>' + bi(link['label']) + '</a>' for link in UI['nav'])
    resume = '<a class="resume-nav" href="/studio/#resume">' + bi(copy['resume']) + '</a>' if DOWNLOADS else ''
    return '<header class="site-header shell"><a class="brand" href="/studio/">' + esc(PROFILE['name']) + '<span> / ' + esc(PROFILE['alias']) + '</span></a><nav class="main-nav" aria-label="' + esc(copy['nav_label']) + '">' + links + '</nav><div class="header-actions"><button type="button" class="language-toggle" data-language-toggle aria-label="' + ('切换为中文' if LANGUAGE['default'] == 'en' else 'Switch to English') + '"><span data-language-label>' + ('中文' if LANGUAGE['default'] == 'en' else 'EN') + '</span></button>' + resume + '<a class="contact-nav" href="/studio/#contact">' + bi(copy['contact']) + '</a></div></header>'


def footer():
    copy = UI['footer']
    return '<footer class="site-footer shell"><span>© <span data-year>2026</span> ' + esc(PROFILE['name']) + ' / ' + esc(PROFILE['alias']) + '</span><a href="/studio/projects/">' + bi(copy['projects']) + '</a><a href="#main">' + bi(copy['top']) + '</a></footer>'


def email_link(slug=None):
    address = PROFILE['contacts'].get('email')
    if not address or not re.fullmatch(r'[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+', address):
        raise ValueError('A valid contact email is required for access requests')
    if not slug:
        return 'mailto:' + address
    copy = UI['access']
    query = urlencode({'subject': fill(copy['email_subject'], slug=slug), 'body': fill(copy['email_body'], slug=slug)}, quote_via=quote)
    return 'mailto:' + address + '?' + query


def access_dialog():
    copy = UI['access']
    return '<dialog id="access-dialog" aria-labelledby="access-title" aria-describedby="access-description"><div class="dialog-top"><span class="eyebrow">' + esc(copy['eyebrow']) + '</span><button type="button" data-close-access aria-label="' + esc(copy['close']) + '">×</button></div><h2 id="access-title">' + bi(copy['title']) + '</h2><p class="access-repository" data-access-name></p><p id="access-description">' + bi(copy['description']) + '</p><ol>' + ''.join('<li>' + bi(step) + '</li>' for step in copy['steps']) + '</ol><div class="dialog-actions"><a class="button button-dark" data-access-email href="' + esc(email_link()) + '">' + bi(copy['email_button']) + '</a><a class="text-link" data-access-github href="https://github.com/liozzazhang" target="_blank" rel="noopener noreferrer">' + bi(copy['github_button']) + '</a></div></dialog>'


def layout(title, description, body, route='', active='home', scripts=''):
    template = (ROOT / '_templates/pages/layout.html').read_text(encoding='utf-8')
    language = LANGUAGE['default']
    values = {'FAVICON': asset('favicon.svg'), 'STYLESHEET': asset('studio.css'), 'SCRIPT': asset('studio.js'), 'LANG': language, 'HTML_LANG': 'en' if language == 'en' else 'zh-CN', 'TITLE': esc(title[language]), 'TITLE_ZH': esc(title['zh']), 'TITLE_EN': esc(title['en']), 'DESCRIPTION': esc(pick(description)), 'URL': 'https://liozzazhang.github.io/studio/' + route, 'HEADER': header(active), 'BODY': body, 'FOOTER': footer(), 'SCRIPTS': scripts, 'DIALOG': access_dialog(), 'SKIP_LINK': bi(UI['skip_link'], tag='a', attrs='class="skip-link" href="#main"'), 'NOSCRIPT': esc(UI['noscript'])}
    for key, value in values.items():
        template = template.replace('{{' + key + '}}', value)
    if re.search(r'\{\{[A-Z_]+\}\}', template):
        raise ValueError('Unresolved layout variable')
    return '\n'.join(line.rstrip() for line in template.splitlines()) + '\n'


def source_link(item):
    copy = UI['project']
    if item['visibility'] == 'private':
        return f'<a class="project-source private-source" href="/studio/projects/{esc(item["slug"])}/access/" data-private-repo="{esc(item["slug"])}" data-request-email="{esc(email_link(item["slug"]))}" data-repository-url="{esc(item["url"])}">' + bi(copy['request_access']) + '</a>'
    return f'<a class="project-source" href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">' + bi(copy['view_source']) + '</a>'


def badge(item):
    labels = UI['project']['badges']
    badges = [bi(labels['private'] if item['visibility'] == 'private' else labels['public'])]
    for flag in ('fork', 'archived'):
        if item.get(flag):
            badges.append(bi(labels[flag]))
    if item.get('status'):
        badges.append(bi(item['status']))
    elif item.get('kind') == 'collection':
        badges.append(bi(labels['collection']))
    elif item.get('legacy'):
        badges.append(bi(labels['legacy']))
    return '<div class="project-badges">' + ''.join(badges) + '</div>'


def project_card(item, categories):
    category = next(category for category in categories if category['id'] == item['category'])
    search = ' '.join([item['slug'], *item['title'].values(), *item['summary'].values(), *item['tags']]).casefold()
    return f'<article class="catalog-card" data-category="{esc(item["category"])}" data-visibility="{item["visibility"]}" data-search="{esc(search)}"><div class="project-top">' + bi(category) + badge(item) + '</div><h3><a href="/studio/projects/' + esc(item['slug']) + '/">' + bi(item['title']) + '</a></h3>' + bi(item['summary'], tag='p', attrs='class="project-summary"') + '<ul class="project-tags">' + ''.join('<li>' + esc(tag) + '</li>' for tag in item['tags'][:4]) + '</ul><div class="project-bottom"><a class="text-link" href="/studio/projects/' + esc(item['slug']) + '/">' + bi(UI['project']['overview']) + '</a>' + source_link(item) + '</div></article>'


def section_title(number, copy):
    return f'<div class="section-title"><span class="section-number">{number}</span><h2>' + bi(copy['title']) + '</h2>' + (bi(copy['note'], tag='p') if copy.get('note') else '') + '</div>'


def contacts(large=False):
    contact, labels = PROFILE['contacts'], UI['contacts']
    links = '<a href="' + esc(email_link()) + '"><span>' + esc(labels['email']) + '</span><strong>' + esc(contact['email']) + '</strong><i>↗</i></a>'
    for field in ('linkedin', 'github'):
        if contact.get(field):
            value = url(contact[field])
            links += '<a href="' + esc(value) + '" target="_blank" rel="noopener noreferrer"><span>' + esc(labels[field]) + '</span><strong>' + esc(contact[field + '_label']) + '</strong><i>↗</i></a>'
    if contact.get('wechat'):
        links += '<div class="contact-value"><span>' + esc(labels['wechat']) + '</span><strong>' + esc(contact['wechat']) + '</strong></div>'
    else:
        links += '<a href="' + esc(email_link()) + '"><span>' + esc(labels['wechat']) + '</span><strong>' + bi(labels['wechat_fallback']) + '</strong><i>↗</i></a>'
    return '<div class="contact-list' + (' is-large' if large else '') + '">' + links + '</div>'


def related_links(slugs, known):
    return ''.join('<a href="/studio/projects/' + esc(slug) + '/">' + esc(slug) + ' ↗</a>' for slug in slugs if slug in known)


def size_label(data):
    size = len(data)
    return f'{size / 1024 / 1024:.1f} MB' if size >= 1024 * 1024 else f'{max(1, round(size / 1024))} KB'


def hero():
    copy = UI['hero']
    intro = ''.join(bi(value, tag='p') for value in PROFILE['intro'])
    resume = '<a class="text-link" href="#resume">' + bi(copy['resume_button']) + '</a>' if DOWNLOADS else ''
    facts = ''.join('<div><dt>' + bi(fact['label']) + '</dt><dd>' + txt(fact['value']) + '</dd></div>' for fact in PROFILE['glance'])
    return '<section class="profile-hero shell" id="about"><div class="hero-main"><p class="eyebrow">' + esc(copy['eyebrow']) + '</p><h1>' + esc(PROFILE['name']) + '<span>' + esc(PROFILE['alias']) + '</span></h1>' + bi(PROFILE['role'], tag='p', attrs='class="hero-role"') + '<div class="hero-intro">' + intro + '</div><div class="hero-actions"><a class="button button-dark" href="#experience">' + bi(copy['experience_button']) + '</a>' + resume + '<a class="text-link" href="projects/">' + bi(copy['projects_link']) + '</a><button type="button" class="print-link" data-print>' + bi(copy['print_button']) + '</button></div></div><aside class="profile-aside"><p class="eyebrow">' + esc(copy['glance_eyebrow']) + '</p><dl class="profile-facts">' + facts + '</dl>' + contacts() + '</aside></section>'


def home_highlights(number, context):
    items = PROFILE.get('highlights', [])
    if not items:
        return ''
    return '<section class="highlight-band shell" id="highlights" aria-label="' + esc(UI['sections']['highlights']['label']) + '"><dl>' + ''.join('<div><dt>' + txt(item['value']) + '</dt><dd>' + bi(item['label']) + '</dd></div>' for item in items) + '</dl></section>'


def home_focus(number, context):
    skills = ''
    if PROFILE.get('skills'):
        skills = '<div class="skill-list">' + ''.join('<div><h4>' + bi(group['title']) + '</h4><p>' + esc(' / '.join(group['items'])) + '</p></div>' for group in PROFILE['skills']) + '</div>'
    return '<section class="editorial-section shell" id="focus">' + section_title(number, UI['sections']['focus']) + '<div class="strength-list">' + ''.join('<article><h3>' + bi(item['title']) + '</h3>' + bi(item['summary'], tag='p') + '</article>' for item in PROFILE.get('strengths', [])) + skills + '</div></section>'


def experience_details(entry, known):
    """Metrics, points and related work shared by roles and their projects."""
    metrics = '<ul class="experience-metrics">' + ''.join(bi(metric, tag='li') for metric in entry['metrics']) + '</ul>' if entry.get('metrics') else ''
    points = '<ul>' + ''.join(bi(point, tag='li') for point in entry['points']) + '</ul>' if entry.get('points') else ''
    related = related_links(entry.get('related', []), known)
    related = '<p class="experience-related">' + bi(UI['experience']['related']) + related + '</p>' if related else ''
    return metrics + points + related


def home_experience(number, context):
    known = context['known']
    timeline = ''
    for job in PROFILE['experience']:
        team = '<span class="experience-team">' + bi(job['team']) + '</span>' if job.get('team') else ''
        projects = ''.join('<section class="experience-project"><h4>' + bi(project['title']) + '</h4>' + experience_details(project, known) + '</section>' for project in job.get('projects', []))
        timeline += '<article class="experience-item"><div class="experience-date">' + txt(job['period']) + '</div><div class="experience-body"><p class="company">' + esc(job['company']) + '</p><h3>' + bi(job['role']) + team + '</h3>' + (bi(job['summary'], tag='p') if job.get('summary') else '') + experience_details(job, known) + projects + '</div></article>'
    return '<section class="editorial-section shell" id="experience">' + section_title(number, UI['sections']['experience']) + '<div class="experience-list">' + timeline + '</div></section>'


def home_evolution(number, context):
    data, copy, known = PROFILE['evolution'], UI['sections']['evolution'], context['known']
    stages = ''.join('<article class="evolution-stage"><span class="stage-index">0' + str(index + 1) + '</span><p class="stage-period">' + txt(stage.get('period', '')) + '</p><h3>' + bi(stage['title']) + '</h3>' + bi(stage['summary'], tag='p') + '<ul>' + ''.join(bi(point, tag='li') for point in stage.get('points', [])) + '</ul></article>' for index, stage in enumerate(data['stages']))
    nodes = ''
    for node in data.get('capabilities', []):
        nodes += '<details class="capability"><summary>' + bi(node['title']) + '<span aria-hidden="true">+</span></summary><div>' + bi(node['summary'], tag='p') + '<ul>' + ''.join(bi(point, tag='li') for point in node.get('points', [])) + '</ul><div class="related-projects">' + related_links(node.get('projects', []), known) + '</div></div></details>'
    link = data.get('link')
    link = '<a class="text-link" href="' + esc(url(link['url'])) + '" target="_blank" rel="noopener noreferrer">' + txt(link['label']) + '</a>' if link else ''
    return '<section class="evolution-section" id="evolution"><div class="shell"><div class="evolution-heading">' + section_title(number, copy) + '<div>' + bi(data['intro'], tag='p') + link + '</div></div><div class="evolution-stages">' + stages + '</div>' + ('<div class="capability-heading">' + bi(copy['capabilities'], tag='h3') + '</div><div class="capability-grid">' + nodes + '</div>' if nodes else '') + '</div></section>'


def home_selected(number, context):
    copy, projects = UI['sections']['selected'], context['projects']
    featured = sorted([item for item in projects if item.get('featured')], key=lambda item: item['featured'])[:context['config'].get('featured_limit', 6)]
    return '<section class="editorial-section shell" id="selected-work">' + section_title(number, copy) + '<div><div class="catalog-grid selected-grid">' + ''.join(project_card(item, context['categories']) for item in featured) + '</div><a class="all-projects-link" href="projects/">' + bi(fill(copy['all_projects'], count=len(projects))) + '</a></div></section>'


def home_resume(number, context):
    if not DOWNLOADS:
        return ''
    copy = UI['downloads']
    cards = ''
    for group in DOWNLOADS:
        rows = ''
        for lang in ('zh', 'en'):
            files = [entry for entry in group['files'] if entry['lang'] == lang]
            if files:
                rows += f'<div class="download-row" data-download-language="{lang}">' + bi(copy['languages'][lang], attrs='class="download-language"') + ''.join('<a href="/studio/downloads/' + esc(entry['file']) + '" download>' + esc(copy['formats'][entry['format']]) + '<small>' + size_label(entry['data']) + '</small></a>' for entry in files) + '</div>'
        cards += '<article class="download-card"><h3>' + bi(group['title']) + '</h3>' + bi(group['description'], tag='p') + '<div class="download-rows">' + rows + '</div></article>'
    return '<section class="editorial-section shell" id="resume">' + section_title(number, UI['sections']['resume']) + '<div class="download-list">' + cards + '</div></section>'


def home_beyond(number, context):
    copy = UI['sections']['beyond']
    personal = '<section class="editorial-section shell" id="beyond">' + section_title(number, copy) + '<div class="prose">' + ''.join(bi(text, tag='p') for text in PROFILE.get('about', [])) + '<a class="text-link" href="wow/">' + bi(copy['wow_link']) + '</a>'
    for education in PROFILE.get('education', []):
        personal += '<div class="education">' + txt(education['period']) + '<h3>' + bi(education['institution']) + '</h3>' + bi(education['degree'], tag='p') + '</div>'
    if PROFILE.get('languages'):
        personal += '<p class="language-skills">' + ' / '.join(bi(value) for value in PROFILE['languages']) + '</p>'
    return personal + '</div></section>'


def home_contact(number, context):
    copy = UI['sections']['contact']
    return '<section class="contact-section shell" id="contact">' + section_title(number, copy) + '<div>' + bi(copy['intro'], tag='p', attrs='class="contact-intro"') + contacts(True) + '</div></section>'


HOME_RENDERERS = {'highlights': home_highlights, 'focus': home_focus, 'experience': home_experience, 'evolution': home_evolution, 'selected': home_selected, 'resume': home_resume, 'beyond': home_beyond, 'contact': home_contact}


def home(config, categories, projects):
    context = {'config': config, 'categories': categories, 'projects': projects, 'known': {item['slug'] for item in projects}}
    body, number = hero(), 0
    for key in UI['home_sections']:
        numbered = 'title' in UI['sections'][key]
        rendered = HOME_RENDERERS[key](f'{number + 1:02d}', context)
        if rendered and numbered:
            number += 1
        body += rendered
    return layout(UI['titles']['home'], PROFILE['intro'][0], body)


def catalog(route, projects, categories, config):
    copy, page = UI['catalog'], UI['catalogs'][route]
    title, description = page['title'], page['description']
    nav = '<nav class="section-switcher" aria-label="' + esc(copy['switcher_label']) + '">' + ''.join('<a href="/studio/' + esc(link['route']) + '/"' + (' aria-current="page"' if link['route'] == route else '') + '>' + bi(link['label']) + '</a>' for link in copy['switcher']) + '</nav>'
    filters = '<button type="button" class="catalog-filter is-active" data-category-button="all" aria-pressed="true">' + bi(copy['all']) + f'<small>{len(projects)}</small></button>'
    for category in categories:
        count = sum(item['category'] == category['id'] for item in projects)
        if count:
            filters += f'<button type="button" class="catalog-filter" data-category-button="{category["id"]}" aria-pressed="false">' + bi(category) + f'<small>{count}</small></button>'
    total = len(projects)
    public = sum(item['visibility'] == 'public' for item in projects)
    visibility = copy['visibility']
    filtered = copy['showing_filtered']
    options = ''.join(f'<option value="{value}" data-zh="{esc(visibility[value]["zh"])}" data-en="{esc(visibility[value]["en"])}">{esc(visibility[value][LANGUAGE["default"]])}</option>' for value in ('all', 'public', 'private'))
    body = '<div class="shell catalog-main">' + nav + '<section class="catalog-hero"><p class="eyebrow">' + esc(fill(copy['eyebrow'], date=config['checked_at'])) + '</p><h1>' + bi(title) + '</h1>' + bi(description, tag='p') + '<div class="catalog-meta">' + bi(fill(copy['meta'], total=total, public=public, private=total - public)) + '</div></section><section aria-label="' + esc(copy['catalog_label']) + '"><div class="catalog-toolbar"><div class="catalog-filters" role="group" aria-label="' + esc(copy['filter_label']) + '">' + filters + '</div><label class="catalog-search"><span class="sr-only">' + bi(copy['search_label']) + '</span><input type="search" id="catalog-search" autocomplete="off" placeholder="' + esc(pick(copy['search_placeholder'])) + '" data-placeholder-zh="' + esc(copy['search_placeholder']['zh']) + '" data-placeholder-en="' + esc(copy['search_placeholder']['en']) + '"><button id="clear-search" hidden type="button">' + bi(copy['clear']) + '</button></label></div><div class="catalog-status"><p id="catalog-result-count" role="status" aria-live="polite" data-total="' + str(total) + '" data-filtered-zh="' + esc(filtered['zh']) + '" data-filtered-en="' + esc(filtered['en']) + '">' + bi(fill(copy['showing'], total=total)) + '</p><label class="visibility-select">' + bi(visibility['label']) + '<select id="visibility-filter">' + options + '</select></label></div><div class="catalog-grid">' + ''.join(project_card(item, categories) for item in projects) + '</div><div id="catalog-empty" class="catalog-empty" hidden><h2>' + bi(copy['empty_title']) + '</h2>' + bi(copy['empty_body'], tag='p') + '<button type="button" data-reset-filters>' + bi(copy['reset']) + '</button></div></section><aside class="catalog-footnote">' + bi(copy['footnote'], tag='p') + '</aside></div>'
    return layout(title, description, body, route + '/', active='projects', scripts='<script src="' + asset('catalog.js') + '" defer></script>')


def detail(item):
    copy = UI['project']
    content = ''
    for lang in ('zh', 'en'):
        rendered = markdown(item['_directory'] / f'README.{lang}.md') or '<p>' + esc(item['summary'][lang]) + '</p>'
        content += f'<div class="localized-content prose" data-content-language="{lang}"' + (' hidden' if lang != LANGUAGE['default'] else '') + '>' + rendered + '</div>'
    body = '<div class="shell detail-main"><a class="breadcrumb" href="/studio/projects/">' + bi(copy['back']) + '</a><section class="detail-heading">' + badge(item) + '<h1>' + bi(item['title']) + '</h1>' + bi(item['summary'], tag='p') + '<ul class="project-tags">' + ''.join('<li>' + esc(tag) + '</li>' for tag in item['tags']) + '</ul>' + source_link(item) + '</section><section class="project-content">' + content + '</section>'
    if item.get('features'):
        body += '<ul class="detail-features">' + ''.join(bi(zh, en, tag='li') for zh, en in zip(item['features']['zh'], item['features']['en'])) + '</ul>'
    if item['visibility'] == 'private':
        body += '<aside class="private-note">' + bi(copy['private_note'], tag='p') + source_link(item) + '</aside>'
    body += '</div>'
    return layout(item['title'], item['summary'], body, f'projects/{item["slug"]}/', active='projects')


def access_page(item):
    copy = UI['access']
    body = '<section class="shell access-page"><a class="breadcrumb" href="/studio/projects/' + esc(item['slug']) + '/">' + bi(copy['page_back']) + '</a><p class="eyebrow">' + esc(copy['page_eyebrow']) + '</p><h1>' + bi(copy['page_title']) + '</h1><h2>' + esc(item['slug']) + '</h2>' + bi(copy['page_body'], tag='p') + '<div class="dialog-actions"><a class="button button-dark" href="' + esc(email_link(item['slug'])) + '">' + bi(copy['email_button']) + '</a><a class="text-link" href="' + esc(item['url']) + '" target="_blank" rel="noopener noreferrer">' + bi(copy['github_button']) + '</a></div></section>'
    return layout(fill(UI['titles']['access'], slug=item['slug']), copy['page_description'], body, f'projects/{item["slug"]}/access/', active='projects')


def not_found():
    copy = UI['not_found']
    body = '<section class="shell access-page"><p class="eyebrow">' + esc(copy['eyebrow']) + '</p><h1>' + bi(copy['title']) + '</h1><p>' + bi(copy['body']) + '</p><div class="dialog-actions"><a class="button button-dark" href="/studio/">' + bi(copy['home']) + '</a><a class="text-link" href="/studio/projects/">' + bi(copy['projects']) + '</a></div></section>'
    return layout(UI['titles']['not_found'], copy['description'], body, '404.html')


def portfolio_redirect():
    copy = UI['portfolio_redirect']
    name = esc(PROFILE['name']) + ' / ' + esc(PROFILE['alias'])
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'self\'; object-src \'none\'; base-uri \'none\'; form-action \'none\'"><meta http-equiv="refresh" content="0;url=/studio/#experience"><link rel="canonical" href="https://liozzazhang.github.io/studio/"><title>' + name + '</title></head><body><h1>' + name + '</h1><p>' + esc(copy['body']) + '<a href="/studio/#experience">' + esc(copy['link']) + '</a></p></body></html>\n'


def build():
    config, profile, categories, projects = load_content()
    LANGUAGE['default'] = config.get('default_language', 'zh')
    UI.clear()
    UI.update(load_ui())
    PROFILE.clear()
    PROFILE.update(profile)
    DOWNLOADS[:] = load_downloads()
    outputs = {SITE / 'index.html': home(config, categories, projects)}
    for route, items in [('projects', projects), ('lab', [item for item in projects if item['group'] != 'wow']), ('wow', [item for item in projects if item['group'] == 'wow'])]:
        outputs[SITE / route / 'index.html'] = catalog(route, items, categories, config)
    for item in projects:
        outputs[SITE / 'projects' / item['slug'] / 'index.html'] = detail(item)
        if item['visibility'] == 'private':
            outputs[SITE / 'projects' / item['slug'] / 'access' / 'index.html'] = access_page(item)
    for group in DOWNLOADS:
        for entry in group['files']:
            outputs[SITE / 'downloads' / entry['file']] = entry['data']
    outputs[SITE / 'portfolio' / 'index.html'] = portfolio_redirect()
    outputs[SITE / '404.html'] = not_found()
    routes = [('' if path.relative_to(SITE).parent == Path('.') else str(path.relative_to(SITE).parent) + '/') for path in outputs if path.name == 'index.html' and 'access' not in path.parts and 'portfolio' not in path.parts]
    outputs[SITE / 'sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>https://liozzazhang.github.io/studio/' + route + '</loc></url>\n' for route in routes) + '</urlset>\n'
    generated = sorted(str(path.relative_to(SITE)) for path in outputs)
    outputs[SITE / '.generated-pages.json'] = json.dumps(generated, ensure_ascii=False, indent=2) + '\n'
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check generated output without changing files')
    args = parser.parse_args()
    outputs = build()
    manifest = SITE / '.generated-pages.json'
    if manifest.is_symlink():
        raise ValueError('Generated manifest must be a regular file')
    for path in outputs:
        if not path.resolve().is_relative_to(SITE.resolve()) or any(parent.is_symlink() for parent in [path, *path.parents] if parent != ROOT.parent):
            raise ValueError('Generated output must stay inside the website without symlinks')
    old = json.loads(manifest.read_text()) if manifest.exists() else []
    stale = []
    for name in old:
        path = SITE / name
        # Deletion is limited to prior generated project pages and resume downloads.
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not STALE_OUTPUT.fullmatch(name):
            continue
        if not path.resolve().is_relative_to(SITE.resolve()):
            raise ValueError('Stale output must stay inside the website')
        if path not in outputs and path.is_file():
            if args.check:
                stale.append(name)
            else:
                path.unlink()
    for path, content in outputs.items():
        data = content if isinstance(content, bytes) else content.encode('utf-8')
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if stale:
        raise SystemExit('Regenerate Studio: ' + ', '.join(stale))
    print(('Checked' if args.check else 'Built') + f' {len(outputs)} outputs from directory content modules.')


if __name__ == '__main__':
    main()
