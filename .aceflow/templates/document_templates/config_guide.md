# AceFlow-PATEOAS 配置指南

## 1. 配置概述

### 1.1 配置体系
AceFlow-PATEOAS采用分层配置体系，确保灵活性和可维护性：
- **核心配置**：工作流规则和动态阈值
- **环境配置**：路径和存储设置
- **AI配置**：决策参数和信任度设置
- **扩展配置**：第三方集成和自定义规则

### 1.2 配置文件位置
所有配置文件集中存放在以下目录：
```
.aceflow/
├── config/
│   ├── dynamic_thresholds.json  # 动态阈值配置
│   └── workflow_rules.json      # 工作流规则配置
└── current_state.json           # 当前状态文件
.vscode/
└── aceflow_agent.json           # AI Agent配置
```

### 1.3 配置加载优先级
1. 环境变量（最高优先级，临时覆盖）
2. 项目级配置（.aceflow/config/）
3. 默认配置（内置，最低优先级）

## 2. 核心配置文件详解

### 2.1 dynamic_thresholds.json

#### 文件路径
`.aceflow/config/dynamic_thresholds.json`

#### 功能描述
定义各阶段的动态阈值和验收标准，支持按任务类型和模块自定义阈值。

#### 配置结构
```json
{
  "global": {
    "time_adjustment_range": 20,
    "memory_retention_days": 30
  },
  "stage_specific": {
    "S3": {
      "test_case_coverage": {
        "default": 80,
        "payment_module": 99,
        "ui_module": 75
      }
    },
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

#### 参数说明

| 层级 | 参数 | 类型 | 描述 | 默认值 |
|------|------|------|------|--------|
| global | time_adjustment_range | int | 阶段时间调整最大范围(%) | 20 |
| global | memory_retention_days | int | 普通记忆保留天数 | 30 |
| stage_specific.S3 | test_case_coverage | object | 测试用例覆盖率阈值(%) | - |
| stage_specific.S4 | unit_test_pass_rate | object | 单元测试通过率阈值(%) | - |

#### 配置示例
为安全模块设置更高的测试覆盖率要求：
```json
"S3": {
  "test_case_coverage": {
    "default": 80,
    "security_module": 98,
    "payment_module": 99
  }
}
```

### 2.2 workflow_rules.json

#### 文件路径
`.aceflow/config/workflow_rules.json`

#### 功能描述
定义工作流分支、记忆池策略和异常处理规则。

#### 配置结构
```json
{
  "workflow_rules": {
    "full_workflow": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
    "quick_workflow": ["S2", "S4", "S5", "S8"]
  },
  "memory_pool_config": {
    "storage_path": "./.aceflow/memory_pool",
    "retention_policy": "critical_forever,temporary_7d"
  },
  "abnormality_mapping": {
    "需求变更": {
      "impact_stages": ["S1", "S2", "S3"],
      "handling_flow": "change_workflow",
      "auto_trigger": true
    }
  },
  "ai_decision_config": {
    "trust_level": "L2",
    "success_threshold": 0.85
  }
}
```

#### 关键配置说明

##### 工作流分支定义
```json
"workflow_rules": {
  "full_workflow": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
  "quick_workflow": ["S2", "S4", "S5", "S8"],
  "change_workflow": ["S1", "S2", "S3", "S4"],
  "emergency_workflow": ["S4", "S5", "S6", "S8"]
}
```

##### 异常处理映射
```json
"abnormality_mapping": {
  "性能不达标": {
    "impact_stages": ["S4", "S3"],
    "handling_flow": "performance_optimization_subflow",
    "auto_trigger": true
  }
}
```

##### AI决策配置
```json
"ai_decision_config": {
  "trust_level": "L2",          // AI决策信任等级(L1/L2/L3)
  "decision_log_path": ".aceflow/logs/ai_decisions.log",
  "success_threshold": 0.85     // 决策成功率阈值
}
```

### 2.3 aceflow_agent.json

#### 文件路径
`.vscode/aceflow_agent.json`

#### 功能描述
VS Code集成配置，定义AI Agent能力和工作路径。

#### 配置结构
```json
{
  "agent_type": "pateoas_aceflow_agent",
  "capabilities": [
    "state_awareness",
    "memory_management",
    "autonomous_navigation",
    "abnormality_handling"
  ],
  "output_config": {
    "root_dir": "aceflow_result",
    "stage_dir_format": "S{stage_number}_{stage_name}",
    "compatibility_mode": true
  },
  "workflow_config": {
    "enable_ai_decision": true,
    "ai_trust_level": "L2",
    "auto_trigger_workflow": true
  }
}
```

#### 关键配置说明

| 参数 | 类型 | 描述 | 可选值 |
|------|------|------|--------|
| capabilities | array | AI Agent能力集 | state_awareness, memory_management等 |
| output_config.root_dir | string | 产物输出根目录 | aceflow_result(默认)或自定义路径 |
| output_config.compatibility_mode | boolean | 是否兼容旧流程目录 | true/false |
| workflow_config.ai_trust_level | string | AI决策信任等级 | L1/L2/L3 |

## 3. 动态阈值配置指南

### 3.1 阈值类型
AceFlow-PATEOAS支持多种类型的动态阈值：
- **覆盖率阈值**：测试用例覆盖率、代码覆盖率
- **通过率阈值**：单元测试通过率、集成测试通过率
- **数量阈值**：缺陷数量、任务数量
- **时间阈值**：阶段耗时、任务耗时

### 3.2 阈值配置策略

#### 按任务复杂度配置
```json
"S4": {
  "unit_test_pass_rate": {
    "default": 90,
    "simple_task": 85,      // 简单任务降低阈值
    "complex_task": 95,     // 复杂任务提高阈值
    "security_task": 98     // 安全相关任务最高阈值
  }
}
```

#### 按模块重要性配置
```json
"S3": {
  "test_case_coverage": {
    "default": 80,
    "core_module": 95,      // 核心模块
    "ui_module": 75,        // UI模块
    "third_party_module": 60 // 第三方集成模块
  }
}
```

### 3.3 阈值调整流程
1. 分析项目特性和质量要求
2. 在dynamic_thresholds.json中配置自定义阈值
3. 提交配置变更并通知团队
4. 运行验证命令检查配置有效性：
   ```bash
   python aceflow_cli.py validate-config
   ```

## 4. 工作流定制指南

### 4.1 添加自定义流程分支
1. 在workflow_rules.json中添加新流程定义：
   ```json
   "workflow_rules": {
     // ... 现有流程 ...
     "research_workflow": ["S1", "S3", "S7", "S8"] // 调研类流程
   }
   ```

2. 添加流程分支决策规则：
   ```json
   "workflow_conditions": {
     "research_workflow": {
       "keywords": ["调研", "研究", "探索"],
       "complexity_threshold": 3
     }
   }
   ```

3. 重启AI Agent使配置生效

### 4.2 自定义异常处理流程
1. 在abnormality_mapping中添加新异常类型：
   ```json
   "abnormality_mapping": {
     // ... 现有异常 ...
     "性能不达标": {
       "impact_stages": ["S4", "S3"],
       "handling_flow": "performance_optimization_subflow",
       "auto_trigger": true
     }
   }
   ```

2. 定义子流程：
   ```json
   "subflows": {
     "performance_optimization_subflow": [
       "S4.1: 性能分析",
       "S4.2: 优化实现",
       "S4.3: 性能测试"
     ]
   }
   ```

## 5. AI Agent配置

### 5.1 信任度等级配置
AI决策信任度分为三级，可在aceflow_agent.json中配置：

| 信任等级 | 描述 | 适用场景 |
|----------|------|----------|
| L1 | 仅提供建议，需人工确认 | 新团队、高风险项目 |
| L2 | 低风险决策自动执行，高风险需确认 | 稳定团队、常规项目 |
| L3 | 全流程自动决策，异常时通知 | 成熟团队、标准化项目 |

配置示例：
```json
"workflow_config": {
  "ai_trust_level": "L2"
}
```

### 5.2 能力开关配置
通过capabilities参数控制AI Agent能力：
```json
"capabilities": [
  "state_awareness",          // 状态感知能力
  "memory_management",         // 记忆管理能力
  "autonomous_navigation",     // 自主导航能力
  "abnormality_handling",      // 异常处理能力
  "auto_documentation"         // 自动文档生成(可选)
]
```

## 6. 产物目录配置

### 6.1 目录结构自定义
通过output_config配置产物目录结构：
```json
"output_config": {
  "root_dir": "custom_output_dir",  // 自定义根目录
  "stage_dir_format": "{stage_number}_{stage_name}_v{version}", // 自定义阶段目录格式
  "compatibility_mode": false      // 禁用旧流程兼容模式
}
```

### 6.2 环境变量覆盖
临时修改产物目录：
```bash
# Linux/Mac
export ACEFLOW_OUTPUT_DIR="special_release"

