# 结构与扩展约定

核对日期：**2026-11-19（Asia/Shanghai）**。

**当前阶段：页面已完成，发布状态以 GitHub Actions/Pages 为准。** `studio` 的目标仓库为 `liozzazhang/studio`，采用项目站点前缀 `/studio/`；页面已经生成不等于已确认上线。

## 页面分工

| 路径 | 内容 |
| --- | --- |
| `/studio/` | 导航首页与目录入口 |
| `/studio/portfolio/` | 个人介绍、高层案例与精选公开作品 |
| `/studio/projects/` | 全部 29 个公开项目 |
| `/studio/lab/` | 22 个工程与参考项目 |
| `/studio/wow/` | 7 个 WoW 插件与配置项目 |

目录分为 AI 与工具集成、平台交付与自动化、安全与访问、可观测性、可视化与架构、开发工具、WoW 插件与配置、历史与参考八类。`legacy`、`archived` 和 `fork` 是相互独立的状态，不通过分类名称推断其值。完整分类表见 [project-catalog.md](project-catalog.md)。

## 文件结构

```text
studio/
  data/
    projects.json            # 公开项目目录的单一数据源
  _templates/
    pages/
      home.html              # 首页生成模板
      catalog.html           # 项目目录生成模板
    site/                    # 新增独立子站的复制模板
  scripts/
    build_catalog.py         # 使用 Python 标准库生成目录页面
    preview.py               # 带 /studio/ 前缀的本地预览
  site/                      # Pages 唯一发布目录
    index.html               # 生成的导航首页
    assets/                  # 共享 CSS、JavaScript 与公开资源
    projects/index.html      # 生成的全部项目目录
    lab/index.html           # 生成的工程目录
    wow/index.html           # 生成的 WoW 目录
    portfolio/               # 个人主页与自身资源
    sitemap.xml              # 生成的站点地图
  .github/workflows/
    pages.yml                # 构建后上传整个 site/
  docs/
    structure.md
    content-sources.md
    project-catalog.md
  README.md
```

## 数据与构建

`data/projects.json` 保存经过核对的公开仓库快照，是项目名称、中英文简介、链接、标签、分类、分组、展示类型与状态的唯一目录来源。当前快照共 29 项，不含私有仓库与 `studio` 自身。这里提交的是公开摘要，不是认证接口返回或原始材料的副本。

`scripts/build_catalog.py` 使用 Python 标准库读取数据和模板，生成导航首页、全部项目／工程／WoW 目录与站点地图，并更新个人页中的精选公开项目区。个人介绍和其他高层案例不由项目目录数据代替。

更新目录的顺序为：

1. 核对要展示的仓库确为公开，确认简介与归属，并更新 `data/projects.json`。
2. 如需改目录布局，编辑 `_templates/pages/`；如需改样式和交互，编辑相应的公开前端文件。
3. 运行 `python3 scripts/build_catalog.py`，再运行 `python3 scripts/build_catalog.py --check`。
4. 运行 `python3 scripts/preview.py`，从 `http://127.0.0.1:4174/studio/` 检查全部入口、筛选、语言切换和资源加载。
5. 同步维护项目来源与 [项目分类表](project-catalog.md)，再提交计划公开的文件。

不要直接编辑生成的目录 HTML 来更新项目内容，因为重新构建会覆盖这些修改。构建和预览无需安装第三方 Python 库，也不需要安装项目仓库本身的运行环境。

## 路径约定

GitHub Pages 将 `site/` 的内容挂载在 `/studio/` 下：`site/projects/index.html` 对应 `/studio/projects/`，`site/assets/example.css` 对应 `/studio/assets/example.css`。`site/` 这个目录名不进入 URL。

站内资源可使用相对路径或明确以 `/studio/` 开头的路径。不要把站点误认为部署在域名根目录，从而生成遗漏项目前缀的链接。预览应使用带 `/studio/` 的入口，覆盖子站返回导航和带结尾斜杠的路径。

## 新增独立子站

从 `_templates/site/` 复制到 `site/` 下的新目录，编辑标题、正文、资源和返回首页的链接。若要在导航首页增加入口，应编辑 `_templates/pages/home.html` 后重新构建。新增项目卡片则更新 `data/projects.json`，不需要新建子站或复制整个项目源码。

## 工作流与发布边界

`.github/workflows/pages.yml` 已配置构建步骤：先运行 `python3 scripts/build_catalog.py`，再上传整个 `site/`。发布任务限制在 `main`，由 `site/**`、`data/**`、`_templates/pages/**`、`scripts/build_catalog.py` 和工作流自身的变化触发，也支持手动运行。Pages 的 Source 应选择 **GitHub Actions**。

`data/`、`_templates/`、`scripts/`、`docs/` 与根目录文档不直接进入 Pages 产物，但所有已提交文件仍可在公开仓库中查看。原始履历、聊天导出、内部资料和凭据不复制进来；原个人站目录保持独立，不会随 `studio` 自动同步。
