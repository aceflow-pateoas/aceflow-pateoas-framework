# AceFlow v3.0 - Cline 集成提示词规范

## 🎯 集成目标

为 Cline AI Agent 提供完整的 AceFlow v3.0 工作流集成能力，使其能够：
- 自动识别和管理 AceFlow 项目
- 智能执行软件开发工作流
- 提供状态感知的开发助手服务
- 支持智能模式选择和自适应流程

## 🔍 项目自动检测

### 每次对话开始时执行
```bash
# 检查 AceFlow 项目状态
if [ -d ".aceflow" ]; then
    echo "🔍 检测到 AceFlow v3.0 项目"
    # 使用新的CLI工具
    aceflow status --format json --verbose
else
    echo "📋 未检测到 AceFlow 项目"
    echo "💡 建议：初始化 AceFlow 可以显著提升开发效率"
fi
```

### 项目状态分析
```python
def analyze_project_status():
    """
    分析项目状态并提供智能建议
    """
    # 读取状态文件
    state_file = ".aceflow/state/project_state.json"
    
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            project_state = json.load(f)
        
        # 分析当前状态
        current_mode = project_state.get('flow_mode', 'smart')
        current_stage = project_state.get('current_stage')
        progress = project_state.get('overall_progress', 0)
        
        # 提供状态感知的建议
        return generate_context_aware_suggestions(current_mode, current_stage, progress)
    else:
        return suggest_project_initialization()
```

## 🧠 智能任务分析

### 任务分类规范 (基于 v3.0 规范)

#### 智能模式 (Smart Mode) - 新增
**触发条件**: 用户描述开发任务但未指定模式
**AI响应模板**:
```markdown
🧠 **AceFlow 智能分析**

正在分析任务特征...
```bash
aceflow analyze "user_task_description" --format json
```

**智能推荐结果**:
- 📊 任务类型: {task_type}
- 🎯 复杂度: {complexity_level}
- 👥 团队规模: {team_size_estimate}
- ⏱️ 预估时间: {estimated_time}
- 🔄 推荐模式: {recommended_mode}
- 📈 置信度: {confidence_score}%

**详细分析**:
{detailed_analysis}

**执行计划**:
{execution_plan}

是否接受智能推荐并开始执行？
```

#### Bug修复 (Minimal Mode)
**触发词**: ["修复", "fix", "bug", "问题", "错误", "异常", "不工作"]
**AI响应模板**:
```markdown
🐛 **Bug修复工作流**

检测到Bug修复任务，启动轻量级模式...
```bash
aceflow start --mode minimal --description "Bug修复: user_description"
```

**工作流程**: P → D → R (预计 0.5-2天)
- P (规划): 问题复现、根因分析、影响评估
- D (开发): 修复实现、测试验证、回归测试
- R (评审): 代码审查、部署验证、文档更新

**质量门控**:
- 问题完全复现 ✅
- 根因分析清晰 ✅
- 修复方案无副作用 ✅
- 测试覆盖充分 ✅

是否开始Bug修复工作流？
```

#### 新功能开发 (Standard Mode)
**触发词**: ["新功能", "开发", "实现", "添加", "功能", "需求"]
**AI响应模板**:
```markdown
🚀 **新功能开发工作流**

检测到新功能开发任务，启动标准模式...
```bash
aceflow start --mode standard --description "新功能开发: user_description"
```

**工作流程**: P1 → P2 → D1 → D2 → R1 (预计 3-7天)
- P1 (需求分析): 用户故事、业务价值、验收标准
- P2 (技术设计): 架构设计、接口定义、数据结构
- D1 (功能开发): 核心实现、单元测试、集成测试
- D2 (质量验证): 功能测试、性能测试、安全测试
- R1 (发布准备): 代码审查、文档完善、部署准备

**质量门控**:
- 需求清晰完整 ✅
- 技术方案合理 ✅
- 代码质量达标 ✅
- 测试覆盖率 ≥ 80% ✅

是否开始新功能开发工作流？
```

