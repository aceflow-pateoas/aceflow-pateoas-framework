#!/usr/bin/env python3
# .aceflow/scripts/init.py
"""
AceFlow 初始化脚本
用于创建新的迭代环境。
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

# --- 配置 ---
BASE_RESULT_DIR = "aceflow_result"
ACEFLOW_DIR = ".aceflow"
STAGE_DIRS = [
    "S1_user_story", "S2_tasks", "S3_testcases", "S4_implementation",
    "S5_test_report", "S6_codereview", "S7_demo", "S7_feedback", "S8_summary"
]
TEMPLATE_FILES = {
    "s1_user_story.md": "# 用户故事：{storyTitle}\n\n作为一名[角色]，我希望[功能]，以便[价值]。\n\n## 验收标准\n- [ ] 标准一\n- [ ] 标准二",
    "s2_tasks_main.md": "# 任务清单总览\n\n| 任务ID | 故事ID | 描述 | 类型 | 预估工时 | 优先级 |\n|---|---|---|---|---|---|",
    "s2_tasks_group.md": "# 分组任务清单: {groupName}\n\n| 任务ID | 描述 | 预估工时 | 优先级 |\n|---|---|---|---|",
    "s3_testcases.md": "# 测试用例: {caseTitle}\n\n- **关联故事**: US-{storyId}\n- **测试步骤**:\n  1. ...\n  2. ...\n- **预期结果**: ...",
    "s4_implementation_report.md": "# 任务实现报告: {taskId}\n\n- **实现概述**: ...\n- **文件变更**: ...",
    "s5_test_report.md": "# 测试报告: {taskId}\n\n- **通过率**: ...%\n- **覆盖率**: ...%\n- **失败项**: ...",
    "s6_code_review.md": "# 代码评审报告\n\n| ID | 文件 | 行号 | 问题描述 | 修复建议 |\n|---|---|---|---|---|",
    "s7_demo_script.md": "# 功能演示脚本\n\n## 场景1: ...\n\n- **步骤**: ...\n- **预期**: ...",
    "s8_summary_report.md": "# 迭代总结报告: {iterationId}\n\n## 完成情况\n...\n\n## 经验教训\n...",
    "s8_learning_summary.md": "# 经验教训总结\n\n## 做的好的\n- ...\n\n## 需要改进的\n- ..."
}

# --- 核心函数 ---
def create_directory_structure(iteration_id: str):
    """创建迭代目录结构"""
    base_path = Path(BASE_RESULT_DIR) / iteration_id
    
    for dir_name in STAGE_DIRS:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        (dir_path / "README.md").write_text(f"# {dir_name}\n\n此目录用于存放{dir_name}阶段的产出物。\n", encoding='utf-8')
    
    print(f"✅ 创建迭代目录结构: {base_path}")

def initialize_state(iteration_id: str):
    """初始化状态文件"""
    state = {
        "iteration_id": iteration_id,
        "current_stage": "S1",
        "status": "not_started",
        "progress": 0,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "memory_refs": [],
        "completed_stages": [],
        "current_task": None,
        "metrics": {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tests": 0,
            "code_coverage": 0
        }
    }
    
    state_path = Path(ACEFLOW_DIR) / "state.json"
    state_path.parent.mkdir(exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ 初始化状态文件: {state_path}")

def create_config_template():
    """创建配置文件模板"""
    config_path = Path(ACEFLOW_DIR) / "config.yaml"
    if config_path.exists():
        print(f"ℹ️  配置文件已存在: {config_path}")
        return

    config_content = """# AceFlow 项目配置文件
project:
  name: "新项目"
  version: "0.1.0"

tech_stack:
  language: "python"
  framework: "fastapi"

execution:
  max_task_hours: 8
  min_test_coverage: 80
  task_organization:
    auto_split_threshold: 10
    group_by: ["story", "type"]
"""
    config_path.write_text(config_content, encoding='utf-8')
    print(f"✅ 创建配置文件模板: {config_path}")

def create_templates():
    """创建模板文件"""
    template_dir = Path(ACEFLOW_DIR) / "templates"
    template_dir.mkdir(exist_ok=True)

    for filename, content in TEMPLATE_FILES.items():
        (template_dir / filename).write_text(content, encoding='utf-8')
    
    print(f"✅ 创建所有报告模板于: {template_dir}")

def create_essential_dirs():
    """创建其他必要的目录"""
    dirs = ["memory", "logs"]
    for d in dirs:
        (Path(ACEFLOW_DIR) / d).mkdir(exist_ok=True)
    print(f"✅ 创建 memory 和 logs 目录。")

# --- 主程序 ---
def main():
    """主函数"""
    if len(sys.argv) > 1:
        iteration_id = sys.argv[1]
    else:
        iteration_id = f"iteration_{datetime.now().strftime('%Y%m%d_%H%M')}"
    
    print(f"\n🚀 初始化 AceFlow 迭代: {iteration_id}\n")
    
    create_directory_structure(iteration_id)
    initialize_state(iteration_id)
    create_config_template()
    create_templates()
    create_essential_dirs()
    
    print("\n✅ 初始化完成！")
    print("\n下一步：")
    print("1. 编辑 .aceflow/config.yaml 配置项目信息。")
    print("2. 在VSCode中使用Code Agent开始S1阶段。")

if __name__ == "__main__":
    main()