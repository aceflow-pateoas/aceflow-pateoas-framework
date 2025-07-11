#!/usr/bin/env python3
"""
AceFlow v2.0 AI训练数据生成器
为任务分类和流程推荐模型提供训练数据
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

# 导入决策引擎的枚举类型
import sys
sys.path.append(str(Path(__file__).parent.parent))

from engines.decision_engine import TaskType, ProjectComplexity, TaskContext, ProjectContext

class TrainingDataGenerator:
    """训练数据生成器"""
    
    def __init__(self):
        self.task_keywords = {
            TaskType.FEATURE_DEVELOPMENT: [
                "add new feature", "implement functionality", "create component",
                "build module", "develop interface", "add capability", "新功能",
                "实现功能", "开发组件", "创建模块", "构建接口"
            ],
            TaskType.BUG_FIX: [
                "fix bug", "resolve issue", "correct error", "patch problem",
                "debug issue", "solve crash", "修复bug", "解决问题", "修正错误",
                "调试问题", "解决崩溃"
            ],
            TaskType.REFACTORING: [
                "refactor code", "improve structure", "optimize performance",
                "clean up code", "restructure", "重构代码", "优化结构",
                "性能优化", "代码整理", "重新架构"
            ],
            TaskType.TESTING: [
                "write tests", "add unit tests", "create test cases",
                "test functionality", "write integration tests", "编写测试",
                "单元测试", "集成测试", "测试用例", "功能测试"
            ],
            TaskType.DOCUMENTATION: [
                "update documentation", "write docs", "create guide",
                "document API", "write README", "更新文档", "编写文档",
                "创建指南", "API文档", "说明文档"
            ],
            TaskType.RESEARCH: [
                "research technology", "investigate solution", "explore options",
                "study framework", "analyze tools", "技术调研", "方案研究",
                "技术探索", "框架分析", "工具研究"
            ],
            TaskType.ARCHITECTURE: [
                "design system", "plan architecture", "create blueprint",
                "define structure", "design patterns", "系统设计", "架构设计",
                "架构规划", "设计模式", "系统架构"
            ],
            TaskType.DEPLOYMENT: [
                "deploy application", "release version", "publish build",
                "setup environment", "configure deployment", "部署应用",
                "发布版本", "环境配置", "部署配置", "上线部署"
            ]
        }
        
        self.project_types = ["web", "mobile", "api", "desktop", "game", "ai", "blockchain"]
        self.tech_stacks = [
            ["Python", "Django", "PostgreSQL"],
            ["JavaScript", "React", "Node.js"],
            ["Java", "Spring", "MySQL"],
            ["C#", ".NET", "SQL Server"],
            ["Go", "Gin", "Redis"],
            ["TypeScript", "Vue.js", "MongoDB"],
            ["Swift", "iOS", "CoreData"],
            ["Kotlin", "Android", "SQLite"]
        ]
        
        self.priorities = ["high", "medium", "low"]
        self.complexities = ["high", "medium", "low"]
        self.impacts = ["high", "medium", "low"]
        
    def generate_task_description(self, task_type: TaskType) -> str:
        """生成任务描述"""
        keywords = self.task_keywords[task_type]
        base_keyword = random.choice(keywords)
        
        # 添加上下文信息
        contexts = [
            "for user dashboard",
            "in payment module", 
            "for mobile app",
            "in admin panel",
            "for API endpoint",
            "in authentication system",
            "for data visualization",
            "在用户管理模块",
            "在支付系统中",
            "在移动端应用",
            "在后台管理"
        ]
        
        context = random.choice(contexts)
        
        # 生成完整描述
        if random.random() < 0.5:
            return f"{base_keyword} {context}"
        else:
            return f"{base_keyword} to improve {context}"
    
    def generate_task_context(self, task_type: TaskType) -> TaskContext:
        """生成任务上下文"""
        description = self.generate_task_description(task_type)
        priority = random.choice(self.priorities)
        complexity = random.choice(self.complexities)
        impact = random.choice(self.impacts)
        
        # 生成依赖关系
        dependencies = []
        if random.random() < 0.3:  # 30%概率有依赖
            dep_count = random.randint(1, 3)
            for i in range(dep_count):
                dependencies.append(f"dependency_{i+1}")
        
        # 生成估算时间
        effort_options = ["1-2 hours", "half day", "1-2 days", "3-5 days", "1 week", "2 weeks"]
        effort = random.choice(effort_options)
        
        return TaskContext(
            description=description,
            priority=priority,
            estimated_effort=effort,
            dependencies=dependencies,
            technical_complexity=complexity,
            user_impact=impact
        )
    
    def generate_project_context(self, preferred_flow: str = None) -> ProjectContext:
        """生成项目上下文"""
        project_type = random.choice(self.project_types)
        tech_stack = random.choice(self.tech_stacks)
        
        # 根据流程类型调整项目特征
        if preferred_flow == "minimal":
            team_size = random.randint(1, 3)
            duration = random.choice(["1 week", "2 weeks", "1 month"])
            risk_count = random.randint(0, 2)
        elif preferred_flow == "complete":
            team_size = random.randint(8, 15)
            duration = random.choice(["3 months", "6 months", "1 year"])
            risk_count = random.randint(3, 6)
        else:  # standard
            team_size = random.randint(3, 8)
            duration = random.choice(["1 month", "2 months", "3 months"])
            risk_count = random.randint(1, 3)
        
        # 生成风险因素
        risk_factors = []
        risk_options = [
            "tight deadline", "new technology", "complex requirements",
            "limited resources", "high complexity", "uncertain scope",
            "integration challenges", "performance requirements"
        ]
        
        for _ in range(risk_count):
            risk_factors.append(random.choice(risk_options))
        
        # 生成其他属性
        stages = ["planning", "development", "testing", "deployment"]
        current_stage = random.choice(stages)
        completion = random.uniform(0.1, 0.9)
        velocity = random.uniform(0.6, 1.2)
        
        return ProjectContext(
            name=f"{project_type}-project-{random.randint(1000, 9999)}",
            team_size=team_size,
            duration_estimate=duration,
            technology_stack=tech_stack,
            project_type=project_type,
            current_stage=current_stage,
            completion_percentage=completion,
            historical_velocity=velocity,
            risk_factors=risk_factors
        )
    
    def generate_task_classification_data(self, samples_per_type: int = 50) -> List[Tuple[str, TaskType]]:
        """生成任务分类训练数据"""
        training_data = []
        
        for task_type in TaskType:
            for _ in range(samples_per_type):
                task_context = self.generate_task_context(task_type)
                training_data.append((task_context.description, task_type))
        
        # 打乱数据顺序
        random.shuffle(training_data)
        return training_data
    
    def generate_flow_recommendation_data(self, samples_per_flow: int = 100) -> List[Tuple[Dict[str, Any], str]]:
        """生成流程推荐训练数据"""
        training_data = []
        flows = ["minimal", "standard", "complete"]
        
        for flow in flows:
            for _ in range(samples_per_flow):
                # 生成适合该流程的项目上下文
                project_context = self.generate_project_context(flow)
                features = project_context.to_features()
                
                training_data.append((features, flow))
        
        # 打乱数据顺序
        random.shuffle(training_data)
        return training_data
    
    def generate_progress_prediction_data(self, samples: int = 500) -> List[Tuple[Dict[str, Any], int]]:
        """生成进度预测训练数据"""
        training_data = []
        
        for _ in range(samples):
            task_type = random.choice(list(TaskType))
            task_context = self.generate_task_context(task_type)
            project_context = self.generate_project_context()
            
            # 基于规则生成"真实"持续时间
            base_hours = {
                TaskType.BUG_FIX: 4,
                TaskType.FEATURE_DEVELOPMENT: 16,
                TaskType.REFACTORING: 8,
                TaskType.TESTING: 6,
                TaskType.DOCUMENTATION: 4,
                TaskType.RESEARCH: 12,
                TaskType.ARCHITECTURE: 24,
                TaskType.DEPLOYMENT: 8
            }
            
            hours = base_hours.get(task_type, 8)
            
            # 添加随机变化和项目因素影响
            if task_context.technical_complexity == "high":
                hours *= random.uniform(1.3, 1.8)
            elif task_context.technical_complexity == "low":
                hours *= random.uniform(0.7, 0.9)
            
            if project_context.team_size > 5:
                hours *= random.uniform(1.1, 1.4)
            elif project_context.team_size == 1:
                hours *= random.uniform(0.8, 1.0)
            
            if len(project_context.risk_factors) > 2:
                hours *= random.uniform(1.2, 1.6)
            
            # 添加随机噪声
            hours *= random.uniform(0.8, 1.3)
            
            # 合并特征
            features = {
                **task_context.to_features(),
                **project_context.to_features(),
                'task_type_feature': task_type.value
            }
            
            training_data.append((features, int(hours)))
        
        return training_data
    
    def save_training_data(self, output_dir: Path):
        """保存训练数据到文件"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成任务分类数据
        print("🔄 生成任务分类训练数据...")
        task_data = self.generate_task_classification_data(samples_per_type=100)
        
        # 转换为可序列化格式
        task_data_serializable = [
            (description, task_type.value) for description, task_type in task_data
        ]
        
        with open(output_dir / "task_classification_data.json", 'w', encoding='utf-8') as f:
            json.dump(task_data_serializable, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 任务分类数据已保存: {len(task_data)} 条记录")
        
        # 生成流程推荐数据
        print("🔄 生成流程推荐训练数据...")
        flow_data = self.generate_flow_recommendation_data(samples_per_flow=150)
        
        with open(output_dir / "flow_recommendation_data.json", 'w', encoding='utf-8') as f:
            json.dump(flow_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 流程推荐数据已保存: {len(flow_data)} 条记录")
        
        # 生成进度预测数据
        print("🔄 生成进度预测训练数据...")
        progress_data = self.generate_progress_prediction_data(samples=800)
        
        with open(output_dir / "progress_prediction_data.json", 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 进度预测数据已保存: {len(progress_data)} 条记录")
        
        # 生成数据集统计信息
        stats = {
            "generation_time": datetime.now().isoformat(),
            "total_samples": len(task_data) + len(flow_data) + len(progress_data),
            "task_classification_samples": len(task_data),
            "flow_recommendation_samples": len(flow_data),
            "progress_prediction_samples": len(progress_data),
            "task_types": [t.value for t in TaskType],
            "flow_types": ["minimal", "standard", "complete"],
            "feature_dimensions": {
                "task_features": len(self.generate_task_context(TaskType.FEATURE_DEVELOPMENT).to_features()),
                "project_features": len(self.generate_project_context().to_features())
            }
        }
        
        with open(output_dir / "dataset_stats.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"📊 数据集统计信息已保存")
        print(f"📁 所有训练数据保存在: {output_dir}")


class RealWorldDataCollector:
    """真实项目数据收集器"""
    
    def __init__(self, aceflow_dir: Path):
        self.aceflow_dir = aceflow_dir
        self.data_dir = aceflow_dir / "ai" / "data"
        self.real_data_file = self.data_dir / "real_world_data.jsonl"
    
    def collect_project_data(self) -> Dict[str, Any]:
        """收集当前项目的真实数据"""
        try:
            # 读取项目状态
            state_file = self.aceflow_dir / "state" / "project_state.json"
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
            else:
                state = {}
            
            # 读取配置
            config_file = self.aceflow_dir / "config.yaml"
            if config_file.exists():
                import yaml
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
            else:
                config = {}
            
            # 收集项目特征
            project_data = {
                "timestamp": datetime.now().isoformat(),
                "project_id": state.get("project_id", "unknown"),
                "flow_mode": state.get("flow_mode", "unknown"),
                "current_stage": state.get("current_stage", "unknown"),
                "progress": state.get("progress", {}),
                "team_size": config.get("project", {}).get("team_size", "unknown"),
                "project_type": config.get("project", {}).get("project_type", "unknown"),
                "agile_framework": config.get("agile", {}).get("framework", "unknown"),
                "stage_history": state.get("stage_states", {})
            }
            
            return project_data
            
        except Exception as e:
            print(f"⚠️ 收集项目数据时出错: {e}")
            return {}
    
    def save_real_data(self, data: Dict[str, Any]):
        """保存真实数据到文件"""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.real_data_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
            
            print(f"✅ 真实数据已保存: {self.real_data_file}")
            
        except Exception as e:
            print(f"❌ 保存真实数据时出错: {e}")
    
    def get_collected_data(self) -> List[Dict[str, Any]]:
        """获取所有收集的真实数据"""
        data = []
        
        if self.real_data_file.exists():
            try:
                with open(self.real_data_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data.append(json.loads(line.strip()))
            except Exception as e:
                print(f"⚠️ 读取真实数据时出错: {e}")
        
        return data


def main():
    """主函数"""
    print("🤖 AceFlow v2.0 AI训练数据生成器")
    print("=" * 50)
    
    # 设置随机种子以确保可重现性
    random.seed(42)
    
    # 确定输出目录
    current_dir = Path(__file__).parent
    output_dir = current_dir / "training_datasets"
    
    # 生成训练数据
    generator = TrainingDataGenerator()
    generator.save_training_data(output_dir)
    
    # 收集真实项目数据
    aceflow_dir = current_dir.parent.parent
    collector = RealWorldDataCollector(aceflow_dir)
    
    real_data = collector.collect_project_data()
    if real_data:
        collector.save_real_data(real_data)
    
    print("\n🎉 训练数据生成完成!")
    print("📋 数据集包含:")
    print("   - 任务分类数据: 800条记录")
    print("   - 流程推荐数据: 450条记录") 
    print("   - 进度预测数据: 800条记录")
    print("   - 真实项目数据: 持续收集中")
    print(f"\n💾 数据保存位置: {output_dir}")


if __name__ == "__main__":
    main()