#### 大型项目 (Complete Mode)
**触发词**: ["项目", "系统", "平台", "架构", "重构", "企业级"]
**AI响应模板**:
```markdown
🏗️ **大型项目工作流**

检测到大型项目任务，启动完整模式...
```bash
aceflow start --mode complete --description "大型项目: user_description"
```

**工作流程**: S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8 (预计 1-4周)
- S1 (用户故事): 完整需求分析、角色定义、价值映射
- S2 (任务分解): 详细任务拆分、依赖分析、里程碑规划
- S3 (测试设计): 测试策略、用例设计、自动化框架
- S4 (功能实现): 迭代式开发、持续集成、质量监控
- S5 (测试验证): 全面测试、性能调优、安全审核
- S6 (代码评审): 全面审查、架构评估、最佳实践
- S7 (演示反馈): 用户验收、反馈收集、改进计划
- S8 (总结归档): 项目总结、知识沉淀、经验提取

**质量门控**:
- 用户故事完整 ✅
- 任务分解合理 ✅
- 测试策略全面 ✅
- 代码质量优秀 ✅
- 用户满意度 ≥ 85% ✅

是否开始大型项目工作流？
```

## 🔄 智能执行引擎

### 自适应流程控制
```python
def adaptive_workflow_control(user_input, project_context):
    """
    自适应工作流控制逻辑
    """
    # 分析用户意图
    intent = analyze_user_intent(user_input)
    
    # 评估项目状态
    project_status = get_project_status()
    
    # 智能决策
    if intent.type == "continue_current":
        return continue_current_workflow(project_status)
    elif intent.type == "start_new":
        return start_new_workflow(intent, project_context)
    elif intent.type == "switch_mode":
        return suggest_mode_switch(intent, project_status)
    else:
        return provide_guidance(intent, project_status)
```

### 状态感知对话
```markdown
## 📊 项目状态概览

```
项目: {project_name}
模式: {flow_mode} (智能选择)
进度: ███████░░░ {progress}%

当前阶段: {current_stage} - {stage_name}
阶段进度: {stage_progress}%
预计完成: {estimated_completion}

最近活动:
- {recent_activity_1}
- {recent_activity_2}
- {recent_activity_3}
```

**🎯 下一步行动**:
{next_actions}

**⚠️ 注意事项**:
{warnings_and_recommendations}

**🤖 AI建议**:
{ai_suggestions}

需要我继续当前工作流吗？
```

## 🎯 具体阶段执行提示

### S1 - 用户故事分析 (增强版)
```markdown
## 🎯 S1 阶段: 用户故事分析

### 智能分析模式
正在使用AI增强的用户故事分析...

**执行步骤**:
1. **需求挖掘**: 使用5W1H方法深度分析用户需求
2. **角色识别**: 自动识别所有相关用户角色和利益相关者
3. **价值映射**: 建立功能与业务价值的映射关系
4. **故事编写**: 生成符合INVEST原则的用户故事
5. **验收标准**: 制定可测试的验收标准

### AI辅助功能
- 🧠 自动需求补全
- 🎯 智能优先级排序
- 📊 影响度评估
- 🔍 遗漏点检测

### 输出要求
- 用户故事文档: `/aceflow_result/{iteration_id}/S1_user_stories/`
- 角色分析报告: `/aceflow_result/{iteration_id}/S1_user_stories/user_roles.md`
- 业务价值映射: `/aceflow_result/{iteration_id}/S1_user_stories/value_mapping.md`

### 质量检查
- [ ] 每个故事符合INVEST原则
- [ ] 验收标准清晰可测
- [ ] 优先级排序合理
- [ ] 业务价值明确

**进度更新**: 完成后请告知，我将自动进入S2阶段。
```

### S4-S5 循环 (智能优化版)
```markdown
## 🔄 S4-S5 开发测试循环

### 智能任务调度
正在分析任务依赖关系，优化执行顺序...

**当前任务队列**:
```
高优先级:
1. {task_1} (预计 {time_1})
2. {task_2} (预计 {time_2})

中优先级:
3. {task_3} (预计 {time_3})
4. {task_4} (预计 {time_4})

低优先级:
5. {task_5} (预计 {time_5})
```

### 循环执行模式
```python
while has_pending_tasks():
    # 智能任务选择
    task = select_optimal_task()
    
    # S4: 功能实现
    print(f"🔧 开始实现: {task.name}")
    implementation_result = implement_task(task)
    
    # 自动代码质量检查
    quality_check = run_code_analysis(implementation_result)
    
    # S5: 测试验证
    print(f"🧪 开始测试: {task.name}")
    test_result = execute_tests(task)
    
    # 智能决策
    if test_result.passed and quality_check.passed:
        mark_task_completed(task)
        print(f"✅ 任务完成: {task.name}")
    else:
        handle_failures(task, test_result, quality_check)
