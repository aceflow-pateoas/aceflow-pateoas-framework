# **AceFlow-PATEOAS 流程规范**

## **1. 概述**

### **1.1 目的**
本规范定义了一套AI优先的软件研发工作流，通过状态驱动和记忆机制，使AI能够自主完成大部分开发任务，最小化人工干预。

### **1.2 适用范围**
- **AI自主执行**：新功能开发、Bug修复、需求变更、紧急上线
- **人机协作**：复杂架构设计、关键决策确认、异常处理

### **1.3 术语定义**
- **PATEOAS**：Prompt as the Engine of AI State - 将提示词作为驱动AI状态转换的核心引擎
- **状态**：`{阶段, 任务, 进度, 记忆, 下一步}` 五元组
- **记忆池**：跨阶段信息存储，格式：`类型-ID-内容`
- **流程分支**：基于任务特征的自适应执行路径

## **2. 核心原则**

### **2.1 状态驱动**
```yaml
state_transition:
  trigger: "阶段完成条件满足"
  action: "自动进入下一阶段"
  fallback: "条件不满足时请求人工确认"
```

### **2.2 流程弹性**
- **自动路由**：AI根据任务类型自动选择执行路径
- **动态阈值**：可配置的质量标准和完成条件
- **智能回退**：检测到问题时自动返回相关阶段

### **2.3 记忆持续**
- **格式标准**：`[类型]-[ID]-[内容]`
- **自动关联**：AI自动识别记忆与阶段的相关性
- **主动召回**：在需要时自动提取相关记忆

### **2.4 AI自主性**
```yaml
autonomy_levels:
  L1_监督: "AI建议，人类决策"
  L2_协作: "AI执行，人类审核" 
  L3_自主: "AI决策并执行，仅异常时人工介入"
```

## **3. 流程框架**

### **3.1 流程总览**
```mermaid
graph TD
    开始[任务输入] --> AI{AI任务分类}
    AI -->|新功能| 完整[S1→S2→S3→DG1→(S4↔S5)→DG2→S6→S7→DG3→S8]
    AI -->|Bug修复| 快速[S2→(S4↔S5)→DG2→S8]
    AI -->|需求变更| 变更[S1→S2→S3→(S4↔S5)]
    AI -->|紧急上线| 紧急[(S4↔S5)→S6→S8]
```
注：(S4↔S5) 表示任务级循环

### **3.2 AI流程选择逻辑**
```python
def select_flow(task_description):
    if "新功能" in task_description or "开发" in task_description:
        return "FULL_FLOW"
    elif "bug" in task_description or "修复" in task_description:
        return "QUICK_FLOW"
    elif "变更" in task_description or "调整" in task_description:
        return "CHANGE_FLOW"
    elif "紧急" in task_description or "P0" in task_description:
        return "URGENT_FLOW"
    else:
        return "REQUEST_CLARIFICATION"
```

## **4. 阶段定义与AI执行规范**

### **4.1 S1：用户故事细化**

**AI执行指令**：
```markdown
任务：将输入需求转换为INVEST原则的用户故事
输入检查：是否包含{用户角色, 功能描述, 业务价值}
执行步骤：
1. 识别所有用户角色
2. 为每个角色生成故事：作为[角色]，我希望[功能]，以便[价值]
3. 验证每个故事的独立性和可测试性
4. 创建记忆文件：REQ-001-[需求简述].md

输出产物：/aceflow_result/{iteration_id}/S1_user_story/s1_user_story.md
完成条件：故事数量≥需求点数量 AND 每个故事符合INVEST
```

**本地状态更新**：
```json
{
  "current_stage": "S1",
  "progress": 100,
  "outputs": ["{iteration_id}/S1_user_story/s1_user_story.md"],
  "memory_created": ["REQ-001-core-requirements.md"]
}
```

### **4.2 S2：任务拆分**

**AI执行指令**：
```markdown
任务：将用户故事分解为可执行任务
输入依赖：S1产出物

执行步骤：
1. foreach 用户故事:
   - 识别技术组件
   - 评估复杂度
   - 拆分任务(目标工时≤8小时)
2. 为每个故事创建任务输入模板
3. 验证任务粒度（≤8小时）
4. 生成任务清单s2_tasks.md
5. 分配优先级(P0-P3)

任务格式：
| 任务ID | 描述 | 预估工时 | 优先级 | 依赖 |
|--------|------|----------|--------|------|
| T001   | [描述] | [小时] | P[0-3] | [依赖ID] |

输出产物：/aceflow_result/{iteration_id}/S2_tasks/s2_tasks.md
完成条件：所有故事已拆分 AND 单任务工时≤8h
```

