from core.state_engine_enhanced import PATEOASStateEngineEnhanced
from .memory_pool import GlobalMemoryPool
from utils.config_loader import load_config
import json

class WorkflowNavigatorEnhanced:
    def __init__(self):
        self.state_engine = PATEOASStateEngineEnhanced()
        self.memory_pool = GlobalMemoryPool()
        self.config = load_config('workflow_rules.json')
        self.workflow_rules = self.config.get('workflow_rules', {})
        
    def determine_workflow(self, task_description):
        """根据任务描述确定流程分支"""
        # 简单实现，实际应基于AI分析
        if "紧急" in task_description or "P0" in task_description:
            return "紧急流程"
        elif "bug" in task_description.lower() or "修复" in task_description:
            return "快速流程"
        elif "变更" in task_description or "调整" in task_description:
            return "变更流程"
        else:
            return "完整流程"
    
    def get_workflow_path(self, workflow_type):
        """获取指定流程分支的阶段路径"""
        paths = {
            "完整流程": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
            "快速流程": ["S2", "S4", "S5", "S8"],
            "变更流程": ["S1", "S2", "S3", "S4"],
            "紧急流程": ["S4", "S5", "S6", "S8"]
        }
        return paths.get(workflow_type, ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"])
    
    def get_next_stage(self, current_stage, workflow_type=None):
        """获取下一阶段"""
        if not workflow_type:
            # 从当前状态获取流程类型
            state = self.state_engine.get_current_state()
            workflow_type = state.get('workflow_type', '完整流程')
            
        path = self.get_workflow_path(workflow_type)
        current_index = path.index(current_stage) if current_stage in path else -1
        
        if current_index >= 0 and current_index < len(path) - 1:
            return path[current_index + 1]
        return None
    
    def get_previous_stage(self, current_stage, workflow_type=None):
        """获取前一阶段"""
        if not workflow_type:
            # 从当前状态获取流程类型
            state = self.state_engine.get_current_state()
            workflow_type = state.get('workflow_type', '完整流程')
            
        path = self.get_workflow_path(workflow_type)
        current_index = path.index(current_stage) if current_stage in path else -1
        
        if current_index > 0:
            return path[current_index - 1]
        return None
    
    def trigger_cross_stage_update(self, source_stage, memory_id, target_stages):
        """触发跨阶段更新"""
        # 1. 获取记忆内容
        memory = self.memory_pool.retrieve_memory(memory_id=memory_id)[0]
        
        # 2. 更新目标阶段状态
        for stage_id in target_stages:
            # 更新阶段状态为需要调整
            state = self.state_engine.get_current_state()
            if state['stage_status'][stage_id] == 'completed':
                state['stage_status'][stage_id] = 'needs_adjustment'
                self.state_engine.save_state(state)
                
                # 3. 创建调整建议记忆
                adjustment_suggestion = f"基于{source_stage}的反馈，需要调整{stage_id}阶段内容: {memory['content']}"
                adj_memory_id = self.memory_pool.store_memory(
                    'ADJ', 
                    adjustment_suggestion,
                    {'related_memory': memory_id, 'source_stage': source_stage, 'target_stage': stage_id}
                )
                
                # 4. 关联记忆到目标阶段
                self.memory_pool.link_memory_to_stage(adj_memory_id, stage_id)
                
        return True
    
    def trigger_feedback_loop(self, current_stage, issue_description, severity='medium'):
        """触发反馈循环，记录问题并建议回退"""
        # 1. 记录异常
        abnormality = self.state_engine.record_abnormality(current_stage, issue_description, severity)
        
        # 2. 获取前一阶段
        previous_stage = self.get_previous_stage(current_stage)
        if previous_stage:
            # 3. 创建反馈建议记忆
            feedback_suggestion = f"基于{current_stage}的问题，需要回退到{previous_stage}进行修正: {issue_description}"
            fb_memory_id = self.memory_pool.store_memory(
                'FDBK', 
                feedback_suggestion,
                {'related_abnormality': abnormality['id'], 'current_stage': current_stage, 'target_stage': previous_stage}
            )
            
            # 4. 关联记忆到目标阶段
            self.memory_pool.link_memory_to_stage(fb_memory_id, previous_stage)
            
            return {'abnormality_id': abnormality['id'], 'suggested_revert_to': previous_stage, 'memory_id': fb_memory_id}
        return {'abnormality_id': abnormality['id'], 'suggested_revert_to': None, 'memory_id': None}
    
    def review_previous_stage(self, current_stage):
        """复查前一阶段产物"""
        previous_stage = self.get_previous_stage(current_stage)
        if previous_stage:
            state = self.state_engine.get_current_state()
            if state['stage_status'][previous_stage] == 'completed':
                # 这里添加复查逻辑，实际应检查前一阶段的输出产物
                review_result = f"复查阶段 {previous_stage} 完成，确认输出产物有效（模拟结果）"
                self.state_engine.record_stage_review(previous_stage, review_result)
                return {'reviewed_stage': previous_stage, 'result': review_result}
        return {'reviewed_stage': None, 'result': '无前一阶段可复查'}
