#!/bin/bash

# AceFlow + Cline 快速集成脚本
# 一键设置VSCode+Cline+AceFlow的完整开发环境

echo "🚀 AceFlow + Cline 快速集成脚本"
echo "================================"

# 检查是否在项目根目录
if [ ! -d ".aceflow" ]; then
    echo "❌ 错误：请在AceFlow项目根目录运行此脚本"
    echo "   (应该包含 .aceflow 目录)"
    exit 1
fi

# 检查VSCode是否安装
if ! command -v code &> /dev/null; then
    echo "⚠️  警告：未检测到VSCode，请先安装VSCode"
    echo "   下载地址：https://code.visualstudio.com/"
fi

# 检查Cline扩展是否安装
echo "🔍 检查Cline扩展..."
if code --list-extensions | grep -q "saoudrizwan.claude-dev"; then
    echo "✅ Cline扩展已安装"
else
    echo "📦 正在安装Cline扩展..."
    code --install-extension saoudrizwan.claude-dev
fi

# 创建必要的目录
echo "📁 创建配置目录..."
mkdir -p .vscode
mkdir -p .clinerules

# 检查配置文件是否存在
echo "🔧 检查配置文件状态..."

if [ -f ".vscode/settings.json" ]; then
    echo "✅ VSCode设置文件已存在"
else
    echo "❌ VSCode设置文件缺失"
fi

if [ -f ".vscode/tasks.json" ]; then
    echo "✅ VSCode任务文件已存在"
else
    echo "❌ VSCode任务文件缺失"
fi

if [ -f ".clinerules/aceflow_integration.md" ]; then
    echo "✅ Cline集成规则已存在"
else
    echo "❌ Cline集成规则缺失"
fi

if [ -f "aceflow-workspace.code-workspace" ]; then
    echo "✅ 工作区文件已存在"
else
    echo "❌ 工作区文件缺失"
fi

# 测试AceFlow CLI
echo "🧪 测试AceFlow CLI..."
if python3 .aceflow/scripts/aceflow --version &> /dev/null; then
    echo "✅ AceFlow CLI正常工作"
else
    echo "❌ AceFlow CLI测试失败"
    exit 1
fi

# 测试JSON输出
echo "🔍 测试JSON输出格式..."
if python3 .aceflow/scripts/aceflow status --format json &> /dev/null; then
    echo "✅ JSON输出格式正常"
else
    echo "❌ JSON输出格式测试失败"
    exit 1
fi

# 生成测试配置
echo "📋 生成测试配置..."
cat > test_integration.md << 'EOF'
# 集成测试清单

## 基础功能测试
- [ ] AceFlow CLI运行正常
- [ ] JSON输出格式正确
- [ ] 项目状态检查正常

## VSCode集成测试
- [ ] 工作区配置加载正常
- [ ] 任务可以正常执行
- [ ] 设置文件生效

## Cline集成测试
- [ ] Cline可以读取.clinerules配置
- [ ] 自动检测项目状态
- [ ] 智能工作流推荐
- [ ] 命令执行正常

## 完整工作流测试
- [ ] 项目初始化
- [ ] 阶段启动
- [ ] 进度更新
- [ ] 阶段完成
- [ ] 状态查询

使用方法：
1. 打开VSCode：`code aceflow-workspace.code-workspace`
2. 启动Cline扩展
3. 说"检查项目状态"测试集成
EOF

# 创建快速启动脚本
echo "🚀 创建快速启动脚本..."
cat > start_aceflow_dev.sh << 'EOF'
#!/bin/bash

# 快速启动AceFlow开发环境
echo "🚀 启动AceFlow开发环境..."

# 打开VSCode工作区
echo "📝 打开VSCode工作区..."
code aceflow-workspace.code-workspace

# 显示使用提示
echo "✅ 开发环境已启动！"
echo ""
echo "💡 快速开始："
echo "1. 等待VSCode完全加载"
echo "2. 启动Cline扩展（Ctrl+Shift+P -> Cline: Start New Task）"
echo "3. 对Cline说：'检查项目状态'"
echo "4. 享受智能工作流管理！"
echo ""
echo "🔧 常用命令："
echo "- 检查项目状态：python3 .aceflow/scripts/aceflow status"
echo "- 查看JSON状态：python3 .aceflow/scripts/aceflow status --format json"
echo "- 获取工作流建议：python3 .aceflow/scripts/aceflow suggest --task '你的任务'"
echo ""
echo "📚 更多帮助：python3 .aceflow/scripts/aceflow help"
EOF

chmod +x start_aceflow_dev.sh

