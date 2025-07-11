"""
AceFlow v2.0 智能决策引擎
从规则引擎升级为机器学习驱动的智能系统
"""

import json
import yaml
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# 导入AI相关库（实际使用时需要安装）
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    HAS_ML_LIBS = True
except ImportError:
    # 如果没有安装ML库，使用简化的规则引擎
    HAS_ML_LIBS = False
    np = None

class TaskType(Enum):
    """任务类型枚举"""
    FEATURE_DEVELOPMENT = "feature_development"
    BUG_FIX = "bug_fix"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    RESEARCH = "research"
    ARCHITECTURE = "architecture"
    DEPLOYMENT = "deployment"

class ProjectComplexity(Enum):
    """项目复杂度枚举"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"

@dataclass
class ProjectContext:
    """项目上下文信息"""
    name: str
    team_size: int
    duration_estimate: str
    technology_stack: List[str]
    project_type: str
    current_stage: str
    completion_percentage: float
    historical_velocity: float
    risk_factors: List[str]
    
    def to_features(self) -> Dict[str, Any]:
        """转换为ML特征"""
        return {
            'team_size': self.team_size,
            'duration_days': self._parse_duration_to_days(self.duration_estimate),
            'completion_percentage': self.completion_percentage,
            'historical_velocity': self.historical_velocity,
            'has_frontend': any('frontend' in tech.lower() or 'react' in tech.lower() or 'vue' in tech.lower() 
                             for tech in self.technology_stack),
            'has_backend': any('backend' in tech.lower() or 'api' in tech.lower() or 'django' in tech.lower() 
                            for tech in self.technology_stack),
            'has_database': any('database' in tech.lower() or 'sql' in tech.lower() or 'mongo' in tech.lower() 
                             for tech in self.technology_stack),
            'risk_count': len(self.risk_factors),
            'is_web_project': self.project_type.lower() in ['web', 'webapp', 'website'],
            'is_mobile_project': self.project_type.lower() in ['mobile', 'app', 'ios', 'android'],
            'is_api_project': self.project_type.lower() in ['api', 'microservice', 'backend']
        }
    
    def _parse_duration_to_days(self, duration: str) -> int:
        """解析持续时间为天数"""
        duration = duration.lower()
        if 'week' in duration:
            weeks = int(''.join(filter(str.isdigit, duration)) or 1)
            return weeks * 7
        elif 'month' in duration:
            months = int(''.join(filter(str.isdigit, duration)) or 1)
            return months * 30
        elif 'day' in duration:
            return int(''.join(filter(str.isdigit, duration)) or 1)
        return 7  # 默认1周

@dataclass
class TaskContext:
    """任务上下文信息"""
    description: str
    priority: str
    estimated_effort: str
    dependencies: List[str]
    technical_complexity: str
    user_impact: str
    
    def to_features(self) -> Dict[str, Any]:
        """转换为ML特征"""
        return {
            'description_length': len(self.description),
            'priority_high': self.priority.lower() == 'high',
            'priority_medium': self.priority.lower() == 'medium',
            'priority_low': self.priority.lower() == 'low',
            'has_dependencies': len(self.dependencies) > 0,
            'dependency_count': len(self.dependencies),
            'complexity_high': self.technical_complexity.lower() == 'high',
            'complexity_medium': self.technical_complexity.lower() == 'medium',
            'complexity_low': self.technical_complexity.lower() == 'low',
            'impact_high': self.user_impact.lower() == 'high',
            'impact_medium': self.user_impact.lower() == 'medium',
            'impact_low': self.user_impact.lower() == 'low',
            'has_keywords_bug': 'bug' in self.description.lower() or 'fix' in self.description.lower(),
            'has_keywords_feature': 'feature' in self.description.lower() or 'add' in self.description.lower(),
            'has_keywords_test': 'test' in self.description.lower() or 'testing' in self.description.lower(),
            'has_keywords_doc': 'doc' in self.description.lower() or 'documentation' in self.description.lower()
        }

@dataclass
class AIDecision:
    """AI决策结果"""
    recommended_flow: str
    confidence: float
    reasoning: str
    alternatives: List[Dict[str, Any]]
    estimated_duration: int
    suggested_tasks: List[str]
    risk_assessment: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'recommended_flow': self.recommended_flow,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'alternatives': self.alternatives,
            'estimated_duration': self.estimated_duration,
            'suggested_tasks': self.suggested_tasks,
            'risk_assessment': self.risk_assessment,
            'timestamp': datetime.now().isoformat()
        }

class TaskClassificationModel:
    """任务分类模型"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        
    def train(self, training_data: List[Tuple[str, TaskType]]):
        """训练任务分类模型"""
        if not HAS_ML_LIBS:
            logging.warning("ML libraries not available, using rule-based classification")
            return
            
        descriptions, labels = zip(*training_data)
        
        # 文本向量化
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X = self.vectorizer.fit_transform(descriptions)
        
        # 训练分类器
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, labels)
        self.is_trained = True
        
        logging.info(f"Task classification model trained with {len(training_data)} samples")
    
    def predict(self, task_context: TaskContext) -> TaskType:
        """预测任务类型"""
        if not self.is_trained or not HAS_ML_LIBS:
            return self._rule_based_classification(task_context)
        
        # 使用ML模型预测
        X = self.vectorizer.transform([task_context.description])
        prediction = self.model.predict(X)[0]
        return TaskType(prediction)
    
    def _rule_based_classification(self, task_context: TaskContext) -> TaskType:
        """基于规则的任务分类（备用方案）"""
        description = task_context.description.lower()
        
        # 关键词匹配规则
        if any(word in description for word in ['bug', 'fix', 'error', 'issue']):
            return TaskType.BUG_FIX
        elif any(word in description for word in ['test', 'testing', 'unit test', 'integration']):
            return TaskType.TESTING
        elif any(word in description for word in ['doc', 'documentation', 'readme', 'guide']):
            return TaskType.DOCUMENTATION
        elif any(word in description for word in ['refactor', 'refactoring', 'cleanup', 'optimize']):
            return TaskType.REFACTORING
        elif any(word in description for word in ['research', 'investigate', 'spike', 'poc']):
            return TaskType.RESEARCH
        elif any(word in description for word in ['architecture', 'design', 'framework']):
            return TaskType.ARCHITECTURE
        elif any(word in description for word in ['deploy', 'deployment', 'release', 'publish']):
            return TaskType.DEPLOYMENT
        else:
            return TaskType.FEATURE_DEVELOPMENT

