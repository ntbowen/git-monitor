# Git 仓库监控系统 - 项目说明

## 项目概述

这是一个基于 GitHub Actions 的自动化 Git 仓库监控系统，用于实时监控指定仓库的变化并发送通知。

## 核心功能

### 1. 监控能力
- ✅ **Commits 监控**：检测新的代码提交
- ✅ **Tags 监控**：检测新的标签创建
- ✅ **Releases 监控**：检测新版本发布
- ✅ **多仓库支持**：同时监控多个仓库

### 2. 通知渠道
- ✅ **Telegram Bot**：通过 Telegram 机器人推送消息
- ✅ **WxPusher**：通过 WxPusher 服务推送到微信
- ✅ **PushPlus**：通过 PushPlus 服务推送到微信（推荐）

### 3. 智能特性
- ✅ **状态持久化**：每个仓库独立状态，避免重复通知
- ✅ **自动定时执行**：支持自定义 Cron 表达式
- ✅ **手动触发**：支持随时手动检查
- ✅ **详细日志**：完整的执行日志便于调试
- ✅ **容错处理**：单个仓库失败不影响其他仓库

## 技术架构

### 技术栈
- **CI/CD**: GitHub Actions
- **语言**: Python 3.11
- **HTTP 客户端**: requests
- **API**: GitHub REST API v3

### 文件结构
```
.
├── .github/workflows/
│   └── git-monitor.yml          # GitHub Actions 工作流
├── scripts/
│   └── monitor.py               # 核心监控脚本
├── .monitor_state.json          # 状态文件（自动生成）
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git 忽略配置
├── requirements.txt             # Python 依赖
├── README.md                    # 完整使用文档
├── QUICKSTART.md                # 快速开始指南
└── PROJECT_SUMMARY.md           # 项目说明（本文件）
```

## 工作原理

### 执行流程

1. **定时触发**
   - GitHub Actions 按 Cron 表达式定时执行
   - 默认每小时执行一次
   - 支持手动触发

2. **状态加载**
   - 读取上次保存的状态文件
   - 获取上次检查的 commit/tag/release

3. **变化检测**
   - 通过 GitHub API 获取最新状态
   - 与历史状态对比，识别变化

4. **通知发送**
   - 如有新变化，格式化消息
   - 并行发送到配置的通知渠道

5. **状态保存**
   - 更新状态文件
   - 提交到 Git 仓库

### 数据流图

```
GitHub Repo → GitHub API → Monitor Script → Notification Services
                                ↓
                          State File (.json)
```

## 配置说明

### 必需配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| MONITORED_REPO | 监控的仓库 | `owner/repo` |

### 可选配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| TELEGRAM_BOT_TOKEN | Telegram Bot Token | - |
| TELEGRAM_CHAT_ID | Telegram Chat ID | - |
| WXPUSHER_APP_TOKEN | WxPusher App Token | - |
| WXPUSHER_UID | WxPusher 用户 UID | - |
| PUSHPLUS_TOKEN | PushPlus Token | - |
| GH_PAT | GitHub Personal Access Token | 可选 |
| CRON_SCHEDULE | Cron 表达式 | `0 * * * *` |

## API 限制

### GitHub API 速率限制

- **默认（自动提供的 token）**: 1000 次/小时
- **Personal Access Token**: 5000 次/小时

**说明**: Actions 自动提供的 token 通常已足够。如需更高限制，可配置 `GH_PAT`。

### Telegram API
- 无严格限制
- 建议不超过 30 条/秒

### WxPusher API
- 免费版：1000 条/天
- 单次最多推送 1000 个 UID

## 安全性

### Secrets 管理
- 所有敏感信息存储在 GitHub Secrets 中
- 不会暴露在代码或日志中
- 使用 GitHub 的加密存储

### 权限要求
- **监控公开仓库**: 使用默认权限即可
- **监控私有仓库**: 需要配置具有 `repo` 权限的 `GH_PAT`
- **写入状态文件**: Actions 自动提供的 token

## 扩展性

### 添加新的监控目标

在 `monitor.py` 中的 `GitHubMonitor` 类添加新方法：

```python
def get_latest_issue(self) -> Optional[Dict]:
    """获取最新的 issue"""
    # 实现逻辑
    pass
```

### 添加新的通知渠道

继承 `NotificationService` 基类：

```python
class EmailNotifier(NotificationService):
    def send(self, title: str, content: str, url: Optional[str] = None) -> bool:
        # 实现邮件发送
        pass
```

### 支持多仓库监控

修改配置解析，支持仓库列表：

```python
repos = os.getenv("MONITORED_REPOS", "").split(",")
for repo in repos:
    # 分别监控每个仓库
    pass
```

## 性能优化

### 当前性能
- 单次执行时间: ~5-10 秒
- API 调用次数: 3 次（commit + tag + release）
- 网络流量: < 100KB

### 优化建议
1. 使用 GraphQL API 减少请求次数
2. 实现增量更新而非全量检查
3. 使用 Redis 缓存状态（如需高频检查）
4. 批量处理多仓库监控

## 故障处理

### 常见问题

1. **API 限流**
   - 配置 GITHUB_TOKEN
   - 降低检查频率

2. **通知失败**
   - 检查 token 是否正确
   - 验证网络连接
   - 查看详细日志

3. **状态文件冲突**
   - Actions 会自动处理
   - 使用 `[skip ci]` 避免循环触发

### 错误恢复

- 脚本使用 try-except 包裹所有外部调用
- API 失败不会中断整个流程
- 状态文件损坏时自动重建

## 最佳实践

### 监控频率建议

| 仓库活跃度 | 建议频率 | Cron 表达式 |
|-----------|----------|-------------|
| 高活跃 | 30 分钟 | `*/30 * * * *` |
| 中活跃 | 1-2 小时 | `0 */2 * * *` |
| 低活跃 | 6-12 小时 | `0 */6 * * *` |
| 归档项目 | 每天 | `0 0 * * *` |

### 通知内容建议

- **Commit**: 适合开发团队日常跟踪
- **Tag**: 适合版本管理和发布跟踪
- **Release**: 适合用户和下游项目关注

### 资源使用

- Actions 免费额度: 2000 分钟/月（公开仓库无限）
- 单次执行: ~0.5 分钟
- 月度消耗: 360 分钟（每小时一次）

## 未来改进

### 计划功能

- [ ] 支持 GitLab、Gitea 等其他 Git 平台
- [ ] Web Dashboard 查看历史通知
- [ ] 自定义过滤规则（如仅监控特定分支）
- [ ] 更丰富的通知格式（Markdown、HTML）
- [ ] 多仓库统一管理界面
- [ ] Webhook 触发（实时监控）
- [ ] 邮件通知支持
- [ ] 钉钉、飞书等企业通知渠道

### 贡献方式

欢迎提交：
- Bug 报告
- 功能建议
- Pull Request
- 文档改进

## 许可证

MIT License - 自由使用、修改和分发

## 联系方式

- Issues: GitHub Issues
- Discussions: GitHub Discussions

---

**最后更新**: 2024-10-26
**版本**: 1.0.0
