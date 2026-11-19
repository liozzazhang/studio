#!/usr/bin/env python3
"""Build static Studio directories from the reviewed public repository catalog."""
import argparse
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "ai": ("AI 与工具集成", "AI & integrations", "{ + }"),
    "platform": ("平台与交付自动化", "Platform & delivery", "↗_"),
    "security": ("安全与访问", "Security & access", "⌘"),
    "observability": ("可观测性", "Observability", "≋"),
    "tools": ("开发工具", "Developer tools", ">_"),
    "visualization": ("可视化表达", "Visual stories", "✳"),
    "wow": ("WoW 插件", "WoW addons", "✦"),
    "archive": ("历史与参考", "Earlier & reference", "↶"),
}
WOW_CATEGORIES = {
    "interface": ("界面与协作", "Interface & groups"),
    "planning": ("团队与路线规划", "Raid & route planning"),
    "information": ("技能与读条提醒", "Timers & cast alerts"),
    "collection": ("早期配置收藏", "Earlier collection"),
}


def esc(value):
    return escape(str(value), quote=True)


def bi(zh, en, tag="span", attributes=""):
    return f'<{tag} data-zh="{esc(zh)}" data-en="{esc(en)}"{(" " + attributes) if attributes else ""}>{esc(zh)}</{tag}>'