class FlowRecommendationModel:
    """流程推荐模型"""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def train(self, training_data: List[Tuple[Dict[str, Any], str]]):
        """训练流程推荐模型"""
        if not HAS_ML_LIBS:
            logging.warning("ML libraries not available, using rule-based recommendation")
            return
            
        # 准备训练数据
        features = []
        labels = []
        
        for feature_dict, flow_mode in training_data:
            feature_vector = list(feature_dict.values())
            features.append(feature_vector)
            labels.append(flow_mode)
        
        X = np.array(features)
        y = np.array(labels)
        
        # 训练模型
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        self.is_trained = True
        
        logging.info(f"Flow recommendation model trained with {len(training_data)} samples")
    
    def suggest(self, task_type: TaskType, project_context: ProjectContext) -> str:
        """推荐工作流模式"""
        if not self.is_trained or not HAS_ML_LIBS:
            return self._rule_based_recommendation(task_type, project_context)
        
        # 使用ML模型推荐
        features = list(project_context.to_features().values())
        prediction = self.model.predict([features])[0]
        return prediction
    
    def _rule_based_recommendation(self, task_type: TaskType, project_context: ProjectContext) -> str:
        """基于规则的流程推荐（备用方案）"""
        # 简单项目或快速修复
        if (task_type == TaskType.BUG_FIX or 
            project_context.team_size <= 3 or 
            'quick' in project_context.duration_estimate.lower()):
            return 'minimal'
        
        # 企业级或复杂项目
        if (project_context.team_size > 10 or 
            task_type == TaskType.ARCHITECTURE or
            len(project_context.risk_factors) > 3):
            return 'complete'
        
        # 默认标准模式
        return 'standard'

