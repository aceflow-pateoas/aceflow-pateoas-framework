# **AceFlow-PATEOAS 流程规范 v2.**

## **1. 概述**

### **1.1 目的**
本规范定义了一套基于Code Agent的AI辅助软件研发工作流，通过状态驱动和结构化提示，使AI Agent能够高效完成开发任务。

### **1.2 适用范围**
- **AI自主执行**：新功能开发、Bug修复、需求变更、紧急上线
- **人机协作**：复杂架构设计、关键决策确认、异常处理

### **1.3 术语定义**
- **PATEOAS**：Prompt as the Engine of AI State - 将提示词作为驱动AI状态转换的核心引擎
- **状态**：`{阶段, 任务, 进度, 记忆, 下一步}` 五元组
- **记忆池**：跨阶段信息存储，格式：`类型-ID-内容`
- **流程分支**：基于任务特征的自适应执行路径

## **2. 核心原则**

- **状态驱动**：阶段完成条件满足时，自动进入下一阶段。
- **流程弹性**：AI根据任务类型自动选择执行路径。
- **记忆持续**：跨阶段信息传递，主动召回相关上下文。
- **AI自主性**：L1(建议), L2(执行), L3(自主)三级模式。

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
注：`(S4↔S5)` 表示任务级循环

### **3.2 AI流程选择逻辑**
AI Agent基于关键词匹配和上下文理解，自动选择合适的执行路径。

## **4. 阶段定义与AI执行规范**

### **4.1 S1：用户故事细化**
**AI执行提示**：
```markdown
## 任务：S1 - 用户故事细化
将输入需求转换为符合INVEST原则的用户故事。

### 输入：
- 用户原始需求描述

### 执行步骤：
1. 识别所有用户角色。
2. 为每个角色生成故事：作为[角色]，我希望[功能]，以便[价值]。
3. 验证每个故事符合INVEST原则。
4. 使用 `.aceflow/templates/s1_user_story.md` 模板格式化输出。

### 输出：
- **用户故事**：`/aceflow_result/{iteration_id}/S1_user_story/s1_{storyId}.md`
- **用户故事清单**：`/aceflow_result/{iteration_id}/S1_user_story/s1_all_user_story.md`
- **需求记忆**：`/.aceflow/memory/REQ-001-[需求简述].md`
```

### **4.2 S2：任务拆分**
**AI执行提示**：
```markdown
## 任务：S2 - 任务拆分
基于用户故事进行任务分解。

### 输入：
- **用户故事**：`/aceflow_result/{iteration_id}/S1_user_story/s1_all_user_story.md`
- **配置文件**：`/.aceflow/config.yaml`

### 执行步骤：
1. 分析每个用户故事，拆分为独立可执行的任务（目标≤8小时）。
2. 评估任务复杂度、依赖关系，并分配优先级。
3. 单个任务文件，使用 `.aceflow/templates/s2_tasks_main.md` 模板格式创建。
4. 主任务清单，使用 `.aceflow/templates/s2_tasks_group.md` 模板格式创建。

### 输出：
- **主任务清单**：`/aceflow_result/{iteration_id}/S2_tasks/s2_all_tasks.md`
- **单个任务文件**：`/aceflow_result/{iteration_id}/S2_tasks/s2_{taskId}.md`
```

### **4.3 S3：测试用例设计**
**AI执行提示**：
```markdown
## 任务：S3 - 测试用例设计
为每个用户故事设计完整的测试用例。

### 输入：
- **用户故事**：`/aceflow_result/{iteration_id}/S1_user_story/s1_all_user_story.md`
- **任务清单**：`/aceflow_result/{iteration_id}/S2_tasks/s2_all_tasks.md`

### 执行步骤：
1. 分析用户故事的验收标准。
2. 设计测试场景：正常流程、边界条件、异常场景。
3. 编写具体测试步骤，并标注自动化可行性。
4. 使用 `.aceflow/templates/s3_testcases.md` 模板格式化输出。
5. 每个任务对应一个 testcases 文件。

### 输出：
- **测试用例**：`/aceflow_result/{iteration_id}/S3_testcases/s3_{taskId}_testcases.md`
- **测试用例汇总**：`/aceflow_result/{iteration_id}/S3_testcases/s3_all_testcases.md`
```

### **4.4 S4-S5：功能实现与测试循环**
**AI执行提示**：
```markdown
## 任务：S4-S5 - 功能实现与测试循环
以任务为单位循环执行开发和测试，直到所有任务完成。

### 循环流程：
1. **选择任务**：从 `s2_all_tasks.md` 中选择一个未完成的任务。
2. **S4 (实现)**：
   - 编写功能代码，遵循项目规范。
   - 使用 `.aceflow/templates/s4_implementation_report.md` 模板创建实现报告。
   - 使用 `.aceflow/templates/s4_implementation.md` 功能实现文档汇总表，存在则跳过。
   - **产出**：
     - 代码文件
     - 单任务实现报告保存到 `/aceflow_result/{iteration_id}/S4_implementation/s4_impl_{taskId}.md`
     - 功能实现文档汇总表保存到 `/aceflow_result/{iteration_id}/S4_implementation/s4_implementation_all.md` 创建。
3. **S5 (测试)**：
   - 运行相关测试（如 `mvn test` 或 `npm test`）。
   - 检查代码覆盖率。
   - 使用 `.aceflow/templates/s5_test_report.md` 模板创建任务测试报告。
   - 使用 `.aceflow/templates/s5_test_report.md` 模板创建汇总测试报告。
   - **产出**：
      - 单格任务测试报告 `/aceflow_result/{iteration_id}/S5_test_report/s5_test_{taskId}.md`
      - 更新汇总报告 `/aceflow_result/{iteration_id}/S5_test_report/s5_test_all.md`
4. **决策与状态更新**：
   - ✅ 测试通过 -> 更新 `s2_all_tasks.md` 中任务状态为“完成”，选择下一任务。
   - ❌ 测试失败 -> 标记为“失败”，修复后重测。
   - 📋 所有任务完成 -> 进入S6。
```

