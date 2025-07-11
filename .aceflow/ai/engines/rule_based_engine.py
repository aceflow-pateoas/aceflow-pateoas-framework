#!/usr/bin/env python3
"""
AceFlow v2.0 基于规则的轻量级决策引擎
专为Agent工具集成设计，无需外部LLM
"""

import json
import yaml
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

# 任务类型枚举
class TaskType(Enum):
    FEATURE_DEVELOPMENT = "feature_development"
    BUG_FIX = "bug_fix"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    RESEARCH = "research"
    ARCHITECTURE = "architecture"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"

# 项目复杂度枚举
class ProjectComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"

# 流程模式枚举
class FlowMode(Enum):
    MINIMAL = "minimal"
    STANDARD = "standard"
    COMPLETE = "complete"

@dataclass
class ProjectProfile:
    """项目特征画像"""
    project_type: str = "unknown"
    team_size: int = 1
    complexity: ProjectComplexity = ProjectComplexity.SIMPLE
    tech_stack: List[str] = None
    has_tests: bool = False
    has_ci_cd: bool = False
    has_documentation: bool = False
    git_activity: str = "low"  # low, medium, high
    file_count: int = 0
    
    def __post_init__(self):
        if self.tech_stack is None:
            self.tech_stack = []

@dataclass
class DecisionResult:
    """决策结果"""
    recommended_flow: str
    confidence: float
    reasoning: str
    steps: List[str]
    estimated_hours: int
    alternatives: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class PatternMatcher:
    """任务模式匹配器"""
    
    def __init__(self):
        self.patterns = {
            TaskType.BUG_FIX: [
                r'(fix|bug|error|issue|problem|crash|fail)',
                r'(修复|错误|问题|故障|崩溃|失败)',
                r'(debug|debugging)',
                r'(not working|broken|incorrect)',
                r'(无法|不能|无效|失效)'
            ],
            TaskType.FEATURE_DEVELOPMENT: [
                r'(add|new|create|implement|build|develop)',
                r'(feature|functionality|capability|module|component)',
                r'(新增|添加|创建|实现|开发|构建)',
                r'(功能|特性|模块|组件|接口)',
                r'(enhancement|improvement|upgrade)',
                r'(增强|改进|升级|扩展)'
            ],
            TaskType.REFACTORING: [
                r'(refactor|refactoring|restructure|reorganize)',
                r'(optimize|optimization|improve|clean)',
                r'(重构|重组|优化|改进|整理)',
                r'(code quality|performance|maintainability)',
                r'(代码质量|性能|可维护性)'
            ],
            TaskType.TESTING: [
                r'(test|testing|unit test|integration test)',
                r'(测试|单元测试|集成测试|测试用例)',
                r'(coverage|test coverage|qa)',
                r'(覆盖率|测试覆盖率|质量保证)',
                r'(verify|validation|check)',
                r'(验证|校验|检查)'
            ],
            TaskType.DOCUMENTATION: [
                r'(doc|docs|documentation|readme|guide)',
                r'(文档|说明|指南|手册)',
                r'(comment|comments|api doc)',
                r'(注释|API文档|接口文档)',
                r'(tutorial|example|demo)',
                r'(教程|示例|演示)'
            ],
            TaskType.RESEARCH: [
                r'(research|investigate|explore|study)',
                r'(调研|研究|探索|分析)',
                r'(poc|proof of concept|spike)',
                r'(原型|概念验证|技术验证)',
                r'(evaluation|comparison|analysis)',
                r'(评估|比较|分析)'
            ],
            TaskType.ARCHITECTURE: [
                r'(architecture|design|structure|framework)',
                r'(架构|设计|结构|框架)',
                r'(system design|technical design)',
                r'(系统设计|技术设计)',
                r'(blueprint|plan|specification)',
                r'(蓝图|规划|规范)'
            ],
            TaskType.DEPLOYMENT: [
                r'(deploy|deployment|release|publish)',
                r'(部署|发布|上线|发版)',
                r'(ci/cd|pipeline|build)',
                r'(环境|生产环境|服务器)',
                r'(docker|kubernetes|container)',
                r'(容器|容器化|编排)'
            ],
            TaskType.MAINTENANCE: [
                r'(maintain|maintenance|update|upgrade)',
                r'(维护|更新|升级|迁移)',
                r'(security|vulnerability|patch)',
                r'(安全|漏洞|补丁)',
                r'(dependency|library|framework)',
                r'(依赖|库|框架)'
            ]
        }
    
    def classify_task(self, task_description: str) -> TaskType:
        """基于模式匹配分类任务"""
        if not task_description:
            return TaskType.FEATURE_DEVELOPMENT
        
        task_lower = task_description.lower()
        scores = {}
        
        for task_type, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, task_lower):
                    score += 1
            scores[task_type] = score
        
        # 返回得分最高的任务类型
        if scores:
            best_type = max(scores, key=scores.get)
            if scores[best_type] > 0:
                return best_type
        
        return TaskType.FEATURE_DEVELOPMENT

