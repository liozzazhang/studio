#!/usr/bin/env python3
"""Generate Studio from independently discoverable, reviewed content modules."""
import argparse
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
SITE = ROOT / 'site'
SLUG = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}')


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
    return f'<{tag} data-zh="{esc(value["zh"])}" data-en="{esc(value["en"])}"{(" " + attrs) if attrs else ""}>{esc(value["zh"])}</{tag}>'


def url(value):
    parsed = urlsplit(value)
    if parsed.scheme == 'https' and parsed.netloc and not parsed.username and not parsed.password:
        return value
    raise ValueError('External links must use HTTPS without credentials')


def load_content():
    config = read_json(CONTENT / 'site.json')
    if config['owner'] != 'liozzazhang' or config['base_path'] != '/studio/' or config['origin'] != 'https://liozzazhang.github.io':
        raise ValueError('Unexpected publication destination')
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
    links = [('home', '/studio/#about', '关于我', 'About'), ('experience', '/studio/#experience', '履历', 'Experience'), ('evolution', '/studio/#evolution', '工程演进', 'Evolution'), ('projects', '/studio/projects/', '作品', 'Projects')]
    return '<header class="site-header shell"><a class="brand" href="/studio/">Lei Zhang<span> / Liozza</span></a><nav class="main-nav" aria-label="Main navigation">' + ''.join(f'<a href="{href}"' + (' aria-current="page"' if key == active else '') + '>' + bi(zh, en) + '</a>' for key, href, zh, en in links) + '</nav><div class="header-actions"><button type="button" class="language-toggle" data-language-toggle aria-label="Switch to English"><span data-language-label>EN</span></button><a class="contact-nav" href="/studio/#contact">' + bi('联系我 ↗', 'Contact ↗') + '</a></div></header>'


def footer():
    return '<footer class="site-footer shell"><span>© <span data-year>2026</span> Lei Zhang / Liozza</span><a href="/studio/projects/">' + bi('项目目录', 'Project index') + '</a><a href="#main">' + bi('回到顶部 ↑', 'Back to top ↑') + '</a></footer>'


def email_link(profile, slug=None):
    address = profile['contacts'].get('email')
    if not address or not re.fullmatch(r'[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+', address):
        raise ValueError('A valid contact email is required for access requests')
    if not slug:
        return 'mailto:' + address
    query = urlencode({'subject': f'Repository access request: {slug}', 'body': f'Hi Lei,\n\nI would like to request access to {slug}.\nGitHub username:\nPurpose / interview context:\nWhat I would like to review:\n\nThank you.'}, quote_via=quote)
    return 'mailto:' + address + '?' + query


def access_dialog(profile):
    return '<dialog id="access-dialog" aria-labelledby="access-title" aria-describedby="access-description"><div class="dialog-top"><span class="eyebrow">REPOSITORY ACCESS</span><button type="button" data-close-access aria-label="Close">×</button></div><h2 id="access-title">' + bi('申请查看项目', 'Request repository access') + '</h2><p class="access-repository" data-access-name></p><p id="access-description">' + bi('这个仓库是私有的。你可以先阅读本站的项目介绍；GitHub 负责验证实际访问权限。', 'This repository is private. You can read the project overview here; GitHub controls access to the repository itself.') + '</p><ol><li>' + bi('通过邮件提供你的 GitHub 用户名。', 'Email me your GitHub username.') + '</li><li>' + bi('注明希望查看的项目、用途或面试背景。', 'Include the project and your purpose or interview context.') + '</li><li>' + bi('我会根据可分享范围回复，并在合适时邀请协作。', 'I will reply with what can be shared and invite you when appropriate.') + '</li></ol><div class="dialog-actions"><a class="button button-dark" data-access-email href="' + esc(email_link(profile)) + '">' + bi('发邮件申请 ↗', 'Request by email ↗') + '</a><a class="text-link" data-access-github href="https://github.com/liozzazhang" target="_blank" rel="noopener noreferrer">' + bi('已有权限，前往 GitHub ↗', 'Already have access? GitHub ↗') + '</a></div></dialog>'


