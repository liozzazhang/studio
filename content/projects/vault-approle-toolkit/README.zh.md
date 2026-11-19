# vault-approle-toolkit

通过 Vault AppRole 获取短期、最小权限凭据，并为命令行、Python 与 Ansible 提供统一的凭据生命周期管理。

## 设计关注

关注短期凭据从申请、使用到撤销的生命周期，以及命令行、Python 与 Ansible 使用同一核心逻辑时的行为一致性。
