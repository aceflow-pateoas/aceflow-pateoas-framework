import json
import os

def load_config(config_name):
    """加载配置文件"""
    # 获取配置文件路径
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "config",
        config_name
    )
    
    # 检查文件是否存在
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
    # 加载配置
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)