def layout(title, description, body, route='', active='home', scripts='', profile=None):
    template = (ROOT / '_templates/pages/layout.html').read_text(encoding='utf-8')
    values = {'TITLE_ZH': esc(title['zh']), 'TITLE_EN': esc(title['en']), 'DESCRIPTION': esc(description), 'URL': 'https://liozzazhang.github.io/studio/' + route, 'HEADER': header(active), 'BODY': body, 'FOOTER': footer(), 'SCRIPTS': scripts, 'DIALOG': access_dialog(profile) if profile else ''}
    for key, value in values.items():
        template = template.replace('{{' + key + '}}', value)
    if re.search(r'\{\{[A-Z_]+\}\}', template):
        raise ValueError('Unresolved layout variable')
    return '\n'.join(line.rstrip() for line in template.splitlines()) + '\n'


def source_link(item, profile):
    if item['visibility'] == 'private':
        return f'<a class="project-source private-source" href="/studio/projects/{esc(item["slug"])}/access/" data-private-repo="{esc(item["slug"])}" data-request-email="{esc(email_link(profile,item["slug"]))}" data-repository-url="{esc(item["url"])}">' + bi('申请访问 ↗', 'Request access ↗') + '</a>'
    return f'<a class="project-source" href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">' + bi('查看仓库 ↗', 'View source ↗') + '</a>'


def badge(item):
    badges = [bi('私有', 'Private') if item['visibility'] == 'private' else bi('公开', 'Public')]
    for flag, zh, en in [('fork','Fork 参考','Reference fork'), ('archived','已归档','Archived')]:
        if item.get(flag):
            badges.append(bi(zh, en))
    if item.get('status'):
        badges.append(bi(item['status']))
    elif item.get('kind') == 'collection':
        badges.append(bi('配置收藏', 'Collection'))
    elif item.get('legacy'):
        badges.append(bi('早期实践', 'Earlier work'))
    return '<div class="project-badges">' + ''.join(badges) + '</div>'


def project_card(item, categories, profile, compact=False):
    category = next(category for category in categories if category['id'] == item['category'])
    search = ' '.join([item['slug'], *item['title'].values(), *item['summary'].values(), *item['tags']]).casefold()
    return f'<article class="catalog-card" data-category="{esc(item["category"])}" data-visibility="{item["visibility"]}" data-search="{esc(search)}"><div class="project-top">' + bi(category) + badge(item) + '</div><h3><a href="/studio/projects/' + esc(item['slug']) + '/">' + bi(item['title']) + '</a></h3>' + bi(item['summary'], tag='p', attrs='class="project-summary"') + '<ul class="project-tags">' + ''.join('<li>' + esc(tag) + '</li>' for tag in item['tags'][:4]) + '</ul><div class="project-bottom"><a class="text-link" href="/studio/projects/' + esc(item['slug']) + '/">' + bi('项目介绍 →', 'Read overview →') + '</a>' + source_link(item, profile) + '</div></article>'


def section_title(number, zh, en, note=None):
    return f'<div class="section-title"><span class="section-number">{number}</span><h2>' + bi(zh, en) + '</h2>' + (bi(note, tag='p') if note else '') + '</div>'


def contacts(profile, large=False):
    contact = profile['contacts']
    links = '<a href="' + esc(email_link(profile)) + '"><span>Email</span><strong>' + esc(contact['email']) + '</strong><i>↗</i></a>'
    for field, label in [('linkedin', 'LinkedIn'), ('github', 'GitHub')]:
        if contact.get(field):
            value = url(contact[field])
            links += '<a href="' + esc(value) + '" target="_blank" rel="noopener noreferrer"><span>' + label + '</span><strong>' + ('Lei Zhang' if field == 'linkedin' else '@liozzazhang') + '</strong><i>↗</i></a>'
    if contact.get('wechat'):
        links += '<div class="contact-value"><span>WeChat</span><strong>' + esc(contact['wechat']) + '</strong></div>'
    else:
        links += '<a href="' + esc(email_link(profile)) + '"><span>WeChat</span><strong>' + bi('通过邮件联系获取', 'Available by email') + '</strong><i>↗</i></a>'
    return '<div class="contact-list' + (' is-large' if large else '') + '">' + links + '</div>'


