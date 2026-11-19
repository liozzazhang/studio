# dns-eyes

DNS Eyes 分布式 DNS 保障平台的个人仓库。

项目状态：工作版本已交付；个人仓库仅完成初始化，暂无代码。

## 工作中的 DNS Eyes

在 Cisco 主导开发的 DNS Eyes，将分布式探针与 Infoblox 检查组织为可重复执行的验证矩阵，并承接 DNS Server 的生命周期：

- 检查 Agent 覆盖 20 个数据中心，支持 NS/ENS、Anycast/BGP、服务状态、多类型 DNS 记录及 UDP/TCP 检查。
- 以 Check/Context/Result、Agent、Target 和 Runner 分离检查规则、执行方式、目标发现与编排，以 YAML 组合验证矩阵，CLI 与门户共用。
- 预检失败保留目标证据，结果从检查逐层汇总到角色、数据中心和全局视图；调度器以站点运行锁与并发信号量约束任务。
- 门户采用 FastAPI、SQLite、SAML SSO 与集中模块权限；支持 DNS Server Build/Destroy，把验证前移到变更与上线准备。

## 本仓库

工作版本的源码属于 Cisco 内部项目，不在此公开。本仓库用于个人整理同类设计，核对时尚未包含实现。
