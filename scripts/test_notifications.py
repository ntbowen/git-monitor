#!/usr/bin/env python3
"""
通知功能测试脚本
用于验证 Telegram 和微信通知配置是否正确
"""

import os
import requests
from datetime import datetime


def test_telegram():
    """测试 Telegram 通知"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("⚠️ Telegram 配置未设置")
        return False
    
    print(f"🔍 测试 Telegram 通知...")
    print(f"   Bot Token: {bot_token[:20]}...")
    print(f"   Chat ID: {chat_id}")
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        message = f"<b>🎉 测试通知</b>\n\n这是一条测试消息\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
        )
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            print("✅ Telegram 通知发送成功！")
            return True
        else:
            print(f"❌ Telegram 发送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ Telegram 发送失败: {e}")
        return False


def test_wxpusher():
    """测试微信通知 (WxPusher)"""
    app_token = os.getenv("WXPUSHER_APP_TOKEN")
    uid = os.getenv("WXPUSHER_UID")
    
    if not app_token or not uid:
        print("⚠️ WxPusher 配置未设置")
        return False
    
    print(f"🔍 测试 WxPusher 通知...")
    print(f"   App Token: {app_token[:20]}...")
    print(f"   UID: {uid}")
    
    try:
        url = "http://wxpusher.zjiecode.com/api/send/message"
        content = f"<h2>🎉 测试通知</h2><br>这是一条测试消息<br>时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        response = requests.post(
            url,
            json={
                "appToken": app_token,
                "content": content,
                "summary": "Git Monitor 测试通知",
                "contentType": 2,  # HTML
                "uids": [uid]
            }
        )
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 1000:
            print("✅ WxPusher 通知发送成功！")
            return True
        else:
            print(f"❌ WxPusher 发送失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"❌ WxPusher 发送失败: {e}")
        return False


def test_pushplus():
    """测试微信通知 (PushPlus)"""
    token = os.getenv("PUSHPLUS_TOKEN")
    
    if not token:
        print("⚠️ PushPlus 配置未设置")
        return False
    
    print(f"🔍 测试 PushPlus 通知...")
    print(f"   Token: {token[:20]}...")
    
    try:
        url = "http://www.pushplus.plus/send"
        content = f"<h2>🎉 测试通知</h2><br>这是一条测试消息<br>时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        response = requests.post(
            url,
            json={
                "token": token,
                "title": "Git Monitor 测试通知",
                "content": content,
                "template": "html"
            }
        )
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 200:
            print("✅ PushPlus 通知发送成功！")
            return True
        else:
            print(f"❌ PushPlus 发送失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"❌ PushPlus 发送失败: {e}")
        return False


def main():
    print("=" * 60)
    print("🧪 Git Monitor 通知功能测试")
    print("=" * 60)
    print()
    
    telegram_ok = test_telegram()
    print()
    wxpusher_ok = test_wxpusher()
    print()
    pushplus_ok = test_pushplus()
    
    print()
    print("=" * 60)
    if telegram_ok or wxpusher_ok or pushplus_ok:
        print("✅ 至少一个通知渠道工作正常！")
    else:
        print("❌ 所有通知渠道都失败，请检查配置")
    print("=" * 60)


if __name__ == "__main__":
    main()
