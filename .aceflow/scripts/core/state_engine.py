import json
import os
from datetime import datetime
from utils.config_loader import load_config

class PATEOASStateEngine:
    def __init__(self, project_root='.'):
        self.project_root = project_root
        self.config = load_config('dynamic_thresholds.json')
        self.state_file = os.path.join(project_root, '.aceflow', 'current_state.json')
        self.stage_definitions = {
            'S1': {'name': '用户故事细化', 'next_stage': 'S2'},
            'S2': {'name': '任务拆分', 'next_stage': 'S3'},
            'S3': {'name': '测试用例设计', 'next_stage': 'S4'},
            'S4': {'name': '功能实现', 'next_stage': 'S5'},
            'S5': {'name': '测试报告', 'next_stage': 'S6'},
            'S6': {'name': '代码评审', 'next_stage': 'S7'},
            'S7': {'name': '演示与反馈', 'next_stage': 'S8'},
            'S8': {'name': '进度汇总', 'next_stage': None}
        }
        
        # 初始化状态目录
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        
        # 初始化状态文件
        if not os.path.exists(self.state_file):
            self.initialize_state()

    def initialize_state(self):
        """初始化项目状态"""
        initial_state = {
            'current_stage': 'S1',
            'stage_status': {stage_id: 'not_started' for stage_id in self.stage_definitions.keys()},
            'progress': {stage_id: 0 for stage_id in self.stage_definitions.keys()},
            'memory_ids': [],
            'last_updated': datetime.now().isoformat(),
            'abnormalities': []
        }
        initial_state['stage_status']['S1'] = 'in_progress'
        
        self.save_state(initial_state)
        return initial_state

    def get_current_state(self):
        """获取当前状态"""
        with open(self.state_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_state(self, state_data):
        """保存状态数据"""
        state_data['last_updated'] = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, ensure_ascii=False, indent=2)

    def update_stage_progress(self, stage_id, progress, memory_ids=None):
        """更新阶段进度"""
        state = self.get_current_state()
        
        if stage_id not in state['progress']:
            raise ValueError(f"无效的阶段ID: {stage_id}")
            
        state['progress'][stage_id] = progress
        state['current_stage'] = stage_id
        
        # 更新状态
        if progress >= 100:
            state['stage_status'][stage_id] = 'completed'
            # 自动进入下一阶段
            next_stage = self.stage_definitions[stage_id]['next_stage']
            if next_stage:
                state['current_stage'] = next_stage
                state['stage_status'][next_stage] = 'in_progress'
        else:
            state['stage_status'][stage_id] = 'in_progress'
            
        # 添加记忆ID
        if memory_ids:
            for mem_id in memory_ids:
                if mem_id not in state['memory_ids']:
                    state['memory_ids'].append(mem_id)
                    
        self.save_state(state)
        return state

    def record_abnormality(self, stage_id, issue_description, severity='medium'):
        """记录异常状态"""
        state = self.get_current_state()
        
        abnormality = {
            'id': f"ABN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'stage_id': stage_id,
            'description': issue_description,
            'severity': severity,
            'detected_at': datetime.now().isoformat(),
            'status': 'unresolved'
        }
        
        state['abnormalities'].append(abnormality)
        self.save_state(state)
        return abnormality

    def resolve_abnormality(self, abnormality_id):
        """解决异常状态"""
        state = self.get_current_state()
        
        for abn in state['abnormalities']:
            if abn['id'] == abnormality_id:
                abn['status'] = 'resolved'
                abn['resolved_at'] = datetime.now().isoformat()
                self.save_state(state)
                return True
                
        return False

    def get_navigation_suggestion(self):
        """获取导航建议，明确区分状态描述与操作建议"""
        state = self.get_current_state()
        current_stage = state['current_stage']
        progress = state['progress'].get(current_stage, 0)
        abnormalities = [a for a in state['abnormalities'] if a['status'] == 'unresolved' and a['stage_id'] == current_stage]
        
        suggestions = []
        
        # 异常处理建议
        if abnormalities:
            for abn in abnormalities:
                suggestions.append({
                    'type': 'abnormality',
                    'priority': 'high' if abn['severity'] == 'high' else 'medium',
                    'message': f"【状态提示】需要处理异常: {abn['description']}",  # 添加明确标识
                    'action_suggestion': f"resolve_abnormality('{abn['id']}')",  # 重命名key，明确为建议
                    'requires_confirmation': True  # 添加是否需要确认的标记
                })
            return suggestions
            
        # 进度建议
        if progress < 100:
            remaining = 100 - progress
            suggestions.append({
                'type': 'progress',
                'priority': 'medium',
                'message': f"【状态提示】当前阶段 {current_stage} 进度: {progress}%，还需完成 {remaining}%",  # 添加明确标识
                'action_suggestion': f"update_stage_progress('{current_stage}', {min(progress + 10, 100)})",  # 明确为建议
                'requires_confirmation': True,
                'rationale': f"建议逐步更新进度，每次增加不超过10%"  # 添加建议理由
            })
        else:
            next_stage = self.stage_definitions[current_stage]['next_stage']
            if next_stage:
                suggestions.append({
                    'type': 'transition',
                    'priority': 'high',
                    'message': f"【状态提示】阶段 {current_stage} 已完成，准备进入 {next_stage}",
                    'action_suggestion': f"update_stage_progress('{next_stage}', 0)",
                    'requires_confirmation': True,
                    'rationale': "请确认是否已完成当前阶段所有工作"
                })
                
        return suggestions