### **4.3 S3：测试用例设计**

**AI执行指令**：
```markdown
任务：基于用户故事生成测试用例
输入依赖：S1产出物, S2产出物

执行步骤：
1. 为每个用户故事生成测试模板
2. 包含：正常流程、边界条件、异常场景
3. 计算覆盖率（本地脚本）
	- 覆盖率计算：(用例覆盖的故事点/总故事点)*100%
4. 生成s3_testcases.md

用例模板：
## TC-[ID]: [测试场景]
- **关联故事**: US-[ID]
- **前置条件**: [条件描述]
- **测试步骤**:
  1. [步骤1]
  2. [步骤2]
- **预期结果**: [预期结果]

输出产物：/aceflow_result/{iteration_id}/S3_testcases/s3_testcases.md
完成条件：覆盖率≥80% AND 核心功能覆盖率=100%
```

### 4.4 S4-S5：功能实现与测试循环

**AI执行指令**：
```markdown
任务：以任务为单位循环执行开发和测试
输入依赖：S2产出物(任务列表), S3产出物(测试用例)

执行模式：
1. 从任务队列中选择下一个任务
   - 优先级：P0 > P1 > P2 > P3
   - 可并行：前后端任务可同时进行
2. S4：实现该任务功能
   - 遵循TDD原则
   - 遵循团队编码规范
3. S5：执行该任务测试
   - 运行对应的测试用例
   - 记录测试结果
4. 循环决策（DG2）
   - 测试通过且有剩余任务：继续下一个
   - 测试失败：修复后重测
   - 所有任务完成：退出循环

报告结构：
# 测试报告
- 执行时间：[时间戳]
- 总计：[总数] | 通过：[数量] | 失败：[数量]
- 覆盖率：[百分比]%

## 失败用例
[失败详情列表]

输出产物：
- S4: /aceflow_result/{iteration_id}/S4_implementation/s4_implementation_{taskId}.md
- S5: /aceflow_result/{iteration_id}/S5_test_report/s5_test_report_{taskId}.md

完成条件：
- 后端、前端代码全部完成 AND 单元测试通过率≥90%
- 所有任务状态为"完成"且测试通过
- 执行率=100% AND 高严重度缺陷=0
```

### **4.6 S6：代码评审**

**AI执行指令**：
```markdown
任务：自动化代码质量检查
检查项：
1. 代码规范：命名/格式/注释
2. 逻辑正确：算法/边界/异常处理  
3. 性能安全：复杂度/内存/SQL注入
4. 架构合理：耦合度/扩展性

评审方式：静态分析 + 规则检查 + 最佳实践对比
输出格式：问题ID|类型|位置|建议|严重度
输出产物：/aceflow_result/{iteration_id}/S6_codereview/s6_codereview.md
完成条件：关键问题=0 AND 一般问题≤3
```

### **4.7 S7：演示与反馈**

**AI执行指令**：
```markdown
任务：准备演示材料并收集反馈
准备内容：
1. 功能演示脚本
2. 核心场景展示
3. 性能指标数据
反馈模板：
- 功能符合度：1-5分
- 用户体验：优/良/需改进
- 改进建议：[具体描述]

输出格式：演示记录 + 反馈汇总 + 改进方案
输出产物：/aceflow_result/{iteration_id}/S7_feedback/s7_feedback.md
完成条件：获得关键干系人反馈≥80%
```

### **4.8 S8：进度汇总**

**AI执行指令**：
```markdown
任务：生成进度报告和后续规划
汇总内容：
1. 各阶段完成情况
2. 关键产出物清单
3. 问题与解决方案
4. 经验教训总结

规划建议：
- 待完成事项
- 优化建议
- 下轮迭代重点

输出格式：结构化报告 + 可视化图表
输出产物：/aceflow_result/{iteration_id}/S8_summary/s8_summary.md
完成条件：报告完整 AND 获得确认
```

## 5. 决策门机制

