# TaskMaster 部署指南

## 🚀 项目概述

TaskMaster 是一个基于 Vue 3 + Express + SQLite 的全栈任务管理系统，具有现代化的用户界面和完整的用户认证功能。

## 📁 项目结构

```
aceflow-pateoas-framework/
├── taskmaster-api/          # 后端 API 服务
│   ├── src/
│   │   ├── app.js          # 主应用文件
│   │   ├── models/         # 数据模型
│   │   ├── routes/         # 路由定义
│   │   ├── middleware/     # 中间件
│   │   └── utils/          # 工具函数
│   ├── package.json
│   └── database.sqlite     # SQLite 数据库
└── taskmaster-web/         # 前端 Web 应用
    ├── src/
    │   ├── components/     # Vue 组件
    │   ├── views/          # 页面组件
    │   ├── stores/         # Pinia 状态管理
    │   ├── api/            # API 调用
    │   └── utils/          # 工具函数
    ├── package.json
    └── vite.config.js      # Vite 配置
```

## 🛠️ 技术栈

### 后端
- **Node.js** - 运行时环境
- **Express.js** - Web 框架
- **SQLite** - 数据库
- **JWT** - 身份认证
- **bcrypt** - 密码加密

### 前端
- **Vue 3** - 前端框架
- **Element Plus** - UI 组件库
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP 客户端
- **Vite** - 构建工具

## 🚀 快速启动

### 1. 环境要求
- Node.js >= 16.0.0
- npm >= 8.0.0

### 2. 安装依赖

```bash
# 安装后端依赖
cd taskmaster-api
npm install

# 安装前端依赖
cd ../taskmaster-web
npm install
```

### 3. 启动服务

```bash
# 启动后端服务 (端口 3001)
cd taskmaster-api
PORT=3001 npm start

# 启动前端服务 (端口 5173)
cd taskmaster-web
npm run dev
```

### 4. 访问应用

- **前端应用**: http://localhost:5173
- **后端API**: http://localhost:3001
- **API健康检查**: http://localhost:3001/health
- **API测试页面**: http://localhost:5173/test.html

## 📋 功能特性

### ✅ 已实现功能

#### 用户认证
- [x] 用户注册
- [x] 用户登录
- [x] JWT 令牌认证
- [x] 自动登录状态保持
- [x] 安全登出

#### 任务管理
- [x] 创建任务
- [x] 编辑任务
- [x] 删除任务
- [x] 复制任务
- [x] 任务状态切换（待办 → 进行中 → 已完成）
- [x] 优先级设置（高、中、低）
- [x] 截止日期设置
- [x] 任务描述

#### 用户界面
- [x] 响应式设计
- [x] 现代化UI设计
- [x] 任务筛选（按状态、优先级）
- [x] 任务搜索
- [x] 加载动画
- [x] 任务卡片交互效果
- [x] 错误处理和用户反馈

### 🎯 高级功能（可扩展）
- [ ] 任务拖拽排序
- [ ] 任务分类/标签
- [ ] 任务统计图表
- [ ] 批量操作
- [ ] 数据导出
- [ ] 主题切换
- [ ] 离线支持
- [ ] 实时通知

## 🔧 API 接口

### 认证接口
```
POST /api/auth/register  # 用户注册
POST /api/auth/login     # 用户登录
```

### 任务接口
```
GET    /api/tasks        # 获取任务列表
POST   /api/tasks        # 创建任务
PUT    /api/tasks/:id    # 更新任务
DELETE /api/tasks/:id    # 删除任务
```

### 其他接口
```
GET /health              # 健康检查
GET /                    # API 信息
```

## 🔒 安全特性

- JWT 令牌认证
- 密码 bcrypt 加密
- 输入数据验证
- SQL 注入防护
- CORS 跨域配置
- 错误信息安全处理

## 📱 响应式支持

- **桌面端**: 1200px+
- **平板端**: 768px - 1199px
- **移动端**: < 768px

## 🐛 调试和测试

### 后端调试
```bash
# 查看日志
cd taskmaster-api
tail -f server.log

# 测试API
curl http://localhost:3001/health
```

### 前端调试
- 打开浏览器开发者工具
- 访问 http://localhost:5173/test.html 进行API测试

## 🚀 生产部署

### 构建前端
```bash
cd taskmaster-web
npm run build
```

### 部署配置

1. **设置环境变量**
```bash
export NODE_ENV=production
export JWT_SECRET=your-secure-secret-key
export PORT=3001
```

2. **启动服务**
```bash
cd taskmaster-api
npm start
```

3. **反向代理配置** (Nginx 示例)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /api {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        root /path/to/taskmaster-web/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

## 📞 故障排除

### 常见问题

1. **端口占用错误**
```bash
# 查找占用端口的进程
lsof -i :3001
# 或者使用其他端口
PORT=3002 npm start
```

2. **依赖安装失败**
```bash
# 清理缓存重新安装
rm -rf node_modules package-lock.json
npm install
```

3. **CORS 错误**
- 确保前端代理配置正确
- 检查后端 CORS 中间件配置

4. **数据库连接错误**
- 确保 SQLite 文件权限正确
- 检查数据库文件路径

## 🎉 项目完成状态

✅ **项目已成功完成！**

- 后端 API 服务正常运行 (http://localhost:3001)
- 前端 Vue 应用正常运行 (http://localhost:5173)
- 用户认证功能完整
- 任务管理功能完整
- 现代化 UI 设计
- 响应式布局支持
- 前后端完全集成

现在您可以：
1. 访问 http://localhost:5173 使用完整的任务管理系统
2. 注册新账户或使用测试账户登录
3. 创建、编辑、删除和管理任务
4. 体验流畅的用户界面和交互效果

祝您使用愉快！🎊