### **4.5 S6：代码评审**
**AI执行提示**：
```markdown
## 任务：S6 - 代码评审
对本次迭代的代码进行全面评审。

### 评审范围：
- 本次迭代修改的所有 `/src/` 目录下的文件。

### 评审清单：
1. **代码质量**：命名、格式、注释。
2. **逻辑正确性**：业务逻辑、边界、错误处理。
3. **性能与安全**：性能问题、安全漏洞。
4. **可维护性**：复杂度、重复代码、设计模式。
   
### VSCode辅助工具：
- ESLint/Pylint, SonarLint, GitLens

### 输出：
- 使用 `.aceflow/templates/s6_code_review.md` 模板创建评审报告。
- **评审报告**：`/aceflow_result/{iteration_id}/S6_codereview/s6_codereview.md`
```

### **4.6 S7：演示与反馈**
**AI执行提示**：
```markdown
## 任务：S7 - 准备演示和收集反馈
准备功能演示材料并设计反馈收集方案。

### 准备内容：
1. **演示脚本**：功能概览、核心场景、性能指标。
2. **演示环境**：确保可用，准备数据。
3. **反馈表单**：满意度、用户体验、改进建议。

### 输出：
- **演示脚本**：使用 `.aceflow/templates/s7_demo_script.md` 模板创建，保存到 `/aceflow_result/{iteration_id}/S7_feedback/demo_script.md`
- **反馈模板**(可选)：`/aceflow_result/{iteration_id}/S7_feedback/feedback_template.md`
```

### **4.7 S8：进度汇总**
**AI执行提示**：
```markdown
## 任务：S8 - 生成进度汇总报告
总结本次迭代的执行情况并提供优化建议。

### 数据来源：
- 状态文件、执行日志、各阶段产出物。

### 执行步骤：
1. 运行分析脚本：`python .aceflow/scripts/analyze.py --iteration {iteration_id}`
2. 使用 `.aceflow/templates/s8_summary_report.md` 模板格式化报告。
3. 使用 `.aceflow/templates/s8_learning_summary.md` 模板总结经验教训。

### 输出：
- **进度报告**：`/aceflow_result/{iteration_id}/S8_summary/summary_report.md`
- **经验总结**：`/.aceflow/memory/LEARN-{iteration_id}.md`
```

## **5. 决策门机制**
- **DG1 (开发前检查)**：S3后，检查任务粒度、测试覆盖率。
- **DG2 (任务循环控制)**：S5后，检查测试结果，控制循环。
- **DG3 (用户验收)**：S7后，检查用户满意度，决定是否返工。

## **6. 配置和脚本**

### **6.1 目录结构**
```
.aceflow/
├── state.json              # 流程状态
├── config.yaml            # 项目配置
├── memory/                # 记忆池（需求、决策、风险、学习）
├── templates/             # 报告和文档模板
│   ├── s1_user_story.md
│   ├── s2_tasks_main.md
│   ├── s2_tasks_group.md
│   ├── s3_testcases.md
│   ├── s4_implementation_report.md
│   ├── s5_test_report.md
│   ├── s6_code_review.md
│   ├── s7_demo_script.md
│   ├── s8_summary_report.md
│   └── s8_learning_summary.md
├── scripts/               # 辅助脚本
│   ├── init.py
│   ├── state_manager.py
│   └── analyze.py
└── logs/                  # 执行日志

aceflow_result/         #流程执行结果目录
```

### **6.2 模板文件说明**
- **s1_user_story.md**: 用户故事格式模板。
- **s2_tasks_main.md**: 主任务清单格式模板。
- **s2_tasks_group.md**: 分组任务清单格式模板。
- **s3_testcases_main.md**: 测试用例格式模板。
- **s3_testcases.md**: 测试用例汇总报告模板。
- **s4_implementation_report.md**: S4实现报告模板。
- **s4_implementation.md**: S4实现汇总报告模板。
- **s5_test_report.md**: S5测试报告模板。
- **s6_code_review.md**: S6代码评审报告模板。
- **s7_demo_script.md**: S7演示脚本模板。
- **s8_summary_report.md**: S8迭代总结报告模板。
- **s8_learning_summary.md**: 经验教训总结模板。

### **6.3 脚本工具**
- **init.py**
  - **说明**：用于创建新的迭代环境，包括目录结构和初始状态文件。
  - **用法**：`python .aceflow/scripts/init.py [iteration_id]`

- **state_manager.py**
  - **说明**：用于更新和查询流程状态。
  - **用法**：`python .aceflow/scripts/state_manager.py <command> [args]`
  - **示例**：`python .aceflow/scripts/state_manager.py update S1 100`

- **analyze.py**
  - **说明**：生成迭代分析报告。
  - **用法**：`python .aceflow/scripts/analyze.py --iteration <id>`

### **6.4 项目配置文件（config.yaml）**
此文件用于定义项目类型、技术栈、执行阈值、代码规范等，使其高度可配置。