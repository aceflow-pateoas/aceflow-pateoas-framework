# TaskMaster API - 用户故事

## 项目概述
**项目名称**：TaskMaster API  
**项目类型**：RESTful API  
**技术栈**：Node.js + Express + SQLite  
**预估工时**：5天  

## 核心用户故事

### 故事1：用户注册
**作为** 一个新用户  
**我希望** 能够创建账户  
**以便** 我能够使用任务管理服务  

**验收标准**：
- 用户可以通过email和密码注册
- 系统验证email格式的有效性
- 密码至少8位字符
- 注册成功后返回用户ID和JWT token

### 故事2：用户登录
**作为** 一个已注册用户  
**我希望** 能够登录系统  
**以便** 我能够访问我的任务  

**验收标准**：
- 用户可以通过email和密码登录
- 登录成功返回JWT token
- 登录失败返回适当的错误信息

### 故事3：创建任务
**作为** 一个已登录用户  
**我希望** 能够创建新任务  
**以便** 我能够记录需要完成的工作  

**验收标准**：
- 任务包含标题、描述、优先级、截止日期
- 任务创建时状态默认为"待办"
- 返回创建的任务信息包含任务ID

### 故事4：查看任务列表
**作为** 一个已登录用户  
**我希望** 能够查看我的所有任务  
**以便** 我能够了解当前的工作安排  

**验收标准**：
- 显示当前用户的所有任务
- 支持按状态筛选（待办/进行中/已完成）
- 支持按优先级排序
- 支持分页查询

### 故事5：更新任务状态
**作为** 一个已登录用户  
**我希望** 能够更新任务的状态  
**以便** 我能够跟踪工作进度  

**验收标准**：
- 可以将任务状态更改为：待办/进行中/已完成
- 更新时间自动记录
- 只能更新自己的任务

### 故事6：删除任务
**作为** 一个已登录用户  
**我希望** 能够删除不需要的任务  
**以便** 我能够保持任务列表的整洁  

**验收标准**：
- 可以删除自己创建的任务
- 删除前需要确认
- 删除后任务不再出现在列表中

## API端点设计

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 任务管理
- `GET /api/tasks` - 获取任务列表
- `POST /api/tasks` - 创建新任务
- `GET /api/tasks/:id` - 获取特定任务
- `PUT /api/tasks/:id` - 更新任务
- `DELETE /api/tasks/:id` - 删除任务

## 数据模型

### 用户表 (users)
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 任务表 (tasks)
```sql
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(20) DEFAULT 'todo',
  priority VARCHAR(10) DEFAULT 'medium',
  due_date DATE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 技术需求
- Node.js 18+
- Express.js框架
- SQLite数据库
- bcrypt密码加密
- jsonwebtoken认证
- express-validator输入验证
- cors跨域支持

## 非功能性需求
- API响应时间 < 200ms
- 支持100并发用户
- 数据安全（密码加密，JWT认证）
- 输入验证和错误处理
- API文档（Swagger/OpenAPI）