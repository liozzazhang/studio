# studio

个人主页与公开作品目录，使用 GitHub Pages 静态托管。导航首页连接个人介绍、全部公开项目、工程工具箱与 WoW 插件目录。

**当前阶段：页面已完成，发布状态以 GitHub Actions/Pages 为准。** 目标仓库为 `liozzazhang/studio`，目标入口为 `https://liozzazhang.github.io/studio/`；本文不以页面文件已生成来断言发布成功。

项目目录按 **2026-11-19（Asia/Shanghai）** 的公开快照整理，共 **29 个项目、8 个分类**，不含 `studio` 自身，也不包含私有仓库。

## 页面与地址

| 页面 | 内容 | GitHub Pages 路径 |
| --- | --- | --- |
| 导航首页 | 介绍与各目录入口 | `/studio/` |
| 个人主页 | 个人介绍、高层案例与精选公开作品 | `/studio/portfolio/` |
| 全部项目 | 29 个公开项目 | `/studio/projects/` |
| 工程工具箱 | 22 个工程与参考项目 | `/studio/lab/` |
| WoW 插件 | 7 个公开插件与配置项目 | `/studio/wow/` |

八类分别为 AI 与工具集成、平台交付与自动化、安全与访问、可观测性、可视化与架构、开发工具、WoW 插件与配置、历史与参考。目录提供中英文切换、分类和关键词筛选，并区分源码、可视化、参考资料及配置收藏。

仓库名称 `studio` 构成项目站点前缀，发布目录 `site/` 本身**不会**进入网址。根首页与各项目目录均已有内容，不再是占位页。

## 本地构建与预览

在仓库根目录依次运行：

```sh
python3 scripts/build_catalog.py
python3 scripts/preview.py
```

构建器与预览服务均只使用 Python 标准库，无需第三方依赖、Node.js 或 npm 安装。生成的网站使用静态 HTML、CSS 与 JavaScript，不需要后端服务器。

打开 `http://127.0.0.1:4174/studio/`。预览脚本按 `/studio/` 前缀挂载网站，用于检查与 GitHub 项目站点一致的导航和资源路径。按 `Ctrl+C` 停止服务器。直接打开 HTML 文件或按无前缀根目录预览，不能充分检查项目站点路径。

可用以下命令检查生成页面是否与目录数据一致：

```sh
python3 scripts/build_catalog.py --check
```

## 内容与文件约定

- `data/projects.json`：项目目录的单一数据源，只提交经过核对的公开项目快照。
- `_templates/pages/`：导航首页与目录页的生成模板。
- `scripts/build_catalog.py`：读取数据和模板，生成首页、三个项目目录、个人页的精选公开项目区与站点地图。
- `site/`：唯一上传到 GitHub Pages 的目录，包含所有公开页面与资源。
- `site/assets/`：各入口共用的样式和脚本。
- `site/portfolio/`：个人主页及其前端资源；原 `liozzazhang.github.io` 本地目录保持独立。
- `_templates/site/`：新增独立子站的复制模板，不作为网页发布。
- `scripts/preview.py`：带项目名前缀的本地预览工具。
- `docs/`：结构、来源与逐项目目录文档，不进入 Pages 产物，但属于公开仓库内容。

修改项目简介、标签、类别、公开链接或状态时，先编辑 `data/projects.json`，再重新构建。不要直接维护生成的目录 HTML；修改其版式应编辑 `_templates/pages/`。个人介绍和高层案例仍在个人页文件中维护，构建器会更新其中的精选公开项目区。

详见 [结构约定](docs/structure.md)、[内容来源](docs/content-sources.md) 和 [项目分类表](docs/project-catalog.md)。

## GitHub Pages 部署

1. 使用 `liozzazhang` 下名为 **`studio`** 的 **Public** 仓库，检查现有内容后再提交和推送 `main`。
2. 进入 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。
3. 工作流先核对目录中的仓库仍为公开，再执行 `python3 scripts/build_catalog.py`，整体上传 `site/` 并部署。
4. 在 **Actions** 中检查工作流结果，再检查 **Pages** 返回的地址与各子站。发布状态以这些实际结果为准。

主分支中 `site/**`、`data/**`、`_templates/pages/**`、`scripts/build_catalog.py`、`scripts/check_public_catalog.py` 或发布工作流自身的变化会触发发布；也可以手动运行。工作流使用 GitHub 的短期工作流身份，无需把 PAT 放进前端或仓库。可见性检查只在构建阶段访问 GitHub API；浏览器不会调用 GitHub API。仓库改为私有或无法核实时，发布会停止，需先修正公开目录。

## 公开内容边界

网站展示公开源码和文档摘要，不表示自动化工具、MCP 服务、CLI 或游戏插件已在 Pages 中运行，也不代表已验证部署或游戏兼容性。Bene 系列只作为公开源码介绍；未镜像含玩家信息的截图，也未镜像 `engineering-evolution` 的原图。

公开仓库中的所有已提交文件都可以被查看，包括数据、文档、模板和脚本。“不作为网页发布”不等于私密。原始履历、聊天导出、内部资料、账号配置、令牌和其他敏感文件不复制到此仓库。