def home(config, profile, categories, projects):
    intro = ''.join(bi(value, tag='p') for value in profile['intro'])
    hero = '<section class="profile-hero shell" id="about"><div class="hero-main"><p class="eyebrow">PERSONAL PROFILE / ENGINEERING & PRACTICE</p><h1>' + esc(profile['name']) + '<span>' + esc(profile['alias']) + '</span></h1>' + bi(profile['role'], tag='p', attrs='class="hero-role"') + '<div class="hero-intro">' + intro + '</div><div class="hero-actions"><a class="button button-dark" href="#experience">' + bi('阅读我的履历 ↓', 'Explore my experience ↓') + '</a><a class="text-link" href="projects/">' + bi('浏览作品 →', 'Explore projects →') + '</a><button type="button" class="print-link" data-print>' + bi('打印 / 存为 PDF', 'Print / save PDF') + '</button></div></div><aside class="profile-aside"><p class="eyebrow">AT A GLANCE</p><dl class="profile-facts"><div><dt>' + bi('目前', 'Currently') + '</dt><dd>Cisco</dd></div><div><dt>' + bi('方向', 'Focus') + '</dt><dd>' + bi('云平台 · 安全 · 自动化', 'Cloud · Security · Automation') + '</dd></div><div><dt>' + bi('所在地', 'Based in') + '</dt><dd>' + bi(profile['location']) + '</dd></div></dl>' + contacts(profile) + '</aside></section>'
    strengths = '<section class="editorial-section shell" id="focus">' + section_title('01', '我的工作', 'What I do') + '<div class="strength-list">' + ''.join('<article><h3>' + bi(item['title']) + '</h3>' + bi(item['summary'], tag='p') + '</article>' for item in profile.get('strengths', [])) + '</div></section>'
    timeline = ''
    for job in profile['experience']:
        timeline += '<article class="experience-item"><div class="experience-date">' + esc(job['period']) + '</div><div class="experience-body"><p class="company">' + esc(job['company']) + '</p><h3>' + bi(job['role']) + '</h3>' + (bi(job['summary'], tag='p') if job.get('summary') else '') + '<ul>' + ''.join(bi(point, tag='li') for point in job.get('points', [])) + '</ul></div></article>'
    if profile.get('skills'):
        skills = '<div class="skill-list">' + ''.join('<div><h4>' + bi(group['title']) + '</h4><p>' + esc(' / '.join(group['items'])) + '</p></div>' for group in profile['skills']) + '</div>'
        strengths = strengths.replace('</div></section>', skills + '</div></section>')
    experience = '<section class="editorial-section shell" id="experience">' + section_title('02', '职业履历', 'Experience', {'zh':'职责、个人贡献与工程方法。','en':'Responsibilities, contributions, and engineering practice.'}) + '<div class="experience-list">' + timeline + '</div></section>'
    evolution_data = profile['evolution']
    stages = ''.join('<article class="evolution-stage"><span class="stage-index">0' + str(index + 1) + '</span><p class="stage-period">' + esc(stage.get('period', '')) + '</p><h3>' + bi(stage['title']) + '</h3>' + bi(stage['summary'], tag='p') + '<ul>' + ''.join(bi(point, tag='li') for point in stage.get('points', [])) + '</ul></article>' for index, stage in enumerate(evolution_data['stages']))
    nodes = ''
    known = {item['slug'] for item in projects}
    for node in evolution_data.get('capabilities', []):
        related = ''.join('<a href="/studio/projects/' + esc(slug) + '/">' + esc(slug) + ' ↗</a>' for slug in node.get('projects', []) if slug in known)
        nodes += '<details class="capability"><summary>' + bi(node['title']) + '<span aria-hidden="true">+</span></summary><div>' + bi(node['summary'], tag='p') + '<ul>' + ''.join(bi(point,tag='li') for point in node.get('points',[])) + '</ul><div class="related-projects">' + related + '</div></div></details>'
    evolution = '<section class="evolution-section" id="evolution"><div class="shell"><div class="evolution-heading">' + section_title('03','工程演进','Engineering evolution') + '<div>' + bi(evolution_data['intro'], tag='p') + '<a class="text-link" href="https://github.com/liozzazhang/engineering-evolution" target="_blank" rel="noopener noreferrer">engineering-evolution ↗</a></div></div><div class="evolution-stages">' + stages + '</div>' + ('<div class="capability-heading">' + bi('能力与方法 · 点击展开', 'Capabilities & methods · Expand to read', tag='h3') + '</div><div class="capability-grid">' + nodes + '</div>' if nodes else '') + '</div></section>'
    featured = sorted([item for item in projects if item.get('featured')], key=lambda item:item['featured'])[:config.get('featured_limit',6)]
    selected = '<section class="editorial-section shell" id="selected-work">' + section_title('04','代表作品','Selected work',{'zh':'从履历中的问题，到可以阅读的实现。','en':'From engineering challenges to implementations you can explore.'}) + '<div><div class="catalog-grid selected-grid">' + ''.join(project_card(item,categories,profile,True) for item in featured) + '</div><a class="all-projects-link" href="projects/">' + bi(f'浏览全部 {len(projects)} 个项目 →',f'Explore all {len(projects)} projects →') + '</a></div></section>'
    personal = '<section class="editorial-section shell" id="beyond">' + section_title('05','工作之外','Beyond work') + '<div class="prose">' + ''.join(bi(text,tag='p') for text in profile.get('about',[])) + '<a class="text-link" href="wow/">' + bi('我的游戏与界面作品 →','Games & interface projects →') + '</a>'
    for education in profile.get('education',[]):
        personal += '<div class="education"><span>' + esc(education['period']) + '</span><h3>' + bi(education['institution']) + '</h3>' + bi(education['degree'],tag='p') + '</div>'
    if profile.get('languages'):
        personal += '<p class="language-skills">' + ' / '.join(bi(value) for value in profile['languages']) + '</p>'
    personal += '</div></section>'
    contact = '<section class="contact-section shell" id="contact">' + section_title('06','联系我','Get in touch') + '<div>' + bi('欢迎就平台工程、安全交付、AI 工作流与工程团队协作交流。面试或项目沟通，请直接发邮件。','I welcome conversations about platform engineering, secure delivery, AI workflows, and engineering teams. For interviews or project discussions, email is the best way to reach me.',tag='p',attrs='class="contact-intro"') + contacts(profile,True) + '</div></section>'
    return layout({'zh':'Lei Zhang / Liozza — 履历与工程作品','en':'Lei Zhang / Liozza — Experience & engineering'},profile['intro'][0]['zh'],hero+strengths+experience+evolution+selected+personal+contact,profile=profile)


