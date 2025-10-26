#!/usr/bin/env python3
"""
Git Repository Monitor
监控指定 Git 仓库的变化（commits, tags, releases）并发送通知
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class StateManager:
    """管理监控状态的持久化"""
    
    def __init__(self, state_file: str = ".monitor_state.json"):
        self.state_file = Path(state_file)
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """加载状态文件"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 加载状态文件失败: {e}")
        return {
            "last_commit": None,
            "last_tag": None,
            "last_release": None,
            "last_check": None
        }
    
    def save_state(self):
        """保存状态到文件"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
            print(f"✓ 状态已保存")
        except Exception as e:
            print(f"⚠️ 保存状态失败: {e}")
    
    def update(self, key: str, value):
        """更新状态"""
        self.state[key] = value
        self.state["last_check"] = datetime.now().isoformat()


class GitHubMonitor:
    """GitHub 仓库监控器"""
    
    def __init__(self, repo: str, token: Optional[str] = None):
        self.repo = repo  # 格式: owner/repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def get_latest_commit(self) -> Optional[Dict]:
        """获取最新的 commit"""
        try:
            url = f"{self.base_url}/repos/{self.repo}/commits"
            response = requests.get(url, headers=self.headers, params={"per_page": 1})
            response.raise_for_status()
            commits = response.json()
            if commits:
                commit = commits[0]
                return {
                    "sha": commit["sha"][:7],
                    "message": commit["commit"]["message"].split('\n')[0],
                    "author": commit["commit"]["author"]["name"],
                    "date": commit["commit"]["author"]["date"],
                    "url": commit["html_url"]
                }
        except Exception as e:
            print(f"⚠️ 获取 commit 失败: {e}")
        return None
    
    def get_latest_tag(self) -> Optional[Dict]:
        """获取最新的 tag"""
        try:
            url = f"{self.base_url}/repos/{self.repo}/tags"
            response = requests.get(url, headers=self.headers, params={"per_page": 1})
            response.raise_for_status()
            tags = response.json()
            if tags:
                tag = tags[0]
                return {
                    "name": tag["name"],
                    "sha": tag["commit"]["sha"][:7],
                    "url": f"https://github.com/{self.repo}/releases/tag/{tag['name']}"
                }
        except Exception as e:
            print(f"⚠️ 获取 tag 失败: {e}")
        return None
    
    def get_latest_release(self) -> Optional[Dict]:
        """获取最新的 release"""
        try:
            url = f"{self.base_url}/repos/{self.repo}/releases/latest"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 404:
                return None  # 没有 release
            response.raise_for_status()
            release = response.json()
            return {
                "tag": release["tag_name"],
                "name": release["name"] or release["tag_name"],
                "published_at": release["published_at"],
                "url": release["html_url"],
                "body": release["body"][:200] if release.get("body") else ""
            }
        except Exception as e:
            print(f"⚠️ 获取 release 失败: {e}")
        return None


class NotificationService:
    """通知服务基类"""
    
    def send(self, title: str, content: str, url: Optional[str] = None) -> bool:
        raise NotImplementedError


class TelegramNotifier(NotificationService):
    """Telegram 通知服务"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send(self, title: str, content: str, url: Optional[str] = None) -> bool:
        """发送 Telegram 消息"""
        try:
            message = f"<b>{title}</b>\n\n{content}"
            if url:
                message += f"\n\n🔗 <a href='{url}'>查看详情</a>"
            
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False
                }
            )
            response.raise_for_status()
            print(f"✓ Telegram 通知已发送")
            return True
        except Exception as e:
            print(f"⚠️ Telegram 发送失败: {e}")
            return False


class WxPusherNotifier(NotificationService):
    """WxPusher 微信通知服务"""
    
    def __init__(self, app_token: str, uid: str):
        self.app_token = app_token
        self.uid = uid
        self.base_url = "http://wxpusher.zjiecode.com/api/send/message"
    
    def send(self, title: str, content: str, url: Optional[str] = None) -> bool:
        """发送微信消息"""
        try:
            # 格式化为 HTML
            html_content = content.replace('\n', '<br>')
            if url:
                html_content += f'<br><br><a href="{url}">🔗 查看详情</a>'
            
            response = requests.post(
                self.base_url,
                json={
                    "appToken": self.app_token,
                    "content": html_content,
                    "summary": title,
                    "contentType": 2,  # HTML
                    "uids": [self.uid]
                }
            )
            response.raise_for_status()
            result = response.json()
            if result.get("code") == 1000:
                print(f"✓ 微信通知已发送")
                return True
            else:
                print(f"⚠️ 微信发送失败: {result.get('msg')}")
                return False
        except Exception as e:
            print(f"⚠️ 微信发送失败: {e}")
            return False


