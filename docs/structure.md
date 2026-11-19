# 结构与扩展约定

核对日期：**2026-11-19（Asia/Shanghai）**。当前内容为 38 个独立项目模块；站点发布状态以本次 GitHub Actions 和实际访问结果为准。

## 信息结构

首页服务于个人展示：自我介绍、职业履历、教育、工程成长脉络、代表项目和联系方式形成连续的阅读顺序。仓库目录提供进一步了解作品的入口，包含工程项目、设计文档、早期实践、参考资料及游戏兴趣项目。

| 路径 | 内容来源与用途 |
| --- | --- |
| `/studio/` | `content/profile.json` 生成的个人介绍、关键成果、履历与代表项目、工程演进，附项目精选和简历下载；分节顺序与文案来自 `content/ui.json` |
| `/studio/downloads/<file>` | `content/downloads/downloads.json` 列出的简历文件 |
| `/studio/projects/` | 自动扫描的全部项目目录，当前 38 项 |
| `/studio/lab/` | `group: engineering`，当前 30 项 |
| `/studio/wow/` | `group: wow`，当前 8 项 |
| `/studio/projects/<slug>/` | 对应模块的元数据与中英 Markdown 详情 |
| `/studio/projects/<slug>/access/` | 私有项目的独立权限与邮件申请说明 |
| `/studio/portfolio/` | 兼容旧链接，跳转到 `/studio/#experience` |

## 文件结构

```text
studio/
  content/
    profile.json                    # 履历与代表项目、关键成果、概览、教育、联系人、能力与工程演进
    ui.json                         # 全部页面文案、首页分节顺序与目录/申请/404 文案
    site.json                       # owner、地址前缀、默认语言、精选数量等
    categories.json                 # 分类 ID 与中英名称
    downloads/
      downloads.json                # 简历下载清单
      files/                        # PDF / DOCX 原件，仅清单内文件发布
    projects/
      <slug>/
        project.json                # 每个项目独立的数据入口
        README.zh.md                # 可选中文详情
        README.en.md                # 可选英文详情
  _templates/pages/
    layout.html                     # 共享页面结构
  scripts/
    build_catalog.py                # 扫描模块，生成首页、目录与详情
    check_public_catalog.py         # 展示声明与公开仓库状态校验
    preview.py                      # 按 /studio/ 前缀提供本地预览
  site/                             # 唯一上传 Pages 的产物目录
    index.html
    assets/
    projects/
      index.html
      <slug>/index.html
      <private-slug>/access/index.html
    lab/index.html
    wow/index.html
    portfolio/index.html
    downloads/<file>                # 简历下载，按字节复制
    sitemap.xml
    .generated-pages.json           # 生成文件清单，支持删除模块或下载后清理
  .github/workflows/pages.yml
  docs/
  README.md
```

## 项目模块契约

构建器扫描 `content/projects/*/project.json`，不依赖手工列出的项目数组。新增项目需要一个与仓库同名的目录及 JSON 文件；详情 Markdown 为可选内容。

```json
{
  "slug": "my-project",
  "title": {"zh": "项目名称", "en": "Project name"},
  "summary": {"zh": "用途与能力摘要。", "en": "Purpose and capabilities."},
  "url": "https://github.com/liozzazhang/my-project",
  "category": "tools",
  "group": "engineering",
  "kind": "source",
  "visibility": "public",
  "tags": ["Python"],
  "order": 400
}
```

将示例改成真实 owned 仓库，目录名、`slug` 与仓库名保持一致。标记为公开的仓库需要能通过发布时的可见性核对。

| 字段 | 规则 |
| --- | --- |
| `title`、`summary` | 必须同时有 `zh` 和 `en` 文本 |
| `category` | 对应 `content/categories.json` 中的 ID |
| `group` | `engineering` 或 `wow` |
| `kind` | 内容类型，如 `source`、`design`、`documentation`、`planned`、`visualization`、`reference`、`collection` |
| `visibility` | 显式填写 `public` 或 `private` |
| `disclosure` | 私有项目必须为 `summary-only`，表示允许公开此模块的摘要 |
| `order` | 可选非负整数，数值越小越靠前 |
| `featured` | 可选非负整数，参与首页精选并按数值升序排列 |
| `status` | 可选双语状态，用于设计、原型或初始化等实际阶段 |
| `fork`、`archived`、`legacy` | 可选布尔标记，分别表示 Fork、GitHub 归档状态与早期实践，不能互相替代 |
| `features`、`sub_category` | 现有模块可保留的扩展内容 |

首页精选数量在 `content/site.json` 的 `featured_limit` 中设置，当前为 6。`default_language` 设为 `en` 或 `zh`，决定生成页面的初始文字、`lang`、标题与描述，以及首次访问时的语言。无需在模板内增加项目名称。

