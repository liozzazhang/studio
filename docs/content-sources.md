# 内容来源与公开范围

核对日期：**2026-11-19（Asia/Shanghai）**。

**当前阶段：页面已完成，发布状态以 GitHub Actions/Pages 为准。** 本文件记录内容来源与展示边界，不作为网站已经上线的证明。

## 公开目录快照

项目目录的单一数据源为 [data/projects.json](../data/projects.json)，保存本次核对的 **29 个公开仓库**，不含 `studio` 自身及任何私有仓库。目录不随实时仓库变化自动增删；新增内容需要再次确认公开范围后更新数据。

该数据生成 `/studio/projects/` 的 29 项总目录、`/studio/lab/` 的 22 项工程与参考目录、`/studio/wow/` 的 7 项 WoW 目录，以及导航首页和个人页的精选公开项目区。八个分类及每个仓库的公开 URL、简介、类型和状态见 [project-catalog.md](project-catalog.md)。

项目简介依据无凭证可访问的公开 GitHub 元数据、README 与必要的仓库目录核对。未执行项目代码、连接目标服务或验证部署；源码、可视化、参考资料和配置收藏各自标注，历史内容、归档状态与 Fork 标记分别保留。公开目录不是可直接在 GitHub Pages 中运行这些项目的应用集合。

## 个人资料与职业摘要

- [GitHub 主页](https://github.com/liozzazhang)
- [公开 Profile API](https://api.github.com/users/liozzazhang)
- [公开仓库 API](https://api.github.com/users/liozzazhang/repos?per_page=100)

个人页采用的公开身份信息包括显示名 `Liozza Zhang`、简介 `Security SRE`、公司 `Cisco` 和地点 `China`。Profile 的公开邮箱与个人网站字段为空；联系入口使用 GitHub，不加入来自认证连接或私有资料的邮箱。

职业介绍与匿名高层案例根据用户此前提供并确认的履历事实概括，仅保留通用职责、个人贡献和工程方法。原始履历、聊天导出、内部文档、原始工具返回及其附件路径不复制到本仓库，也不公开内部项目名称、客户、地址、规模、成功率、拓扑或操作参数。

“理性、自驱”“关注长期演进”等描述来自用户自述，不扩写为预测准确度、未经确认的业绩或雇主背书。个人页中的抽象示意图不作为真实生产环境截图或运行状态展示。

## 工程项目的功能范围

公开 README 的描述用于确定功能范围，不自动构成已验证的运行保证。例如：

- `py-duo` 介绍 SAML 身份校验与策略能力，不扩写为完整会话或身份平台。
- `mcp-jenkins` 保留受限作业范围，不推定可操作任意 Jenkins 作业。
- `mcp-servicenow-chg` 按文档区分查询与管理能力，不把事件查询扩写为完整事件管理。
- 历史工具和早期架构资料不作为当前版本部署教程；公开说明较少的仓库采用保守简介。

第三方软件与商标仍归各自权利人。未标记 Fork 不等于全部内容原创；公开可访问也不等于可以任意复制和再分发素材。

## Bene 系列与 WoW 收藏

Bene 系列依据已公开仓库的 README 与结构介绍功能，并提供**公开源码**入口。不声称插件已上架、完成运行验证或已确认适配当前游戏版本，也不把公开源码卡片作为在线游戏应用。

本次**未镜像含玩家信息的截图**，未复制个人账号或角色配置、第三方字体与插件纹理。个人页中的抽象游戏界面为独立绘制的示意图，不是游戏截图或插件运行截图。

[wowaddones](https://github.com/liozzazhang/wowaddones) 单独标记为历史插件与配置收藏。其收录的 ElvUI、WeakAuras、AngryKeystones 等具有第三方作者，不将这些插件归为用户本人开发。

## 可视化与参考归属

[engineering-evolution](https://github.com/liozzazhang/engineering-evolution) 只展示通用简介与 GitHub 源码入口；本次**未镜像其原图**，未复制图中的内部名称、生产指标或详细内容。

[kubernetes-handbook](https://github.com/liozzazhang/kubernetes-handbook) 是 Jimmy Song 参考手册的 Fork，按参考资料展示，并保留 `fork` 标记，不作为用户本人撰写的书籍。

## 持续维护

内容调整先更新公开数据与相应模板，再运行 `python3 scripts/build_catalog.py` 生成页面，并使用本地预览核对。项目目录生成过程不需要获取私有仓库，也不会把原始履历导入网站。

本文件、目录数据及其余已提交材料均属于公开仓库内容。后续加入图片、附件或其他素材时，需先确认可以公开、移除个人与非公开信息，并核对第三方授权和署名要求；不将设计图、计划功能或目标访问地址表述为已上线结果。