class ProjectAnalyzer:
    """项目分析器"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.aceflow_dir = self.project_root / ".aceflow"
    
    def analyze_project(self) -> ProjectProfile:
        """分析项目特征"""
        profile = ProjectProfile()
        
        # 分析项目类型
        profile.project_type = self._detect_project_type()
        
        # 分析团队规模
        profile.team_size = self._estimate_team_size()
        
        # 分析复杂度
        profile.complexity = self._assess_complexity()
        
        # 分析技术栈
        profile.tech_stack = self._detect_tech_stack()
        
        # 分析项目特征
        profile.has_tests = self._has_tests()
        profile.has_ci_cd = self._has_ci_cd()
        profile.has_documentation = self._has_documentation()
        profile.git_activity = self._assess_git_activity()
        profile.file_count = self._count_files()
        
        return profile
    
    def _detect_project_type(self) -> str:
        """检测项目类型"""
        # 检查配置文件
        config_file = self.aceflow_dir / "config.yaml"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if 'project' in config and 'project_type' in config['project']:
                        return config['project']['project_type']
            except:
                pass
        
        # 基于文件检测
        if (self.project_root / "package.json").exists():
            return "web"
        elif (self.project_root / "requirements.txt").exists() or (self.project_root / "pyproject.toml").exists():
            return "python"
        elif (self.project_root / "pom.xml").exists():
            return "java"
        elif (self.project_root / "Cargo.toml").exists():
            return "rust"
        elif (self.project_root / "go.mod").exists():
            return "go"
        elif (self.project_root / "pubspec.yaml").exists():
            return "flutter"
        else:
            return "unknown"
    
    def _estimate_team_size(self) -> int:
        """估算团队规模"""
        # 从配置文件读取
        config_file = self.aceflow_dir / "config.yaml"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if 'project' in config and 'team_size' in config['project']:
                        team_size_str = config['project']['team_size']
                        if isinstance(team_size_str, int):
                            return team_size_str
                        elif isinstance(team_size_str, str):
                            # 解析 "1-5人" 格式
                            import re
                            match = re.search(r'(\d+)', team_size_str)
                            if match:
                                return int(match.group(1))
            except:
                pass
        
        # 基于Git提交者数量估算
        try:
            import subprocess
            result = subprocess.run(
                ["git", "log", "--pretty=format:%ae", "--since=3 months ago"],
                capture_output=True, text=True, cwd=self.project_root
            )
            if result.returncode == 0:
                contributors = set(result.stdout.strip().split('\n'))
                return max(1, len(contributors))
        except:
            pass
        
        return 1
    
    def _assess_complexity(self) -> ProjectComplexity:
        """评估项目复杂度"""
        score = 0
        
        # 文件数量
        file_count = self._count_files()
        if file_count > 100:
            score += 2
        elif file_count > 50:
            score += 1
        
        # 目录深度
        max_depth = self._get_max_directory_depth()
        if max_depth > 5:
            score += 2
        elif max_depth > 3:
            score += 1
        
        # 技术栈复杂度
        tech_stack = self._detect_tech_stack()
        if len(tech_stack) > 5:
            score += 2
        elif len(tech_stack) > 3:
            score += 1
        
        # 配置文件数量
        config_files = self._count_config_files()
        if config_files > 10:
            score += 2
        elif config_files > 5:
            score += 1
        
        # 依赖数量
        dependencies = self._count_dependencies()
        if dependencies > 50:
            score += 2
        elif dependencies > 20:
            score += 1
        
        # 根据得分确定复杂度
        if score >= 7:
            return ProjectComplexity.ENTERPRISE
        elif score >= 5:
            return ProjectComplexity.COMPLEX
        elif score >= 3:
            return ProjectComplexity.MODERATE
        else:
            return ProjectComplexity.SIMPLE
    
    def _detect_tech_stack(self) -> List[str]:
        """检测技术栈"""
        tech_stack = []
        
        # 检查常见文件
        tech_indicators = {
            "package.json": ["JavaScript", "Node.js"],
            "requirements.txt": ["Python"],
            "pyproject.toml": ["Python"],
            "pom.xml": ["Java", "Maven"],
            "build.gradle": ["Java", "Gradle"],
            "Cargo.toml": ["Rust"],
            "go.mod": ["Go"],
            "pubspec.yaml": ["Flutter", "Dart"],
            "composer.json": ["PHP"],
            "Gemfile": ["Ruby"],
            "mix.exs": ["Elixir"],
            "project.clj": ["Clojure"],
            "*.csproj": ["C#", ".NET"],
            "Dockerfile": ["Docker"],
            "docker-compose.yml": ["Docker Compose"],
            "k8s": ["Kubernetes"],
            ".github/workflows": ["GitHub Actions"],
            ".gitlab-ci.yml": ["GitLab CI"],
            "terraform": ["Terraform"],
            "ansible": ["Ansible"]
        }
        
        for file_pattern, technologies in tech_indicators.items():
            if '*' in file_pattern:
                # 通配符匹配
                pattern = file_pattern.replace('*', '**/*')
                if list(self.project_root.glob(pattern)):
                    tech_stack.extend(technologies)
            else:
                # 精确匹配
                if (self.project_root / file_pattern).exists():
                    tech_stack.extend(technologies)
        
        return list(set(tech_stack))
    
    def _count_files(self) -> int:
        """统计文件数量（排除隐藏文件和常见忽略目录）"""
        ignore_dirs = {'.git', '.aceflow', 'node_modules', '__pycache__', '.pytest_cache', 'target', 'build', 'dist'}
        ignore_files = {'.gitignore', '.DS_Store', 'Thumbs.db'}
        
        count = 0
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                # 检查是否在忽略目录中
                if any(ignore_dir in file_path.parts for ignore_dir in ignore_dirs):
                    continue
                # 检查是否是忽略文件
                if file_path.name in ignore_files:
                    continue
                count += 1
        
        return count
    
    def _get_max_directory_depth(self) -> int:
        """获取目录最大深度"""
        max_depth = 0
        for path in self.project_root.rglob('*'):
            if path.is_dir():
                depth = len(path.relative_to(self.project_root).parts)
                max_depth = max(max_depth, depth)
        return max_depth
    
    def _count_config_files(self) -> int:
        """统计配置文件数量"""
        config_patterns = [
            "*.json", "*.yaml", "*.yml", "*.toml", "*.ini", "*.cfg", "*.config",
            "*.properties", "*.env", "Dockerfile", "docker-compose*"
        ]
        
        count = 0
        for pattern in config_patterns:
            count += len(list(self.project_root.glob(pattern)))
        
        return count
    
    def _count_dependencies(self) -> int:
        """统计依赖数量"""
        count = 0
        
        # package.json
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)
                    count += len(data.get('dependencies', {}))
                    count += len(data.get('devDependencies', {}))
            except:
                pass
        
        # requirements.txt
        requirements = self.project_root / "requirements.txt"
        if requirements.exists():
            try:
                with open(requirements, 'r') as f:
                    lines = f.readlines()
                    count += len([line for line in lines if line.strip() and not line.startswith('#')])
            except:
                pass
        
        # pyproject.toml
        pyproject = self.project_root / "pyproject.toml"
        if pyproject.exists():
            try:
                import toml
                with open(pyproject, 'r') as f:
                    data = toml.load(f)
                    if 'tool' in data and 'poetry' in data['tool'] and 'dependencies' in data['tool']['poetry']:
                        count += len(data['tool']['poetry']['dependencies'])
            except:
                pass
        
        return count
    
    def _has_tests(self) -> bool:
        """检查是否有测试文件"""
        test_patterns = [
            "**/test_*.py", "**/tests/*.py", "**/*_test.py",
            "**/test*.js", "**/tests/*.js", "**/*.test.js", "**/*.spec.js",
            "**/test*.java", "**/tests/*.java", "**/*Test.java",
            "**/test*.go", "**/*_test.go"
        ]
        
        for pattern in test_patterns:
            if list(self.project_root.glob(pattern)):
                return True
        
        return False
    
    def _has_ci_cd(self) -> bool:
        """检查是否有CI/CD配置"""
        ci_cd_files = [
            ".github/workflows",
            ".gitlab-ci.yml",
            ".travis.yml",
            "circle.yml",
            "appveyor.yml",
            "jenkins.yml",
            "Jenkinsfile"
        ]
        
        for file_path in ci_cd_files:
            if (self.project_root / file_path).exists():
                return True
        
        return False
    
    def _has_documentation(self) -> bool:
        """检查是否有文档"""
        doc_files = [
            "README.md", "README.rst", "README.txt",
            "docs", "doc", "documentation",
            "CHANGELOG.md", "CHANGELOG.rst",
            "API.md", "api.md"
        ]
        
        for file_path in doc_files:
            if (self.project_root / file_path).exists():
                return True
        
        return False
    
    def _assess_git_activity(self) -> str:
        """评估Git活动水平"""
        try:
            import subprocess
            from datetime import datetime, timedelta
            
            # 最近3个月的提交数
            three_months_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            result = subprocess.run(
                ["git", "log", "--oneline", f"--since={three_months_ago}"],
                capture_output=True, text=True, cwd=self.project_root
            )
            
            if result.returncode == 0:
                commit_count = len(result.stdout.strip().split('\n'))
                if commit_count > 100:
                    return "high"
                elif commit_count > 20:
                    return "medium"
                else:
                    return "low"
        except:
            pass
        
        return "low"

class RuleEngine:
    """规则引擎"""
    
    def __init__(self):
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict[str, Any]:
        """加载决策规则"""
        return {
            "flow_rules": {
                "minimal": {
                    "conditions": [
                        {"field": "task_type", "operator": "in", "value": ["BUG_FIX", "MAINTENANCE", "DOCUMENTATION"]},
                        {"field": "team_size", "operator": "<=", "value": 3},
                        {"field": "complexity", "operator": "==", "value": "SIMPLE"},
                        {"field": "urgency", "operator": "==", "value": "high"}
                    ],
                    "weight": 1.0
                },
                "standard": {
                    "conditions": [
                        {"field": "task_type", "operator": "in", "value": ["FEATURE_DEVELOPMENT", "TESTING", "REFACTORING"]},
                        {"field": "team_size", "operator": "between", "value": [3, 8]},
                        {"field": "complexity", "operator": "in", "value": ["MODERATE", "COMPLEX"]},
                        {"field": "has_tests", "operator": "==", "value": True}
                    ],
                    "weight": 1.0
                },
                "complete": {
                    "conditions": [
                        {"field": "task_type", "operator": "in", "value": ["ARCHITECTURE", "RESEARCH", "DEPLOYMENT"]},
                        {"field": "team_size", "operator": ">", "value": 8},
                        {"field": "complexity", "operator": "==", "value": "ENTERPRISE"},
                        {"field": "has_ci_cd", "operator": "==", "value": True}
                    ],
                    "weight": 1.0
                }
            },
            "estimation_rules": {
                "BUG_FIX": {"base_hours": 4, "complexity_factor": 1.2},
                "FEATURE_DEVELOPMENT": {"base_hours": 16, "complexity_factor": 1.5},
                "REFACTORING": {"base_hours": 8, "complexity_factor": 1.3},
                "TESTING": {"base_hours": 6, "complexity_factor": 1.1},
                "DOCUMENTATION": {"base_hours": 4, "complexity_factor": 1.0},
                "RESEARCH": {"base_hours": 12, "complexity_factor": 1.4},
                "ARCHITECTURE": {"base_hours": 24, "complexity_factor": 1.6},
                "DEPLOYMENT": {"base_hours": 8, "complexity_factor": 1.2},
                "MAINTENANCE": {"base_hours": 6, "complexity_factor": 1.1}
            }
        }
    
    def evaluate_flow_rules(self, task_type: TaskType, project_profile: ProjectProfile, 
                           urgency: str = "medium") -> Dict[str, float]:
        """评估流程规则，返回各流程的匹配分数"""
        scores = {}
        
        # 构建评估上下文
        context = {
            "task_type": task_type.value.upper(),
            "team_size": project_profile.team_size,
            "complexity": project_profile.complexity.value.upper(),
            "has_tests": project_profile.has_tests,
            "has_ci_cd": project_profile.has_ci_cd,
            "urgency": urgency
        }
        
        # 评估每个流程
        for flow_name, flow_rule in self.rules["flow_rules"].items():
            score = self._evaluate_conditions(flow_rule["conditions"], context)
            scores[flow_name] = score * flow_rule["weight"]
        
        return scores
    
    def _evaluate_conditions(self, conditions: List[Dict], context: Dict) -> float:
        """评估条件集合，返回匹配分数"""
        if not conditions:
            return 0.0
        
        matched_count = 0
        total_count = len(conditions)
        
        for condition in conditions:
            if self._evaluate_single_condition(condition, context):
                matched_count += 1
        
        return matched_count / total_count
    
    def _evaluate_single_condition(self, condition: Dict, context: Dict) -> bool:
        """评估单个条件"""
        field = condition["field"]
        operator = condition["operator"]
        value = condition["value"]
        
        if field not in context:
            return False
        
        context_value = context[field]
        
        if operator == "==":
            return context_value == value
        elif operator == "!=":
            return context_value != value
        elif operator == "<":
            return context_value < value
        elif operator == "<=":
            return context_value <= value
        elif operator == ">":
            return context_value > value
        elif operator == ">=":
            return context_value >= value
        elif operator == "in":
            return context_value in value
        elif operator == "not_in":
            return context_value not in value
        elif operator == "between":
            return value[0] <= context_value <= value[1]
        else:
            return False
    
    def estimate_duration(self, task_type: TaskType, project_profile: ProjectProfile) -> int:
        """估算任务持续时间"""
        task_key = task_type.value.upper()
        
        if task_key not in self.rules["estimation_rules"]:
            return 8  # 默认8小时
        
        rule = self.rules["estimation_rules"][task_key]
        base_hours = rule["base_hours"]
        complexity_factor = rule["complexity_factor"]
        
        # 应用复杂度因子
        complexity_multiplier = {
            ProjectComplexity.SIMPLE: 1.0,
            ProjectComplexity.MODERATE: 1.2,
            ProjectComplexity.COMPLEX: 1.5,
            ProjectComplexity.ENTERPRISE: 2.0
        }
        
        hours = base_hours * complexity_factor * complexity_multiplier[project_profile.complexity]
        
        # 应用团队规模因子
        if project_profile.team_size > 5:
            hours *= 1.2  # 大团队协调成本
        elif project_profile.team_size == 1:
            hours *= 0.9  # 单人项目效率
        
        return int(hours)

class RuleBasedDecisionEngine:
    """基于规则的决策引擎"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.pattern_matcher = PatternMatcher()
        self.project_analyzer = ProjectAnalyzer(self.project_root)
        self.rule_engine = RuleEngine()
    
    def make_decision(self, task_input: str, context: Dict[str, Any] = None) -> DecisionResult:
        """做出决策"""
        if context is None:
            context = {}
        
        # 1. 任务分类
        task_type = self.pattern_matcher.classify_task(task_input)
        
        # 2. 项目分析
        project_profile = self.project_analyzer.analyze_project()
        
        # 3. 应用上下文覆盖
        self._apply_context_overrides(project_profile, context)
        
        # 4. 流程推荐
        flow_scores = self.rule_engine.evaluate_flow_rules(
            task_type, project_profile, context.get("urgency", "medium")
        )
        
        # 5. 选择最佳流程
        recommended_flow = max(flow_scores, key=flow_scores.get)
        confidence = flow_scores[recommended_flow]
        
        # 6. 生成步骤
        steps = self._generate_steps(recommended_flow)
        
        # 7. 估算时间
        estimated_hours = self.rule_engine.estimate_duration(task_type, project_profile)
        
        # 8. 生成推理解释
        reasoning = self._generate_reasoning(task_type, project_profile, recommended_flow, confidence)
        
        # 9. 提供替代方案
        alternatives = self._generate_alternatives(flow_scores, recommended_flow)
        
        # 10. 元数据
        metadata = {
            "task_type": task_type.value,
            "project_profile": asdict(project_profile),
            "flow_scores": flow_scores,
            "timestamp": datetime.now().isoformat()
        }
        
        return DecisionResult(
            recommended_flow=recommended_flow,
            confidence=confidence,
            reasoning=reasoning,
            steps=steps,
            estimated_hours=estimated_hours,
            alternatives=alternatives,
            metadata=metadata
        )
    
    def _apply_context_overrides(self, project_profile: ProjectProfile, context: Dict[str, Any]):
        """应用上下文覆盖"""
        if "team_size" in context:
            project_profile.team_size = context["team_size"]
        if "project_type" in context:
            project_profile.project_type = context["project_type"]
        if "complexity" in context:
            if isinstance(context["complexity"], str):
                project_profile.complexity = ProjectComplexity(context["complexity"])
    
    def _generate_steps(self, flow_mode: str) -> List[str]:
        """生成流程步骤"""
        flow_steps = {
            "minimal": [
                "Planning (P): 需求分析和任务规划",
                "Development (D): 开发实现",
                "Review (R): 代码审查和测试验证"
            ],
            "standard": [
                "Planning 1 (P1): 需求分析和架构设计",
                "Planning 2 (P2): 详细设计和任务分解",
                "Development 1 (D1): 核心功能开发",
                "Development 2 (D2): 集成和优化",
                "Review 1 (R1): 测试和质量验证"
            ],
            "complete": [
                "Strategy (S1): 项目策略和目标制定",
                "Analysis (S2): 需求分析和可行性研究",
                "Design (S3): 系统设计和架构规划",
                "Planning (S4): 详细计划和资源分配",
                "Development (S5): 开发实现",
                "Integration (S6): 系统集成和联调",
                "Testing (S7): 全面测试和质量保证",
                "Deployment (S8): 部署和上线"
            ]
        }
        
        return flow_steps.get(flow_mode, flow_steps["standard"])
    
    def _generate_reasoning(self, task_type: TaskType, project_profile: ProjectProfile, 
                          recommended_flow: str, confidence: float) -> str:
        """生成推理解释"""
        reasons = []
        
        # 任务类型相关推理
        if task_type == TaskType.BUG_FIX:
            reasons.append("这是一个bug修复任务，通常需要快速响应")
        elif task_type == TaskType.FEATURE_DEVELOPMENT:
            reasons.append("这是功能开发任务，需要完整的开发流程")
        elif task_type == TaskType.ARCHITECTURE:
            reasons.append("这是架构设计任务，需要严格的规划和审查")
        
        # 项目特征相关推理
        if project_profile.team_size <= 3:
            reasons.append("小团队适合轻量级流程")
        elif project_profile.team_size > 8:
            reasons.append("大团队需要更严格的协调流程")
        
        if project_profile.complexity == ProjectComplexity.SIMPLE:
            reasons.append("项目复杂度较低，可以简化流程")
        elif project_profile.complexity == ProjectComplexity.ENTERPRISE:
            reasons.append("企业级项目需要完整的质量保证流程")
        
        # 技术特征相关推理
        if project_profile.has_tests:
            reasons.append("项目有测试基础，支持标准化流程")
        if project_profile.has_ci_cd:
            reasons.append("项目有CI/CD支持，适合自动化流程")
        
        # 置信度解释
        if confidence > 0.8:
            confidence_text = "高置信度推荐"
        elif confidence > 0.6:
            confidence_text = "中等置信度推荐"
        else:
            confidence_text = "低置信度推荐，请根据实际情况调整"
        
        reasoning = f"推荐使用{recommended_flow}流程，{confidence_text}。"
        if reasons:
            reasoning += "主要原因：" + "，".join(reasons) + "。"
        
        return reasoning
    
    def _generate_alternatives(self, flow_scores: Dict[str, float], 
                             recommended_flow: str) -> List[Dict[str, Any]]:
        """生成替代方案"""
        alternatives = []
        
        # 排序并排除推荐流程
        sorted_flows = sorted(
            [(flow, score) for flow, score in flow_scores.items() if flow != recommended_flow],
            key=lambda x: x[1], reverse=True
        )
        
        for flow, score in sorted_flows[:2]:  # 最多2个替代方案
            reason = self._get_alternative_reason(flow, score)
            alternatives.append({
                "flow": flow,
                "confidence": score,
                "reason": reason
            })
        
        return alternatives
    
    def _get_alternative_reason(self, flow: str, score: float) -> str:
        """获取替代方案的推荐理由"""
        reasons = {
            "minimal": "如果时间紧迫或团队经验丰富，可以选择轻量级流程",
            "standard": "如果需要平衡效率和质量，可以选择标准流程",
            "complete": "如果质量要求很高或团队较大，可以选择完整流程"
        }
        
        base_reason = reasons.get(flow, "可以考虑此流程")
        
        if score > 0.5:
            return f"{base_reason}（匹配度：{score:.1%}）"
        else:
            return f"{base_reason}（匹配度较低：{score:.1%}）"

