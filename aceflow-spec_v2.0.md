# AceFlow v2.0 规范文档

> **版本**: v2.0.0  
> **更新时间**: 2025-07-11  
> **类型**: 技术规范  
> **适用范围**: AceFlow工作流管理系统

## 🎯 系统概述

AceFlow v2.0是一个AI驱动的软件开发工作流管理系统，基于PATEOAS（Hypermedia as the Engine of Application State）理念，提供分层式、渐进式的开发流程管理。

### 核心理念
- **状态驱动架构**: 基于项目状态自动推荐和管理工作流
- **分层式流程**: 支持轻量级、标准、完整三种流程模式
- **AI智能决策**: 基于项目特征和历史数据提供智能建议
- **敏捷集成**: 与Scrum、Kanban等敏捷框架深度集成

## 📋 流程模式规范

### 1. 轻量级模式 (Minimal Mode)
**代码标识**: `minimal`  
**适用场景**: 1-5人团队，快速迭代，原型验证  
**典型周期**: 2-7天

#### 阶段定义
```yaml
工作流模式: P → D → R

P (Planning/规划):
  - 时长: 4-8小时
  - 目标: 明确需求、设计方案、制定计划
  - 交付物: 需求文档、技术方案、任务列表

D (Development/开发):
  - 时长: 1-4天
  - 目标: 编码实现、测试验证、代码审查
  - 交付物: 功能代码、测试用例、代码文档

R (Review/评审):
  - 时长: 2-4小时
  - 目标: 功能验证、性能测试、用户反馈
  - 交付物: 测试报告、评审记录、改进建议
```

### 2. 标准模式 (Standard Mode)
**代码标识**: `standard`  
**适用场景**: 3-10人团队，企业应用，复杂功能  
**典型周期**: 1-2周

#### 阶段定义
```yaml
工作流模式: P1 → P2 → D1 → D2 → R1

P1 (需求分析):
  - 时长: 1-2天
  - 目标: 收集用户需求、分析业务场景
  - 交付物: 用户故事、业务流程图、需求规格说明

P2 (技术规划):
  - 时长: 1-2天
  - 目标: 技术方案设计、任务分解
  - 交付物: 架构设计、API设计、开发计划

D1 (功能实现):
  - 时长: 3-5天
  - 目标: 核心功能开发、模块集成
  - 交付物: 核心模块代码、集成接口、单元测试

D2 (质量验证):
  - 时长: 2-3天
  - 目标: 单元测试、集成测试、用户测试
  - 交付物: 测试套件、测试报告、缺陷修复

R1 (发布评审):
  - 时长: 1天
  - 目标: 代码审查、性能评估、文档整理
  - 交付物: 代码审查报告、性能测试报告、发布文档
```

### 3. 完整模式 (Complete Mode)
**代码标识**: `complete`  
**适用场景**: 10+人团队，关键系统，严格质量控制  
**典型周期**: 2-4周

#### 阶段定义
```yaml
工作流模式: S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8

S1 (用户故事):
  - 时长: 2-3天
  - 目标: 收集和分析用户需求
  - 交付物: 用户故事地图、验收标准、优先级排序

S2 (任务拆分):
  - 时长: 2-3天
  - 目标: 技术任务分解和规划
  - 交付物: 工作分解结构、技术任务清单、依赖关系图

S3 (测试用例):
  - 时长: 2-3天
  - 目标: 设计测试策略和用例
  - 交付物: 测试计划、测试用例库、自动化测试框架

S4 (功能实现):
  - 时长: 5-8天
  - 目标: 核心功能开发
  - 交付物: 功能模块代码、API接口实现、数据库脚本

S5 (测试执行):
  - 时长: 3-5天
  - 目标: 全面测试验证
  - 交付物: 测试执行报告、缺陷跟踪记录、性能测试报告

S6 (代码评审):
  - 时长: 2-3天
  - 目标: 代码质量审查
  - 交付物: 代码审查报告、重构建议、最佳实践文档

S7 (演示反馈):
  - 时长: 1-2天
  - 目标: 用户演示和反馈收集
  - 交付物: 演示材料、用户反馈报告、改进计划

S8 (总结归档):
  - 时长: 1天
  - 目标: 项目总结和知识归档
  - 交付物: 项目总结报告、知识库更新、最佳实践提取
```

