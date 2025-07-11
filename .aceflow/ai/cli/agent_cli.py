#!/usr/bin/env python3
"""
AceFlow v2.0 CLI工具 - Agent集成版本
为Cursor、Cline、Copilot等AI工具提供智能工作流建议
"""

import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# 导入决策引擎
sys.path.append(str(Path(__file__).parent.parent))
from engines.rule_based_engine import get_decision_engine, DecisionResult

class AceFlowCLI:
    """AceFlow CLI工具"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.aceflow_dir = self.project_root / ".aceflow"
        self.version = "2.0.0"
        self.engine = get_decision_engine(self.project_root)
    
    def describe(self, output_format: str = "json") -> str:
        """描述工具能力，供Agent发现和理解"""
        description = {
            "name": "AceFlow",
            "version": self.version,
            "description": "AI驱动的软件开发工作流管理工具",
            "capabilities": [
                "智能工作流程推荐",
                "任务分类和优先级建议",
                "开发阶段管理",
                "进度跟踪和预测",
                "项目复杂度分析",
                "团队协作优化"
            ],
            "use_cases": [
                "项目规划和流程选择",
                "任务管理和跟踪",
                "开发效率优化",
                "质量保证流程",
                "敏捷开发支持"
            ],
            "trigger_patterns": [
                "工作流",
                "流程",
                "项目规划",
                "任务管理",
                "开发流程",
                "敏捷开发",
                "项目管理"
            ],
            "integration": {
                "cli_commands": {
                    "suggest": {
                        "description": "智能工作流推荐",
                        "usage": "aceflow suggest --task '任务描述' [选项]",
                        "example": "aceflow suggest --task '修复登录bug' --format json"
                    },
                    "plan": {
                        "description": "项目规划建议",
                        "usage": "aceflow plan --project-type web --team-size 5 [选项]",
                        "example": "aceflow plan --project-type web --team-size 5 --format json"
                    },
                    "track": {
                        "description": "进度跟踪",
                        "usage": "aceflow track --stage current [选项]",
                        "example": "aceflow track --stage current --format json"
                    },
                    "status": {
                        "description": "项目状态查询",
                        "usage": "aceflow status [选项]",
                        "example": "aceflow status --format json"
                    }
                },
                "output_formats": ["json", "yaml", "text"],
                "response_schema": {
                    "type": "object",
                    "properties": {
                        "recommended_flow": {"type": "string"},
                        "confidence": {"type": "number"},
                        "reasoning": {"type": "string"},
                        "steps": {"type": "array"},
                        "estimated_hours": {"type": "integer"},
                        "alternatives": {"type": "array"}
                    }
                }
            },
            "when_to_use": {
                "scenarios": [
                    "用户询问如何组织开发流程",
                    "需要制定项目计划",
                    "想要标准化开发流程",
                    "需要跟踪项目进度",
                    "选择合适的开发模式"
                ],
                "keywords": [
                    "workflow", "process", "planning", "management",
                    "工作流", "流程", "规划", "管理"
                ]
            }
        }
        
        if output_format == "yaml":
            return yaml.dump(description, default_flow_style=False, allow_unicode=True)
        elif output_format == "text":
            return self._format_description_text(description)
        else:
            return json.dumps(description, indent=2, ensure_ascii=False)
    
    def suggest(self, task: str, **kwargs) -> Dict[str, Any]:
        """智能工作流推荐"""
        if not task:
            raise ValueError("任务描述不能为空")
        
        # 构建上下文
        context = {}
        if kwargs.get("team_size"):
            context["team_size"] = int(kwargs["team_size"])
        if kwargs.get("project_type"):
            context["project_type"] = kwargs["project_type"]
        if kwargs.get("complexity"):
            context["complexity"] = kwargs["complexity"]
        if kwargs.get("urgency"):
            context["urgency"] = kwargs["urgency"]
        
        # 获取决策结果
        result = self.engine.make_decision(task, context)
        
        # 格式化输出
        return self._format_decision_result(result)
    
    def plan(self, **kwargs) -> Dict[str, Any]:
        """项目规划建议"""
        # 构建虚拟任务描述
        project_type = kwargs.get("project_type", "web")
        team_size = kwargs.get("team_size", 5)
        
        task_description = f"为{project_type}项目制定开发计划"
        
        context = {
            "project_type": project_type,
            "team_size": int(team_size),
            "urgency": kwargs.get("urgency", "medium")
        }
        
        if kwargs.get("complexity"):
            context["complexity"] = kwargs["complexity"]
        
        # 获取决策结果
        result = self.engine.make_decision(task_description, context)
        
        # 增加项目规划特定信息
        planning_result = self._format_decision_result(result)
        planning_result["project_recommendations"] = self._generate_project_recommendations(context)
        
        return planning_result
    
    def track(self, **kwargs) -> Dict[str, Any]:
        """进度跟踪"""
        stage = kwargs.get("stage", "current")
        
        # 读取项目状态
        project_state = self._load_project_state()
        
        if not project_state:
            return {
                "error": "未找到项目状态，请先初始化项目",
                "suggestion": "运行 'aceflow init' 初始化项目"
            }
        
        # 构建跟踪结果
        tracking_result = {
            "project_id": project_state.get("project_id", "unknown"),
            "flow_mode": project_state.get("flow_mode", "unknown"),
            "current_stage": project_state.get("current_stage", "unknown"),
            "overall_progress": project_state.get("progress", {}).get("overall", 0),
            "stage_states": project_state.get("stage_states", {}),
            "last_updated": project_state.get("last_updated", "unknown"),
            "recommendations": []
        }
        
        # 添加进度建议
        if tracking_result["overall_progress"] < 30:
            tracking_result["recommendations"].append("项目处于早期阶段，建议专注于需求分析和设计")
        elif tracking_result["overall_progress"] < 70:
            tracking_result["recommendations"].append("项目进展良好，建议保持当前开发节奏")
        else:
            tracking_result["recommendations"].append("项目接近完成，建议重点关注测试和部署准备")
        
        return tracking_result
    
    def status(self, **kwargs) -> Dict[str, Any]:
        """项目状态查询"""
        # 读取项目状态和配置
        project_state = self._load_project_state()
        project_config = self._load_project_config()
        
        # 分析项目特征
        project_profile = self.engine.project_analyzer.analyze_project()
        
        status_result = {
            "project_info": {
                "name": project_config.get("project", {}).get("name", "unknown"),
                "type": project_profile.project_type,
                "team_size": project_profile.team_size,
                "complexity": project_profile.complexity.value,
                "tech_stack": project_profile.tech_stack
            },
            "current_state": project_state or {},
            "project_health": {
                "has_tests": project_profile.has_tests,
                "has_ci_cd": project_profile.has_ci_cd,
                "has_documentation": project_profile.has_documentation,
                "file_count": project_profile.file_count,
                "git_activity": project_profile.git_activity
            },
            "recommendations": []
        }
        
        # 生成健康建议
        if not project_profile.has_tests:
            status_result["recommendations"].append("建议添加测试用例以提高代码质量")
        
        if not project_profile.has_ci_cd:
            status_result["recommendations"].append("建议配置CI/CD流程以自动化部署")
        
        if not project_profile.has_documentation:
            status_result["recommendations"].append("建议完善项目文档以提高可维护性")
        
        return status_result
    
    def memory(self, action: str, **kwargs) -> Dict[str, Any]:
        """记忆管理"""
        memory_dir = self.aceflow_dir / "memory"
        
        if action == "list":
            return self._list_memories(memory_dir)
        elif action == "search":
            query = kwargs.get("query", "")
            return self._search_memories(memory_dir, query)
        elif action == "clean":
            return self._clean_memories(memory_dir)
        else:
            return {"error": f"不支持的记忆操作: {action}"}
    
    def _format_decision_result(self, result: DecisionResult) -> Dict[str, Any]:
        """格式化决策结果"""
        return {
            "recommended_flow": result.recommended_flow,
            "confidence": result.confidence,
            "reasoning": result.reasoning,
            "steps": result.steps,
            "estimated_hours": result.estimated_hours,
            "alternatives": result.alternatives,
            "timestamp": datetime.now().isoformat(),
            "task_type": result.metadata.get("task_type", "unknown")
        }
    
    def _generate_project_recommendations(self, context: Dict[str, Any]) -> List[str]:
        """生成项目规划建议"""
        recommendations = []
        
        team_size = context.get("team_size", 1)
        project_type = context.get("project_type", "web")
        
        # 团队规模建议
        if team_size <= 3:
            recommendations.append("小团队建议使用敏捷开发模式，快速迭代")
        elif team_size > 8:
            recommendations.append("大团队建议制定详细的协作流程和代码规范")
        
        # 项目类型建议
        if project_type == "web":
            recommendations.append("Web项目建议重点关注性能优化和用户体验")
        elif project_type == "mobile":
            recommendations.append("移动应用建议关注多平台适配和离线功能")
        elif project_type == "api":
            recommendations.append("API项目建议重点关注接口设计和文档完善")
        
        return recommendations
    
    def _load_project_state(self) -> Optional[Dict[str, Any]]:
        """加载项目状态"""
        state_file = self.aceflow_dir / "state" / "project_state.json"
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return None
        
        return None
    
    def _load_project_config(self) -> Optional[Dict[str, Any]]:
        """加载项目配置"""
        config_file = self.aceflow_dir / "config.yaml"
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception:
                return None
        
        return None
    
    def _list_memories(self, memory_dir: Path) -> Dict[str, Any]:
        """列出记忆"""
        if not memory_dir.exists():
            return {"memories": [], "count": 0}
        
        memories = []
        for memory_file in memory_dir.glob("*.json"):
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                    memories.append({
                        "id": memory_file.stem,
                        "timestamp": memory_data.get("timestamp", "unknown"),
                        "content_preview": memory_data.get("content", "")[:100] + "..." if len(memory_data.get("content", "")) > 100 else memory_data.get("content", ""),
                        "keywords": memory_data.get("keywords", [])
                    })
            except Exception:
                continue
        
        return {"memories": memories, "count": len(memories)}
    
    def _search_memories(self, memory_dir: Path, query: str) -> Dict[str, Any]:
        """搜索记忆"""
        if not memory_dir.exists():
            return {"results": [], "count": 0}
        
        results = []
        query_lower = query.lower()
        
        for memory_file in memory_dir.glob("*.json"):
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                    
                    # 简单的关键词匹配
                    content = memory_data.get("content", "").lower()
                    keywords = [k.lower() for k in memory_data.get("keywords", [])]
                    
                    if query_lower in content or any(query_lower in keyword for keyword in keywords):
                        results.append({
                            "id": memory_file.stem,
                            "timestamp": memory_data.get("timestamp", "unknown"),
                            "content": memory_data.get("content", ""),
                            "relevance": self._calculate_relevance(query_lower, content, keywords)
                        })
            except Exception:
                continue
        
        # 按相关性排序
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return {"results": results, "count": len(results)}
    
    def _calculate_relevance(self, query: str, content: str, keywords: List[str]) -> float:
        """计算相关性分数"""
        score = 0.0
        
        # 内容匹配
        if query in content:
            score += 1.0
        
        # 关键词匹配
        for keyword in keywords:
            if query in keyword:
                score += 0.5
        
        return score
    
    def _clean_memories(self, memory_dir: Path) -> Dict[str, Any]:
        """清理记忆"""
        if not memory_dir.exists():
            return {"message": "记忆目录不存在", "cleaned": 0}
        
        cleaned_count = 0
        
        # 清理空文件或损坏文件
        for memory_file in memory_dir.glob("*.json"):
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                    
                    # 检查是否为空或无效记忆
                    if not memory_data.get("content") or len(memory_data.get("content", "")) < 10:
                        memory_file.unlink()
                        cleaned_count += 1
            except Exception:
                # 删除损坏的文件
                memory_file.unlink()
                cleaned_count += 1
        
        return {"message": f"清理完成，删除了{cleaned_count}个无效记忆", "cleaned": cleaned_count}
    
    def _format_description_text(self, description: Dict[str, Any]) -> str:
        """格式化文本描述"""
        text = f"{description['name']} v{description['version']}\n"
        text += f"{description['description']}\n\n"
        
        text += "核心能力:\n"
        for capability in description['capabilities']:
            text += f"  - {capability}\n"
        
        text += "\n使用场景:\n"
        for use_case in description['use_cases']:
            text += f"  - {use_case}\n"
        
        text += "\n触发关键词:\n"
        text += f"  {', '.join(description['trigger_patterns'])}\n"
        
        return text

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="AceFlow v2.0 - AI驱动的软件开发工作流管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--version", action="version", version="AceFlow v2.0.0")
    parser.add_argument("--format", choices=["json", "yaml", "text"], default="json",
                       help="输出格式")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    parser.add_argument("--quiet", action="store_true", help="静默模式")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # describe命令
    describe_parser = subparsers.add_parser("describe", help="描述工具能力")
    describe_parser.add_argument("--format", choices=["json", "yaml", "text"], default="json")
    
    # suggest命令
    suggest_parser = subparsers.add_parser("suggest", help="智能工作流推荐")
    suggest_parser.add_argument("--task", required=True, help="任务描述")
    suggest_parser.add_argument("--team-size", type=int, help="团队规模")
    suggest_parser.add_argument("--project-type", help="项目类型")
    suggest_parser.add_argument("--complexity", choices=["simple", "moderate", "complex", "enterprise"], help="项目复杂度")
    suggest_parser.add_argument("--urgency", choices=["low", "medium", "high"], default="medium", help="紧急程度")
    
    # plan命令
    plan_parser = subparsers.add_parser("plan", help="项目规划建议")
    plan_parser.add_argument("--project-type", default="web", help="项目类型")
    plan_parser.add_argument("--team-size", type=int, default=5, help="团队规模")
    plan_parser.add_argument("--complexity", choices=["simple", "moderate", "complex", "enterprise"], help="项目复杂度")
    plan_parser.add_argument("--urgency", choices=["low", "medium", "high"], default="medium", help="紧急程度")
    
    # track命令
    track_parser = subparsers.add_parser("track", help="进度跟踪")
    track_parser.add_argument("--stage", default="current", help="阶段")
    
    # status命令
    status_parser = subparsers.add_parser("status", help="项目状态查询")
    
    # memory命令
    memory_parser = subparsers.add_parser("memory", help="记忆管理")
    memory_parser.add_argument("action", choices=["list", "search", "clean"], help="操作类型")
    memory_parser.add_argument("--query", help="搜索查询")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        cli = AceFlowCLI()
        
        if args.command == "describe":
            result = cli.describe(args.format)
            print(result)
        
        elif args.command == "suggest":
            result = cli.suggest(
                task=args.task,
                team_size=args.team_size,
                project_type=args.project_type,
                complexity=args.complexity,
                urgency=args.urgency
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "plan":
            result = cli.plan(
                project_type=args.project_type,
                team_size=args.team_size,
                complexity=args.complexity,
                urgency=args.urgency
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "track":
            result = cli.track(stage=args.stage)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "status":
            result = cli.status()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "memory":
            result = cli.memory(args.action, query=args.query)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(json.dumps({"error": str(e)}, indent=2, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()