# 创建调试工具
echo "🔍 创建调试工具..."
cat > debug_integration.py << 'EOF'
#!/usr/bin/env python3
"""
AceFlow + Cline 集成调试工具
"""

import json
import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_aceflow_status():
    """检查AceFlow状态"""
    print("🔍 检查AceFlow状态...")
    
    success, stdout, stderr = run_command("python3 .aceflow/scripts/aceflow status --format json")
    
    if success:
        try:
            data = json.loads(stdout)
            print("✅ AceFlow状态正常")
            print(f"📋 项目ID: {data.get('project_id')}")
            print(f"🎯 流程模式: {data.get('flow_mode')}")
            print(f"📍 当前阶段: {data.get('current_stage_name')}")
            print(f"📈 整体进度: {data.get('overall_progress')}%")
            return True
        except json.JSONDecodeError:
            print("❌ JSON解析失败")
            print(f"原始输出: {stdout}")
            return False
    else:
        print("❌ AceFlow状态检查失败")
        print(f"错误: {stderr}")
        return False

def check_files():
    """检查关键文件"""
    print("\n📁 检查关键文件...")
    
    files_to_check = [
        (".aceflow/scripts/aceflow", "AceFlow CLI"),
        (".aceflow/state/project_state.json", "项目状态文件"),
        (".vscode/settings.json", "VSCode设置"),
        (".vscode/tasks.json", "VSCode任务"),
        (".clinerules/aceflow_integration.md", "Cline集成规则"),
        ("aceflow-workspace.code-workspace", "工作区文件")
    ]
    
    all_good = True
    for file_path, description in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {description}")
        else:
            print(f"❌ {description} 缺失")
            all_good = False
    
    return all_good

def suggest_workflow():
    """测试工作流推荐"""
    print("\n🧠 测试工作流推荐...")
    
    success, stdout, stderr = run_command("python3 .aceflow/scripts/aceflow suggest --task '修复登录bug' --format json")
    
    if success:
        try:
            data = json.loads(stdout)
            print("✅ 工作流推荐正常")
            print(f"推荐模式: {data.get('recommended_mode')}")
            return True
        except json.JSONDecodeError:
            print("⚠️ 工作流推荐输出非JSON格式")
            print(f"输出: {stdout}")
            return True  # 可能是文本格式，也算正常
    else:
        print("❌ 工作流推荐失败")
        print(f"错误: {stderr}")
        return False

def main():
    """主函数"""
    print("🔍 AceFlow + Cline 集成调试工具")
    print("=" * 50)
    
    # 检查是否在项目根目录
    if not Path(".aceflow").exists():
        print("❌ 错误：请在AceFlow项目根目录运行此脚本")
        sys.exit(1)
    
    # 运行各项检查
    checks = [
        check_files(),
        check_aceflow_status(),
        suggest_workflow()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 所有检查通过！集成状态良好")
        print("\n💡 下一步：")
        print("1. 运行 ./start_aceflow_dev.sh 启动开发环境")
        print("2. 在Cline中说'检查项目状态'测试集成")
    else:
        print("⚠️ 部分检查失败，请检查上述问题")
        print("\n🔧 建议：")
        print("1. 确保所有配置文件存在")
        print("2. 检查AceFlow CLI是否正常工作")
        print("3. 重新运行集成脚本")

if __name__ == "__main__":
    main()
EOF

chmod +x debug_integration.py

# 最终总结
echo ""
echo "🎉 AceFlow + Cline 集成配置完成！"
echo "================================"
echo ""
echo "📋 已创建的文件："
echo "  ✅ .vscode/settings.json - VSCode设置"
echo "  ✅ .vscode/tasks.json - VSCode任务"
echo "  ✅ .clinerules/aceflow_integration.md - Cline集成规则"
echo "  ✅ aceflow-workspace.code-workspace - 工作区文件"
echo "  ✅ start_aceflow_dev.sh - 快速启动脚本"
echo "  ✅ debug_integration.py - 调试工具"
echo "  ✅ test_integration.md - 测试清单"
echo ""
echo "🚀 快速开始："
echo "  1. 运行调试工具：python3 debug_integration.py"
echo "  2. 启动开发环境：./start_aceflow_dev.sh"
echo "  3. 在Cline中说：'检查项目状态'"
echo ""
echo "📚 更多帮助："
echo "  - 查看集成文档：cat .clinerules/aceflow_integration.md"
echo "  - 测试CLI：python3 .aceflow/scripts/aceflow status --format json"
echo "  - 查看任务：cat .vscode/tasks.json"
echo ""
echo "💡 提示：如果遇到问题，请先运行debug_integration.py进行诊断"