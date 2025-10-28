# Git Repository Monitor 📡

自动监控指定 Git 仓库的变化（commits, tags, releases），并通过 Telegram 和微信（WxPusher）发送通知。

## 功能特性

- ✅ 监控新的 commits
- ✅ 监控新的 tags
- ✅ 监控新的 releases
- ✅ Telegram Bot 通知
- ✅ 微信通知（通过 WxPusher）
- ✅ 自动定时检查
- ✅ 状态持久化，避免重复通知

## 快速开始

### 1. Fork 或克隆此仓库

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. 配置 GitHub Variables 和 Secrets

进入仓库的 **Settings → Secrets and variables → Actions**

#### 📋 Variables（非敏感信息）- 推荐

在 **Variables** 标签页添加：

| Variable 名称 | 说明 | 示例 |
|------------|------|------|
| `MONITORED_REPOS` | 要监控的仓库列表（多个仓库用逗号分隔） | `torvalds/linux,microsoft/vscode` |
| `MONITORED_REPO` | 单个仓库监控（向后兼容） | `torvalds/linux` |
| `MONITOR_COMMITS` | 是否监控 commits（可选） | `true` / `false` |
| `MONITOR_TAGS` | 是否监控 tags（可选） | `true` / `false` |
| `MONITOR_RELEASES` | 是否监控 releases（可选） | `true` / `false` |

**优势：**
- ✅ 可直接查看和编辑，无需重新输入
- ✅ 非敏感信息无需加密
- ✅ 更方便管理

**说明：**
- 优先使用 `MONITORED_REPOS` 支持多仓库监控
- 多个仓库用英文逗号分隔，如：`owner1/repo1,owner2/repo2,owner3/repo3`
- 监控内容配置默认全部启用（`true`），可设置为 `false` 禁用
- 支持灵活组合，如：只监控 tags 和 releases，不监控 commits

**监控内容配置示例：**
```
# 只监控 releases
MONITOR_COMMITS=false
MONITOR_TAGS=false
MONITOR_RELEASES=true

# 只监控 tags 和 releases
MONITOR_COMMITS=false
MONITOR_TAGS=true
MONITOR_RELEASES=true
```

#### 🔐 Secrets（敏感信息）

在 **Secrets** 标签页添加以下通知服务配置（至少选择一个）：

##### Telegram 配置（可选）

| Secret 名称 | 说明 | 获取方式 |
|------------|------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 与 @BotFather 对话创建 bot |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 发送消息给 @userinfobot 获取 |

**获取 Telegram 配置步骤：**

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 创建新 bot
3. 按提示设置 bot 名称和用户名
4. 获得 Bot Token（格式：`1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ`）
5. 搜索 `@userinfobot`，发送任意消息获取你的 Chat ID

##### 微信配置（可选，选择其中一个或多个）

**方案1：WxPusher**

