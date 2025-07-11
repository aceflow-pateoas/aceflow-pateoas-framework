import os
import json
import shutil
from ..core.memory_pool import GlobalMemoryPool

class MemoryMigrator:
    def __init__(self, source_dir, target_dir=None):
        self.source_dir = source_dir
        self.target_dir = target_dir or './.aceflow/memory_pool'
        self.memory_pool = GlobalMemoryPool()
        
    def migrate(self):
        """执行记忆迁移"""
        # 检查源目录是否存在
        if not os.path.exists(self.source_dir):
            print(f"源目录不存在: {self.source_dir}")
            return False
            
        # 创建目标目录
        os.makedirs(self.target_dir, exist_ok=True)
        
        # 遍历源目录
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        # 读取记忆文件
                        with open(file_path, 'r', encoding='utf-8') as f:
                            memory_data = json.load(f)
                            
                        # 确定记忆类型
                        mem_type = memory_data.get('type', 'UNK')
                        if mem_type not in self.memory_pool.memory_types:
                            print(f"跳过未知记忆类型: {mem_type} - {file}")
                            continue
                            
                        # 存储到新记忆池
                        new_memory_id = self.memory_pool.store_memory(
                            mem_type,
                            memory_data.get('content', ''),
                            memory_data.get('metadata', {})
                        )
                        
                        print(f"迁移记忆: {file} → {new_memory_id}")
                        
                    except Exception as e:
                        print(f"迁移失败 {file}: {str(e)}")
        
        print("记忆迁移完成")
        return True

if __name__ == "__main__":
    # 默认从旧记忆池目录迁移
    migrator = MemoryMigrator(source_dir='./old_memory_pool')
    migrator.migrate()