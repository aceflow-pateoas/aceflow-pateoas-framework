# AceFlow v2.0 迁移指南

> 从传统开发流程或AceFlow v1.x迁移到AceFlow v2.0的完整指南

## 📋 迁移概述

AceFlow v2.0引入了重大改进，包括：
- 三种流程模式（轻量级、标准、完整）
- 增强的敏捷集成
- 现代化Web界面
- 智能状态管理
- 简化的配置系统

## 🎯 迁移路径

### 1. 从传统开发流程迁移

#### 1.1 从瀑布模型迁移

**传统瀑布流程：**
```
需求分析 → 系统设计 → 编码实现 → 测试 → 部署 → 维护
```

**推荐AceFlow模式：** 标准模式或完整模式

**映射关系：**
- 需求分析 → P1 (Requirements)
- 系统设计 → P2 (Planning)  
- 编码实现 → D1 (Implementation)
- 测试 → D2 (Testing)
- 部署 → R1 (Review)

**迁移步骤：**
```bash
# 1. 初始化AceFlow项目
python .aceflow/scripts/aceflow init --mode=standard

# 2. 配置项目信息
python .aceflow/scripts/aceflow config --set project.methodology=waterfall_migration

# 3. 导入现有项目状态
python .aceflow/scripts/aceflow start P1
```

#### 1.2 从敏捷Scrum迁移

**现有Scrum流程：**
```
Sprint Planning → Daily Scrum → Sprint Review → Sprint Retrospective
```

**推荐AceFlow模式：** 轻量级模式

**映射关系：**
- Sprint Planning → P (Planning)
- Daily Scrum → D阶段检查点
- Sprint Review & Retrospective → R (Review)

**迁移步骤：**
```bash
# 1. 初始化为轻量级模式
python .aceflow/scripts/aceflow init --mode=minimal

# 2. 配置Scrum集成
python .aceflow/scripts/aceflow config --set agile.framework=scrum
python .aceflow/scripts/aceflow config --set agile.iteration_length=2weeks

# 3. 导入Sprint Backlog
python .aceflow/scripts/aceflow start P
```

#### 1.3 从Kanban迁移

**现有Kanban流程：**
```
To Do → In Progress → Review → Done
```

**推荐AceFlow模式：** 轻量级模式

**映射关系：**
- To Do → P (Planning)
- In Progress → D (Development)
- Review → R (Review)
- Done → 已完成状态

**迁移步骤：**
```bash
# 1. 初始化项目
python .aceflow/scripts/aceflow init --mode=minimal

# 2. 配置Kanban集成
python .aceflow/scripts/aceflow config --set agile.framework=kanban

# 3. 设置WIP限制
python .aceflow/scripts/aceflow config --set agile.wip_limits.development=5
```

### 2. 从AceFlow v1.x迁移

#### 2.1 版本兼容性

| v1.x特性 | v2.0对应 | 迁移难度 |
|----------|----------|----------|
| 8阶段流程 | 完整模式 | 低 |
| 配置文件 | 新配置格式 | 中 |
| 状态管理 | 增强状态引擎 | 低 |
| CLI命令 | 新CLI接口 | 中 |
| 记忆系统 | 兼容 | 低 |

#### 2.2 配置文件迁移

**v1.x配置格式：**
```yaml
# 旧格式
aceflow:
  version: "1.0"
  stages: [S1, S2, S3, S4, S5, S6, S7, S8]
  current_stage: S3
```

**v2.0配置格式：**
```yaml
# 新格式
project:
  name: "项目名称"
  created_at: "2025-01-10"
  
flow:
  mode: "complete"
  current_stage: "S3"
  
agile:
  enabled: true
  framework: "scrum"
```

**自动迁移工具：**
```bash
# 自动迁移配置文件
python .aceflow/scripts/migrate_config.py --from-version 1.0
```

#### 2.3 状态数据迁移

**v1.x状态格式：**
```json
{
  "current_stage": "S3",
  "stage_status": {
    "S1": "completed",
    "S2": "completed",
    "S3": "in_progress"
  }
}
```

**v2.0状态格式：**
```json
{
  "flow_mode": "complete",
  "current_stage": "S3",
  "stage_states": {
    "S1": {
      "status": "completed",
      "progress": 100,
      "start_time": "2025-01-10T09:00:00",
      "end_time": "2025-01-10T17:00:00"
    }
  }
}
```

**迁移脚本：**
```bash
# 迁移状态数据
python .aceflow/scripts/migrate_state.py --backup
```

## 🛠️ 迁移工具

### 自动迁移脚本

创建迁移脚本 `migrate_to_v2.py`:

```python
#!/usr/bin/env python3
"""
AceFlow v1.x to v2.0 迁移工具
"""

import json
import yaml
import shutil
from pathlib import Path
from datetime import datetime

class AceFlowMigrator:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.aceflow_dir = project_root / ".aceflow"
        self.backup_dir = project_root / ".aceflow_backup"
        
    def migrate(self):
        """执行完整迁移"""
        print("🔄 开始AceFlow v2.0迁移...")
        
        # 1. 备份现有数据
        self.backup_existing_data()
        
        # 2. 检测现有配置
        old_config = self.detect_old_config()
        
        # 3. 迁移配置文件
        self.migrate_config(old_config)
        
        # 4. 迁移状态数据
        self.migrate_state_data()
        
        # 5. 迁移模板文件
        self.migrate_templates()
        
        # 6. 更新目录结构
        self.update_directory_structure()
        
        print("✅ 迁移完成！")
        print(f"📁 备份目录: {self.backup_dir}")
        
    def backup_existing_data(self):
        """备份现有数据"""
        if self.aceflow_dir.exists():
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)
            shutil.copytree(self.aceflow_dir, self.backup_dir)
            print(f"📦 已备份到: {self.backup_dir}")
```

