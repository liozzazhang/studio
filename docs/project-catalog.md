# 公开项目目录

核对日期：**2026-11-19（Asia/Shanghai）**。本目录依据 [data/projects.json](../data/projects.json) 的固定快照生成，共 **29 个公开仓库**，不含承载网站本身的 `studio`，不收录私有仓库。

本次按该快照整理，不据实时仓库变化自动补项。网站入口分工为：`/studio/projects/` 展示全部 29 项，`/studio/lab/` 展示工程与参考项目 22 项，`/studio/wow/` 展示 WoW 项目 7 项；`/studio/portfolio/` 保留个人介绍与高层案例。

## 核对范围与类型

目录只提供项目简介、分类和公开 GitHub 入口。简介依据公开元数据、README 与必要的仓库结构整理；未执行仓库代码，未连接目标服务，未验证部署、生产效果或安全保证。后端服务、CLI、自动化框架及游戏插件不会因此在 GitHub Pages 中运行。

| 类型标记 | 含义 | 数量 |
| --- | --- | ---: |
| `source` | 源码、框架、脚本或相关工程文档；不是在线应用验证标记 | 26 |
| `visualization` | 可视化类项目；此目录仅保留简介与源码入口 | 1 |
| `reference` | 参考资料，不作为本人原创项目展示 | 1 |
| `collection` | 插件与配置收藏，可能包含第三方作品 | 1 |

状态标记与类型互相独立：`legacy` 表示历史内容；`archived` 表示 GitHub 仓库已归档；`fork` 表示 GitHub 明确标记为 Fork。历史内容不一定已归档，收藏也不等于 Fork；未标记 Fork 不能证明全部代码或素材完全原创。

## 分类概览

| 分类 | 数量 | 范围 |
| --- | ---: | --- |
| AI 与工具集成 | 2 | 工程与参考 |
| 平台交付与自动化 | 5 | 工程与参考 |
| 安全与访问 | 2 | 工程与参考 |
| 可观测性 | 1 | 工程与参考 |
| 可视化与架构 | 1 | 工程与参考 |
| 开发工具 | 3 | 工程与参考 |
| WoW 插件与配置 | 7 | WoW |
| 历史与参考 | 8 | 工程与参考 |

## 项目清单

### AI 与工具集成

