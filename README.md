# Studio · Lei Zhang / Liozza

面向面试官、HR 与工程同行的个人网站。首页以关键成果、详细履历、工程演进、代表作品、简历下载和联系方式介绍我，项目目录作为履历的进一步证据与补充。

站点地址：[liozzazhang.github.io/studio](https://liozzazhang.github.io/studio/) · [GitHub 仓库](https://github.com/liozzazhang/studio)。本次改版已于 2026-11-19 发布，桌面、手机及线上私有项目申请入口已核对。[部署记录](https://github.com/liozzazhang/studio/actions/runs/44481910241)。

采用纯静态 HTML、CSS 与 JavaScript，通过 GitHub Pages 发布，无需 VM 或运行时后端。当前内容包含 **38 个仓库：30 个公开、8 个私有摘要，分为 8 类**；其中工程与参考项目 30 个，WoW 项目 8 个。

## 页面与内容

| 地址 | 内容 |
| --- | --- |
| `/studio/` | 自我介绍、关键成果、按职位分组的代表项目、教育、工程演进、代表作品及邮箱、LinkedIn、WeChat、GitHub |
| `/studio/#resume` | 简历下载：AI、技术、管理三个方向的简历与 AI 项目 Casebook，各有中英文 PDF 与 Word |
| `/studio/downloads/<file>` | 由 `content/downloads/` 复制生成的下载文件 |
| `/studio/projects/` | 全部项目，可按分类、可见性与关键词浏览 |
| `/studio/lab/` | 工程、设计与参考项目 |
| `/studio/wow/` | WoW 插件、个人原型及历史配置收藏 |
| `/studio/projects/<slug>/` | 自动生成的双语项目介绍 |
| `/studio/projects/<slug>/access/` | 私有项目的访问申请说明，无 JavaScript 时也可使用 |
| `/studio/portfolio/` | 兼容旧地址，跳转到首页履历区 |

首页整合了 `engineering-evolution` 的四阶段经历与九个能力主题，保留方法和演进关系，不镜像原图或内部细节。

## 只改内容，不改代码

所有面向读者的文字都在 `content/` 中；`scripts/build_catalog.py` 只负责校验和排版，不含页面文案。

```text
content/
  profile.json                  # 个人信息、概览、关键成果、履历与代表项目、技能、工程演进
  ui.json                       # 导航、页面标题、各节标题与说明、首页分节顺序、目录与申请文案
  site.json                     # 站点配置、default_language 与 featured_limit
  categories.json               # 分类名称与顺序
  downloads/
    downloads.json              # 简历下载清单（分组、说明、语言与格式）
    files/                      # 简历文件，仅清单中列出的文件会发布
  projects/
    my-project/
      project.json              # 项目卡片信息，必需
      README.zh.md              # 中文项目详情，可选
      README.en.md              # 英文项目详情，可选
```

常见修改：

- **履历与成果**：编辑 `profile.json`。`experience[]` 每个职位可写 `team`（团队规模）、`summary`、`metrics`（数字标签）、`points`、`related`（项目 slug），以及 `projects[]` 代表项目（同样支持 `title`、`metrics`、`points`、`related`）。`highlights` 为首页关键成果数字，`glance` 为右侧概览。
- **页面文案与分节**：编辑 `ui.json`。`home_sections` 决定首页分节顺序，删掉某一项即隐藏该节，节号自动重排；含 `{count}`、`{slug}` 等占位符的文案由构建器填充。
- **简历下载**：替换 `downloads/files/` 中的文件，或在 `downloads.json` 中增删分组与文件。文件名只能包含字母、数字、`_`、`.`、`-`，格式仅 `pdf` / `docx`，单个不超过 5 MB，内容须与扩展名一致；未列入清单的文件不会发布，从清单移除后构建会清理 `site/downloads/` 中的旧文件。

## 按目录维护项目

每个项目是独立内容模块。向 `content/projects/` 放入一个项目目录，提交并推送到 `main` 后即可自动构建，无需修改中心项目列表或页面代码。

最小项目示例：将下面内容保存为 `content/projects/my-project/project.json`，并把示例名称、URL 和简介替换为自己的真实仓库信息。

```json
{
  "slug": "my-project",
  "title": {"zh": "项目名称", "en": "Project name"},
  "summary": {"zh": "项目解决的问题和主要能力。", "en": "The problem and main capability."},
  "url": "https://github.com/liozzazhang/my-project",
  "category": "tools",
  "group": "engineering",
  "kind": "source",
  "visibility": "public",
  "tags": ["Python", "CLI"],
  "order": 400
}
```

`slug` 必须与目录名和仓库名一致；URL 必须指向配置的 GitHub owner。`category` 使用 `categories.json` 中的分类 ID，`group` 为 `engineering` 或 `wow`。`order` 越小越靠前；设置整数 `featured` 可参与首页精选，按数值升序选取，数量由 `content/site.json` 的 `featured_limit` 控制，当前为 6。首次访问的语言由 `default_language`（`en` / `zh`）决定，当前为英文；访客切换后记住其选择。

详情 Markdown 支持标题、列表、段落、粗体、行内代码与 HTTPS 链接。原始 HTML、JavaScript 和图片语法不会作为活动内容执行或加载。可选 `status` 使用 `{"zh": "设计阶段", "en": "Design stage"}`，用于区分设计文档、个人原型、初始化项目等实际状态。

## 私有仓库的展示与申请

私有项目设置 `"visibility": "private"` 和 `"disclosure": "summary-only"`。本轮按用户明确要求收录其名称及经过整理的高层摘要；**这些摘要和 Markdown 本身会公开**，不应放入仅供获授权读者阅读的材料。

访问仓库时，网站显示权限说明和邮件申请入口；申请邮件包含项目名，并提示填写 GitHub 用户名、用途或面试背景。申请入口只打开邮件客户端，不自动发送邮件。已有权限者可继续前往 GitHub，实际权限由 GitHub 验证与管理。网站不会代理私有源码，也不改变仓库可见性。

## 本地构建与预览

仅使用 Python 标准库，无需安装 npm 或 Python 第三方包。在仓库根目录运行：

```sh
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
python3 scripts/preview.py
```

打开 `http://127.0.0.1:4174/studio/`，检查与 GitHub 项目站一致的 `/studio/` 前缀路径。生成页面由构建器维护；直接修改生成 HTML 会在下次构建时被覆盖。

删除项目模块并重新构建后，构建器根据生成清单清理其旧详情页和申请页。不要手动维护项目路由清单。

## 自动发布与内容边界

推送 `content/**`、共享模板、站点资源或构建脚本到 `main` 后，GitHub Actions 校验内容和公开仓库可见性、重新构建，并仅上传 `site/` 到 Pages，也支持手动触发。私有摘要必须显式声明 `summary-only`，发布检查不会下载其源码。公开项目变为私有或无法确认公开状态时，先调整其展示声明，再重新发布。

`content/`、模板、脚本和文档中，除 `content/downloads/` 中清单列出的简历会复制到 `site/downloads/` 外，其余不进入 Pages 上传目录；但它们都属于公开仓库，仍然可以被查看。只提交计划公开的资料：经确认对外发布的简历成品可以放入 `content/downloads/files/`；简历草稿、聊天导出、内部文档、凭据、账号配置与敏感截图不放进这个仓库。

更新简历 PDF 时，从 Word 原稿导出后先检查页脚：公司设备上的 Word 可能按敏感度标签自动加上 “Cisco Confidential” 等标记，这类标记必须去除后再提交。

项目介绍不等于已验证运行、部署或游戏兼容性；设计阶段和空仓库保留状态标记。Bene 项目不因源码可访问而变更许可，Fork 和第三方插件收藏单独标注归属。

详见 [结构约定](docs/structure.md)、[内容来源](docs/content-sources.md) 和 [项目分类表](docs/project-catalog.md)。