def catalog(route, title, description, projects, categories, config, profile):
    nav = '<nav class="section-switcher" aria-label="Project directories">' + ''.join('<a href="/studio/' + slug + '/"' + (' aria-current="page"' if slug == route else '') + '>' + bi(zh,en) + '</a>' for slug,zh,en in [('projects','全部作品','All projects'),('lab','工程项目','Engineering'),('wow','游戏与界面','Games & interfaces')]) + '</nav>'
    filters = '<button type="button" class="catalog-filter is-active" data-category-button="all" aria-pressed="true">' + bi('全部','All') + f'<small>{len(projects)}</small></button>'
    for category in categories:
        count = sum(item['category'] == category['id'] for item in projects)
        if count:
            filters += f'<button type="button" class="catalog-filter" data-category-button="{category["id"]}" aria-pressed="false">' + bi(category) + f'<small>{count}</small></button>'
    body = '<div class="shell catalog-main">' + nav + '<section class="catalog-hero"><p class="eyebrow">PROJECT INDEX / ' + config['checked_at'] + '</p><h1>' + bi(title) + '</h1>' + bi(description,tag='p') + '<div class="catalog-meta">' + bi(f'{len(projects)} 个项目 · {sum(item["visibility"] == "public" for item in projects)} 公开 · {sum(item["visibility"] == "private" for item in projects)} 私有', f'{len(projects)} projects · {sum(item["visibility"] == "public" for item in projects)} public · {sum(item["visibility"] == "private" for item in projects)} private') + '</div></section><section aria-label="Project catalog"><div class="catalog-toolbar"><div class="catalog-filters" role="group" aria-label="Filter by area">' + filters + '</div><label class="catalog-search"><span class="sr-only">' + bi('搜索项目','Search projects') + '</span><input type="search" id="catalog-search" autocomplete="off" placeholder="搜索项目、功能或技术" data-placeholder-zh="搜索项目、功能或技术" data-placeholder-en="Search projects, features, or technologies"><button id="clear-search" hidden type="button">' + bi('清空','Clear') + '</button></label></div><div class="catalog-status"><p id="catalog-result-count" role="status" aria-live="polite" data-total="' + str(len(projects)) + '">' + bi(f'显示 {len(projects)} 个项目',f'Showing {len(projects)} projects') + '</p><label class="visibility-select">' + bi('可见性','Visibility') + '<select id="visibility-filter"><option value="all" data-zh="全部" data-en="All">全部</option><option value="public" data-zh="公开仓库" data-en="Public">公开仓库</option><option value="private" data-zh="私有仓库" data-en="Private">私有仓库</option></select></label></div><div class="catalog-grid">' + ''.join(project_card(item,categories,profile) for item in projects) + '</div><div id="catalog-empty" class="catalog-empty" hidden><h2>' + bi('没有匹配的项目','No matching projects') + '</h2>' + bi('请调整关键词或筛选条件。','Try different keywords or filters.',tag='p') + '<button type="button" data-reset-filters>' + bi('重置筛选','Reset filters') + '</button></div></section><aside class="catalog-footnote">' + bi('私有项目展示经整理的公开摘要；仓库内容仍由 GitHub 权限控制。设计文档、早期实践与 Fork 均单独标识。','Private projects have curated public summaries; GitHub still controls access to repository contents. Design work, earlier projects, and forks are labeled.',tag='p') + '</aside></div>'
    return layout(title,description['zh'],body,route+'/',active='projects',scripts='<script src="/studio/assets/catalog.js" defer></script>',profile=profile)