# Windows
set ACEFLOW_OUTPUT_DIR=special_release
```

## 7. 配置最佳实践

### 7.1 版本控制
- 将所有配置文件纳入版本控制
- 重大变更前创建配置备份
- 记录配置变更原因和影响范围

### 7.2 配置验证
定期验证配置有效性：
```bash
# 验证配置完整性
python aceflow_cli.py validate-config

# 检查配置与当前状态兼容性
python aceflow_cli.py check-compatibility
```

### 7.3 性能优化
- 对于大型项目，增加memory_retention_days
- 高频变更项目降低AI决策信任等级
- 复杂项目适当降低部分阶段阈值要求

## 8. 常见配置问题排查

### 8.1 配置不生效
1. 检查配置文件路径是否正确
2. 确认配置格式是否符合JSON规范
3. 检查是否存在重复配置项（后者会覆盖前者）
4. 重启VS Code或AI Agent

### 8.2 阈值调整不当
症状：流程频繁卡壳或质量下降
解决：
- 运行`python aceflow_cli.py analyze-thresholds`获取优化建议
- 逐步调整阈值，每次调整幅度不超过10%
- 参考历史项目配置和行业标准

### 8.3 记忆池存储问题
症状：记忆无法跨阶段传递
解决：
- 检查memory_pool_config.storage_path配置
- 确认目录权限是否可写
- 运行`python aceflow_cli.py check-memory-pool`修复记忆池

## 9. 附录：默认配置参考

### 9.1 默认dynamic_thresholds.json
```json
{
  "global": {
    "time_adjustment_range": 20,
    "memory_retention_days": 30
  },
  "stage_specific": {
    "S3": {
      "test_case_coverage": {
        "default": 80,
        "payment_module": 99,
        "ui_module": 75,
        "security_module": 95
      }
    },
    "S4": {
      "unit_test_pass_rate": {
        "default": 90,
        "critical_task": 95,
        "minor_task": 85
      },
      "code_coverage": {
        "default": 80,
        "security_module": 95
      }
    },
    "S5": {
      "defect_tolerance": {
        "high_severity": 0,
        "medium_severity": 3,
        "low_severity": 5
      }
    }
  }
}
```

### 9.2 默认workflow_rules.json
```json
{
  "workflow_rules": {
    "full_workflow": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
    "quick_workflow": ["S2", "S4", "S5", "S8"],
    "change_workflow": ["S1", "S2", "S3", "S4"],
    "emergency_workflow": ["S4", "S5", "S6", "S8"]
  },
  "memory_pool_config": {
    "storage_path": "./.aceflow/memory_pool",
    "retention_policy": "critical_forever,temporary_7d"
  },
  "abnormality_mapping": {
    "需求变更": {
      "impact_stages": ["S1", "S2", "S3"],
      "handling_flow": "change_workflow",
      "auto_trigger": true
    },
    "性能不达标": {
      "impact_stages": ["S4", "S3"],
      "handling_flow": "performance_optimization_subflow",
      "auto_trigger": true
    },
    "架构问题": {
      "impact_stages": ["S2", "S4"],
      "handling_flow": "architecture_review_subflow",
      "auto_trigger": true
    }
  },
  "ai_decision_config": {
    "trust_level": "L2",
    "decision_log_path": ".aceflow/logs/ai_decisions.log",
    "success_threshold": 0.85
  },
  "subflows": {
    "performance_optimization_subflow": [
      "S4.1: 性能分析",
      "S4.2: 优化实现",
      "S4.3: 性能测试"
    ],
    "architecture_review_subflow": [
      "S2.1: 架构评审",
      "S2.2: 任务重排",
      "S4.1: 架构调整"
    ]
  }
}
```