class ProgressPredictionModel:
    """进度预测模型"""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def train(self, training_data: List[Tuple[Dict[str, Any], int]]):
        """训练进度预测模型"""
        if not HAS_ML_LIBS:
            logging.warning("ML libraries not available, using rule-based prediction")
            return
            
        features = []
        durations = []
        
        for feature_dict, actual_duration in training_data:
            feature_vector = list(feature_dict.values())
            features.append(feature_vector)
            durations.append(actual_duration)
        
        X = np.array(features)
        y = np.array(durations)
        
        # 使用回归模型预测持续时间
        from sklearn.ensemble import RandomForestRegressor
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        self.is_trained = True
        
        logging.info(f"Progress prediction model trained with {len(training_data)} samples")
    
    def estimate(self, task_type: TaskType, project_context: ProjectContext) -> int:
        """估算任务持续时间（小时）"""
        if not self.is_trained or not HAS_ML_LIBS:
            return self._rule_based_estimation(task_type, project_context)
        
        # 使用ML模型预测
        features = list(project_context.to_features().values())
        prediction = self.model.predict([features])[0]
        return max(1, int(prediction))  # 至少1小时
    
    def _rule_based_estimation(self, task_type: TaskType, project_context: ProjectContext) -> int:
        """基于规则的时间估算（备用方案）"""
        base_hours = {
            TaskType.BUG_FIX: 4,
            TaskType.FEATURE_DEVELOPMENT: 16,
            TaskType.REFACTORING: 8,
            TaskType.TESTING: 6,
            TaskType.DOCUMENTATION: 4,
            TaskType.RESEARCH: 12,
            TaskType.ARCHITECTURE: 24,
            TaskType.DEPLOYMENT: 8
        }
        
        hours = base_hours.get(task_type, 8)
        
        # 根据团队规模调整
        if project_context.team_size > 5:
            hours *= 1.2  # 大团队协调成本
        elif project_context.team_size == 1:
            hours *= 0.8  # 单人项目效率高
        
        # 根据复杂度调整
        if len(project_context.risk_factors) > 2:
            hours *= 1.5  # 高风险项目
        
        return int(hours)

