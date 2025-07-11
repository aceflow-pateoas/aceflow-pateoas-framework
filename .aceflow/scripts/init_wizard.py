#!/usr/bin/env python3
"""
AceFlow 快速初始化向导
支持轻量级、标准和完整三种模式的项目初始化
"""

import os
import sys
import yaml
import json
from typing import Dict, List, Optional
from pathlib import Path
import questionary
from datetime import datetime

class AceFlowInitWizard:
    """AceFlow项目初始化向导"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.aceflow_dir = self.project_root / ".aceflow"
        self.config = {}
        self.templates_dir = Path(__file__).parent.parent / "templates"
        
    def run(self):
        """运行初始化向导"""
        print("🚀 AceFlow 项目初始化向导")
        print("=" * 50)
        
        # 检查是否已经初始化
        if self.aceflow_dir.exists():
            if not questionary.confirm(
                "当前目录已经包含 AceFlow 配置，是否重新初始化？",
                default=False
            ).ask():
                print("初始化已取消")
                return
        
        # 收集项目信息
        project_info = self._collect_project_info()
        
        # 选择流程模式
        flow_mode = self._select_flow_mode(project_info)
        
        # 配置敏捷集成
        agile_config = self._configure_agile_integration()
        
        # 生成项目配置
        self._generate_project_config(project_info, flow_mode, agile_config)
        
        # 创建项目结构
        self._create_project_structure(flow_mode)
        
        # 生成初始模板
        self._generate_initial_templates(flow_mode)
        
        # 显示完成信息
        self._show_completion_info(flow_mode)
        
    def _collect_project_info(self) -> Dict:
        """收集项目基本信息"""
        print("\\n📋 项目信息收集")
        print("-" * 20)
        
        project_info = {
            'name': questionary.text(
                "项目名称:",
                default=self.project_root.name
            ).ask(),
            
            'description': questionary.text(
                "项目描述:",
                default=""
            ).ask(),
            
            'team_size': questionary.select(
                "团队规模:",
                choices=[
                    "1-3人 (小型团队)",
                    "4-8人 (中型团队)", 
                    "9-15人 (大型团队)",
                    "15+人 (企业团队)"
                ]
            ).ask(),
            
            'project_duration': questionary.select(
                "项目周期:",
                choices=[
                    "1-7天 (快速迭代)",
                    "1-4周 (短期项目)",
                    "1-3个月 (中期项目)",
                    "3+个月 (长期项目)"
                ]
            ).ask(),
            
            'project_type': questionary.select(
                "项目类型:",
                choices=[
                    "Web应用",
                    "移动应用",
                    "桌面应用",
                    "API/微服务",
                    "数据分析",
                    "机器学习",
                    "其他"
                ]
            ).ask(),
            
            'tech_stack': self._detect_tech_stack()
        }
        
        # 提取数字用于决策
        project_info['team_size_num'] = int(project_info['team_size'].split('-')[0])
        project_info['is_short_term'] = '1-7天' in project_info['project_duration'] or '1-4周' in project_info['project_duration']
        
        return project_info
    
    def _detect_tech_stack(self) -> Dict:
        """自动检测技术栈"""
        tech_stack = {
            'frontend': [],
            'backend': [],
            'database': [],
            'tools': []
        }
        
        # 检测前端技术
        if (self.project_root / "package.json").exists():
            try:
                with open(self.project_root / "package.json", 'r') as f:
                    package_json = json.load(f)
                    deps = {**package_json.get('dependencies', {}), **package_json.get('devDependencies', {})}
                    
                    if 'react' in deps:
                        tech_stack['frontend'].append('React')
                    if 'vue' in deps:
                        tech_stack['frontend'].append('Vue.js')
                    if 'angular' in deps:
                        tech_stack['frontend'].append('Angular')
                    if 'next' in deps:
                        tech_stack['frontend'].append('Next.js')
                        
            except Exception:
                pass
        
        # 检测后端技术
        if (self.project_root / "requirements.txt").exists():
            tech_stack['backend'].append('Python')
        if (self.project_root / "pom.xml").exists():
            tech_stack['backend'].append('Java')
        if (self.project_root / "go.mod").exists():
            tech_stack['backend'].append('Go')
        if (self.project_root / "Cargo.toml").exists():
            tech_stack['backend'].append('Rust')
            
        # 检测数据库
        config_files = ['.env', 'docker-compose.yml', 'config.yml']
        for config_file in config_files:
            if (self.project_root / config_file).exists():
                try:
                    with open(self.project_root / config_file, 'r') as f:
                        content = f.read().lower()
                        if 'mysql' in content:
                            tech_stack['database'].append('MySQL')
                        if 'postgresql' in content or 'postgres' in content:
                            tech_stack['database'].append('PostgreSQL')
                        if 'mongodb' in content:
                            tech_stack['database'].append('MongoDB')
                        if 'redis' in content:
                            tech_stack['database'].append('Redis')
                except Exception:
                    pass
        
        return tech_stack
    
    def _select_flow_mode(self, project_info: Dict) -> str:
        """选择流程模式"""
        print("\\n🔄 流程模式选择")
        print("-" * 20)
        
        # 智能推荐
        recommended_mode = self._recommend_flow_mode(project_info)
        
        mode_choices = [
            {
                'name': f"轻量级模式 (P→D→R) {'✅ 推荐' if recommended_mode == 'minimal' else ''}",
                'value': 'minimal'
            },
            {
                'name': f"标准模式 (P1→P2→D1→D2→R1) {'✅ 推荐' if recommended_mode == 'standard' else ''}",
                'value': 'standard'
            },
            {
                'name': f"完整模式 (S1→S2→S3→S4→S5→S6→S7→S8) {'✅ 推荐' if recommended_mode == 'complete' else ''}",
                'value': 'complete'
            }
        ]
        
        print(f"基于项目信息，推荐使用: {self._get_mode_name(recommended_mode)}")
        
        selected_mode = questionary.select(
            "选择流程模式:",
            choices=mode_choices
        ).ask()
        
        return selected_mode
    
    def _recommend_flow_mode(self, project_info: Dict) -> str:
        """基于项目信息推荐流程模式"""
        team_size = project_info['team_size_num']
        is_short_term = project_info['is_short_term']
        
        if team_size <= 5 and is_short_term:
            return 'minimal'
        elif team_size <= 10 and not '3+个月' in project_info['project_duration']:
            return 'standard'
        else:
            return 'complete'
    
    def _get_mode_name(self, mode: str) -> str:
        """获取模式显示名称"""
        mode_names = {
            'minimal': '轻量级模式',
            'standard': '标准模式',
            'complete': '完整模式'
        }
        return mode_names.get(mode, mode)
    
    def _configure_agile_integration(self) -> Dict:
        """配置敏捷集成"""
        print("\\n🏃 敏捷集成配置")
        print("-" * 20)
        
        enable_agile = questionary.confirm(
            "是否启用敏捷开发集成？",
            default=True
        ).ask()
        
        if not enable_agile:
            return {'enabled': False}
        
        framework = questionary.select(
            "选择敏捷框架:",
            choices=[
                "Scrum",
                "Kanban", 
                "自定义",
                "暂不配置"
            ]
        ).ask()
        
        config = {
            'enabled': True,
            'framework': framework.lower()
        }
        
        if framework == "Scrum":
            config.update({
                'iteration_length': questionary.select(
                    "Sprint长度:",
                    choices=["1周", "2周", "3周", "4周"]
                ).ask(),
                'ceremonies': {
                    'planning': True,
                    'daily_standup': True,
                    'review': True,
                    'retrospective': True
                }
            })
        elif framework == "Kanban":
            config.update({
                'lanes': ["待办", "进行中", "评审", "完成"],
                'wip_limits': {
                    '进行中': 3,
                    '评审': 2
                }
            })
        
        return config
    
    def _generate_project_config(self, project_info: Dict, flow_mode: str, agile_config: Dict):
        """生成项目配置文件"""
        config = {
            'project': {
                'name': project_info['name'],
                'description': project_info['description'],
                'created_at': datetime.now().isoformat(),
                'team_size': project_info['team_size'],
                'project_duration': project_info['project_duration'],
                'project_type': project_info['project_type'],
                'tech_stack': project_info['tech_stack']
            },
            'flow': {
                'mode': flow_mode,
                'auto_switch': True,
                'current_stage': self._get_initial_stage(flow_mode)
            },
            'agile': agile_config,
            'ai': {
                'enabled': True,
                'decision_support': True,
                'auto_recommendations': True
            },
            'memory': {
                'enabled': True,
                'retention_days': 30,
                'auto_cleanup': True
            }
        }
        
        self.config = config
        
        # 保存配置
        self.aceflow_dir.mkdir(parents=True, exist_ok=True)
        with open(self.aceflow_dir / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    def _get_initial_stage(self, flow_mode: str) -> str:
        """获取初始阶段"""
        initial_stages = {
            'minimal': 'P',
            'standard': 'P1',
            'complete': 'S1'
        }
        return initial_stages.get(flow_mode, 'P')
    
    def _create_project_structure(self, flow_mode: str):
        """创建项目目录结构"""
        
        # 创建基础目录
        directories = [
            self.aceflow_dir / "templates",
            self.aceflow_dir / "memory_pool",
            self.aceflow_dir / "config",
            self.aceflow_dir / "scripts"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        # 创建状态文件
        initial_state = {
            'current_stage': self._get_initial_stage(flow_mode),
            'flow_mode': flow_mode,
            'stage_status': {},
            'progress': {},
            'memory_ids': [],
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.aceflow_dir / "current_state.json", 'w') as f:
            json.dump(initial_state, f, indent=2)
    
    def _generate_initial_templates(self, flow_mode: str):
        """生成初始模板文件"""
        templates_dir = self.aceflow_dir / "templates"
        
        if flow_mode == 'minimal':
            self._create_minimal_templates(templates_dir)
        elif flow_mode == 'standard':
            self._create_standard_templates(templates_dir)
        else:
            self._create_complete_templates(templates_dir)
    
    def _create_minimal_templates(self, templates_dir: Path):
        """创建轻量级模板"""
        
        # P阶段模板
        p_template = """# 规划阶段 (Planning)

