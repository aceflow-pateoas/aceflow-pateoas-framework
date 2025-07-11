import sys
import os

def check_environment():
    """检查AceFlow运行环境"""
    print("=== AceFlow 环境检查 ===")
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("❌ Python版本需3.6及以上")
        return False
        
    # 检查关键目录
    required_dirs = [".aceflow/scripts", ".aceflow/config", ".aceflow/templates"]
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"❌ 缺失目录: {dir_path}")
            return False
            
    # 检查关键文件
    required_files = [
        ".aceflow/scripts/core/workflow_navigator.py",
        ".aceflow/config/workflow_rules.json",
        "aceflow_cli.py"
    ]
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ 缺失文件: {file_path}")
            return False
            
    print("✅ 环境检查通过")
    return True

if __name__ == "__main__":
    check_environment()