## 首页与界面文案契约

构建器不保存面向读者的文案，缺少必需字段时直接报错。

| 文件 / 字段 | 用途 |
| --- | --- |
| `ui.json` `home_sections` | 首页分节顺序，可选 `highlights`、`focus`、`experience`、`evolution`、`selected`、`resume`、`beyond`、`contact`；移除即隐藏，节号按实际渲染顺序生成 |
| `ui.json` `sections.<id>` | 各节 `title`、可选 `note` 与该节按钮文案；`highlights` 只有无障碍 `label`，不编号 |
| `ui.json` 其他键 | 导航、header/footer、页面标题、hero 按钮、目录页、徽标、私有申请弹窗与邮件模板、404 |
| `profile.json` `glance` | hero 右侧概览，`value` 可为纯文本或中英对象 |
| `profile.json` `highlights` | 首页关键成果，`value` 为纯文本或中英对象，`label` 为中英说明 |
| `profile.json` `experience[]` | `period`、`company`、`role` 必填；可选 `team`、`summary`、`metrics`、`points`、`related`、`projects[]`。`period`（含工程演进与教育）可为纯文本或中英对象 |
| `experience[].projects[]` | `title` 必填；可选 `metrics`、`points`、`related`（项目 slug，不存在的 slug 不显示） |
| `profile.json` `evolution.link` | 工程演进区外链，需 HTTPS |
| `profile.json` `contacts` | `linkedin_label`、`github_label` 为对应链接的显示名 |

文案中的 `{count}`、`{slug}`、`{date}`、`{total}`、`{public}`、`{private}`、`{visible}` 由构建器或目录脚本填充。

## 简历下载契约

`content/downloads/downloads.json` 是分组数组。每组包含 `id`、`order`、中英 `title` 与 `description`，以及 `files`：每个文件写 `lang`（`zh` / `en`）、`format`（`pdf` / `docx`）和 `file`（`files/` 下的文件名）。

构建时校验文件名、扩展名与 `format` 一致、文件为普通文件且不超过 5 MB、文件头与格式一致（PDF 为 `%PDF-`，DOCX 为 ZIP），再按字节复制到 `site/downloads/`。未列入清单的文件不发布；从清单删除后，构建会按 `.generated-pages.json` 清理旧下载文件。

## Markdown 与页面生成

`README.zh.md` 和 `README.en.md` 可以放项目背景、功能范围、个人贡献与设计选择。构建器提供安全的 Markdown 子集：标题、列表、段落、粗体、行内代码与 HTTPS 链接；不会执行原始 HTML 或 JavaScript，不加载 Markdown 图片。

内容文件必须为普通文件，项目目录不能是符号链接；路径、owner、分类、可见性和双语元数据会在构建时校验。构建器根据模块自动生成路由，并使用 `site/.generated-pages.json` 记录生成页面；删除模块后重新构建，会清理对应的旧生成页面。

`site/` 是产物，不是个人资料的主要编辑位置。修改内容编辑 `content/`，修改排版编辑共享模板和资源，随后重新构建。

## 私有项目与权限入口

私有项目在项目目录和详情中公开展示获授权的名称、摘要及状态。点击仓库入口时显示权限弹窗；无 JavaScript 时使用独立 `access/` 页面。两处都说明通过邮件提供 GitHub 用户名、项目及用途，由站主按可分享范围回复。

弹窗与申请页只说明访问流程，不提供身份认证，不授予 GitHub 权限；实际仓库读取由 GitHub 控制。`summary-only` 也不是内容加密：模块 JSON 和 Markdown 都存于公开 Studio 仓库，仅能放计划公开的内容。

## 构建、删除与发布

1. 编辑 `content/profile.json` 更新履历、联系人与工程演进，编辑 `content/ui.json` 更新页面文案，或更新 `content/downloads/`；也可新增、修改、删除独立项目模块。
2. 运行 `python3 scripts/build_catalog.py` 生成产物与清理已删除模块的旧页面。
3. 运行 `python3 scripts/build_catalog.py --check`，确认生成结果与内容一致。
4. 运行 `python3 scripts/preview.py`，从 `http://127.0.0.1:4174/studio/` 核对中英切换、导航、搜索和私有申请入口。
5. 提交并推送 `main`，检查 GitHub Actions 和实际线上结果。

`content/**` 的变动会触发 Pages 工作流；构建只使用 Python 标准库。运行时网页不查询 GitHub API，也不含用于读取私有仓库的凭据。

Pages 把 `site/` 内容挂载在 `/studio/` 下，`site/` 本身不会进入 URL。仅该目录被上传；公开源码仓库内其他已提交文件仍然可以被浏览。