### 手动迁移清单

#### 迁移前准备
- [ ] 备份现有项目数据
- [ ] 记录当前配置和状态
- [ ] 确认团队成员了解新版本变化
- [ ] 准备迁移测试环境

#### 配置迁移
- [ ] 转换配置文件格式
- [ ] 更新流程模式设置
- [ ] 配置敏捷集成参数
- [ ] 验证AI设置

#### 数据迁移
- [ ] 迁移阶段状态数据
- [ ] 转换进度信息
- [ ] 保留历史记录
- [ ] 更新时间戳格式

#### 模板迁移
- [ ] 更新模板文件格式
- [ ] 适配新的阶段结构
- [ ] 检查自定义模板
- [ ] 验证模板完整性

#### 功能验证
- [ ] 测试CLI命令
- [ ] 验证Web界面
- [ ] 检查状态管理
- [ ] 确认AI功能正常

## 🎯 分阶段迁移策略

### 阶段1：准备阶段（1-2天）
**目标**：了解新版本，准备迁移环境

**任务**：
1. 学习AceFlow v2.0新特性
2. 评估当前项目状态
3. 制定迁移计划
4. 准备测试环境

**输出**：
- 迁移计划文档
- 风险评估报告
- 团队培训材料

### 阶段2：试点迁移（2-3天）
**目标**：小规模试点验证

**任务**：
1. 选择1-2个小项目试点
2. 执行完整迁移流程
3. 收集问题和反馈
4. 优化迁移工具

**输出**：
- 试点迁移报告
- 问题和解决方案清单
- 优化的迁移工具

### 阶段3：批量迁移（3-5天）
**目标**：迁移所有项目

**任务**：
1. 批量执行迁移
2. 监控迁移进度
3. 解决迁移问题
4. 验证迁移结果

**输出**：
- 迁移完成报告
- 项目状态清单
- 问题处理记录

### 阶段4：稳定运行（1-2周）
**目标**：确保新版本稳定运行

**任务**：
1. 监控系统运行状态
2. 收集用户反馈
3. 解决遗留问题
4. 优化配置参数

**输出**：
- 运行状态报告
- 用户反馈汇总
- 优化建议

## 📊 迁移验证

### 功能验证清单

#### 基础功能
- [ ] 项目初始化正常
- [ ] 状态管理正确
- [ ] 进度跟踪准确
- [ ] 阶段切换顺畅

#### 高级功能
- [ ] AI建议有效
- [ ] 记忆系统运行
- [ ] 敏捷集成正常
- [ ] Web界面可用

#### 性能验证
- [ ] 启动时间合理
- [ ] 响应速度良好
- [ ] 内存使用正常
- [ ] 并发处理稳定

### 回滚方案

如果迁移出现问题，可以按以下步骤回滚：

```bash
# 1. 停止新版本服务
python .aceflow/scripts/aceflow stop

# 2. 恢复备份数据
rm -rf .aceflow
mv .aceflow_backup .aceflow

# 3. 验证回滚结果
python .aceflow/scripts/aceflow status

# 4. 重新启动服务
python .aceflow/scripts/aceflow start
```

## 🚀 迁移后优化

### 配置优化
1. **调整流程模式**：根据实际使用情况选择最适合的模式
2. **优化敏捷集成**：配置符合团队习惯的敏捷参数
3. **个性化设置**：根据团队需求调整AI和通知设置

### 性能优化
1. **清理无用数据**：删除迁移过程中的临时文件
2. **优化配置参数**：调整缓存和超时设置
3. **监控系统性能**：建立性能监控机制

### 团队培训
1. **新功能培训**：介绍v2.0的新特性和使用方法
2. **最佳实践分享**：分享迁移经验和优化建议
3. **持续支持**：建立问题反馈和支持机制

## 🎉 迁移成功标准

### 技术标准
- [ ] 所有项目成功迁移
- [ ] 功能验证100%通过
- [ ] 性能指标满足要求
- [ ] 数据完整性验证通过

### 业务标准
- [ ] 团队接受度良好
- [ ] 工作效率提升
- [ ] 用户满意度高
- [ ] 问题处理及时

### 持续改进
- [ ] 建立反馈机制
- [ ] 定期评估效果
- [ ] 优化使用流程
- [ ] 规划下一步改进

## 📞 迁移支持

### 技术支持
- **文档支持**：完整的迁移文档和FAQ
- **工具支持**：自动化迁移脚本和验证工具
- **社区支持**：GitHub Issues和讨论区

### 咨询服务
- **迁移咨询**：专业的迁移规划和实施建议
- **技术培训**：团队培训和最佳实践分享
- **后续支持**：迁移后的优化和问题解决

恭喜你完成AceFlow v2.0迁移！享受AI驱动的敏捷开发体验吧！🎉