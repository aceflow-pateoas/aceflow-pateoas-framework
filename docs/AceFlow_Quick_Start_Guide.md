# AceFlow v2.0 快速入门指南

> AI驱动的敏捷开发工作流框架 - 轻量级版本

## 🚀 快速开始

### 安装和初始化

```bash
# 1. 进入项目目录
cd your-project

# 2. 初始化AceFlow项目
python .aceflow/scripts/aceflow init

# 3. 查看项目状态
python .aceflow/scripts/aceflow status
```

### 第一次使用

1. **选择流程模式** - 根据项目规模选择合适的模式
   - 轻量级模式 (1-5人团队)
   - 标准模式 (3-10人团队)  
   - 完整模式 (10+人团队)

2. **配置敏捷集成** - 可选择Scrum、Kanban或自定义框架

3. **开始第一个迭代**
   ```bash
   # 开始当前阶段
   python .aceflow/scripts/aceflow start
   
   # 更新进度
   python .aceflow/scripts/aceflow progress --progress 50
   
   # 完成阶段
   python .aceflow/scripts/aceflow complete
   ```

## 📋 三种流程模式

### 轻量级模式 (P→D→R)
适合：小型团队、快速迭代、原型验证

```
Planning (规划) → Development (开发) → Review (评审)
```

**特点**：
- 流程简单，学习成本低
- 适合1-7天的短周期迭代
- 重点关注核心功能交付

**典型用时**：2-7天

### 标准模式 (P1→P2→D1→D2→R1)  
适合：中型项目、敏捷团队

```
Requirements (需求) → Planning (规划) → Implementation (实现) → Testing (测试) → Review (评审)
```

**特点**：
- 平衡的流程复杂度
- 适合1-4周的迭代周期
- 更好的质量保证

**典型用时**：1-2周

### 完整模式 (S1→S2→S3→S4→S5→S6→S7→S8)
适合：大型项目、企业级应用

```
用户故事 → 任务拆分 → 测试用例 → 功能实现 → 测试执行 → 代码评审 → 演示反馈 → 总结归档
```

**特点**：
- 完整的软件开发生命周期
- 严格的质量控制和文档要求
- 适合关键系统和合规项目

**典型用时**：2-4周

## 🎯 核心命令

### 基础操作
```bash
# 查看帮助
python .aceflow/scripts/aceflow help

# 查看项目状态
python .aceflow/scripts/aceflow status

# 获取AI建议
python .aceflow/scripts/aceflow next

# 启动Web界面
python .aceflow/scripts/aceflow web --serve
```

### 流程管理
```bash
# 开始阶段
python .aceflow/scripts/aceflow start [阶段ID]

# 更新进度
python .aceflow/scripts/aceflow progress --progress 75

# 完成阶段  
python .aceflow/scripts/aceflow complete [阶段ID]

# 切换流程模式
python .aceflow/scripts/aceflow mode minimal
```

### 交付物管理
```bash
# 列出交付物
python .aceflow/scripts/aceflow deliverable --list

# 标记交付物完成
python .aceflow/scripts/aceflow deliverable --deliverable "功能实现" 

# 交互式管理
python .aceflow/scripts/aceflow deliverable
```

## 🏃 敏捷集成

### Scrum集成
```yaml
# 配置Sprint
agile:
  framework: scrum
  iteration_length: "2weeks"
  ceremonies:
    planning: true      # 映射到P阶段
    daily_standup: true # D阶段检查点
    review: true        # R阶段评审
    retrospective: true # R阶段反思
```

### Kanban集成
```yaml
# 配置看板
agile:
  framework: kanban
  board_config:
    lanes: ["规划中", "开发中", "评审中", "已完成"]
    wip_limits:
      "开发中": 5
      "评审中": 2
```

## 🧠 AI智能助手

### 智能建议
AceFlow AI助手会根据当前状态提供个性化建议：

- **阶段建议**：何时开始/完成阶段
- **任务优先级**：高优先级任务提醒
- **风险预警**：检测潜在问题
- **最佳实践**：敏捷开发建议

### 记忆系统
AI助手会记住项目中的重要信息：

- **需求记忆**：用户需求和期望
- **技术记忆**：技术决策和约束
- **问题记忆**：遇到的问题和解决方案
- **反馈记忆**：用户反馈和改进建议

```bash
# 添加记忆
python .aceflow/scripts/aceflow memory --add

# 搜索记忆
python .aceflow/scripts/aceflow memory --search "API设计"
```