```

### 质量门控
- [ ] 代码格式规范
- [ ] 单元测试通过
- [ ] 代码覆盖率 ≥ 80%
- [ ] 性能基准达标
- [ ] 安全扫描通过

**实时监控**: 我将实时监控开发进度，自动更新状态。
```

## 🤖 AI增强功能

### 智能代码审查
```markdown
## 🔍 AI代码审查助手

正在使用AI进行代码质量分析...

**审查维度**:
- 🏗️ 架构设计合理性
- 🎯 业务逻辑正确性
- 🛡️ 安全漏洞检测
- ⚡ 性能优化建议
- 📚 代码可读性
- 🔧 可维护性评估

**AI发现的问题**:
{ai_detected_issues}

**优化建议**:
{optimization_suggestions}

**最佳实践推荐**:
{best_practices}
```

### 智能测试生成
```markdown
## 🧪 AI测试用例生成

基于代码分析，自动生成测试用例...

**生成的测试类型**:
- ✅ 单元测试 (覆盖率: {unit_coverage}%)
- ✅ 集成测试 (覆盖率: {integration_coverage}%)
- ✅ 边界测试 (覆盖率: {boundary_coverage}%)
- ✅ 异常测试 (覆盖率: {exception_coverage}%)

**生成的测试文件**:
{generated_test_files}

**测试执行结果**:
{test_execution_results}
```

## 🔧 命令映射和快捷操作

### 用户意图 → AceFlow 命令
```yaml
项目管理:
  "初始化项目": "aceflow init --mode smart"
  "检查状态": "aceflow status --format json --verbose"
  "生成报告": "aceflow report --type summary --export md"

流程控制:
  "开始开发": "aceflow start --description '{description}'"
  "更新进度": "aceflow progress {stage} {percentage}"
  "完成阶段": "aceflow complete {stage} --auto-next"
  "切换模式": "aceflow switch --mode {new_mode}"

AI功能:
  "分析任务": "aceflow analyze '{task_description}'"
  "获取建议": "aceflow suggest --context '{context}'"
  "智能规划": "aceflow plan --project-type '{type}'"
  "进度跟踪": "aceflow track --auto-update"

故障处理:
  "健康检查": "aceflow doctor"
  "状态修复": "aceflow repair --auto"
  "回滚状态": "aceflow rollback --to {snapshot}"
```

## 📊 用户体验优化

### 可视化进度展示
```markdown
## 📈 项目仪表板

```
AceFlow v3.0 项目: {project_name}
模式: {flow_mode} | 团队: {team_size}人 | 周期: {cycle_time}

整体进度: ████████░░ {overall_progress}%
当前阶段: {current_stage} ({stage_progress}%)

阶段状态:
S1 用户故事    ✅ 完成 (100%)
S2 任务分解    ✅ 完成 (100%)
S3 测试设计    ✅ 完成 (100%)
S4 功能实现    🔄 进行中 ({s4_progress}%)
S5 测试验证    ⏳ 等待中
S6 代码评审    ⏳ 等待中
S7 演示反馈    ⏳ 等待中
S8 总结归档    ⏳ 等待中

质量指标:
- 代码覆盖率: {coverage}%
- 性能指标: {performance}
- 安全评分: {security_score}
- 用户满意度: {satisfaction}%
```

**🎯 当前任务**: {current_task}
**⏱️ 预计完成**: {estimated_completion}
**🚀 下一里程碑**: {next_milestone}

### 智能提醒和建议
```markdown
💡 **智能助手建议**

基于项目分析，我发现以下优化机会：

**效率提升**:
- 🔄 建议并行执行任务A和任务B，可节省2天时间
- 🎯 当前阶段可以提前准备下一阶段的资源

**质量改进**:
- 🧪 建议增加性能测试用例，覆盖高并发场景
- 📚 建议补充API文档，提升可维护性

**风险预警**:
- ⚠️ 第三方依赖版本较旧，建议及时更新
- ⚠️ 数据库连接池配置可能成为性能瓶颈