def render(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", str(value))
    if re.search(r"\{\{[A-Z_]+\}\}", template):
        raise ValueError("Unresolved page template value")
    return template


def load_catalog():
    data = json.loads((ROOT / "data/projects.json").read_text())
    seen = set()
    for item in data["projects"]:
        slug = item["slug"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", slug) or slug in seen:
            raise ValueError("Invalid or duplicate repository name")
        seen.add(slug)
        if item["visibility"] != "public" or item["url"] != f"https://github.com/liozzazhang/{slug}":
            raise ValueError("Catalog must contain reviewed public repositories only")
        if item["category"] not in CATEGORIES:
            raise ValueError("Unknown project category")
        for field in ("title", "summary"):
            if not all(isinstance(item[field][lang], str) and item[field][lang] for lang in ("zh", "en")):
                raise ValueError("Every project needs Chinese and English copy")
    return data


def badge(item):
    if item.get("fork"):
        return "Fork 参考", "Reference fork"
    if item.get("archived"):
        return "已归档", "Archived"
    if item.get("kind") == "collection":
        return "配置收藏", "Collection"
    if item.get("legacy"):
        return "早期实践", "Earlier work"
    if item["group"] == "wow":
        return "插件源码", "Addon source"
    if item["kind"] == "visualization":
        return "交互可视化", "Visualization"
    return "代码仓库", "Source repository"


def project_card(item, wow_page=False):
    category = item.get("sub_category", "collection") if wow_page else item["category"]
    label = WOW_CATEGORIES[category] if wow_page else CATEGORIES[category][:2]
    glyph = CATEGORIES[item["category"]][2]
    badges = badge(item)
    search = " ".join([item["slug"], *item["title"].values(), *item["summary"].values(), *item["tags"]]).casefold()
    features = item.get("features")
    feature_html = ""
    if wow_page and features:
        feature_html = '<ul class="catalog-features">' + ''.join(
            bi(zh, en, "li") for zh, en in zip(features["zh"][:2], features["en"][:2])
        ) + '</ul>'
    muted = ' is-reference' if item.get('legacy') or item.get('fork') or item.get('kind') == 'collection' else ''
    return (
        f'<article class="catalog-card cat-{esc(item["category"])}{muted}" data-category="{esc(category)}" data-search="{esc(search)}">'
        '<div class="catalog-card-top">' + bi(label[0], label[1], attributes='class="catalog-category"')
        + bi(badges[0], badges[1], attributes='class="catalog-badge"') + '</div>'
        f'<div class="catalog-symbol" aria-hidden="true">{esc(glyph)}</div>'
        '<h3>' + bi(item['title']['zh'], item['title']['en']) + '</h3>'
        f'<p class="catalog-slug">{esc(item["slug"])}</p>'
        + bi(item['summary']['zh'], item['summary']['en'], 'p', 'class="catalog-summary"') + feature_html
        + '<ul class="catalog-tags">' + ''.join('<li>'+esc(tag)+'</li>' for tag in item['tags'][:4]) + '</ul>'
        + f'<a class="catalog-source" href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer" aria-label="{esc(item["slug"])} on GitHub">'
        + bi('查看仓库', 'View repository') + '<span aria-hidden="true">↗</span></a></article>'
    )


def build_page(slug, title, description, eyebrow, projects, checked_at):
    wow_page = slug == 'wow'
    categories = WOW_CATEGORIES if wow_page else CATEGORIES
    filters = '<button type="button" class="catalog-filter is-active" data-category-button="all" aria-pressed="true">' + bi('全部', 'All') + f'<small>{len(projects)}</small></button>'
    for key, label in categories.items():
        count = sum((item.get('sub_category') if wow_page else item['category']) == key for item in projects)
        if count:
            filters += f'<button type="button" class="catalog-filter" data-category-button="{key}" aria-pressed="false">' + bi(label[0], label[1]) + f'<small>{count}</small></button>'
    nav = ''
    for route, zh, en in [('projects', '全部项目', 'All projects'), ('lab', '工程工具箱', 'Engineering lab'), ('wow', 'WoW 插件', 'WoW addons')]:
        current = ' aria-current="page"' if route == slug else ''
        nav += f'<a href="../{route}/"{current}>' + bi(zh, en) + '</a>'
    footnote = (
        ('Bene 系列展示个人插件源码与界面规划；早期第三方插件配置收藏单独标识。', 'The Bene collection presents personal addon source and interface planning; earlier third-party configuration collections are labeled separately.')
        if wow_page else
        ('按公开 README 与仓库结构整理。源码工具、可视化作品、历史项目和 Fork 参考分别标识。', 'Organized from public READMEs and repository structure, with source tools, visual work, earlier projects, and reference forks labeled separately.')
    )
    values = {"TITLE_ZH": esc(title[0]), "TITLE_EN": esc(title[1]), "DESCRIPTION_ZH": esc(description[0]), "DESCRIPTION_EN": esc(description[1]), "PAGE_SLUG": slug, "EYEBROW": eyebrow, "COUNT": len(projects), "CHECKED_AT": checked_at, "SECTION_NAV": nav, "FILTERS": filters, "CARDS": '\n'.join(project_card(item, wow_page) for item in projects), "FOOTNOTE_ZH": esc(footnote[0]), "FOOTNOTE_EN": esc(footnote[1])}
    path = ROOT / 'site' / slug / 'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    return path, render((ROOT / '_templates/pages/catalog.html').read_text(), values)


def build():
    data = load_catalog()
    projects = data['projects']
    engineering = [item for item in projects if item['group'] != 'wow']
    wow = [item for item in projects if item['group'] == 'wow']
    pages = [
        build_page('projects', ('所有公开项目', 'All public projects'), ('从工程工具到游戏界面，用分类与关键词找到感兴趣的项目。', 'From engineering tools to game interfaces. Find projects by area or keyword.'), 'THE COMPLETE COLLECTION', projects, data['checked_at']),
        build_page('lab', ('工程工具箱', 'Engineering lab'), ('把平台经验写成工具。这里收录集成、交付、安全访问、可观测性与开发实践。', 'Turning platform experience into tools: integrations, delivery, secure access, observability, and developer practice.'), 'ENGINEERING / TOOLS / REUSE', engineering, data['checked_at']),
        build_page('wow', ('艾泽拉斯角落', 'Azeroth corner'), ('Bene 系列插件：整理界面、规划协作，把需要的信息放在看得见的位置。', 'The Bene addon collection: organize interfaces, plan together, and put useful information where it belongs.'), 'WORLD OF WARCRAFT / BENE', wow, data['checked_at']),
    ]
    home = render((ROOT / '_templates/pages/home.html').read_text(), {'PROJECT_COUNT': len(projects), 'ENGINEERING_COUNT': len(engineering), 'WOW_COUNT': len(wow), 'BENE_COUNT': sum(not item.get('legacy') for item in wow), 'MCP_COUNT': sum(item['slug'].startswith('mcp-') for item in projects)})
    pages.append((ROOT / 'site/index.html', home))
    portfolio_path = ROOT / 'site/portfolio/index.html'
    portfolio = portfolio_path.read_text()
    selected_slugs = ['mcp-jenkins', 'rolling-update-controller', 'py-duo', 'metrics-deploy', 'BeneUI', 'engineering-evolution']
    by_slug = {item['slug']: item for item in projects}
    selection = '<section class="opensource-section shell section-space" id="opensource" aria-labelledby="opensource-heading"><div class="section-heading"><div><p class="eyebrow section-index">04 <span>/</span> PUBLIC PROJECTS & TOOLS</p><h2 id="opensource-heading">' + bi('把工程经验，留在代码里。', 'Engineering experience, shared in code.') + '</h2></div><a class="text-link" href="../projects/">' + bi('浏览所有公开项目', 'Browse all public projects') + '<span aria-hidden="true">↗</span></a></div>' + bi('这里精选近期公开的工具与作品，涵盖平台工程、集成、安全、可观测性和游戏界面。', 'A selection of recently published tools and projects spanning platforms, integrations, security, observability, and game interfaces.', 'p', 'class="opensource-description"') + '<div class="repository-grid">'
    for slug in selected_slugs:
        item = by_slug[slug]
        selection += f'<a class="repository-link" href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer"><div class="repository-top"><span>' + esc(' / '.join(item['tags'][:2])) + '</span><span aria-hidden="true">↗</span></div><h3>' + esc(item['slug']) + '</h3>' + bi(item['summary']['zh'], item['summary']['en'], 'p') + '</a>'
    selection += '</div></section>\n\n'
    start = portfolio.index('<section class="opensource-section')
    end = portfolio.index('<section class="play-section', start)
    portfolio = portfolio[:start] + selection + portfolio[end:]
    pages.append((portfolio_path, portfolio))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>https://liozzazhang.github.io/studio/{path}</loc></url>\n' for path in ['', 'portfolio/', 'projects/', 'lab/', 'wow/']) + '</urlset>\n'
    pages.append((ROOT / 'site/sitemap.xml', sitemap))
    return pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check generated pages without writing them')
    args = parser.parse_args()
    outputs = build()
    stale = []
    for path, content in outputs:
        if args.check:
            if not path.is_file() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(content)
    if stale:
        raise SystemExit('Regenerate catalog pages: ' + ', '.join(stale))
    print(('Checked' if args.check else 'Built') + f' {len(outputs)} static outputs from data/projects.json')


if __name__ == '__main__':
    main()
