# 配置检查清单 ✓

在启动监控前，请按此清单逐项检查。

## 📋 GitHub Variables 配置（非敏感信息）

路径：Settings → Secrets and variables → Actions → **Variables** 标签页

### 必需项

- [ ] **MONITORED_REPOS** 或 **MONITORED_REPO** 已配置
  - **多仓库**：`MONITORED_REPOS=owner1/repo1,owner2/repo2`
  - **单仓库**：`MONITORED_REPO=owner/repo`
  - 💡 使用 Variable 可以随时查看和编辑

### 可选项

- [ ] **CRON_SCHEDULE** 已配置（自定义检查频率）
  - 默认：`0 * * * *`（每小时）
  - 示例：`0 */6 * * *`（每6小时）

## 🔐 GitHub Secrets 配置（敏感信息）

路径：Settings → Secrets and variables → Actions → **Secrets** 标签页

### Telegram 配置（二选一或全选）

- [ ] **TELEGRAM_BOT_TOKEN** 已配置
  - 从 @BotFather 获取
  - 格式：`1234567890:ABCdef...`

- [ ] **TELEGRAM_CHAT_ID** 已配置
  - 从 @userinfobot 获取
  - 格式：数字 ID（如 `123456789`）

### 微信配置（三选一或全选）

- [ ] **WXPUSHER_APP_TOKEN** 已配置
  - 从 wxpusher.zjiecode.com 获取
  - 格式：`AT_...`

- [ ] **WXPUSHER_UID** 已配置
  - 从微信公众号获取
  - 格式：`UID_...`

- [ ] **PUSHPLUS_TOKEN** 已配置（推荐）
  - 从 www.pushplus.plus 获取
  - 格式：Token 字符串

### 高级配置（可选）

- [ ] **GH_PAT** 已配置（提高 API 限制或访问私有仓库）
  - 从 GitHub Settings → Developer settings 创建 Personal Access Token
  - 权限：`public_repo`（公开仓库）或 `repo`（私有仓库）
  - ⚠️ 注意：Secret 名称不能以 `GITHUB_` 开头，使用 `GH_PAT`
  - 默认提供的 token（1000次/小时）通常已足够

## 🔧 GitHub Actions 配置

- [ ] 已 fork 或克隆本仓库
- [ ] 已启用 GitHub Actions
  - Actions 标签 → Enable workflows
- [ ] 工作流文件存在
  - `.github/workflows/git-monitor.yml`

## ✅ 功能验证

- [ ] 已手动触发一次测试运行
  - Actions → Git Repository Monitor → Run workflow
- [ ] 检查运行日志无报错
  - 点击具体运行记录查看
- [ ] （如配置了通知）已收到测试通知
  - 首次运行不发通知，等第二次运行或有新变化时才发

## 🎯 最终确认

- [ ] 监控的仓库地址正确
- [ ] 至少配置了一种通知方式
- [ ] 理解首次运行不会发送通知（只记录状态）
- [ ] 知道如何查看运行日志
- [ ] 知道如何手动触发检查

## 📝 Cron 表达式参考

选择适合你的检查频率：

| 频率 | Cron 表达式 | 说明 |
|------|------------|------|
| 每 15 分钟 | `*/15 * * * *` | 高频监控 |
| 每 30 分钟 | `*/30 * * * *` | 活跃仓库 |
| 每 1 小时 | `0 * * * *` | 默认值 |
| 每 2 小时 | `0 */2 * * *` | 中等活跃 |
| 每 6 小时 | `0 */6 * * *` | 低频监控 |
| 每 12 小时 | `0 */12 * * *` | 归档项目 |
| 每天 00:00 | `0 0 * * *` | 每日汇总 |
| 工作日 09:00 | `0 9 * * 1-5` | 工作时间 |

## 🔍 故障排查

如遇问题，请按以下步骤检查：

1. **查看 Actions 日志**
   - Actions → Git Repository Monitor → 点击具体运行
   - 查看 "Run monitor script" 步骤的输出

2. **验证 Secrets 配置**
   - 确保名称完全正确（区分大小写）
   - 确保值没有多余空格

3. **检查 API 限制**
   - 默认限制：每小时 1000 次（足够使用）
   - 如需更高限制，配置 GH_PAT
   - 或降低检查频率

4. **测试通知服务**
   - Telegram：发送测试消息给 bot
   - 微信：检查 WxPusher/PushPlus 配置

5. **查看仓库权限**
   - 公开仓库：无需额外配置
   - 私有仓库：必须配置有 `repo` 权限的 `GH_PAT`

## 🎉 完成！

当所有项目都打勾后，你的监控系统就配置完成了！

**下一步**：等待定时任务自动运行，或手动触发一次测试。

---

有问题？查看 [README.md](README.md) 或 [QUICKSTART.md](QUICKSTART.md)