## 🎨 Web界面

AceFlow提供现代化的Web界面：

### 启动方式
```bash
# 方式1：本地服务器（推荐）
python .aceflow/scripts/aceflow web --serve --port 8080

# 方式2：直接打开文件
python .aceflow/scripts/aceflow web
```

### 主要功能
- **工作台面板**：项目概览、当前阶段、任务列表
- **流程导航**：可视化流程图、阶段切换
- **AI助手面板**：智能建议、快速操作
- **记忆中心**：知识库管理、搜索检索

## 📊 项目模板

### Bug修复模板
适用场景：紧急Bug、生产问题

```
问题定位 (10分钟) → 修复实施 (30-120分钟) → 发布部署 (15分钟)
```

### 快速功能开发
适用场景：小功能、MVP验证

```
快速设计 (30分钟) → 开发实现 (2-6小时) → 验证发布 (30分钟)
```

### 原型验证
适用场景：新产品验证、创新功能

```
快速原型 (4-8小时) → 用户验证 (2-4小时) → 结果分析 (1小时)
```

## ⚙️ 配置指南

### 项目配置
```yaml
# .aceflow/config.yaml
project:
  name: "我的项目"
  team_size: "1-3人"
  
flow:
  mode: "minimal"
  auto_switch: true
  
agile:
  enabled: true
  framework: "scrum"
  
ai:
  enabled: true
  auto_recommendations: true
```

### 流程模式配置
```yaml
# .aceflow/config/flow_modes.yaml
flow_modes:
  minimal:
    stages: [P, D, R]
    workflow_pattern: "P→D→R"
    suitable_for: ["小型项目", "快速迭代"]
```

## 🔄 模式切换

### 智能切换
AceFlow支持在项目进行中切换流程模式：

```bash
# 切换到标准模式，保留进度
python .aceflow/scripts/aceflow mode standard

# 切换到轻量级模式，重置进度
python .aceflow/scripts/aceflow mode minimal --reset
```

### 数据迁移
切换模式时，AceFlow会智能映射阶段状态：

- **轻量级 → 标准**：P→P1+P2, D→D1+D2, R→R1
- **标准 → 完整**：P1→S1, P2→S2, D1→S3+S4, D2→S5, R1→S6+S7+S8
- **完整 → 轻量级**：S1+S2→P, S3+S4+S5→D, S6+S7+S8→R

## 📈 最佳实践

### 团队协作
1. **明确角色分工**：产品负责人、开发人员、测试人员
2. **定期同步**：使用daily standup检查点
3. **持续反馈**：及时更新进度和问题

### 质量保证
1. **交付物检查**：确保每个阶段的交付物完整
2. **进度跟踪**：定期更新阶段进度
3. **问题记录**：及时记录和解决问题

### 流程优化
1. **数据驱动**：基于历史数据优化流程
2. **持续改进**：定期回顾和调整流程
3. **工具集成**：与现有工具深度集成

## 🚨 常见问题

### Q: 如何选择合适的流程模式？
**A**: 根据团队规模和项目复杂度：
- 1-5人，简单项目 → 轻量级模式
- 3-10人，中等复杂度 → 标准模式  
- 10+人，复杂项目 → 完整模式

### Q: 可以中途切换模式吗？
**A**: 可以。AceFlow支持智能模式切换，会自动迁移进度数据。

### Q: AI建议准确吗？
**A**: AI建议基于项目上下文和最佳实践，可作为参考。最终决策仍需团队判断。

### Q: 如何与现有工具集成？
**A**: AceFlow提供API接口，支持与Jira、GitHub、Azure DevOps等工具集成。

### Q: Web界面需要网络吗？
**A**: 不需要。Web界面完全基于本地文件，支持离线使用。

## 📞 获取帮助

- **命令行帮助**：`python .aceflow/scripts/aceflow help`
- **详细文档**：查看 `.aceflow/` 目录下的文档文件
- **示例项目**：参考模板文件和配置示例
- **社区支持**：GitHub Issues和讨论区

## 🎉 下一步

恭喜你完成了AceFlow快速入门！接下来可以：

1. **深入学习**：探索高级功能和配置选项
2. **定制化**：根据团队需求调整模板和流程
3. **集成工具**：连接现有的开发工具链
4. **分享经验**：为社区贡献使用经验和改进建议

开始你的AI驱动敏捷开发之旅吧！🚀