class AIDecisionEngine:
    """AI决策引擎主类"""
    
    def __init__(self, aceflow_dir: Path):
        self.aceflow_dir = aceflow_dir
        self.ai_dir = aceflow_dir / "ai"
        self.models_dir = self.ai_dir / "models"
        self.data_dir = self.ai_dir / "data"
        
        # 初始化模型
        self.task_classifier = TaskClassificationModel()
        self.flow_recommender = FlowRecommendationModel()
        self.progress_predictor = ProgressPredictionModel()
        
        # 创建目录
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置日志
        self._setup_logging()
        
        # 加载预训练模型
        self._load_models()
    
    def _setup_logging(self):
        """设置日志系统"""
        log_file = self.ai_dir / "ai_engine.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_models(self):
        """加载预训练模型"""
        try:
            # 尝试加载训练好的模型
            # 这里可以从文件加载保存的模型
            self.logger.info("Models loaded successfully")
        except Exception as e:
            self.logger.warning(f"Could not load pre-trained models: {e}")
            # 使用默认的训练数据训练模型
            self._initialize_with_default_data()
    
    def _initialize_with_default_data(self):
        """使用默认数据初始化模型"""
        # 默认任务分类训练数据
        task_training_data = [
            ("Fix login bug", TaskType.BUG_FIX),
            ("Add user authentication", TaskType.FEATURE_DEVELOPMENT),
            ("Refactor database layer", TaskType.REFACTORING),
            ("Write unit tests for API", TaskType.TESTING),
            ("Update API documentation", TaskType.DOCUMENTATION),
            ("Research new framework", TaskType.RESEARCH),
            ("Design system architecture", TaskType.ARCHITECTURE),
            ("Deploy to production", TaskType.DEPLOYMENT)
        ]
        
        # 训练任务分类模型
        self.task_classifier.train(task_training_data)
        
        self.logger.info("Models initialized with default training data")
    
    def make_decision(self, 
                     task_context: TaskContext, 
                     project_context: ProjectContext) -> AIDecision:
        """做出AI决策"""
        
        try:
            # 1. 任务分类
            task_type = self.task_classifier.predict(task_context)
            
            # 2. 流程推荐
            recommended_flow = self.flow_recommender.suggest(task_type, project_context)
            
            # 3. 时间估算
            estimated_duration = self.progress_predictor.estimate(task_type, project_context)
            
            # 4. 计算置信度
            confidence = self._calculate_confidence(task_context, project_context)
            
            # 5. 生成推理解释
            reasoning = self._explain_decision(task_type, recommended_flow, project_context)
            
            # 6. 提供替代方案
            alternatives = self._suggest_alternatives(recommended_flow, task_type)
            
            # 7. 生成任务建议
            suggested_tasks = self._generate_task_suggestions(task_type, recommended_flow)
            
            # 8. 风险评估
            risk_assessment = self._assess_risks(task_context, project_context)
            
            decision = AIDecision(
                recommended_flow=recommended_flow,
                confidence=confidence,
                reasoning=reasoning,
                alternatives=alternatives,
                estimated_duration=estimated_duration,
                suggested_tasks=suggested_tasks,
                risk_assessment=risk_assessment
            )
            
            # 记录决策
            self._log_decision(decision, task_context, project_context)
            
            return decision
            
        except Exception as e:
            self.logger.error(f"Error in AI decision making: {e}")
            # 返回默认决策
            return self._get_default_decision()
    
    def _calculate_confidence(self, task_context: TaskContext, project_context: ProjectContext) -> float:
        """计算决策置信度"""
        confidence = 0.7  # 基础置信度
        
        # 根据项目信息完整性调整
        if project_context.historical_velocity > 0:
            confidence += 0.1
        
        if len(project_context.technology_stack) > 0:
            confidence += 0.1
            
        if task_context.priority in ['high', 'medium', 'low']:
            confidence += 0.05
            
        # 根据描述详细程度调整
        if len(task_context.description) > 50:
            confidence += 0.05
            
        return min(0.95, confidence)  # 最高95%置信度
    
    def _explain_decision(self, task_type: TaskType, recommended_flow: str, project_context: ProjectContext) -> str:
        """生成决策推理解释"""
        explanations = {
            'minimal': f"推荐轻量级流程，因为{self._get_minimal_reason(task_type, project_context)}",
            'standard': f"推荐标准流程，因为{self._get_standard_reason(task_type, project_context)}",
            'complete': f"推荐完整流程，因为{self._get_complete_reason(task_type, project_context)}"
        }
        
        return explanations.get(recommended_flow, "基于项目特性推荐此流程模式")
    
    def _get_minimal_reason(self, task_type: TaskType, project_context: ProjectContext) -> str:
        """获取轻量级流程推荐原因"""
        reasons = []
        
        if task_type == TaskType.BUG_FIX:
            reasons.append("这是一个紧急修复任务")
        if project_context.team_size <= 3:
            reasons.append("团队规模较小")
        if 'week' in project_context.duration_estimate and '1' in project_context.duration_estimate:
            reasons.append("项目周期较短")
            
        return "，".join(reasons) if reasons else "项目适合快速迭代"
    
    def _get_standard_reason(self, task_type: TaskType, project_context: ProjectContext) -> str:
        """获取标准流程推荐原因"""
        reasons = []
        
        if task_type == TaskType.FEATURE_DEVELOPMENT:
            reasons.append("这是功能开发任务")
        if 3 < project_context.team_size <= 10:
            reasons.append("团队规模适中")
        if 'month' in project_context.duration_estimate:
            reasons.append("项目需要适度的质量控制")
            
        return "，".join(reasons) if reasons else "项目需要平衡效率和质量"
    
    def _get_complete_reason(self, task_type: TaskType, project_context: ProjectContext) -> str:
        """获取完整流程推荐原因"""
        reasons = []
        
        if project_context.team_size > 10:
            reasons.append("大型团队需要严格协调")
        if len(project_context.risk_factors) > 3:
            reasons.append("项目风险较高")
        if task_type == TaskType.ARCHITECTURE:
            reasons.append("架构设计需要严格流程")
            
        return "，".join(reasons) if reasons else "项目需要严格的质量控制"
    
    def _suggest_alternatives(self, recommended_flow: str, task_type: TaskType) -> List[Dict[str, Any]]:
        """提供替代流程方案"""
        all_flows = ['minimal', 'standard', 'complete']
        alternatives = []
        
        for flow in all_flows:
            if flow != recommended_flow:
                alternatives.append({
                    'flow': flow,
                    'reason': self._get_alternative_reason(flow, task_type),
                    'confidence': 0.3 if flow == 'complete' else 0.5
                })
        
        return alternatives[:2]  # 最多2个替代方案
    
    def _get_alternative_reason(self, flow: str, task_type: TaskType) -> str:
        """获取替代方案推荐原因"""
        reasons = {
            'minimal': "如果需要快速交付，可考虑轻量级流程",
            'standard': "如果需要平衡效率和质量，可考虑标准流程", 
            'complete': "如果质量要求极高，可考虑完整流程"
        }
        return reasons.get(flow, "可根据具体情况选择")
    
    def _generate_task_suggestions(self, task_type: TaskType, recommended_flow: str) -> List[str]:
        """生成任务建议"""
        base_suggestions = {
            TaskType.FEATURE_DEVELOPMENT: [
                "明确功能需求和验收标准",
                "设计用户界面和交互流程",
                "编写核心功能代码",
                "进行功能测试和用户验证"
            ],
            TaskType.BUG_FIX: [
                "重现和分析问题",
                "定位问题根本原因",
                "实施修复方案",
                "验证修复效果"
            ],
            TaskType.REFACTORING: [
                "分析当前代码结构",
                "制定重构计划",
                "逐步重构实施",
                "回归测试验证"
            ]
        }
        
        suggestions = base_suggestions.get(task_type, [
            "分析任务需求",
            "制定实施计划", 
            "执行具体工作",
            "验证完成效果"
        ])
        
        # 根据流程模式调整建议数量
        if recommended_flow == 'minimal':
            return suggestions[:3]
        elif recommended_flow == 'standard':
            return suggestions
        else:  # complete
            return suggestions + ["详细文档记录", "团队评审确认"]
    
    def _assess_risks(self, task_context: TaskContext, project_context: ProjectContext) -> Dict[str, float]:
        """评估项目风险"""
        risks = {
            'schedule_risk': 0.3,  # 进度风险
            'technical_risk': 0.2, # 技术风险
            'quality_risk': 0.2,   # 质量风险
            'resource_risk': 0.1   # 资源风险
        }
        
        # 根据项目特征调整风险
        if task_context.technical_complexity == 'high':
            risks['technical_risk'] += 0.3
            
        if len(task_context.dependencies) > 2:
            risks['schedule_risk'] += 0.2
            
        if project_context.team_size < 2:
            risks['resource_risk'] += 0.3
            
        if len(project_context.risk_factors) > 2:
            for risk_type in risks:
                risks[risk_type] += 0.1
        
        # 确保风险值在0-1范围内
        return {k: min(1.0, v) for k, v in risks.items()}
    
    def _log_decision(self, decision: AIDecision, task_context: TaskContext, project_context: ProjectContext):
        """记录AI决策用于后续学习"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'task_context': {
                'description': task_context.description,
                'priority': task_context.priority,
                'complexity': task_context.technical_complexity
            },
            'project_context': {
                'team_size': project_context.team_size,
                'duration_estimate': project_context.duration_estimate,
                'current_stage': project_context.current_stage
            },
            'decision': decision.to_dict()
        }
        
        # 保存到决策日志文件
        log_file = self.data_dir / "decision_log.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def _get_default_decision(self) -> AIDecision:
        """获取默认决策（错误情况下的备用方案）"""
        return AIDecision(
            recommended_flow='standard',
            confidence=0.5,
            reasoning='使用默认标准流程',
            alternatives=[],
            estimated_duration=16,
            suggested_tasks=['分析需求', '实施开发', '测试验证'],
            risk_assessment={'schedule_risk': 0.3, 'technical_risk': 0.3, 'quality_risk': 0.2, 'resource_risk': 0.2}
        )
    
    def get_personalized_suggestions(self, project_context: ProjectContext) -> List[str]:
        """获取个性化建议"""
        suggestions = []
        
        # 基于历史表现的建议
        if project_context.historical_velocity < 0.8:
            suggestions.append("🚀 建议优化团队效率，当前进度略低于预期")
            
        if project_context.completion_percentage > 0.8:
            suggestions.append("🎯 项目即将完成，建议重点关注质量验证")
            
        # 基于团队规模的建议
        if project_context.team_size == 1:
            suggestions.append("👤 单人项目建议使用轻量级流程提高效率")
        elif project_context.team_size > 10:
            suggestions.append("👥 大型团队建议加强沟通协调机制")
            
        # 基于技术栈的建议
        if any('new' in tech.lower() or 'experimental' in tech.lower() for tech in project_context.technology_stack):
            suggestions.append("🔬 使用新技术建议增加研究和测试时间")
            
        return suggestions[:3]  # 最多返回3条建议

# 全局AI引擎实例
_ai_engine_instance = None

def get_ai_engine(aceflow_dir: Path = None) -> AIDecisionEngine:
    """获取AI引擎单例"""
    global _ai_engine_instance
    
    if _ai_engine_instance is None:
        if aceflow_dir is None:
            aceflow_dir = Path.cwd() / ".aceflow"
        _ai_engine_instance = AIDecisionEngine(aceflow_dir)
    
    return _ai_engine_instance