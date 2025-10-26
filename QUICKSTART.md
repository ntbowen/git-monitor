# 快速开始指南 🚀

5 分钟内启动 Git 仓库监控！

## 第一步：配置 Secrets

进入你的 GitHub 仓库页面：

```
Settings → Secrets and variables → Actions → New repository secret
```

### 最小配置（必需）

添加一个 secret：

- **Name**: `MONITORED_REPO`
- **Secret**: `torvalds/linux` （替换为你要监控的仓库）

### Telegram 配置（推荐）

添加两个 secrets：

1. **TELEGRAM_BOT_TOKEN**
   - 打开 Telegram，搜索 `@BotFather`
   - 发送 `/newbot` 并按提示操作
   - 复制获得的 token

2. **TELEGRAM_CHAT_ID**
   - 在 Telegram 搜索 `@userinfobot`
   - 发送任意消息，获取你的 ID
   - 复制那个数字 ID

### 微信配置（可选）

添加两个 secrets：

1. **WXPUSHER_APP_TOKEN**
   - 访问 http://wxpusher.zjiecode.com/admin/
   - 注册并创建应用
   - 复制 APP_TOKEN

2. **WXPUSHER_UID**
   - 微信扫码关注 WxPusher 公众号
   - 点击"我的" → "我的UID"
   - 复制 UID

## 第二步：启用工作流

1. 点击仓库的 **Actions** 标签
2. 点击绿色按钮 "I understand my workflows, go ahead and enable them"
3. 找到 "Git Repository Monitor"
4. 点击 "Enable workflow"

## 第三步：测试运行

1. 在 Actions 页面，点击 "Git Repository Monitor"
2. 点击 "Run workflow" 下拉菜单
3. 点击绿色的 "Run workflow" 按钮
4. 等待 30 秒左右
5. 点击运行记录查看日志

## 完成！

✅ 现在监控已经启动，会自动每小时检查一次

✅ 有新的 commit/tag/release 时会自动发送通知

## 可选配置

### 修改检查频率

添加 `CRON_SCHEDULE` secret：

- 每 30 分钟: `*/30 * * * *`
- 每 2 小时: `0 */2 * * *`
- 每 6 小时: `0 */6 * * *`
- 每天一次: `0 0 * * *`

### 提高 API 限制

添加 `GITHUB_TOKEN` secret：

1. GitHub 头像 → Settings
2. Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token
4. 勾选 `public_repo`
5. 复制生成的 token

## 常见问题

**Q: 为什么首次运行没收到通知？**

A: 首次运行只会记录当前状态，不会发送通知。等下次有新变化时才会通知。

**Q: 如何查看运行日志？**

A: Actions → Git Repository Monitor → 点击具体的运行记录 → monitor 任务

**Q: 如何手动触发？**

A: Actions → Git Repository Monitor → Run workflow → Run workflow

## 需要帮助？

查看完整文档：[README.md](README.md)