def detail(item, categories, profile):
    content = ''
    for lang in ('zh','en'):
        path = item['_directory'] / f'README.{lang}.md'
        rendered = markdown(path)
        if not rendered:
            rendered = '<p>' + esc(item['summary'][lang]) + '</p>'
        if rendered:
            content += f'<div class="localized-content prose" data-content-language="{lang}"' + (' hidden' if lang == 'en' else '') + '>' + rendered + '</div>'
    if not content:
        content = bi(item['summary'],tag='p',attrs='class="prose"')
    body = '<div class="shell detail-main"><a class="breadcrumb" href="/studio/projects/">' + bi('← 全部项目','← All projects') + '</a><section class="detail-heading">' + badge(item) + '<h1>' + bi(item['title']) + '</h1>' + bi(item['summary'],tag='p') + '<ul class="project-tags">' + ''.join('<li>' + esc(tag) + '</li>' for tag in item['tags']) + '</ul>' + source_link(item,profile) + '</section><section class="project-content">' + content + '</section>'
    if item.get('features'):
        body += '<ul class="detail-features">' + ''.join(bi(zh,en,tag='li') for zh,en in zip(item['features']['zh'],item['features']['en'])) + '</ul>'
    if item['visibility'] == 'private':
        body += '<aside class="private-note">' + bi('此页仅介绍项目的功能和设计思路。源码需要单独申请权限。','This page covers functionality and design only. Repository access requires a separate request.',tag='p') + source_link(item,profile) + '</aside>'
    body += '</div>'
    return layout(item['title'],item['summary']['zh'],body,f'projects/{item["slug"]}/',active='projects',profile=profile)


def access_page(item,profile):
    body = '<section class="shell access-page"><a class="breadcrumb" href="/studio/projects/' + esc(item['slug']) + '/">' + bi('← 返回项目介绍','← Back to overview') + '</a><p class="eyebrow">PRIVATE REPOSITORY</p><h1>' + bi('申请仓库访问权限','Request repository access') + '</h1><h2>' + esc(item['slug']) + '</h2>' + bi('仓库为私有状态，本站不会授予或绕过 GitHub 权限。请发邮件提供你的 GitHub 用户名、希望查看的内容和用途。我会根据可分享范围回复。','This repository is private. This site cannot grant or bypass GitHub permissions. Email me your GitHub username, what you would like to review, and your purpose. I will reply with what can be shared.',tag='p') + '<div class="dialog-actions"><a class="button button-dark" href="' + esc(email_link(profile,item['slug'])) + '">' + bi('发邮件申请 ↗','Request by email ↗') + '</a><a class="text-link" href="' + esc(item['url']) + '" target="_blank" rel="noopener noreferrer">' + bi('已有权限，前往 GitHub ↗','Already have access? GitHub ↗') + '</a></div></section>'
    return layout({'zh':'申请访问 · '+item['slug'],'en':'Request access · '+item['slug']},'Repository access request',body,f'projects/{item["slug"]}/access/',active='projects',profile=profile)


