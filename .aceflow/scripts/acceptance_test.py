#!/usr/bin/env python3
"""
AceFlow v2.0 第1阶段验收测试脚本
全面测试核心功能和用户体验
"""

import os
import sys
import json
import yaml
import subprocess
import time
from pathlib import Path
from datetime import datetime

class AceFlowAcceptanceTest:
    def __init__(self):
        self.project_root = Path.cwd()
        self.aceflow_dir = self.project_root / ".aceflow"
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test(self, test_name, passed, message=""):
        """记录测试结果"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = f"{status} {test_name}"
        if message:
            result += f" - {message}"
        
        self.test_results.append(result)
        print(result)
        return passed
    
    def run_command(self, command, expect_success=True):
        """运行命令并返回结果"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                cwd=self.project_root
            )
            
            if expect_success:
                return result.returncode == 0, result.stdout, result.stderr
            else:
                return result.returncode != 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def test_directory_structure(self):
        """测试目录结构完整性"""
        print("\n🗂️  测试目录结构...")
        
        required_dirs = [
            ".aceflow",
            ".aceflow/scripts",
            ".aceflow/config", 
            ".aceflow/templates",
            ".aceflow/web",
            ".aceflow/state",
            ".aceflow/templates/minimal",
            ".aceflow/templates/standard"
        ]
        
        for dir_path in required_dirs:
            path = self.project_root / dir_path
            self.log_test(
                f"目录存在: {dir_path}",
                path.exists() and path.is_dir()
            )
    
    def test_core_files(self):
        """测试核心文件存在性"""
        print("\n📄 测试核心文件...")
        
        required_files = [
            ".aceflow/scripts/aceflow",
            ".aceflow/scripts/wizard.py", 
            ".aceflow/config.yaml",
            ".aceflow/state/project_state.json",
            ".aceflow/config/flow_modes.yaml",
            ".aceflow/config/agile_integration.yaml",
            ".aceflow/web/index.html",
            ".aceflow/templates/minimal/template.yaml",
            ".aceflow/templates/minimal/requirements.md",
            ".aceflow/templates/minimal/tasks.md",
            ".aceflow/templates/standard/template.yaml",
            ".clineignore",
            ".clinerules/quality_rules.yaml"
        ]
        
        for file_path in required_files:
            path = self.project_root / file_path
            self.log_test(
                f"文件存在: {file_path}",
                path.exists() and path.is_file()
            )
    
    def test_file_permissions(self):
        """测试文件权限"""
        print("\n🔐 测试文件权限...")
        
        executable_files = [
            ".aceflow/scripts/aceflow",
            ".aceflow/scripts/wizard.py"
        ]
        
        for file_path in executable_files:
            path = self.project_root / file_path
            if path.exists():
                is_executable = os.access(path, os.X_OK)
                self.log_test(
                    f"可执行权限: {file_path}",
                    is_executable
                )
    
    def test_config_files(self):
        """测试配置文件格式"""
        print("\n⚙️  测试配置文件...")
        
        # 测试主配置文件
        config_file = self.aceflow_dir / "config.yaml"
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 检查必需的配置项
            required_keys = ['project', 'flow', 'agile', 'ai', 'web']
            all_keys_present = all(key in config for key in required_keys)
            
            self.log_test(
                "主配置文件格式正确",
                all_keys_present,
                f"包含所需配置项: {required_keys}"
            )
            
        except Exception as e:
            self.log_test(
                "主配置文件格式正确",
                False,
                f"解析错误: {e}"
            )
        
        # 测试状态文件
        state_file = self.aceflow_dir / "state" / "project_state.json"
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            required_keys = ['project_id', 'flow_mode', 'current_stage', 'stage_states']
            all_keys_present = all(key in state for key in required_keys)
            
            self.log_test(
                "状态文件格式正确",
                all_keys_present,
                f"包含所需状态项: {required_keys}"
            )
            
        except Exception as e:
            self.log_test(
                "状态文件格式正确",
                False,
                f"解析错误: {e}"
            )
    
    def test_cli_commands(self):
        """测试CLI命令功能"""
        print("\n🖥️  测试CLI命令...")
        
        # 测试help命令
        success, stdout, stderr = self.run_command("python3 .aceflow/scripts/aceflow help")
        self.log_test(
            "help命令正常",
            success and "AceFlow v2.0" in stdout
        )
        
        # 测试status命令
        success, stdout, stderr = self.run_command("python3 .aceflow/scripts/aceflow status")
        self.log_test(
            "status命令正常",
            success and "项目状态" in stdout
        )
        
        # 测试start命令（如果还没有活跃阶段）
        success, stdout, stderr = self.run_command("python3 .aceflow/scripts/aceflow start")
        if "已开始阶段" in stdout or "当前已有活跃阶段" in stdout:
            self.log_test("start命令正常", True)
        else:
            self.log_test("start命令正常", success)
        
        # 测试progress命令
        success, stdout, stderr = self.run_command("python3 .aceflow/scripts/aceflow progress --progress 50")
        if "进度更新" in stdout or "没有活跃的阶段" in stdout:
            self.log_test("progress命令正常", True)
        else:
            self.log_test("progress命令正常", success)
        
        # 测试web命令
        success, stdout, stderr = self.run_command("python3 .aceflow/scripts/aceflow web")
        self.log_test(
            "web命令正常",
            success and ("Web界面已打开" in stdout or "index.html" in stdout)
        )
    
    def test_flow_modes(self):
        """测试流程模式配置"""
        print("\n🔄 测试流程模式...")
        
        flow_config_file = self.aceflow_dir / "config" / "flow_modes.yaml"
        try:
            with open(flow_config_file, 'r', encoding='utf-8') as f:
                flow_config = yaml.safe_load(f)
            
            # 检查三种模式是否都存在
            required_modes = ['minimal', 'standard', 'complete']
            modes_exist = all(mode in flow_config['flow_modes'] for mode in required_modes)
            
            self.log_test(
                "流程模式配置完整",
                modes_exist,
                f"包含模式: {required_modes}"
            )
            
            # 检查轻量级模式的阶段配置
            minimal_mode = flow_config['flow_modes']['minimal']
            minimal_stages = minimal_mode.get('stages', {})
            expected_stages = ['P', 'D', 'R']
            stages_correct = all(stage in minimal_stages for stage in expected_stages)
            
            self.log_test(
                "轻量级模式阶段正确",
                stages_correct,
                f"包含阶段: {expected_stages}"
            )
            
        except Exception as e:
            self.log_test(
                "流程模式配置完整",
                False,
                f"配置错误: {e}"
            )
    
    def test_templates(self):
        """测试项目模板"""
        print("\n📋 测试项目模板...")
        
        # 测试轻量级模板
        minimal_template = self.aceflow_dir / "templates" / "minimal" / "template.yaml"
        try:
            with open(minimal_template, 'r', encoding='utf-8') as f:
                template = yaml.safe_load(f)
            
            has_project_config = 'project' in template
            has_flow_config = 'flow' in template
            has_init_config = 'initialization' in template
            
            self.log_test(
                "轻量级模板配置正确",
                has_project_config and has_flow_config and has_init_config
            )
            
        except Exception as e:
            self.log_test(
                "轻量级模板配置正确",
                False,
                f"模板错误: {e}"
            )
        
        # 测试模板文档文件
        template_docs = [
            ".aceflow/templates/minimal/requirements.md",
            ".aceflow/templates/minimal/tasks.md"
        ]
        
        for doc_file in template_docs:
            path = self.project_root / doc_file
            content_exists = False
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_exists = len(content.strip()) > 0
            
            self.log_test(
                f"模板文档: {Path(doc_file).name}",
                content_exists
            )
    
    def test_web_interface(self):
        """测试Web界面"""
        print("\n🌐 测试Web界面...")
        
        web_file = self.aceflow_dir / "web" / "index.html"
        
        if web_file.exists():
            with open(web_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查关键HTML元素
            has_title = "AceFlow" in content
            has_styles = "<style>" in content
            has_scripts = "<script>" in content
            has_flow_modes = "flow-modes" in content
            has_stages = "stages-container" in content
            
            self.log_test(
                "Web界面HTML结构完整",
                has_title and has_styles and has_scripts
            )
            
            self.log_test(
                "Web界面功能组件完整",
                has_flow_modes and has_stages
            )
            
            # 检查响应式设计
            has_responsive = "@media" in content
            self.log_test(
                "Web界面支持响应式设计",
                has_responsive
            )
        else:
            self.log_test("Web界面文件存在", False)
    
    def test_agile_integration(self):
        """测试敏捷集成配置"""
        print("\n🔄 测试敏捷集成...")
        
        agile_config_file = self.aceflow_dir / "config" / "agile_integration.yaml"
        try:
            with open(agile_config_file, 'r', encoding='utf-8') as f:
                agile_config = yaml.safe_load(f)
            
            # 检查敏捷框架配置
            has_scrum = 'scrum' in agile_config.get('agile_frameworks', {})
            has_kanban = 'kanban' in agile_config.get('agile_frameworks', {})
            has_integration = 'integration_templates' in agile_config
            
            self.log_test(
                "敏捷框架配置完整",
                has_scrum and has_kanban and has_integration
            )
            
            # 检查Scrum配置详细信息
            if has_scrum:
                scrum_config = agile_config['agile_frameworks']['scrum']
                has_ceremonies = 'ceremonies' in scrum_config
                has_artifacts = 'artifacts' in scrum_config
                has_integration_mapping = 'integration' in scrum_config
                
                self.log_test(
                    "Scrum配置详细完整",
                    has_ceremonies and has_artifacts and has_integration_mapping
                )
            
        except Exception as e:
            self.log_test(
                "敏捷集成配置完整",
                False,
                f"配置错误: {e}"
            )
    
    def test_wizard_functionality(self):
        """测试快速启动向导"""
        print("\n🧙 测试快速启动向导...")
        
        wizard_file = self.aceflow_dir / "scripts" / "wizard.py"
        
        if wizard_file.exists():
            # 检查向导脚本的基本结构
            with open(wizard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_wizard_class = "class AceFlowWizard" in content
            has_main_function = "def main(" in content
            has_template_selection = "select_template" in content
            has_project_config = "configure_project" in content
            
            self.log_test(
                "快速启动向导结构完整",
                has_wizard_class and has_main_function
            )
            
            self.log_test(
                "向导功能模块完整",
                has_template_selection and has_project_config
            )
            
            # 测试向导脚本语法正确性
            success, stdout, stderr = self.run_command("python3 -m py_compile .aceflow/scripts/wizard.py")
            self.log_test(
                "向导脚本语法正确",
                success
            )
        else:
            self.log_test("快速启动向导文件存在", False)
    
    def test_documentation_quality(self):
        """测试文档质量"""
        print("\n📚 测试文档质量...")
        
        # 检查项目级文档
        doc_files = [
            "AceFlow_Optimization_Plan.md",
            "AceFlow_Migration_Guide.md", 
            "AceFlow_Quick_Start_Guide.md"
        ]
        
        for doc_file in doc_files:
            path = self.project_root / doc_file
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查文档长度和结构
                has_content = len(content) > 1000  # 至少1000字符
                has_headers = content.count('#') >= 5  # 至少5个标题
                has_chinese = any('\u4e00' <= char <= '\u9fff' for char in content)  # 包含中文
                
                self.log_test(
                    f"文档质量: {doc_file}",
                    has_content and has_headers and has_chinese
                )
            else:
                self.log_test(f"文档存在: {doc_file}", False)
    
    def test_integration_complete(self):
        """测试整体集成完整性"""
        print("\n🔗 测试整体集成...")
        
        # 测试从初始化到完成一个完整流程
        try:
            # 备份当前状态
            state_file = self.aceflow_dir / "state" / "project_state.json"
            backup_file = self.aceflow_dir / "state" / "project_state_backup.json"
            
            if state_file.exists():
                with open(state_file, 'r') as f:
                    original_state = f.read()
                with open(backup_file, 'w') as f:
                    f.write(original_state)
            
            # 测试完整工作流
            workflow_success = True
            
            # 1. 开始阶段
            success, stdout, stderr = self.run_command("python3 .aceflow/scripts/aceflow start P")
            if not success and "当前已有活跃阶段" not in stdout:
                workflow_success = False
            
            # 2. 更新进度
            success, stdout, stderr = self.run_command("python3 .aceflow/scripts/aceflow progress --progress 100")
            if not success and "进度更新" not in stdout:
                workflow_success = False
            
            # 3. 完成阶段
            success, stdout, stderr = self.run_command("python3 .aceflow/scripts/aceflow complete")
            if not success and "完成阶段" not in stdout:
                workflow_success = False
            
            self.log_test(
                "完整工作流测试",
                workflow_success
            )
            
            # 恢复原始状态
            if backup_file.exists():
                with open(backup_file, 'r') as f:
                    original_state = f.read()
                with open(state_file, 'w') as f:
                    f.write(original_state)
                backup_file.unlink()
            
        except Exception as e:
            self.log_test(
                "完整工作流测试",
                False,
                f"测试错误: {e}"
            )
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🧪 开始AceFlow v2.0第1阶段验收测试")
        print("=" * 60)
        
        start_time = time.time()
        
        # 运行所有测试
        self.test_directory_structure()
        self.test_core_files()
        self.test_file_permissions()
        self.test_config_files()
        self.test_cli_commands()
        self.test_flow_modes()
        self.test_templates()
        self.test_web_interface()
        self.test_agile_integration()
        self.test_wizard_functionality()
        self.test_documentation_quality()
        self.test_integration_complete()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 生成测试报告
        self.generate_report(duration)
    
    def generate_report(self, duration):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 验收测试报告")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"📈 测试统计:")
        print(f"   总测试数: {self.total_tests}")
        print(f"   通过测试: {self.passed_tests}")
        print(f"   失败测试: {self.total_tests - self.passed_tests}")
        print(f"   成功率: {success_rate:.1f}%")
        print(f"   测试耗时: {duration:.2f}秒")
        
        print(f"\n📋 详细结果:")
        for result in self.test_results:
            print(f"   {result}")
        
        # 总体评估
        print(f"\n🎯 验收结果:")
        if success_rate >= 90:
            print("   🎉 验收通过 - 第1阶段开发目标已达成")
            print("   ✨ 系统功能完整，质量良好，可以进入第2阶段")
        elif success_rate >= 80:
            print("   ⚠️  有条件通过 - 存在少量问题需要修复")
            print("   🔧 建议修复失败项后再进入下一阶段")
        else:
            print("   ❌ 验收未通过 - 存在重大问题需要解决")
            print("   🛠️  需要重点修复失败项目")
        
        # 保存报告
        self.save_report(duration, success_rate)
    
    def save_report(self, duration, success_rate):
        """保存测试报告到文件"""
        report_data = {
            "test_time": datetime.now().isoformat(),
            "duration_seconds": duration,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.total_tests - self.passed_tests,
            "success_rate": success_rate,
            "test_results": self.test_results,
            "stage": "第1阶段验收测试",
            "version": "AceFlow v2.0"
        }
        
        # 创建报告目录
        reports_dir = self.aceflow_dir / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        # 保存JSON格式报告
        report_file = reports_dir / f"acceptance_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 测试报告已保存: {report_file}")

def main():
    """主函数"""
    print("🚀 AceFlow v2.0 第1阶段验收测试")
    print("测试AI驱动的敏捷开发工作流框架核心功能")
    print()
    
    # 检查是否在正确的项目目录
    aceflow_dir = Path(".aceflow")
    if not aceflow_dir.exists():
        print("❌ 错误: 当前目录不是AceFlow项目目录")
        print("请在包含.aceflow目录的项目根目录下运行此脚本")
        sys.exit(1)
    
    # 运行测试
    tester = AceFlowAcceptanceTest()
    tester.run_all_tests()

if __name__ == "__main__":
    main()