## 🔧 技术架构规范

### 1. 系统组件
```yaml
核心组件:
  - CLI工具: .aceflow/scripts/aceflow
  - 状态管理: .aceflow/state/project_state.json
  - 配置管理: .aceflow/config/flow_modes.yaml
  - AI引擎: .aceflow/ai/
  - 模板系统: .aceflow/templates/

扩展组件:
  - Web界面: .aceflow/web/
  - 记忆池: .aceflow/memory_pool/
  - 报告系统: .aceflow/reports/
```

### 2. 状态管理规范
```json
{
  "project_id": "string",
  "flow_mode": "minimal|standard|complete",
  "current_stage": "string|null",
  "stage_states": {
    "stage_id": {
      "status": "pending|in_progress|completed",
      "progress": "0-100",
      "start_time": "ISO8601",
      "end_time": "ISO8601",
      "deliverables": ["string"]
    }
  },
  "created_at": "ISO8601",
  "last_updated": "ISO8601",
  "version": "string",
  "ai_suggestions": ["object"],
  "memory_pool": {
    "requirements": ["object"],
    "decisions": ["object"],
    "issues": ["object"],
    "feedback": ["object"]
  }
}
```

### 3. CLI命令规范
```bash
# 核心命令
aceflow init [--mode minimal|standard|complete]
aceflow start [stage_id] [--auto-docs]
aceflow progress --progress <0-100> [--stage stage_id]
aceflow complete [stage_id] [--generate]
aceflow status [--format text|json] [--verbose]

# AI增强命令
aceflow describe                    # 工具能力描述
aceflow suggest --task "string"    # 智能工作流推荐
aceflow plan --project-type "type" # 项目规划建议
aceflow track                       # 智能进度跟踪
aceflow memory                      # 记忆管理

# 辅助命令
aceflow web                         # 启动Web界面
aceflow help                        # 显示帮助
```

## 🤖 AI集成规范

### 1. 任务分类标准
```yaml
Bug修复类:
  触发词: ["修复", "fix", "bug", "问题", "错误", "不工作", "异常", "报错"]
  推荐模式: minimal
  预估时间: 30分钟-3小时
  
新功能开发:
  触发词: ["新功能", "添加", "实现", "开发", "需要一个", "用户需要"]
  推荐模式: standard
  预估时间: 1-5天
  
重构优化:
  触发词: ["重构", "优化", "改进", "重写", "架构调整", "性能优化"]
  推荐模式: standard/complete
  预估时间: 根据复杂度评估
  
大型项目:
  触发词: ["新项目", "从零开始", "完整系统", "企业级", "复杂功能"]
  推荐模式: complete
  预估时间: 2-4周
```

### 2. 智能决策流程
```yaml
1. 项目状态检测:
   - 检查.aceflow目录存在性
   - 读取项目状态文件
   - 分析当前阶段和进度

2. 用户意图分析:
   - 自然语言处理
   - 任务类型识别
   - 复杂度评估

3. 工作流推荐:
   - 基于项目特征推荐模式
   - 生成具体行动建议
   - 提供时间估算

4. 执行监控:
   - 实时进度跟踪
   - 异常状态检测
   - 自动化建议生成
```

