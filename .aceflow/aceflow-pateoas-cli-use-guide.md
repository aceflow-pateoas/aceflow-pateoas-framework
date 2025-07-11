# AceFlow-PATEOAS CLI 工具使用指南

## 目录
1. [概述](#1-概述)
2. [环境准备](#2-环境准备)
3. [快速入门](#3-快速入门)
4. [命令参考](#4-命令参考)
5. [常见工作流示例](#5-常见工作流示例)
6. [故障排除](#6-故障排除)
7. [高级配置](#7-高级配置)
8. [附录](#8-附录)

## 1. 概述

AceFlow-PATEOAS CLI 工具是基于 AceFlow 流程框架与 PATEOAS 状态管理方法论的命令行接口，提供流程导航、状态管理、记忆操作等核心功能，支持完整流程、快速流程、变更流程和紧急流程四种工作模式。

### 核心功能
- 智能流程分支决策
- 阶段进度跟踪与更新
- 异常状态记录与解决
- AI 导航建议生成
- 记忆池管理与检索

## 2. 环境准备

### 2.1 系统要求
- Python 3.6 及以上版本
- 操作系统：Windows/macOS/Linux

### 2.2 依赖安装
```bash
# 克隆项目仓库后执行
cd aceflow-project
pip install -r requirements.txt
```

### 2.3 环境验证
```bash
# 检查 Python 版本
python --version  # 应显示 3.6+

# 运行环境检查脚本
python check_env.py
# 成功输出：✅ 环境检查通过
```

## 3. 快速入门

### 3.1 初始化项目
```bash
# 创建新项目目录
mkdir aceflow-demo && cd aceflow-demo

# 初始化 AceFlow 项目结构
python aceflow_cli.py init
```

初始化成功后将创建以下目录结构：
```
.aceflow/
├── config/           # 配置文件目录
├── memory_pool/      # 记忆池存储
├── scripts/          # 核心脚本
├── templates/        # 流程模板
└── current_state.json # 当前状态文件
```

### 3.2 确定流程分支
```bash
# 分析任务描述并推荐流程分支
python aceflow_cli.py determine-workflow "开发用户注册功能模块"
```

输出示例：
```
推荐流程分支: 完整流程
阶段路径: S1 → S2 → S3 → S4 → S5 → S6 → S7 → S8
决策依据: 
- 任务包含"开发"关键词，判定为新功能开发
- 未检测到"紧急"、"修复"等特殊标识
- 任务复杂度评估: 中 (6/10)，适合完整流程
```

### 3.3 更新阶段进度
```bash
# 更新 S1 阶段进度至 100%（完成）
python aceflow_cli.py update-status S1 100
```

### 3.4 获取导航建议
```bash
python aceflow_cli.py get-suggestions
```

输出示例：
```
导航建议:
- [high] 阶段 S1 已完成，准备进入 S2
```

## 4. 命令参考

### 4.1 流程管理命令

#### determine-workflow
**功能**：根据任务描述自动分析并推荐流程分支  
**用法**：`python aceflow_cli.py determine-workflow "<任务描述>"`  
**示例**：
```bash
python aceflow_cli.py determine-workflow "修复登录页面验证码不显示问题"
```
**输出**：推荐流程分支及阶段路径

#### set-workflow
**功能**：手动设置流程分支  
**用法**：`python aceflow_cli.py set-workflow <流程类型>`  
**流程类型**：`full_workflow`（完整流程）、`quick_workflow`（快速流程）、`change_workflow`（变更流程）、`emergency_workflow`（紧急流程）  
**示例**：
```bash
python aceflow_cli.py set-workflow quick_workflow
```

#### load-template
**功能**：加载指定阶段的模板文件  
**用法**：`python aceflow_cli.py load-template <阶段ID> [输出路径]`  
**示例**：
```bash
python aceflow_cli.py load-template S2 ./s2_tasks.md
```

### 4.2 状态管理命令

#### update-status
**功能**：更新指定阶段的进度  
**用法**：`python aceflow_cli.py update-status <阶段ID> <进度百分比>`  
**示例**：
```bash
python aceflow_cli.py update-status S4 75
```

#### get-status
**功能**：查询当前项目状态  
**用法**：`python aceflow_cli.py get-status [阶段ID]`  
**示例**：
```bash
# 查询所有阶段状态
python aceflow_cli.py get-status

# 查询特定阶段状态
python aceflow_cli.py get-status S3
```

#### record-abnormality
**功能**：记录异常状态  
**用法**：`python aceflow_cli.py record-abnormality <阶段ID> "<异常描述>" [--severity 严重度]`  
**严重度**：`high`（高）、`medium`（中，默认）、`low`（低）  
**示例**：
```bash
python aceflow_cli.py record-abnormality S4 "用户注册接口返回500错误" --severity high
```

#### resolve-abnormality
**功能**：标记异常状态为已解决  
**用法**：`python aceflow_cli.py resolve-abnormality <异常ID>`  
**示例**：
```bash
python aceflow_cli.py resolve-abnormality ABN-202507101530
```

### 4.3 导航与建议命令

#### get-suggestions
**功能**：获取AI导航建议  
**用法**：`python aceflow_cli.py get-suggestions`  
**示例**：
```bash
python aceflow_cli.py get-suggestions
```

#### explain-decision
**功能**：解释最近一次流程决策依据  
**用法**：`python aceflow_cli.py explain-decision`  
**示例**：
```bash
python aceflow_cli.py explain-decision
```

### 4.4 记忆池命令

#### store-memory
**功能**：手动存储记忆片段  
**用法**：`python aceflow_cli.py store-memory <记忆类型> "<内容>" [--metadata key=value]`  
**记忆类型**：`REQ`（需求）、`CON`（约束）、`TASK`（任务）、`CODE`（代码）、`TEST`（测试）、`DEFECT`（缺陷）、`FDBK`（反馈）  
**示例**：
```bash
python aceflow_cli.py store-memory REQ "用户要求支持手机号登录" --metadata source=PRD author=product_manager
```

#### retrieve-memory
**功能**：检索记忆片段  
**用法**：`python aceflow_cli.py retrieve-memory [--type 记忆类型] [--keywords 关键词]`  
**示例**：
```bash
# 检索所有需求记忆
python aceflow_cli.py retrieve-memory --type REQ

# 检索包含"登录"关键词的记忆
python aceflow_cli.py retrieve-memory --keywords 登录
```

### 4.5 工具命令

#### validate-config
**功能**：验证配置文件完整性  
**用法**：`python aceflow_cli.py validate-config [--check-templates]`  
**示例**：
```bash
# 基本配置验证
python aceflow_cli.py validate-config

# 包含模板文件验证
python aceflow_cli.py validate-config --check-templates
```

#### export-state
**功能**：导出当前状态数据  
**用法**：`python aceflow_cli.py export-state [输出文件路径]`  
**示例**：
```bash
python aceflow_cli.py export-state ./current_state_backup.json
```

#### import-state
**功能**：导入状态数据  
**用法**：`python aceflow_cli.py import-state <状态文件路径>`  
**示例**：
```bash
python aceflow_cli.py import-state ./current_state_backup.json
```

## 5. 常见工作流示例

### 5.1 新功能开发（完整流程）
```bash
# 1. 初始化项目
python aceflow_cli.py init

# 2. 确定流程分支
python aceflow_cli.py determine-workflow "开发用户注册功能"

# 3. 加载 S1 模板并编辑
python aceflow_cli.py load-template S1 ./s1_user_story.md
# 编辑 s1_user_story.md 文件...

# 4. 更新 S1 进度
python aceflow_cli.py update-status S1 100

# 5. 获取导航建议（自动进入 S2）
python aceflow_cli.py get-suggestions

# 6. 继续 S2 任务拆分...
python aceflow_cli.py load-template S2 ./s2_tasks.md
```

### 5.2 Bug 修复（快速流程）
```bash
# 1. 初始化项目（如已初始化可跳过）
python aceflow_cli.py init

# 2. 设置为快速流程
python aceflow_cli.py set-workflow quick_workflow

# 3. 加载 S2 模板（直接任务拆分）
python aceflow_cli.py load-template S2 ./s2_tasks.md

# 4. 更新开发进度
python aceflow_cli.py update-status S2 100
python aceflow_cli.py update-status S4 100  # 直接进入开发阶段

# 5. 记录测试结果
python aceflow_cli.py update-status S5 100

# 6. 完成进度汇总
python aceflow_cli.py update-status S8 100
```

### 5.3 需求变更处理
```bash
# 1. 记录需求变更记忆
python aceflow_cli.py store-memory FDBK "用户要求增加第三方登录功能"

# 2. 设置为变更流程
python aceflow_cli.py set-workflow change_workflow

# 3. 更新需求和任务
python aceflow_cli.py load-template S1 ./s1_user_story.md  # 更新用户故事
python aceflow_cli.py load-template S2 ./s2_tasks.md       # 更新任务拆分
python aceflow_cli.py load-template S3 ./s3_testcases.md   # 更新测试用例

# 4. 执行开发和测试
python aceflow_cli.py update-status S1 100
python aceflow_cli.py update-status S2 100
python aceflow_cli.py update-status S3 100
python aceflow_cli.py update-status S4 100
```

## 6. 故障排除

### 6.1 导入错误
**错误信息**：`ImportError: attempted relative import beyond top-level package`  
**解决方案**：
```bash
# 1. 检查 __init__.py 文件是否存在
ls -la .aceflow/scripts/{__,core/__,cli/__,utils/__}init__.py

# 2. 确保 aceflow_cli.py 路径配置正确
cat aceflow_cli.py | grep sys.path.append
```

### 6.2 状态文件损坏
**错误信息**：`JSONDecodeError: Expecting value: line 1 column 1 (char 0)`  
**解决方案**：
```bash
# 1. 尝试恢复备份
cp .aceflow/current_state.json.bak .aceflow/current_state.json

# 2. 如无备份，重新初始化状态
python aceflow_cli.py init --reset-state
```

### 6.3 命令不存在
**错误信息**：`error: unrecognized arguments: new-command`  
**解决方案**：
```bash
# 1. 检查命令拼写
python aceflow_cli.py --help  # 查看所有可用命令

# 2. 更新到最新版本
git pull origin main
```

### 6.4 模板加载失败
**错误信息**：`FileNotFoundError: [Errno 2] No such file or directory: '.aceflow/templates/stage_templates/s1_user_story.md'`  
**解决方案**：
```bash
# 1. 验证模板路径配置
cat .vscode/aceflow_agent.json | grep templates

# 2. 重新安装模板文件
python aceflow_cli.py install-templates
```

## 7. 高级配置

### 7.1 动态阈值调整
编辑 `.aceflow/config/dynamic_thresholds.json` 文件：
```json
{
  "stage_specific": {
    "S4": {
      "unit_test_pass_rate": {
        "default": 90,
        "critical_task": 95,
        "minor_task": 85
      }
    }
  }
}
```

### 7.2 AI 决策信任度设置
编辑 `.vscode/aceflow_agent.json` 文件：
```json
{
  "workflow_config": {
    "ai_trust_level": "L2",  // L1:仅建议, L2:低风险自动执行, L3:全流程自动决策
    "success_threshold": 0.85
  }
}
```

### 7.3 自定义流程分支
编辑 `.aceflow/config/workflow_rules.json` 文件，添加自定义流程：
```json
{
  "workflow_rules": {
    "research_workflow": ["S1", "S3", "S7", "S8"]  // 调研类流程
  },
  "workflow_conditions": {
    "research_workflow": {
      "keywords": ["调研", "研究", "探索"],
      "complexity_threshold": 3
    }
  }
}
```

## 8. 附录

### 8.1 阶段 ID 与名称对应表
| 阶段 ID | 名称 | 核心任务 |
|---------|------|----------|
| S1 | 用户故事细化 | 将需求转化为用户故事 |
| S2 | 任务拆分 | 将用户故事拆分为开发任务 |
| S3 | 测试用例设计 | 设计测试用例 |
| S4 | 功能实现 | 代码开发与单元测试 |
| S5 | 测试报告 | 执行测试并生成报告 |
| S6 | 代码评审 | 代码质量与规范评审 |
| S7 | 演示与反馈 | 功能演示与反馈收集 |
| S8 | 进度汇总 | 项目进度总结与规划 |

### 8.2 记忆类型说明
| 记忆类型 | 代码 | 描述 | 示例 |
|----------|------|------|------|
| 需求记忆 | REQ | 记录用户需求和期望 | 用户需要支持手机号登录 |
| 约束记忆 | CON | 技术约束和限制条件 | 必须兼容IE11浏览器 |
| 任务记忆 | TASK | 任务相关信息 | 登录模块需在5月前完成 |
| 代码记忆 | CODE | 代码实现细节 | 使用JWT进行身份验证 |
| 测试记忆 | TEST | 测试相关信息 | 测试用例TC-001验证登录功能 |
| 缺陷记忆 | DEFECT | 缺陷和问题记录 | 登录接口在密码含特殊字符时失败 |
| 反馈记忆 | FDBK | 用户反馈信息 | 用户认为注册流程太复杂 |

### 8.3 常用命令速查表
| 任务 | 命令 |
|------|------|
| 初始化项目 | `python aceflow_cli.py init` |
| 选择流程分支 | `python aceflow_cli.py determine-workflow "任务描述"` |
| 更新阶段进度 | `python aceflow_cli.py update-status Sx 进度` |
| 获取导航建议 | `python aceflow_cli.py get-suggestions` |
| 记录异常 | `python aceflow_cli.py record-abnormality Sx "描述"` |
| 检索记忆 | `python aceflow_cli.py retrieve-memory --keywords 关键词` |
| 验证配置 | `python aceflow_cli.py validate-config` |