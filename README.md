# Studio · Lei Zhang / Liozza

面向面试官、HR 与工程同行的个人网站。首页以详细履历、工程演进、代表作品和联系方式介绍我，项目目录作为履历的进一步证据与补充。

站点地址：[liozzazhang.github.io/studio](https://liozzazhang.github.io/studio/) · [GitHub 仓库](https://github.com/liozzazhang/studio)。本次改版的发布结果以仓库的 GitHub Actions 与线上页面为准。

采用纯静态 HTML、CSS 与 JavaScript，通过 GitHub Pages 发布，无需 VM 或运行时后端。当前内容包含 **38 个仓库：30 个公开、8 个私有摘要，分为 8 类**；其中工程与参考项目 30 个，WoW 项目 8 个。

## 页面与内容

| 地址 | 内容 |
| --- | --- |
| `/studio/` | 自我介绍、完整履历、教育、工程演进、代表作品及邮箱、LinkedIn、WeChat、GitHub |
| `/studio/projects/` | 全部项目，可按分类、可见性与关键词浏览 |
| `/studio/lab/` | 工程、设计与参考项目 |
| `/studio/wow/` | WoW 插件、个人原型及历史配置收藏 |
| `/studio/projects/<slug>/` | 自动生成的双语项目介绍 |
| `/studio/projects/<slug>/access/` | 私有项目的访问申请说明，无 JavaScript 时也可使用 |
| `/studio/portfolio/` | 兼容旧地址，跳转到首页履历区 |

首页整合了 `engineering-evolution` 的四阶段经历与九个能力主题，保留方法和演进关系，不镜像原图或内部细节。

## 按目录维护项目

每个项目是独立内容模块。向 `content/projects/` 放入一个项目目录，提交并推送到 `main` 后即可自动构建，无需修改中心项目列表或页面代码。

```text
content/
  profile.json                  # 首页履历、联系方式、工程演进
  site.json                     # 站点配置与 featured_limit
  categories.json               # 分类名称与顺序
  projects/
    my-project/
      project.json              # 项目卡片信息，必需
      README.zh.md              # 中文项目详情，可选
      README.en.md              # 英文项目详情，可选
```

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

`slug` 必须与目录名和仓库名一致；URL 必须指向配置的 GitHub owner。`category` 使用 `categories.json` 中的分类 ID，`group` 为 `engineering` 或 `wow`。`order` 越小越靠前；设置整数 `featured` 可参与首页精选，按数值升序选取，数量由 `content/site.json` 的 `featured_limit` 控制，当前为 6。

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

`content/`、模板、脚本和文档不进入 Pages 上传目录，但它们属于公开仓库，仍然可以被查看。只提交计划公开的资料；原始履历、聊天导出、内部文档、凭据、账号配置与敏感截图不放进这个仓库。

项目介绍不等于已验证运行、部署或游戏兼容性；设计阶段和空仓库保留状态标记。Bene 项目不因源码可访问而变更许可，Fork 和第三方插件收藏单独标注归属。

详见 [结构约定](docs/structure.md)、[内容来源](docs/content-sources.md) 和 [项目分类表](docs/project-catalog.md)。
