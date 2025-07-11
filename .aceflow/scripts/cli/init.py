import os
import json
from datetime import datetime
from ..core.state_engine import PATEOASStateEngine
from ..core.memory_pool import GlobalMemoryPool
from ..utils.logger import get_logger

# 初始化日志
logger = get_logger("aceflow.init")

def initialize_project(project_root='.', reset_state=False):
    """
    初始化AceFlow-PATEOAS项目结构
    
    参数:
        project_root (str): 项目根目录路径，默认为当前目录
        reset_state (bool): 是否重置现有状态，默认为False
    """
    try:
        # 1. 创建核心目录结构
        directories = [
            ".aceflow/config",
            ".aceflow/scripts/core",
            ".aceflow/scripts/cli",
            ".aceflow/scripts/utils",
            ".aceflow/scripts/migrations",
            ".aceflow/memory_pool/REQ",
            ".aceflow/memory_pool/CON",
            ".aceflow/memory_pool/TASK",
            ".aceflow/memory_pool/CODE",
            ".aceflow/memory_pool/TEST",
            ".aceflow/memory_pool/DEFECT",
            ".aceflow/memory_pool/FDBK",
            ".aceflow/templates/stage_templates",
            ".aceflow/templates/auxiliary_templates",
            ".aceflow/logs",
            "aceflow_result",
            ".vscode"
        ]
        
        for dir_path in directories:
            full_path = os.path.join(project_root, dir_path)
            os.makedirs(full_path, exist_ok=True)
            logger.info(f"创建目录: {full_path}")

        # 2. 初始化状态引擎
        state_engine = PATEOASStateEngine(project_root)
        if reset_state:
            logger.info("重置现有状态...")
            state_engine.initialize_state()

        # 3. 初始化记忆池
        memory_pool = GlobalMemoryPool()
        logger.info("全局记忆池初始化完成")

        # 4. 创建基础配置文件（如不存在）
        create_default_configs(project_root)

        # 5. 创建.gitignore文件
        create_gitignore(project_root)

        logger.info("项目初始化完成！")
        print("✅ AceFlow-PATEOAS项目初始化成功")
        print("📁 项目结构已创建")
        print("🔧 状态引擎和记忆池已初始化")
        print("📝 基础配置文件已生成")
        
        return True
        
    except Exception as e:
        logger.error(f"初始化失败: {str(e)}", exc_info=True)
        print(f"❌ 初始化失败: {str(e)}")
        return False