# 全局引擎实例
_engine_instance = None

def get_decision_engine(project_root: Path = None) -> RuleBasedDecisionEngine:
    """获取决策引擎单例"""
    global _engine_instance
    
    if _engine_instance is None:
        _engine_instance = RuleBasedDecisionEngine(project_root)
    
    return _engine_instance

def main():
    """测试主函数"""
    engine = get_decision_engine()
    
    # 测试用例
    test_cases = [
        "修复用户登录页面的显示错误",
        "为移动应用添加推送通知功能",
        "重构支付模块的代码结构",
        "编写API接口的单元测试",
        "更新项目的技术文档",
        "调研新的前端框架",
        "设计微服务架构",
        "部署应用到生产环境"
    ]
    
    print("🤖 AceFlow基于规则的决策引擎测试")
    print("=" * 50)
    
    for i, task in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {task}")
        print("-" * 30)
        
        result = engine.make_decision(task)
        print(f"推荐流程: {result.recommended_flow}")
        print(f"置信度: {result.confidence:.1%}")
        print(f"推理: {result.reasoning}")
        print(f"预估时间: {result.estimated_hours}小时")
        print(f"流程步骤: {len(result.steps)}个步骤")
        
        if result.alternatives:
            print("替代方案:")
            for alt in result.alternatives:
                print(f"  - {alt['flow']}: {alt['reason']}")

if __name__ == "__main__":
    main()