| Secret 名称 | 说明 | 获取方式 |
|------------|------|---------|
| `WXPUSHER_APP_TOKEN` | WxPusher 应用Token | [WxPusher官网](http://wxpusher.zjiecode.com) 注册并创建应用 |
| `WXPUSHER_UID` | WxPusher 用户UID | 关注 WxPusher 公众号后在"我的"-"我的UID"中查看 |

**获取 WxPusher 配置步骤：**

1. 访问 [WxPusher 官网](http://wxpusher.zjiecode.com/admin/)
2. 注册账号并登录
3. 创建应用，获取 `APP_TOKEN`
4. 微信扫码关注 WxPusher 公众号
5. 在公众号中点击"我的" → "我的UID"获取 `UID`

**方案2：PushPlus（推荐，更简单）**

| Secret 名称 | 说明 | 获取方式 |
|------------|------|---------|
| `PUSHPLUS_TOKEN` | PushPlus Token | [PushPlus官网](http://www.pushplus.plus) 注册并获取Token |

**获取 PushPlus 配置步骤：**

1. 访问 [PushPlus 官网](http://www.pushplus.plus)
2. 使用微信扫码登录
3. 在"发送消息"页面找到你的 `Token`
4. 复制 Token 即可使用

##### 高级配置（可选）

| Secret 名称 | 说明 | 用途 |
|------------|------|------|
| `GH_PAT` | GitHub Personal Access Token | 提高 API 限制或访问私有仓库 |

**何时需要配置 GH_PAT：**
- 需要更高 API 限制（默认1000次/小时，PAT 可达5000次/小时）
- 监控私有仓库（需要 `repo` 权限）

**获取步骤：**
1. GitHub 头像 → Settings → Developer settings
2. Personal access tokens → Tokens (classic) → Generate new token
3. 权限：`public_repo`（私有仓库需要 `repo`）
4. 在 Secrets 中添加名为 `GH_PAT` 的 secret

⚠️ **注意**：Secret 名称不能以 `GITHUB_` 开头

### 3. 启用 GitHub Actions

1. 进入仓库的 **Actions** 标签
2. 点击 "I understand my workflows, go ahead and enable them"
3. 找到 "Git Repository Monitor" workflow
4. 点击 "Enable workflow"

### 4. 手动触发测试

1. 在 Actions 页面，点击左侧的 "Git Repository Monitor"
2. 点击右上角的 "Run workflow"
3. 点击绿色的 "Run workflow" 按钮
4. 等待运行完成，检查是否收到通知

## 工作流程

```mermaid
graph LR
    A[定时触发] --> B[检查仓库]
    B --> C{有新变化?}
    C -->|是| D[发送通知]
    C -->|否| E[记录状态]
    D --> E
    E --> F[保存状态]
```

1. **定时检查**：按照配置的 Cron 表达式定时运行
2. **获取最新状态**：通过 GitHub API 获取最新的 commit、tag、release
3. **对比状态**：与上次保存的状态对比，检测变化
4. **发送通知**：如有新变化，发送到配置的通知渠道
5. **保存状态**：更新状态文件，避免重复通知

## 本地测试

### 前置要求

- Python 3.8+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置环境变量

```bash
# 必需 - 支持多仓库（逗号分隔）
export MONITORED_REPOS="owner1/repo1,owner2/repo2"
# 或单个仓库
# export MONITORED_REPO="owner/repo"

# 可选：Telegram
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# 可选：微信（三选一或多选）
export WXPUSHER_APP_TOKEN="your_app_token"
export WXPUSHER_UID="your_uid"
export PUSHPLUS_TOKEN="your_pushplus_token"

# 可选：GitHub PAT（提高 API 限制或访问私有仓库）
# 注意：本地测试时环境变量名为 GITHUB_TOKEN
# 但在 GitHub Secrets 中必须使用 GH_PAT（不能以 GITHUB_ 开头）
export GITHUB_TOKEN="your_github_pat"
```

### 运行脚本

```bash
python scripts/monitor.py
```

## 文件结构

```
.
├── .github/
│   └── workflows/
│       └── git-monitor.yml    # GitHub Actions 工作流配置
├── scripts/
│   └── monitor.py             # 核心监控脚本
├── .gitignore                 # Git 忽略文件
├── .monitor_state.json        # 状态文件（自动生成）
├── requirements.txt           # Python 依赖
└── README.md                  # 使用文档
```

## 通知格式

### Commit 通知
```
📝 owner/repo 新提交

Commit: abc1234
作者: John Doe
消息: Fix bug in login function
时间: 2024-01-01T12:00:00Z

🔗 查看详情
```

### Tag 通知
```
🏷️ owner/repo 新标签

标签: v1.2.0
Commit: def5678

🔗 查看详情
```

### Release 通知
```
🚀 owner/repo 新版本发布

版本: Version 1.2.0
标签: v1.2.0
发布时间: 2024-01-01T12:00:00Z

说明:
- Added new feature X
- Fixed bug Y
...

🔗 查看详情
```

## 常见问题

### Q: 为什么没有收到通知？

**A:** 请检查：
1. Secrets 是否正确配置
2. GitHub Actions 是否启用
3. 查看 Actions 运行日志，确认是否有错误
4. 确认监控的仓库是否有新变化
5. 首次运行不会发送通知（只记录初始状态）

### Q: 如何修改检查频率？

**A:** 需要直接编辑工作流文件：

1. 编辑 `.github/workflows/git-monitor.yml`
2. 修改第6行的 `cron` 值：
   ```yaml
   schedule:
     - cron: '0 */6 * * *'  # 修改这里
   ```
3. 提交并推送更改

**常用间隔：**
- 每小时：`0 * * * *`
- 每2小时：`0 */2 * * *`
- 每6小时：`0 */6 * * *`
- 每12小时：`0 */12 * * *`
- 每天：`0 0 * * *`

⚠️ **注意：** GitHub Actions 的 `schedule` 触发器不支持使用变量，必须硬编码在工作流文件中。

### Q: API 限流怎么办？

**A:** 
- 自动提供的 token：每小时 1000 次（足够使用）
- Personal Access Token：每小时 5000 次

**如需更高限制，可配置 `GH_PAT`：**
1. GitHub 头像 → Settings → Developer settings
2. Personal access tokens → Tokens (classic) → Generate new token
3. 权限：`public_repo`（私有仓库需要 `repo`）
4. 在仓库 Secrets 中添加名为 `GH_PAT` 的 secret（不能使用 `GITHUB_` 前缀）

### Q: 能监控私有仓库吗？

**A:** 可以。需要：
1. 创建具有 `repo` 权限的 GitHub Personal Access Token
2. 在 Secrets 中添加 `GH_PAT`（注意：不能使用 `GITHUB_` 前缀）

### Q: 如何监控多个仓库？

**A:** 支持同时监控多个仓库：
1. 在 Secrets 中设置 `MONITORED_REPOS`（多个仓库用逗号分隔）
2. 示例：`torvalds/linux,microsoft/vscode,golang/go`
3. 每个仓库的状态独立管理，互不影响

### Q: 状态文件是什么？

**A:** `.monitor_state.json` 保存上次检查的状态（最新的 commit、tag、release）。工作流会自动提交这个文件，以便下次运行时对比变化。

## 进阶配置

### 自定义通知格式

编辑 `scripts/monitor.py` 中的格式化函数：
- `format_commit_message()`
- `format_tag_message()`
- `format_release_message()`

### 添加其他通知渠道

在 `scripts/monitor.py` 中继承 `NotificationService` 类实现新的通知器：

```python
class MyNotifier(NotificationService):
    def send(self, title: str, content: str, url: Optional[str] = None) -> bool:
        # 实现你的通知逻辑
        pass
```

### 监控特定分支

修改 `GitHubMonitor.get_latest_commit()` 方法，在 API 请求中添加 `sha` 参数：

```python
params = {"per_page": 1, "sha": "your-branch-name"}
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [GitHub API 文档](https://docs.github.com/en/rest)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [WxPusher 文档](http://wxpusher.zjiecode.com/docs)

---

**Star ⭐ 如果觉得有用！**