| 公开仓库 | 简介 | 类型 | 状态 |
| --- | --- | --- | --- |
| [mcp-jenkins](https://github.com/liozzazhang/mcp-jenkins) | 面向受限定 Jenkins 作业范围的 MCP 服务，提供作业与构建查询、参数化触发、控制台日志及完成轮询。 | `source` | — |
| [mcp-servicenow-chg](https://github.com/liozzazhang/mcp-servicenow-chg) | 将 ServiceNow 的变更与事件查询，以及变更和操作文档管理接入 AI 客户端的 MCP 服务。 | `source` | — |

### 平台交付与自动化

| 公开仓库 | 简介 | 类型 | 状态 |
| --- | --- | --- | --- |
| [ansible-collection-ops-pipeline](https://github.com/liozzazhang/ansible-collection-ops-pipeline) | 可扩展的 Ansible 集合，为软件包、容器及服务操作提供分阶段执行、健康检查与回滚能力。 | `source` | — |
| [rolling-update-controller](https://github.com/liozzazhang/rolling-update-controller) | 基于 Ansible 的服务软件包滚动更新控制器，整合阶段化执行、健康检查与失败恢复。 | `source` | — |
| [pg-repmgr-rolling-upgrade](https://github.com/liozzazhang/pg-repmgr-rolling-upgrade) | 面向 repmgr 管理的 PostgreSQL 集群，以 Ansible 编排操作系统与软件包滚动升级，并提供健康与复制检查。 | `source` | — |
| [airflow-etl-framework](https://github.com/liozzazhang/airflow-etl-framework) | 以类组织 Airflow ETL 流程，提供配置加载、存储适配与任务通知等通用能力。 | `source` | — |
| [https-proxy](https://github.com/liozzazhang/https-proxy) | 以声明式 YAML 生成 nginx 配置，并通过 Ansible 交付容器化 HTTPS 反向代理的工具。 | `source` | — |

### 安全与访问

| 公开仓库 | 简介 | 类型 | 状态 |
| --- | --- | --- | --- |
| [jumpserver-helper](https://github.com/liozzazhang/jumpserver-helper) | 用于 SSH 跳板机延迟探测、选择与目标别名管理的 Shell 工具集，支持生成 ProxyJump 配置。 | `source` | — |
| [py-duo](https://github.com/liozzazhang/py-duo) | 面向 Duo 等身份提供方的 Python SAML SP 客户端，提供身份校验、组与属性策略、FastAPI 适配和调试工具。 | `source` | — |

### 可观测性

| 公开仓库 | 简介 | 类型 | 状态 |
| --- | --- | --- | --- |
| [metrics-deploy](https://github.com/liozzazhang/metrics-deploy) | 使用可复用插件、配置组合与目标定义，生成、校验并通过 Ansible 部署 Telegraf 采集配置。 | `source` | — |

### 可视化与架构

| 公开仓库 | 简介 | 类型 | 状态 |
| --- | --- | --- | --- |
| [engineering-evolution](https://github.com/liozzazhang/engineering-evolution) | 以交互式图谱整理云基础设施、平台架构与 AI 工作流方向的个人工程经历。 | `visualization` | — |

### 开发工具

| 公开仓库 | 简介 | 类型 | 状态 |
| --- | --- | --- | --- |
| [pyrel](https://github.com/liozzazhang/pyrel) | 按配置构建 Python 包，并向启用的 Git、GitHub Releases 或 PyPI 目标执行发布的命令行工具。 | `source` | — |
| [set_mtu](https://github.com/liozzazhang/set_mtu) | 用于查询 Linux 网卡 MTU 状态，并进行临时与持久化设置的 Shell 工具。 | `source` | — |
| [super-dict](https://github.com/liozzazhang/super-dict) | 为 Python 嵌套字典提供点路径读取、写入、合并与展开，并支持自定义路径分隔符。 | `source` | — |

### WoW 插件与配置

| 公开仓库 | 简介 | 类型 | 状态 |
| --- | --- | --- | --- |
| [BeneUI](https://github.com/liozzazhang/BeneUI) | 为 Bene 系列组织字体、材质、配色与插件外观覆盖，并通过公开接口连接 EllesmereUI 的配置方案。 | `source` | — |
| [raid_playbook](https://github.com/liozzazhang/raid_playbook) | 把团本报名、首领时间轴与减伤任务排在开打之前，并向团员同步任务和文字语音提醒。 | `source` | — |
| [group_board](https://github.com/liozzazhang/group_board) | 基于暴雪正式服预组队列表，整合队伍搜索、条件筛选、招募申请与队友记录。 | `source` | — |
| [mplus_roadbook](https://github.com/liozzazhang/mplus_roadbook) | 收录玩家自己的 MDT 路线，逐波整理计划和标记，并在副本中通过 HUD、声音与语音展示。 | `source` | — |
| [key_skill_reminder](https://github.com/liozzazhang/key_skill_reminder) | 把可读取的敌对读条集中显示在屏幕中央，并提供本地姓名板强调与分副本外观设置。 | `source` | — |
| [self_skill_reminder](https://github.com/liozzazhang/self_skill_reminder) | 为自身增益、技能、饰品与药水设置计时和组合条件，并通过文字、语音或音效提醒。 | `source` | — |
| [wowaddones](https://github.com/liozzazhang/wowaddones) | 保留早期使用过的第三方插件与界面配置，记录个人游戏环境的历史形态。 | `collection` | `legacy` |

### 历史与参考

| 公开仓库 | 简介 | 类型 | 状态 |
| --- | --- | --- | --- |
| [CI-CD](https://github.com/liozzazhang/CI-CD) | 早期 GitLab CI/CD 流水线架构与集成说明，配有流程图和示例文档。 | `source` | `legacy` |
| [docker-builder](https://github.com/liozzazhang/docker-builder) | 早期 Docker 镜像构建示例，包含 Makefile、GitLab CI 配置及构建流程说明。 | `source` | `legacy` |
| [ecs-helper](https://github.com/liozzazhang/ecs-helper) | 已归档的早期部署辅助代码，记录基于 Consul 的服务自动部署实践。 | `source` | `legacy` · `archived` |
| [events_handler](https://github.com/liozzazhang/events_handler) | 已归档的早期个人 Python 示例仓库，提供简要运行说明，具体功能未获 README 充分说明。 | `source` | `legacy` · `archived` |
| [heketi-glusterfs-cluster](https://github.com/liozzazhang/heketi-glusterfs-cluster) | 基于 Helm 的 GlusterFS 与 Heketi 部署示例及安装文档，记录早期 Kubernetes 存储实践。 | `source` | `legacy` |
| [JARVIS](https://github.com/liozzazhang/JARVIS) | 早期个人 Python 代码仓库，README 仅标注运维管理方向，具体功能未获充分说明。 | `source` | `legacy` |
| [kubernetes-handbook](https://github.com/liozzazhang/kubernetes-handbook) | Jimmy Song 的 Kubernetes 中文参考手册 Fork，作为云原生学习资料与参考索引收藏。 | `reference` | `legacy` · `fork` |
| [message-transfer](https://github.com/liozzazhang/message-transfer) | 早期 Go 消息转发服务，支持将 Grafana 告警 Webhook 转换为企业微信机器人通知。 | `source` | `legacy` |

## 展示边界

- `engineering-evolution` 只保留通用简介与 GitHub 源码入口，不复制图表、生产指标或非公开背景。
- `kubernetes-handbook` 是 Jimmy Song 的参考手册 Fork，标为 `reference` 与 `fork`，不作为本人撰写的参考书。
- `wowaddones` 是个人插件与配置收藏，标为 `collection`；所收录第三方插件不据此归为本人开发。
- JARVIS 与 events_handler 的公开说明较少，简介维持保守范围，不从名称推断未说明的功能。
- 不复制原始敏感材料、凭据、内网地址、客户信息、实际部署参数或生产规模；公开可访问的素材也不当然具有任意再分发许可。

后续更新应先确认公开范围与展示内容，再修改项目数据并同步生成本文件；不将私有仓库加入公开目录。