### 5.1 DG1: 进入开发前检查
- 位置：S3之后
- 判断：任务是否都≤8小时 且 测试覆盖≥80%
- 通过：进入任务循环
- 不通过：返回S2重新拆分

### 5.2 DG2: 任务循环控制  
- 位置：每个任务测试后
- 判断：是否还有未完成任务
- 是：继续下一个任务
- 否：进入S6评审

### 5.3 DG3: 用户验收
- 位置：S7演示后
- 判断：用户满意度≥80%
- 通过：完成迭代
- 不通过：重大问题返回S1，小问题继续

## **6. 本地状态管理**

### **6.1 目录结构**
```
.aceflow/
├── state.json          # 当前状态
├── config.yaml         # 配置阈值
├── memory/            # 记忆池
│   ├── REQ-*.md       # 需求
│   ├── DEC-*.md       # 决策
│   └── RISK-*.md      # 风险
└── logs/              # 执行日志
```

### **6.2 状态数据结构**
```json
{
  "current_stage": "S1",
  "status": "in_progress|blocked|completed",
  "progress": 75,
  "memory_refs": ["REQ-001", "DEC-001"],
  "next_action": {
    "condition": "progress >= 100",
    "target": "S2"
  }
}
```

### **6.3 状态转换规则**
```python
def state_transition(current_state):
    if meets_completion_criteria(current_state):
        return auto_proceed_next()
    elif has_blocking_issues(current_state):
        return request_human_intervention()
    else:
        return continue_current_stage()
```

## **7. 异常处理规范**

### **7.1 AI异常识别**
```yaml
exception_rules:
  - name: "测试覆盖率不足"
    check: "coverage < 80%"
    action: |
      1. 提示用户当前覆盖率
      2. 询问是否自动补充测试用例
      3. 如果是，返回S3补充用例
  
  - name: "任务粒度过大"  
    check: "estimated_hours > 8"
    action: |
      1. 显示当前任务预估工时
      2. 自动建议拆分方案
      3. 等待用户确认后执行拆分
```

### **7.2 自动处理策略**
| 异常类型 | AI处理方式 | 人工介入条件 |
|---------|-----------|-------------|
| 任务超时 | 自动分解为子任务 | 分解后仍>8h |
| 测试失败 | 分析原因并尝试修复 | 修复2次失败 |
| 需求不清 | 基于上下文推断 | 置信度<70% |
| 代码冲突 | 自动合并或隔离 | 核心模块冲突 |

## **8. 人机协作规范**

### **8.1 AI决策边界**
```yaml
ai_can_decide:
  - 常规任务拆分
  - 标准测试用例生成
  - 代码格式优化
  - 简单bug修复

require_human:
  - 架构变更
  - 核心算法选择
  - 外部系统集成
  - 数据模型修改
```

### **8.2 协作接口**
```markdown
AI请求格式：
[HUMAN_INPUT_REQUIRED]
上下文：[当前状态和问题描述]
需要决策：[具体问题]
建议选项：[AI分析的可选方案]
影响分析：[各方案的影响]
```

## **9. 附录**

### **9.1 AI执行检查清单**
- [ ] 任务类型正确识别
- [ ] 流程路径自动选择
- [ ] 状态信息完整记录
- [ ] 记忆跨阶段传递正常
- [ ] 异常自动处理适当
- [ ] 人工介入时机合理

### **9.2 AI工具链**
```yaml
# .aceflow/tools.yaml
tools:
  task_classifier: "基于关键词的规则引擎"
  state_engine: "本地状态文件管理"
  memory_system: "文件索引系统"
  code_generator: "VSCode代码片段"
  test_runner: "VSCode测试命令"
  quality_checker: "VSCode扩展"
```

### **9.3 文件系统结构**
```
.
├── .aceflow/
│   ├── state.json              # 唯一的流程状态文件
│   └── memory/                 # 记忆池目录
│       ├── REQ-001-sso-login.md
│       └── DEC-001-use-jwt.md
│
├── aceflow_result/             # 所有阶段的产出物
│   ├── iteration1/				# 迭代1
│   │   ├── S1_user_story/
│   │   ├── S2_tasks/
│   │   └── ...
│   ├── iteration2/				# 迭代2
│   │   └── ...
│
└── src/                        # 项目源代码
```