def build():
    config,profile,categories,projects = load_content()
    outputs = {SITE/'index.html':home(config,profile,categories,projects)}
    for route,title,description,items in [
        ('projects',{'zh':'作品与项目','en':'Projects & practice'},{'zh':'这些项目记录了我的工程实践：做过什么、如何设计，以及如何把经验变成工具。','en':'A record of my engineering practice: what I built, how I designed it, and how experience became reusable tools.'},projects),
        ('lab',{'zh':'工程项目','en':'Engineering projects'},{'zh':'平台交付、安全、可观测性、AI 集成与开发工具。','en':'Platform delivery, security, observability, AI integrations, and developer tools.'},[item for item in projects if item['group']!='wow']),
        ('wow',{'zh':'游戏与界面','en':'Games & interfaces'},{'zh':'从信息展示、团队协作到技能提醒，把游戏中的想法写成工具。','en':'Interface design, group collaboration, and ability reminders: turning ideas from games into tools.'},[item for item in projects if item['group']=='wow'])]:
        outputs[SITE/route/'index.html'] = catalog(route,title,description,items,categories,config,profile)
    for item in projects:
        outputs[SITE/'projects'/item['slug']/'index.html'] = detail(item,categories,profile)
        if item['visibility'] == 'private':
            outputs[SITE/'projects'/item['slug']/'access'/'index.html'] = access_page(item,profile)
    outputs[SITE/'portfolio'/'index.html'] = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'self\'; object-src \'none\'; base-uri \'none\'; form-action \'none\'"><meta http-equiv="refresh" content="0;url=/studio/#experience"><link rel="canonical" href="https://liozzazhang.github.io/studio/"><title>Lei Zhang / Liozza</title></head><body><h1>Lei Zhang / Liozza</h1><p>个人介绍已移至首页。<a href="/studio/#experience">阅读履历 / Read my experience</a></p></body></html>\n'
    outputs[SITE/'404.html'] = layout({'zh':'页面未找到 — Lei Zhang','en':'Page not found — Lei Zhang'},'Page not found','<section class="shell access-page"><p class="eyebrow">404 / PAGE NOT FOUND</p><h1>' + bi('这个页面暂时没有内容','This page could not be found') + '</h1><p>' + bi('可以返回个人主页，或继续浏览项目目录。','Return to my profile or browse the project index.') + '</p><div class="dialog-actions"><a class="button button-dark" href="/studio/">' + bi('个人主页','My profile') + '</a><a class="text-link" href="/studio/projects/">' + bi('浏览项目','Browse projects') + '</a></div></section>','404.html',profile=profile)
    routes = [('' if path.relative_to(SITE).parent == Path('.') else str(path.relative_to(SITE).parent) + '/') for path in outputs if path.name=='index.html' and 'access' not in path.parts and 'portfolio' not in path.parts]
    outputs[SITE/'sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>https://liozzazhang.github.io/studio/' + route + '</loc></url>\n' for route in routes) + '</urlset>\n'
    generated = sorted(str(path.relative_to(SITE)) for path in outputs)
    outputs[SITE/'.generated-pages.json'] = json.dumps(generated,ensure_ascii=False,indent=2)+'\n'
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Check generated output without changing files')
    args = parser.parse_args()
    outputs = build()
    manifest = SITE/'.generated-pages.json'
    if manifest.is_symlink():
        raise ValueError('Generated manifest must be a regular file')
    for path in outputs:
        if not path.resolve().is_relative_to(SITE.resolve()) or any(parent.is_symlink() for parent in [path, *path.parents] if parent != ROOT.parent):
            raise ValueError('Generated output must stay inside the website without symlinks')
    old = json.loads(manifest.read_text()) if manifest.exists() else []
    stale = []
    for name in old:
        path = SITE/name
        # Deletion is limited to prior generated pages in the project namespace.
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not re.fullmatch(r'projects/[A-Za-z0-9_.-]+/(?:access/)?index\.html',name):
            continue
        if not path.resolve().is_relative_to(SITE.resolve()):
            raise ValueError('Stale output must stay inside the website')
        if path not in outputs and path.is_file():
            if args.check:
                stale.append(name)
            else:
                path.unlink()
    for path,content in outputs.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding='utf-8') != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content,encoding='utf-8')
    if stale:
        raise SystemExit('Regenerate Studio: '+', '.join(stale))
    print(('Checked' if args.check else 'Built')+f' {len(outputs)} outputs from directory content modules.')


if __name__ == '__main__':
    main()