## 项目概述
- **项目名称**: {project_name}
- **负责人**: 
- **预计工期**: 
- **优先级**: 

## 需求描述
### 用户故事
作为 [用户角色]，我希望 [功能描述]，以便 [价值/目标]。

### 验收标准
- [ ] 标准1
- [ ] 标准2
- [ ] 标准3

## 任务清单
- [ ] 任务1
- [ ] 任务2
- [ ] 任务3

## 风险评估
- **技术风险**: 
- **时间风险**: 
- **资源风险**: 

---
*创建时间: {created_at}*
*模板版本: minimal-v1.0*
"""
        
        # D阶段模板
        d_template = """# 开发阶段 (Development)

## 开发计划
- **开始时间**: 
- **预计完成**: 
- **开发人员**: 

## 技术方案
### 架构设计
- **技术栈**: 
- **核心组件**: 
- **数据结构**: 

### 实现计划
- [ ] 环境搭建
- [ ] 核心功能开发
- [ ] 单元测试
- [ ] 集成测试

## 开发日志
### [日期] 
- **进展**: 
- **问题**: 
- **解决方案**: 

## 代码提交
- **分支**: 
- **提交记录**: 
- **代码评审**: 

---
*创建时间: {created_at}*
*模板版本: minimal-v1.0*
"""
        
        # R阶段模板
        r_template = """# 评审阶段 (Review)

