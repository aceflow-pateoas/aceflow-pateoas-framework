# 快速启动向导
# 交互式项目初始化工具

#!/usr/bin/env python3
"""
AceFlow 快速启动向导
帮助用户快速初始化新项目
"""

import os
import yaml
import json
from pathlib import Path
from datetime import datetime

class AceFlowWizard:
    def __init__(self):
        self.aceflow_dir = Path(".aceflow")
        self.templates_dir = self.aceflow_dir / "templates"
        self.project_config = {}
        
    def run(self):
        """运行快速启动向导"""
        print("🚀 欢迎使用 AceFlow 快速启动向导")
        print("=" * 50)
        
        # 1. 项目基本信息
        self.collect_basic_info()
        
        # 2. 选择项目模板
        template = self.select_template()
        
        # 3. 配置项目参数
        self.configure_project(template)
        
        # 4. 初始化项目
        self.initialize_project(template)
        
        print("\n🎉 项目初始化完成！")
        self.show_next_steps()
    
    def collect_basic_info(self):
        """收集项目基本信息"""
        print("\n📋 项目基本信息")
        print("-" * 20)
        
        self.project_config['name'] = input("项目名称: ").strip()
        self.project_config['description'] = input("项目描述 (可选): ").strip()
        
        # 团队规模
        print("\n团队规模:")
        print("1. 1-3人 (个人/小团队)")
        print("2. 4-10人 (中型团队)")
        print("3. 10+人 (大型团队)")
        
        team_choice = input("请选择 (1-3): ").strip()
        team_sizes = {
            '1': '1-3人',
            '2': '4-10人', 
            '3': '10+人'
        }
        self.project_config['team_size'] = team_sizes.get(team_choice, '1-3人')
        
        # 项目周期
        print("\n预期开发周期:")
        print("1. <1周 (快速原型/小功能)")
        print("2. 1-4周 (中型功能)")
        print("3. 1-3月 (完整应用)")
        print("4. >3月 (大型系统)")
        
        duration_choice = input("请选择 (1-4): ").strip()
        durations = {
            '1': '<1周',
            '2': '1-4周',
            '3': '1-3月',
            '4': '>3月'
        }
        self.project_config['duration'] = durations.get(duration_choice, '1-4周')
    
    def select_template(self):
        """选择项目模板"""
        print("\n🎯 选择流程模式")
        print("-" * 20)
        
        # 智能推荐
        recommended = self.recommend_template()
        print(f"💡 AI推荐: {recommended['name']} ({recommended['reason']})")
        
        print("\n可用模式:")
        templates = {
            '1': {
                'id': 'minimal',
                'name': '轻量级模式',
                'stages': 'P→D→R (3阶段)',
                'duration': '2-7天',
                'suitable': '小型项目、快速迭代、原型验证'
            },
            '2': {
                'id': 'standard', 
                'name': '标准模式',
                'stages': 'P1→P2→D1→D2→R1 (5阶段)',
                'duration': '1-2周',
                'suitable': '中型项目、敏捷团队、企业应用'
            },
            '3': {
                'id': 'complete',
                'name': '完整模式', 
                'stages': 'S1→...→S8 (8阶段)',
                'duration': '2-4周',
                'suitable': '大型项目、关键系统、严格质量控制'
            }
        }
        
        for key, template in templates.items():
            print(f"{key}. {template['name']}")
            print(f"   流程: {template['stages']}")
            print(f"   周期: {template['duration']}")
            print(f"   适用: {template['suitable']}")
            print()
        
        choice = input(f"请选择模式 (1-3, 推荐: {recommended['choice']}): ").strip()
        if not choice:
            choice = recommended['choice']
        
        selected_template = templates.get(choice, templates['1'])
        print(f"✅ 已选择: {selected_template['name']}")
        
        return selected_template
    
    def recommend_template(self):
        """智能推荐模板"""
        team_size = self.project_config['team_size']
        duration = self.project_config['duration']
        
        # 简单的推荐逻辑
        if '1-3人' in team_size and ('<1周' in duration or '1-4周' in duration):
            return {
                'choice': '1',
                'name': '轻量级模式',
                'reason': '小团队短周期项目，适合快速迭代'
            }
        elif '4-10人' in team_size and '1-4周' in duration:
            return {
                'choice': '2', 
                'name': '标准模式',
                'reason': '中型团队，需要平衡效率和质量'
            }
        elif '10+人' in team_size or '>3月' in duration:
            return {
                'choice': '3',
                'name': '完整模式', 
                'reason': '大型团队或长周期项目，需要严格质量控制'
            }
        else:
            return {
                'choice': '2',
                'name': '标准模式',
                'reason': '通用选择，适合大部分项目'
            }
    
    def configure_project(self, template):
        """配置项目参数"""
        print(f"\n⚙️ 配置 {template['name']}")
        print("-" * 20)
        
        # 加载模板配置
        template_file = self.templates_dir / template['id'] / "template.yaml"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                template_config = yaml.safe_load(f)
            
            # 根据模板提示收集额外信息
            if 'initialization' in template_config and 'prompts' in template_config['initialization']:
                for prompt in template_config['initialization']['prompts']:
                    if prompt.get('required', False) or input(f"配置 {prompt['question']}? (y/n): ").lower().startswith('y'):
                        if prompt['type'] == 'select':
                            print(f"{prompt['question']}:")
                            for i, option in enumerate(prompt['options'], 1):
                                print(f"  {i}. {option}")
                            choice = input("请选择: ").strip()
                            try:
                                self.project_config[prompt['key']] = prompt['options'][int(choice)-1]
                            except (ValueError, IndexError):
                                self.project_config[prompt['key']] = prompt['options'][0]
                        else:
                            self.project_config[prompt['key']] = input(f"{prompt['question']}: ").strip()
        
        # 敏捷集成选项
        print("\n🔄 敏捷集成:")
        print("1. Scrum")
        print("2. Kanban") 
        print("3. 不使用")
        
        agile_choice = input("选择敏捷框架 (1-3): ").strip()
        agile_frameworks = {'1': 'scrum', '2': 'kanban', '3': 'none'}
        self.project_config['agile_framework'] = agile_frameworks.get(agile_choice, 'none')
        
        if self.project_config['agile_framework'] != 'none':
            self.project_config['iteration_length'] = input("迭代周期 (如: 2weeks): ").strip() or "2weeks"
    
    def initialize_project(self, template):
        """初始化项目"""
        print(f"\n🔨 初始化项目...")
        
        # 创建配置文件
        config = {
            'project': {
                'name': self.project_config.get('name', 'Untitled Project'),
                'description': self.project_config.get('description', ''),
                'team_size': self.project_config.get('team_size', '1-3人'),
                'created_at': datetime.now().isoformat(),
                'template': template['id']
            },
            'flow': {
                'mode': template['id'],
                'current_stage': None
            },
            'agile': {
                'enabled': self.project_config['agile_framework'] != 'none',
                'framework': self.project_config.get('agile_framework', 'none'),
                'iteration_length': self.project_config.get('iteration_length', '2weeks')
            },
            'ai': {
                'enabled': True,
                'auto_recommendations': True
            }
        }
        
        # 保存配置
        config_file = self.aceflow_dir / "config.yaml"
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        # 初始化状态
        state = {
            'project_id': self.project_config.get('name', 'untitled').lower().replace(' ', '-'),
            'flow_mode': template['id'],
            'current_stage': None,
            'stage_states': {},
            'created_at': datetime.now().isoformat(),
            'version': '2.0.0',
            'progress': {'overall': 0, 'stages': {}},
            'deliverables': {},
            'memory_pool': {'requirements': [], 'decisions': [], 'issues': []}
        }
        
        state_file = self.aceflow_dir / "state" / "project_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print("✅ 配置文件已创建")
        print("✅ 项目状态已初始化")
        
        # 复制模板文件
        self.copy_template_files(template)
    
    def copy_template_files(self, template):
        """复制模板文件到项目"""
        template_dir = self.templates_dir / template['id']
        
        if not template_dir.exists():
            print("⚠️  模板文件不存在，跳过文件复制")
            return
        
        # 创建文档目录
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)
        
        # 复制markdown模板文件
        for template_file in template_dir.glob("*.md"):
            target_file = docs_dir / template_file.name
            
            # 读取模板内容并替换变量
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单的变量替换
            for key, value in self.project_config.items():
                content = content.replace(f"{{{{{key}}}}}", str(value))
            
            # 写入目标文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print("✅ 模板文件已复制到 docs/ 目录")
    
    def show_next_steps(self):
        """显示下一步操作建议"""
        print("\n🎯 下一步操作:")
        print("1. python .aceflow/scripts/aceflow status  # 查看项目状态")
        print("2. python .aceflow/scripts/aceflow start   # 开始第一个阶段")
        print("3. python .aceflow/scripts/aceflow web     # 打开Web界面")
        print("\n📚 文档位置:")
        print("- 项目文档: docs/ 目录")
        print("- 配置文件: .aceflow/config.yaml")
        print("- 状态文件: .aceflow/state/project_state.json")

def main():
    """主函数"""
    wizard = AceFlowWizard()
    try:
        wizard.run()
    except KeyboardInterrupt:
        print("\n\n👋 已取消初始化")
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")

if __name__ == "__main__":
    main()