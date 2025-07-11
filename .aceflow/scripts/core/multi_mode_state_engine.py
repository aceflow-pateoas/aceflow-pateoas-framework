#!/usr/bin/env python3
"""
AceFlow 增强状态引擎 v2.0
支持轻量级、标准、完整三种流程模式的状态管理
"""

import json
import yaml
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StageStatus(Enum):
    """阶段状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"

class FlowMode(Enum):
    """流程模式枚举"""
    MINIMAL = "minimal"
    STANDARD = "standard"
    COMPLETE = "complete"

@dataclass
class StageInfo:
    """阶段信息"""
    id: str
    name: str
    display_name: str
    description: str
    duration_estimate: str
    deliverables: List[str]
    next_stage: Optional[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class StageState:
    """阶段状态"""
    stage_id: str
    status: StageStatus
    progress: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    assignee: Optional[str] = None
    notes: List[str] = None
    deliverables_status: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.notes is None:
            self.notes = []
        if self.deliverables_status is None:
            self.deliverables_status = {}

class MultiModeStateEngine:
    """多模式状态引擎"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.aceflow_dir = self.project_root / ".aceflow"
        self.config_file = self.aceflow_dir / "config.yaml"
        self.state_file = self.aceflow_dir / "current_state.json"
        self.flow_modes_file = self.aceflow_dir / "config" / "flow_modes.yaml"
        
        # 加载配置
        self.config = self._load_config()
        self.flow_modes = self._load_flow_modes()
        self.current_mode = FlowMode(self.config.get('flow', {}).get('mode', 'minimal'))
        
        # 初始化状态
        self.state = self._load_state()
        
    def _load_config(self) -> Dict:
        """加载项目配置"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
        return {}
    
    def _load_flow_modes(self) -> Dict:
        """加载流程模式配置"""
        try:
            if self.flow_modes_file.exists():
                with open(self.flow_modes_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载流程模式配置失败: {e}")
        return {}
    
    def _load_state(self) -> Dict:
        """加载当前状态"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                    # 转换datetime字符串
                    for stage_id, stage_state in state_data.get('stage_states', {}).items():
                        if stage_state.get('start_time'):
                            stage_state['start_time'] = datetime.fromisoformat(stage_state['start_time'])
                        if stage_state.get('end_time'):
                            stage_state['end_time'] = datetime.fromisoformat(stage_state['end_time'])
                    return state_data
        except Exception as e:
            logger.error(f"加载状态失败: {e}")
        
        # 返回默认状态
        return self._create_default_state()
    
    def _create_default_state(self) -> Dict:
        """创建默认状态"""
        stages = self.get_stages_for_mode(self.current_mode)
        initial_stage = stages[0].id if stages else None
        
        return {
            'flow_mode': self.current_mode.value,
            'current_stage': initial_stage,
            'stage_states': {},
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'version': '2.0'
            }
        }
    
    def _save_state(self):
        """保存当前状态"""
        try:
            # 确保目录存在
            self.aceflow_dir.mkdir(parents=True, exist_ok=True)
            
            # 准备保存的数据
            save_data = self.state.copy()
            save_data['metadata']['last_updated'] = datetime.now().isoformat()
            
            # 转换datetime对象为字符串
            for stage_id, stage_state in save_data.get('stage_states', {}).items():
                if isinstance(stage_state.get('start_time'), datetime):
                    stage_state['start_time'] = stage_state['start_time'].isoformat()
                if isinstance(stage_state.get('end_time'), datetime):
                    stage_state['end_time'] = stage_state['end_time'].isoformat()
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"保存状态失败: {e}")
    
    def get_stages_for_mode(self, mode: FlowMode) -> List[StageInfo]:
        """获取指定模式的阶段列表"""
        if not self.flow_modes or 'flow_modes' not in self.flow_modes:
            return []
        
        mode_config = self.flow_modes['flow_modes'].get(mode.value, {})
        stages_config = mode_config.get('stages', [])
        
        stages = []
        for stage_config in stages_config:
            stage = StageInfo(
                id=stage_config['id'],
                name=stage_config['name'],
                display_name=stage_config['display_name'],
                description=stage_config['description'],
                duration_estimate=stage_config['duration_estimate'],
                deliverables=stage_config['deliverables'],
                next_stage=stage_config.get('next_stage'),
                dependencies=stage_config.get('dependencies', [])
            )
            stages.append(stage)
        
        return stages
    
    def get_current_stage_info(self) -> Optional[StageInfo]:
        """获取当前阶段信息"""
        if not self.state.get('current_stage'):
            return None
        
        stages = self.get_stages_for_mode(self.current_mode)
        for stage in stages:
            if stage.id == self.state['current_stage']:
                return stage
        return None
    
    def get_stage_state(self, stage_id: str) -> StageState:
        """获取阶段状态"""
        stage_state_data = self.state.get('stage_states', {}).get(stage_id, {})
        
        return StageState(
            stage_id=stage_id,
            status=StageStatus(stage_state_data.get('status', StageStatus.PENDING.value)),
            progress=stage_state_data.get('progress', 0),
            start_time=stage_state_data.get('start_time'),
            end_time=stage_state_data.get('end_time'),
            assignee=stage_state_data.get('assignee'),
            notes=stage_state_data.get('notes', []),
            deliverables_status=stage_state_data.get('deliverables_status', {})
        )
    
    def update_stage_state(self, stage_id: str, **kwargs):
        """更新阶段状态"""
        if 'stage_states' not in self.state:
            self.state['stage_states'] = {}
        
        if stage_id not in self.state['stage_states']:
            self.state['stage_states'][stage_id] = {}
        
        stage_state = self.state['stage_states'][stage_id]
        
        # 更新状态字段
        for key, value in kwargs.items():
            if key == 'status' and isinstance(value, StageStatus):
                stage_state[key] = value.value
            elif key in ['start_time', 'end_time'] and isinstance(value, datetime):
                stage_state[key] = value
            else:
                stage_state[key] = value
        
        # 自动设置时间戳
        if 'status' in kwargs:
            if kwargs['status'] == StageStatus.IN_PROGRESS and 'start_time' not in stage_state:
                stage_state['start_time'] = datetime.now()
            elif kwargs['status'] == StageStatus.COMPLETED:
                stage_state['end_time'] = datetime.now()
                stage_state['progress'] = 100
        
        self._save_state()
        logger.info(f"更新阶段 {stage_id} 状态: {kwargs}")
    
    def start_stage(self, stage_id: str, assignee: Optional[str] = None) -> bool:
        """开始阶段"""
        # 检查依赖
        if not self._check_dependencies(stage_id):
            logger.error(f"阶段 {stage_id} 的依赖条件未满足")
            return False
        
        # 更新状态
        self.update_stage_state(
            stage_id,
            status=StageStatus.IN_PROGRESS,
            start_time=datetime.now(),
            assignee=assignee
        )
        
        # 更新当前阶段
        self.state['current_stage'] = stage_id
        self._save_state()
        
        logger.info(f"开始阶段: {stage_id}")
        return True
    
    def complete_stage(self, stage_id: str, notes: List[str] = None) -> bool:
        """完成阶段"""
        stage_info = self._get_stage_info_by_id(stage_id)
        if not stage_info:
            logger.error(f"未找到阶段: {stage_id}")
            return False
        
        # 检查交付物
        if not self._check_deliverables(stage_id):
            logger.warning(f"阶段 {stage_id} 的交付物尚未完成")
        
        # 更新状态
        update_data = {
            'status': StageStatus.COMPLETED,
            'end_time': datetime.now(),
            'progress': 100
        }
        
        if notes:
            existing_notes = self.get_stage_state(stage_id).notes
            update_data['notes'] = existing_notes + notes
        
        self.update_stage_state(stage_id, **update_data)
        
        # 移动到下一阶段
        if stage_info.next_stage:
            self.state['current_stage'] = stage_info.next_stage
            self._save_state()
        
        logger.info(f"完成阶段: {stage_id}")
        return True
    
    def _get_stage_info_by_id(self, stage_id: str) -> Optional[StageInfo]:
        """根据ID获取阶段信息"""
        stages = self.get_stages_for_mode(self.current_mode)
        for stage in stages:
            if stage.id == stage_id:
                return stage
        return None
    
    def _check_dependencies(self, stage_id: str) -> bool:
        """检查阶段依赖"""
        stage_info = self._get_stage_info_by_id(stage_id)
        if not stage_info or not stage_info.dependencies:
            return True
        
        for dep_stage_id in stage_info.dependencies:
            dep_state = self.get_stage_state(dep_stage_id)
            if dep_state.status != StageStatus.COMPLETED:
                return False
        
        return True
    
    def _check_deliverables(self, stage_id: str) -> bool:
        """检查交付物完成情况"""
        stage_state = self.get_stage_state(stage_id)
        stage_info = self._get_stage_info_by_id(stage_id)
        
        if not stage_info or not stage_info.deliverables:
            return True
        
        for deliverable in stage_info.deliverables:
            if not stage_state.deliverables_status.get(deliverable, False):
                return False
        
        return True
    
    def update_deliverable_status(self, stage_id: str, deliverable: str, completed: bool):
        """更新交付物状态"""
        stage_state_data = self.state.get('stage_states', {}).get(stage_id, {})
        deliverables_status = stage_state_data.get('deliverables_status', {})
        deliverables_status[deliverable] = completed
        
        self.update_stage_state(stage_id, deliverables_status=deliverables_status)
        
        # 自动更新进度
        self._update_stage_progress(stage_id)
    
    def _update_stage_progress(self, stage_id: str):
        """自动更新阶段进度"""
        stage_info = self._get_stage_info_by_id(stage_id)
        stage_state = self.get_stage_state(stage_id)
        
        if not stage_info or not stage_info.deliverables:
            return
        
        total_deliverables = len(stage_info.deliverables)
        completed_deliverables = sum(1 for d in stage_info.deliverables 
                                   if stage_state.deliverables_status.get(d, False))
        
        progress = int((completed_deliverables / total_deliverables) * 100)
        self.update_stage_state(stage_id, progress=progress)
    
    def switch_flow_mode(self, new_mode: FlowMode, preserve_progress: bool = True) -> bool:
        """切换流程模式"""
        if new_mode == self.current_mode:
            logger.info(f"已经是 {new_mode.value} 模式")
            return True
        
        old_mode = self.current_mode
        
        # 如果保留进度，尝试映射状态
        if preserve_progress:
            success = self._migrate_state(old_mode, new_mode)
            if not success:
                logger.error(f"从 {old_mode.value} 到 {new_mode.value} 的状态迁移失败")
                return False
        else:
            # 重置状态
            self.state = self._create_default_state()
        
        # 更新模式
        self.current_mode = new_mode
        self.state['flow_mode'] = new_mode.value
        
        # 更新配置文件
        self.config['flow']['mode'] = new_mode.value
        self._save_config()
        self._save_state()
        
        logger.info(f"切换流程模式: {old_mode.value} -> {new_mode.value}")
        return True
    
    def _migrate_state(self, old_mode: FlowMode, new_mode: FlowMode) -> bool:
        """迁移状态数据"""
        try:
            # 获取映射规则
            migration_rules = self.flow_modes.get('mode_switching', {}).get('mapping_rules', {})
            mapping_key = f"{old_mode.value}_to_{new_mode.value}"
            
            if mapping_key not in migration_rules:
                logger.warning(f"未找到 {mapping_key} 的映射规则，将尝试智能映射")
                return self._smart_migrate_state(old_mode, new_mode)
            
            mapping = migration_rules[mapping_key]
            new_stage_states = {}
            
            for new_stage_id, old_stage_spec in mapping.items():
                if ',' in old_stage_spec:
                    # 多个旧阶段合并
                    old_stage_ids = [s.strip() for s in old_stage_spec.split(',')]
                    merged_state = self._merge_stage_states(old_stage_ids)
                    new_stage_states[new_stage_id] = merged_state
                else:
                    # 单个阶段映射
                    old_stage_state = self.state.get('stage_states', {}).get(old_stage_spec)
                    if old_stage_state:
                        new_stage_states[new_stage_id] = old_stage_state
            
            self.state['stage_states'] = new_stage_states
            
            # 更新当前阶段
            new_stages = self.get_stages_for_mode(new_mode)
            if new_stages:
                # 找到第一个未完成的阶段
                for stage in new_stages:
                    stage_state = new_stage_states.get(stage.id, {})
                    if stage_state.get('status') != StageStatus.COMPLETED.value:
                        self.state['current_stage'] = stage.id
                        break
                else:
                    # 所有阶段都完成了，设置为最后一个阶段
                    self.state['current_stage'] = new_stages[-1].id
            
            return True
            
        except Exception as e:
            logger.error(f"状态迁移失败: {e}")
            return False
    
    def _smart_migrate_state(self, old_mode: FlowMode, new_mode: FlowMode) -> bool:
        """智能状态迁移"""
        try:
            old_stages = self.get_stages_for_mode(old_mode)
            new_stages = self.get_stages_for_mode(new_mode)
            
            # 简单的阶段名称匹配
            new_stage_states = {}
            
            for new_stage in new_stages:
                # 尝试找到最匹配的旧阶段
                best_match = None
                best_score = 0
                
                for old_stage in old_stages:
                    score = self._calculate_stage_similarity(old_stage, new_stage)
                    if score > best_score:
                        best_score = score
                        best_match = old_stage
                
                if best_match and best_score > 0.5:
                    old_state = self.state.get('stage_states', {}).get(best_match.id)
                    if old_state:
                        new_stage_states[new_stage.id] = old_state
            
            self.state['stage_states'] = new_stage_states
            
            # 设置当前阶段
            if new_stages:
                self.state['current_stage'] = new_stages[0].id
                for stage in new_stages:
                    stage_state = new_stage_states.get(stage.id, {})
                    if stage_state.get('status') != StageStatus.COMPLETED.value:
                        self.state['current_stage'] = stage.id
                        break
            
            return True
            
        except Exception as e:
            logger.error(f"智能迁移失败: {e}")
            return False
    
    def _calculate_stage_similarity(self, stage1: StageInfo, stage2: StageInfo) -> float:
        """计算阶段相似度"""
        # 简单的字符串相似度计算
        name_similarity = self._string_similarity(stage1.name.lower(), stage2.name.lower())
        desc_similarity = self._string_similarity(stage1.description.lower(), stage2.description.lower())
        
        return (name_similarity + desc_similarity) / 2
    
    def _string_similarity(self, s1: str, s2: str) -> float:
        """计算字符串相似度"""
        if not s1 or not s2:
            return 0.0
        
        # 简单的Jaccard相似度
        set1 = set(s1.split())
        set2 = set(s2.split())
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def _merge_stage_states(self, stage_ids: List[str]) -> Dict:
        """合并多个阶段状态"""
        merged_state = {
            'status': StageStatus.PENDING.value,
            'progress': 0,
            'notes': [],
            'deliverables_status': {}
        }
        
        all_completed = True
        total_progress = 0
        valid_states = 0
        
        for stage_id in stage_ids:
            stage_state = self.state.get('stage_states', {}).get(stage_id)
            if stage_state:
                valid_states += 1
                
                # 状态：如果有任何一个未完成，则合并状态为进行中
                if stage_state.get('status') != StageStatus.COMPLETED.value:
                    all_completed = False
                
                # 进度：平均值
                total_progress += stage_state.get('progress', 0)
                
                # 合并注释
                notes = stage_state.get('notes', [])
                merged_state['notes'].extend(notes)
                
                # 合并交付物状态
                deliverables = stage_state.get('deliverables_status', {})
                merged_state['deliverables_status'].update(deliverables)
                
                # 时间信息
                if stage_state.get('start_time') and not merged_state.get('start_time'):
                    merged_state['start_time'] = stage_state['start_time']
                
                if stage_state.get('end_time'):
                    merged_state['end_time'] = stage_state['end_time']
        
        # 设置合并后的状态
        if all_completed and valid_states > 0:
            merged_state['status'] = StageStatus.COMPLETED.value
            merged_state['progress'] = 100
        elif valid_states > 0:
            merged_state['status'] = StageStatus.IN_PROGRESS.value
            merged_state['progress'] = total_progress // valid_states
        
        return merged_state
    
    def _save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
    
    def get_flow_summary(self) -> Dict:
        """获取流程摘要"""
        stages = self.get_stages_for_mode(self.current_mode)
        stage_states = []
        
        total_progress = 0
        completed_stages = 0
        
        for stage in stages:
            state = self.get_stage_state(stage.id)
            stage_states.append({
                'id': stage.id,
                'name': stage.display_name,
                'status': state.status.value,
                'progress': state.progress,
                'assignee': state.assignee
            })
            
            total_progress += state.progress
            if state.status == StageStatus.COMPLETED:
                completed_stages += 1
        
        overall_progress = total_progress // len(stages) if stages else 0
        
        return {
            'mode': self.current_mode.value,
            'current_stage': self.state.get('current_stage'),
            'overall_progress': overall_progress,
            'completed_stages': completed_stages,
            'total_stages': len(stages),
            'stages': stage_states
        }
    
    def get_next_actions(self) -> List[Dict]:
        """获取下一步行动建议"""
        actions = []
        current_stage_id = self.state.get('current_stage')
        
        if not current_stage_id:
            return actions
        
        current_stage = self._get_stage_info_by_id(current_stage_id)
        current_state = self.get_stage_state(current_stage_id)
        
        if not current_stage:
            return actions
        
        # 基于当前阶段状态提供建议
        if current_state.status == StageStatus.PENDING:
            actions.append({
                'type': 'start_stage',
                'title': f'开始 {current_stage.display_name}',
                'description': current_stage.description,
                'priority': 'high'
            })
        
        elif current_state.status == StageStatus.IN_PROGRESS:
            # 检查未完成的交付物
            for deliverable in current_stage.deliverables:
                if not current_state.deliverables_status.get(deliverable, False):
                    actions.append({
                        'type': 'complete_deliverable',
                        'title': f'完成交付物: {deliverable}',
                        'description': f'在 {current_stage.display_name} 阶段完成此交付物',
                        'priority': 'medium'
                    })
            
            # 如果所有交付物完成，建议完成阶段
            if self._check_deliverables(current_stage_id):
                actions.append({
                    'type': 'complete_stage',
                    'title': f'完成 {current_stage.display_name}',
                    'description': '所有交付物已完成，可以结束当前阶段',
                    'priority': 'high'
                })
        
        elif current_state.status == StageStatus.COMPLETED:
            # 建议进入下一阶段
            if current_stage.next_stage:
                next_stage = self._get_stage_info_by_id(current_stage.next_stage)
                if next_stage:
                    actions.append({
                        'type': 'start_next_stage',
                        'title': f'开始 {next_stage.display_name}',
                        'description': next_stage.description,
                        'priority': 'high'
                    })
        
        return actions


def main():
    """测试函数"""
    engine = MultiModeStateEngine()
    
    # 获取流程摘要
    summary = engine.get_flow_summary()
    print("流程摘要:", json.dumps(summary, indent=2, ensure_ascii=False))
    
    # 获取下一步行动
    actions = engine.get_next_actions()
    print("下一步行动:", json.dumps(actions, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()