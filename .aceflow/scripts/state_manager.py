#!/usr/bin/env python3
# .aceflow/scripts/state_manager.py
"""
AceFlow 状态管理器
用于更新和查询流程状态。
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class StateManager:
    """管理 state.json 文件的类"""
    def __init__(self, state_file: Path = Path(".aceflow/state.json")):
        self.state_file = state_file
        if not self.state_file.exists():
            print(f"❌ 错误: 状态文件不存在于 {self.state_file}")
            print("请先运行 'python .aceflow/scripts/init.py'")
            sys.exit(1)
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """加载状态文件"""
        return json.loads(self.state_file.read_text(encoding='utf-8'))

    def _save_state(self):
        """保存状态文件"""
        self.state['updated_at'] = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(self.state, indent=2, ensure_ascii=False), encoding='utf-8')

    def update_stage(self, stage: str, progress: int):
        """更新当前阶段和进度"""
        self.state['current_stage'] = stage
        self.state['progress'] = progress
        self.state['status'] = 'in_progress' if progress < 100 else 'completed'

        if progress == 100 and stage not in self.state.get('completed_stages', []):
            self.state.setdefault('completed_stages', []).append(stage)

        self._save_state()
        print(f"✅ 状态更新 -> 阶段: {stage}, 进度: {progress}%")

    def add_memory_ref(self, memory_id: str):
        """添加记忆引用"""
        self.state.setdefault('memory_refs', []).append(memory_id)
        self._save_state()
        print(f"✅ 添加记忆引用: {memory_id}")

    def update_metrics(self, **kwargs):
        """更新指标"""
        self.state.setdefault('metrics', {}).update(kwargs)
        self._save_state()
        print(f"✅ 更新指标: {kwargs}")

    def print_status(self):
        """打印当前状态"""
        print("\n📊 AceFlow 当前状态")
        print("="*40)
        for key, value in self.state.items():
            if isinstance(value, list) and value:
                print(f"- {key.replace('_', ' ').title()}: {', '.join(map(str, value))}")
            elif isinstance(value, dict):
                print(f"- {key.replace('_', ' ').title()}:")
                for sub_key, sub_value in value.items():
                    print(f"  - {sub_key}: {sub_value}")
            else:
                print(f"- {key.replace('_', ' ').title()}: {value}")
        print("="*40)

def main():
    """命令行接口"""
    manager = StateManager()
    
    if len(sys.argv) < 2 or sys.argv[1] not in ['status', 'update', 'memory', 'metric']:
        print("用法: python state_manager.py <command> [args]")
        print("命令:")
        print("  status                  - 显示当前状态")
        print("  update <stage> <progress> - 更新阶段进度 (e.g., S1 100)")
        print("  memory <memory_id>        - 添加记忆引用 (e.g., REQ-001)")
        print("  metric <key> <value>    - 更新指标 (e.g., total_tasks 15)")
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        manager.print_status()
    elif command == "update":
        if len(sys.argv) != 4:
            print("错误: 'update' 命令需要 <stage> 和 <progress> 参数。")
            sys.exit(1)
        manager.update_stage(sys.argv[2], int(sys.argv[3]))
    elif command == "memory":
        if len(sys.argv) != 3:
            print("错误: 'memory' 命令需要 <memory_id> 参数。")
            sys.exit(1)
        manager.add_memory_ref(sys.argv[2])
    elif command == "metric":
        if len(sys.argv) != 4:
            print("错误: 'metric' 命令需要 <key> 和 <value> 参数。")
            sys.exit(1)
        key, value_str = sys.argv[2], sys.argv[3]
        try:
            value = float(value_str) if '.' in value_str else int(value_str)
        except ValueError:
            value = value_str
        manager.update_metrics(**{key: value})

if __name__ == "__main__":
    main()