class PushPlusNotifier(NotificationService):
    """PushPlus 微信通知服务"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "http://www.pushplus.plus/send"
    
    def send(self, title: str, content: str, url: Optional[str] = None) -> bool:
        """发送微信消息"""
        try:
            # 格式化为 HTML
            html_content = content.replace('\n', '<br>')
            if url:
                html_content += f'<br><br><a href="{url}">🔗 查看详情</a>'
            
            response = requests.post(
                self.base_url,
                json={
                    "token": self.token,
                    "title": title,
                    "content": html_content,
                    "template": "html"
                }
            )
            response.raise_for_status()
            result = response.json()
            if result.get("code") == 200:
                print(f"✓ PushPlus 通知已发送")
                return True
            else:
                print(f"⚠️ PushPlus 发送失败: {result.get('msg')}")
                return False
        except Exception as e:
            print(f"⚠️ PushPlus 发送失败: {e}")
            return False


def format_commit_message(commit: Dict, repo: str) -> tuple:
    """格式化 commit 消息"""
    title = f"📝 {repo} 新提交"
    content = (
        f"Commit: {commit['sha']}\n"
        f"作者: {commit['author']}\n"
        f"消息: {commit['message']}\n"
        f"时间: {commit['date']}"
    )
    return title, content, commit['url']


def format_tag_message(tag: Dict, repo: str) -> tuple:
    """格式化 tag 消息"""
    title = f"🏷️ {repo} 新标签"
    content = (
        f"标签: {tag['name']}\n"
        f"Commit: {tag['sha']}"
    )
    return title, content, tag['url']


def format_release_message(release: Dict, repo: str) -> tuple:
    """格式化 release 消息"""
    title = f"🚀 {repo} 新版本发布"
    content = (
        f"版本: {release['name']}\n"
        f"标签: {release['tag']}\n"
        f"发布时间: {release['published_at']}\n"
    )
    if release['body']:
        content += f"\n说明:\n{release['body']}..."
    return title, content, release['url']


def main():
    """主函数"""
    print("=" * 60)
    print("🔍 Git Repository Monitor 启动")
    print("=" * 60)
    
    # 获取配置
    repo = os.getenv("MONITORED_REPO")
    if not repo:
        print("❌ 错误: 未设置 MONITORED_REPO")
        return
    
    github_token = os.getenv("GITHUB_TOKEN")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    wxpusher_token = os.getenv("WXPUSHER_APP_TOKEN")
    wxpusher_uid = os.getenv("WXPUSHER_UID")
    pushplus_token = os.getenv("PUSHPLUS_TOKEN")
    
    print(f"📦 监控仓库: {repo}")
    
    # 初始化服务
    state_mgr = StateManager()
    monitor = GitHubMonitor(repo, github_token)
    notifiers = []
    
    if telegram_token and telegram_chat_id:
        notifiers.append(TelegramNotifier(telegram_token, telegram_chat_id))
        print("✓ Telegram 通知已启用")
    
    if wxpusher_token and wxpusher_uid:
        notifiers.append(WxPusherNotifier(wxpusher_token, wxpusher_uid))
        print("✓ WxPusher 通知已启用")
    
    if pushplus_token:
        notifiers.append(PushPlusNotifier(pushplus_token))
        print("✓ PushPlus 通知已启用")
    
    if not notifiers:
        print("⚠️ 警告: 未配置任何通知服务")
    
    print("-" * 60)
    
    # 检查 commits
    print("🔍 检查最新 commit...")
    latest_commit = monitor.get_latest_commit()
    if latest_commit:
        if state_mgr.state["last_commit"] != latest_commit["sha"]:
            if state_mgr.state["last_commit"] is not None:  # 不是首次运行
                print(f"✨ 发现新 commit: {latest_commit['sha']}")
                title, content, url = format_commit_message(latest_commit, repo)
                for notifier in notifiers:
                    notifier.send(title, content, url)
            else:
                print(f"📌 初始 commit: {latest_commit['sha']}")
            state_mgr.update("last_commit", latest_commit["sha"])
        else:
            print("  无新 commit")
    
    # 检查 tags
    print("🔍 检查最新 tag...")
    latest_tag = monitor.get_latest_tag()
    if latest_tag:
        if state_mgr.state["last_tag"] != latest_tag["name"]:
            if state_mgr.state["last_tag"] is not None:
                print(f"✨ 发现新 tag: {latest_tag['name']}")
                title, content, url = format_tag_message(latest_tag, repo)
                for notifier in notifiers:
                    notifier.send(title, content, url)
            else:
                print(f"📌 初始 tag: {latest_tag['name']}")
            state_mgr.update("last_tag", latest_tag["name"])
        else:
            print("  无新 tag")
    
    # 检查 releases
    print("🔍 检查最新 release...")
    latest_release = monitor.get_latest_release()
    if latest_release:
        if state_mgr.state["last_release"] != latest_release["tag"]:
            if state_mgr.state["last_release"] is not None:
                print(f"✨ 发现新 release: {latest_release['name']}")
                title, content, url = format_release_message(latest_release, repo)
                for notifier in notifiers:
                    notifier.send(title, content, url)
            else:
                print(f"📌 初始 release: {latest_release['name']}")
            state_mgr.update("last_release", latest_release["tag"])
        else:
            print("  无新 release")
    
    # 保存状态
    state_mgr.save_state()
    
    print("-" * 60)
    print(f"✅ 监控完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