## 功能验证
### 验收测试
- [ ] 功能测试通过
- [ ] 性能测试通过
- [ ] 兼容性测试通过
- [ ] 安全测试通过

### 问题清单
| 问题描述 | 严重程度 | 状态 | 负责人 |
|----------|----------|------|--------|
|          |          |      |        |

## 代码质量
- **代码覆盖率**: 
- **静态分析**: 
- **代码规范**: 

## 部署准备
- [ ] 部署文档更新
- [ ] 配置文件准备
- [ ] 数据库迁移
- [ ] 回滚方案

## 交付物
- [ ] 功能代码
- [ ] 测试报告
- [ ] 部署文档
- [ ] 用户手册

---
*创建时间: {created_at}*
*模板版本: minimal-v1.0*
"""
        
        # 写入模板文件
        templates = {
            'P_planning.md': p_template,
            'D_development.md': d_template,
            'R_review.md': r_template
        }
        
        for filename, content in templates.items():
            with open(templates_dir / filename, 'w', encoding='utf-8') as f:
                f.write(content.format(
                    project_name=self.config['project']['name'],
                    created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ))
    
    def _create_standard_templates(self, templates_dir: Path):
        """创建标准模板"""
        # TODO: 实现标准模式模板
        pass
    
    def _create_complete_templates(self, templates_dir: Path):
        """创建完整模板"""
        # TODO: 实现完整模式模板
        pass
    
    def _show_completion_info(self, flow_mode: str):
        """显示完成信息"""
        print("\\n🎉 AceFlow 项目初始化完成！")
        print("=" * 50)
        print(f"✅ 流程模式: {self._get_mode_name(flow_mode)}")
        print(f"✅ 项目名称: {self.config['project']['name']}")
        print(f"✅ 配置文件: {self.aceflow_dir / 'config.yaml'}")
        print(f"✅ 状态文件: {self.aceflow_dir / 'current_state.json'}")
        
        print("\\n🚀 快速开始:")
        print("1. aceflow status        # 查看当前状态")
        print("2. aceflow next          # 获取下一步建议")
        print("3. aceflow progress      # 更新进度")
        
        if self.config['agile']['enabled']:
            print("\\n🏃 敏捷集成:")
            print(f"- 框架: {self.config['agile']['framework']}")
            if self.config['agile']['framework'] == 'scrum':
                print(f"- Sprint长度: {self.config['agile']['iteration_length']}")
        
        print("\\n📖 更多帮助:")
        print("- aceflow help           # 查看帮助")
        print("- aceflow docs           # 打开文档")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AceFlow 项目初始化向导')
    parser.add_argument('--mode', choices=['minimal', 'standard', 'complete'], 
                       help='直接指定流程模式')
    parser.add_argument('--non-interactive', action='store_true', 
                       help='非交互式模式')
    
    args = parser.parse_args()
    
    try:
        wizard = AceFlowInitWizard()
        
        if args.non_interactive:
            # TODO: 实现非交互式初始化
            print("非交互式模式尚未实现")
            sys.exit(1)
        else:
            wizard.run()
            
    except KeyboardInterrupt:
        print("\\n\\n用户取消初始化")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ 初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()