### 3. 输出格式规范
```json
// 状态查询JSON输出
{
  "initialized": true,
  "project_id": "string",
  "flow_mode": "minimal|standard|complete",
  "current_stage": "string|null",
  "current_stage_name": "string|null",
  "overall_progress": "number",
  "completed_stages": "number",
  "total_stages": "number",
  "last_updated": "ISO8601",
  "version": "string",
  "next_actions": [
    {
      "action": "string",
      "stage": "string",
      "stage_name": "string",
      "command": "string",
      "priority": "high|medium|low",
      "description": "string"
    }
  ],
  "health_check": {
    "overall_health": "good|warning|error",
    "issues": ["string"],
    "recommendations": ["string"]
  },
  "ai_ready": true
}
```

## 🔄 集成规范

### 1. IDE集成标准
```yaml
VSCode集成:
  - 工作区配置: aceflow-workspace.code-workspace
  - 任务配置: .vscode/tasks.json
  - 设置文件: .vscode/settings.json
  - 扩展要求: ["saoudrizwan.claude-dev"]

AI Agent集成:
  - 提示词配置: .clinerules/aceflow_integration.md
  - 自动检测: 每次对话开始时检查项目状态
  - 命令执行: 支持所有CLI命令的自动执行
  - 状态同步: 实时更新项目状态
```

### 2. 文件系统规范
```yaml
必需文件:
  - .aceflow/scripts/aceflow           # 主CLI工具
  - .aceflow/state/project_state.json  # 项目状态
  - .aceflow/config/flow_modes.yaml    # 流程配置

配置文件:
  - .vscode/settings.json              # VSCode设置
  - .vscode/tasks.json                 # VSCode任务
  - .clinerules/aceflow_integration.md # AI集成规则
  - aceflow-workspace.code-workspace   # 工作区配置

模板文件:
  - .aceflow/templates/minimal/        # 轻量级模板
  - .aceflow/templates/standard/       # 标准模板
  - .aceflow/templates/complete/       # 完整模板
```

## 📊 质量标准

### 1. 性能要求
- CLI命令响应时间: < 2秒
- 状态文件读写: < 100ms
- JSON输出生成: < 500ms
- AI决策响应: < 3秒

### 2. 可用性要求
- 学习时间: 新用户2-4小时上手
- 配置复杂度: 初始化步骤≤5个
- 错误处理: 所有错误都有明确的解决建议
- 文档完整性: 所有功能都有使用示例

### 3. 兼容性要求
- Python版本: 3.8+
- 操作系统: Linux, macOS, Windows
- VSCode版本: 1.60+
- 扩展兼容: Cline, Cursor, Copilot

## 🔒 安全规范

### 1. 数据保护
- 项目状态文件权限控制
- 敏感信息不记录在状态文件中
- 内存池数据加密存储
- 网络传输使用HTTPS

### 2. 代码安全
- 输入验证和清理
- 防止代码注入攻击
- 文件路径安全检查
- 权限最小化原则

## 🚀 扩展规范

### 1. 插件系统
```yaml
插件接口:
  - 阶段生命周期钩子
  - 自定义AI决策规则
  - 外部工具集成
  - 自定义模板系统

扩展点:
  - AI决策引擎
  - 模板渲染器
  - 状态存储后端
  - 报告生成器
```

### 2. API规范
```yaml
REST API:
  - GET /status - 获取项目状态
  - POST /stages/{id}/start - 开始阶段
  - PUT /stages/{id}/progress - 更新进度
  - POST /stages/{id}/complete - 完成阶段
  - GET /suggest - 获取AI建议

WebSocket API:
  - /ws/status - 实时状态更新
  - /ws/progress - 进度实时推送
  - /ws/ai-suggestions - AI建议推送
```

## 📚 版本管理

### 1. 版本号规范
- 主版本号: 重大架构变更
- 次版本号: 功能增加或修改
- 修订版本号: Bug修复和优化

### 2. 向后兼容性
- 状态文件格式向后兼容
- CLI命令参数向后兼容
- 配置文件格式向后兼容
- API接口向后兼容

---

*此规范文档是AceFlow v2.0系统的技术标准，所有集成和扩展开发都应遵循此规范。*