def create_default_configs(project_root):
    """创建默认配置文件"""
    # workflow_rules.json
    workflow_rules_path = os.path.join(project_root, ".aceflow", "config", "workflow_rules.json")
    if not os.path.exists(workflow_rules_path):
        default_workflow_rules = {
            "workflow_rules": {
                "full_workflow": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
                "quick_workflow": ["S2", "S4", "S5", "S8"],
                "change_workflow": ["S1", "S2", "S3", "S4"],
                "emergency_workflow": ["S4", "S5", "S6", "S8"]
            },
            "memory_pool_config": {
                "storage_path": "./.aceflow/memory_pool",
                "retention_policy": "critical_forever,temporary_7d"
            },
            "ai_decision_config": {
                "trust_level": "L2",
                "success_threshold": 0.85
            }
        }
        
        with open(workflow_rules_path, 'w', encoding='utf-8') as f:
            json.dump(default_workflow_rules, f, ensure_ascii=False, indent=2)
        logger.info(f"创建默认配置: {workflow_rules_path}")

    # dynamic_thresholds.json
    thresholds_path = os.path.join(project_root, ".aceflow", "config", "dynamic_thresholds.json")
    if not os.path.exists(thresholds_path):
        default_thresholds = {
            "global": {
                "time_adjustment_range": 20,
                "memory_retention_days": 30
            },
            "stage_specific": {
                "S3": {
                    "test_case_coverage": {
                        "default": 80,
                        "payment_module": 99,
                        "ui_module": 75
                    }
                },
                "S4": {
                    "unit_test_pass_rate": {
                        "default": 90,
                        "critical_task": 95,
                        "minor_task": 85
                    }
                }
            }
        }
        
        with open(thresholds_path, 'w', encoding='utf-8') as f:
            json.dump(default_thresholds, f, ensure_ascii=False, indent=2)
        logger.info(f"创建默认配置: {thresholds_path}")

    # aceflow_agent.json (VS Code配置)
    agent_config_path = os.path.join(project_root, ".vscode", "aceflow_agent.json")
    if not os.path.exists(agent_config_path):
        default_agent_config = {
            "agent_type": "pateoas_aceflow_agent",
            "capabilities": [
                "state_awareness",
                "memory_management",
                "autonomous_navigation",
                "abnormality_handling"
            ],
            "state_templates": ".aceflow/templates/stage_templates/",
            "memory_pool_config": {
                "storage_path": ".aceflow/memory_pool/",
                "retention_policy": "critical_forever,temporary_7d"
            },
            "output_config": {
                "root_dir": "aceflow_result",
                "stage_dir_format": "S{stage_number}_{stage_name}",
                "compatibility_mode": true
            }
        }
        
        with open(agent_config_path, 'w', encoding='utf-8') as f:
            json.dump(default_agent_config, f, ensure_ascii=False, indent=2)
        logger.info(f"创建默认配置: {agent_config_path}")

    # process_index.json (流程索引)
    index_path = os.path.join(project_root, ".aceflow", "process_index.json")
    if not os.path.exists(index_path):
        default_index = {
            "process_spec": {
                "path": ".aceflow/templates/document_templates/process_spec.md",
                "sections": [
                    {"name": "核心原则", "anchor": "#_2-核心原则"},
                    {"name": "阶段定义", "anchor": "#_4-阶段定义与执行规范"},
                    {"name": "状态管理", "anchor": "#_5-状态管理规范"}
                ]
            },
            "templates": {
                "stage_templates": ".aceflow/templates/stage_templates/",
                "auxiliary_templates": ".aceflow/templates/auxiliary_templates/",
                "available_templates": [
                    "s1_user_story.md", "s2_tasks.md", "s3_testcases.md",
                    "s4_implementation.md", "s5_test_report.md", "s6_codereview.md",
                    "s7_demo_feedback.md", "s8_progress_index.md", "task-status-table.md"
                ]
            },
            "config_files": {
                "dynamic_thresholds": ".aceflow/config/dynamic_thresholds.json",
                "workflow_rules": ".aceflow/config/workflow_rules.json",
                "agent_config": ".vscode/aceflow_agent.json"
            }
        }
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(default_index, f, ensure_ascii=False, indent=2)
        logger.info(f"创建流程索引: {index_path}")

def create_gitignore(project_root):
    """创建.gitignore文件，排除临时文件和敏感信息"""
    gitignore_path = os.path.join(project_root, ".gitignore")
    ignore_content = """# AceFlow-PATEOAS 临时文件
.aceflow/logs/
.aceflow/memory_pool/
.aceflow/current_state.json
.aceflow/*.log

# 产物目录
aceflow_result/

# Python 环境文件
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# VS Code 配置
.vscode/settings.json
.vscode/launch.json
!.vscode/extensions.json
!.vscode/aceflow_agent.json
"""
    
    # 如果.gitignore不存在或不包含AceFlow规则，则添加
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(ignore_content)
        logger.info("创建.gitignore文件")
    else:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "# AceFlow-PATEOAS 临时文件" not in content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write("\n" + ignore_content)
            logger.info("更新.gitignore文件，添加AceFlow规则")

# 命令行入口函数
def init_project(args):
    """CLI命令：初始化项目"""
    initialize_project(reset_state=getattr(args, 'reset', False))

# 命令配置
def add_init_command(subparsers):
    """添加init命令到解析器"""
    init_parser = subparsers.add_parser('init', help='初始化AceFlow-PATEOAS项目结构')
    init_parser.add_argument('--reset', action='store_true', help='重置现有状态文件')
    init_parser.set_defaults(func=init_project)