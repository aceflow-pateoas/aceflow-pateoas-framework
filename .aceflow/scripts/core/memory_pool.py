import os
import json
import hashlib
from datetime import datetime, timedelta
from utils.config_loader import load_config

class GlobalMemoryPool:
    def __init__(self):
        self.config = load_config('workflow_rules.json')
        self.storage_path = self.config.get('memory_pool_config', {}).get('storage_path', './.aceflow/memory_pool')
        self.memory_types = {
            'REQ': '需求记忆',
            'CON': '约束记忆',
            'TASK': '任务记忆',
            'CODE': '代码记忆',
            'TEST': '测试记忆',
            'DEFECT': '缺陷记忆',
            'FDBK': '反馈记忆'
        }
        # 创建存储目录
        os.makedirs(self.storage_path, exist_ok=True)
        for mem_type in self.memory_types.keys():
            os.makedirs(os.path.join(self.storage_path, mem_type), exist_ok=True)

    def generate_memory_id(self, mem_type, content):
        """生成唯一记忆ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        hash_obj = hashlib.md5(content.encode('utf-8'))
        short_hash = hash_obj.hexdigest()[:6]
        return f"MEM-{mem_type}-{timestamp}-{short_hash}"

    def store_memory(self, mem_type, content, metadata=None):
        """存储记忆片段"""
        if mem_type not in self.memory_types:
            raise ValueError(f"不支持的记忆类型: {mem_type}")
            
        memory_id = self.generate_memory_id(mem_type, content)
        memory_data = {
            'id': memory_id,
            'type': mem_type,
            'description': self.memory_types[mem_type],
            'content': content,
            'metadata': metadata or {},
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat() if mem_type != 'REQ' else None
        }
        
        # 保存到文件
        file_path = os.path.join(self.storage_path, mem_type, f"{memory_id}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=2)
            
        return memory_id

    def retrieve_memory(self, memory_id=None, mem_type=None, keywords=None):
        """检索记忆片段"""
        results = []
        
        # 确定要搜索的目录
        search_dirs = [os.path.join(self.storage_path, t) for t in self.memory_types.keys()] if not mem_type else [os.path.join(self.storage_path, mem_type)]
        
        # 搜索文件
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
                
            for filename in os.listdir(search_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(search_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        memory = json.load(f)
                        
                    # 检查过期
                    if memory['expires_at'] and datetime.fromisoformat(memory['expires_at']) < datetime.now():
                        continue
                        
                    # 筛选条件
                    if memory_id and memory['id'] != memory_id:
                        continue
                        
                    if keywords and not any(keyword in memory['content'] for keyword in keywords):
                        continue
                        
                    results.append(memory)
                    
        return results

    def link_memory_to_stage(self, memory_id, stage_id):
        """将记忆关联到阶段"""
        link_file = os.path.join(self.storage_path, 'stage_links.json')
        links = {}
        
        if os.path.exists(link_file):
            with open(link_file, 'r', encoding='utf-8') as f:
                links = json.load(f)
                
        if stage_id not in links:
            links[stage_id] = []
            
        if memory_id not in links[stage_id]:
            links[stage_id].append(memory_id)
            
        with open(link_file, 'w', encoding='utf-8') as f:
            json.dump(links, f, ensure_ascii=False, indent=2)
            
    def get_stage_memories(self, stage_id):
        """获取阶段关联的记忆"""
        link_file = os.path.join(self.storage_path, 'stage_links.json')
        if not os.path.exists(link_file):
            return []
            
        with open(link_file, 'r', encoding='utf-8') as f:
            links = json.load(f)
            
        memory_ids = links.get(stage_id, [])
        return [self.retrieve_memory(memory_id=mid)[0] for mid in memory_ids if self.retrieve_memory(memory_id=mid)]