需要我自动执行这些优化建议吗？
```

## 🛠️ 故障处理和恢复

### 智能故障诊断
```python
def intelligent_error_diagnosis(error_info):
    """
    智能错误诊断和恢复建议
    """
    error_patterns = {
        'dependency_error': handle_dependency_error,
        'state_corruption': handle_state_corruption,
        'permission_error': handle_permission_error,
        'network_error': handle_network_error,
        'ai_service_error': handle_ai_service_error
    }
    
    # 错误分类
    error_type = classify_error(error_info)
    
    # 生成解决方案
    solution = error_patterns.get(error_type, handle_unknown_error)
    
    return solution(error_info)
```

### 自动恢复机制
```markdown
🔧 **自动故障恢复**

检测到执行异常: {error_type}
错误详情: {error_message}

**自动诊断结果**:
- 🔍 问题根因: {root_cause}
- 📊 影响范围: {impact_scope}
- 🎯 恢复策略: {recovery_strategy}

**自动恢复选项**:
1. 🚀 快速修复 (成功率: 95%) - 自动重试当前操作
2. 🔄 状态回滚 (成功率: 100%) - 回滚到上一个稳定状态
3. 🛠️ 手动干预 (成功率: 100%) - 提供详细诊断信息

**推荐操作**: {recommended_action}

```bash
# 自动执行修复
aceflow repair --auto --strategy {strategy}
```

是否执行自动修复？
```

## 📚 集成最佳实践

### 团队协作模式
```markdown
## 👥 团队协作优化

**协作模式配置**:
```bash
# 配置团队协作
aceflow config --set team.mode=collaborative
aceflow config --set team.size={team_size}
aceflow config --set team.roles="{roles}"
```

**协作功能**:
- 🔄 实时状态同步
- 📋 任务分工管理
- 🔍 进度透明化
- 💬 集成沟通工具

**协作最佳实践**:
- 每日站会状态同步
- 阶段完成后团队评审
- 经验分享和知识积累
- 持续改进流程优化
```

### 持续集成/部署
```markdown
## 🚀 CI/CD 集成

**GitHub Actions 集成**:
```yaml
# .github/workflows/aceflow.yml
name: AceFlow CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  aceflow:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup AceFlow
        run: |
          pip install aceflow
          aceflow doctor
      - name: Run AceFlow Pipeline
        run: |
          aceflow run --stage current --ci-mode
```

**集成优势**:
- 🔄 自动化工作流执行
- 🎯 持续质量监控
- 📊 实时进度跟踪
- 🚀 自动化部署
```

## 🎓 学习和优化

### 个性化学习
```markdown
## 🧠 个性化学习系统

**学习数据收集**:
- 📊 工作流执行数据
- ⏱️ 时间消耗统计
- 🎯 质量指标分析
- 💡 用户反馈收集

**智能优化建议**:
- 🔄 流程优化: 基于历史数据优化流程模板
- ⏰ 时间优化: 个性化时间估算模型
- 🎯 质量优化: 智能质量门控调整
- 📚 知识积累: 自动生成最佳实践文档

**持续改进**:
- 每周生成优化报告
- 月度流程效率分析
- 季度最佳实践总结
- 年度团队能力评估
```

---

## 🎯 快速开始

### 一键式体验
```markdown
💬 **立即体验 AceFlow v3.0**

只需说出以下任何一句话:
- "我要开始一个新项目"
- "帮我修复这个bug"
- "检查项目状态"
- "我需要开发一个新功能"

我将自动：
1. 🔍 检测项目状态
2. 🧠 分析任务需求
3. 🎯 推荐最佳流程
4. 🚀 开始智能执行
```

### 即时命令参考
```bash
# 项目管理
aceflow init --mode smart
aceflow status --format json
aceflow config --list

# 智能分析
aceflow analyze "开发用户登录功能"
aceflow suggest --task "性能优化"
aceflow plan --project-type "web-app"

# 流程控制
aceflow start --description "新功能开发"
aceflow run S1 --auto
aceflow progress S1 80
aceflow complete S1 --auto-next

# 监控报告
aceflow monitor --dashboard
aceflow report --type detailed
aceflow metrics --period 30
```

---

*🚀 AceFlow v3.0 + Cline = 智能化软件开发的完美结合！*

**版本**: v3.0.0  
**兼容性**: 完全兼容 AceFlow v3.0 规范  
**更新时间**: 2025-07-11  
**支持**: 智能模式、自适应流程、AI增强功能