#!/usr/bin/env python3
"""
状态文件诊断工具
用于检查监控状态和诊断问题
"""

import json
from pathlib import Path
from datetime import datetime

def main():
    state_file = Path(".monitor_state.json")
    
    print("=" * 60)
    print("🔍 监控状态诊断工具")
    print("=" * 60)
    
    if not state_file.exists():
        print("\n❌ 状态文件不存在")
        print("   这可能是首次运行，或状态文件被删除")
        return
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except Exception as e:
        print(f"\n❌ 读取状态文件失败: {e}")
        return
    
    if not state:
        print("\n⚠️ 状态文件为空")
        return
    
    print(f"\n📊 监控仓库数量: {len(state)}")
    print("\n" + "=" * 60)
    
    for i, (repo, repo_state) in enumerate(sorted(state.items()), 1):
        print(f"\n{i}. {repo}")
        print("-" * 60)
        
        last_commit = repo_state.get("last_commit")
        last_tag = repo_state.get("last_tag")
        last_release = repo_state.get("last_release")
        last_check = repo_state.get("last_check")
        
        if last_commit:
            print(f"   Last Commit:  {last_commit[:8]}...")
        else:
            print(f"   Last Commit:  (未记录)")
        
        if last_tag:
            print(f"   Last Tag:     {last_tag}")
        else:
            print(f"   Last Tag:     (未记录)")
        
        if last_release:
            print(f"   Last Release: {last_release}")
        else:
            print(f"   Last Release: (未记录)")
        
        if last_check:
            try:
                check_time = datetime.fromisoformat(last_check)
                time_diff = datetime.now() - check_time
                hours = int(time_diff.total_seconds() / 3600)
                minutes = int((time_diff.total_seconds() % 3600) / 60)
                print(f"   Last Check:   {check_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"                 ({hours}小时{minutes}分钟前)")
            except:
                print(f"   Last Check:   {last_check}")
        else:
            print(f"   Last Check:   (未记录)")
    
    print("\n" + "=" * 60)
    print("💡 提示：")
    print("   - 如果某个仓库的状态已记录，只有新的变化才会触发通知")
    print("   - 如果需要重新检测所有变化，可以删除状态文件：")
    print("     rm .monitor_state.json")
    print("=" * 60)

if __name__ == "__main__":
    main()
