#!/bin/bash

echo "🚀 TaskMaster 系统验证脚本"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_service() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo -n "检查 $name... "
    response=$(curl -s "$url" 2>/dev/null)
    if [[ $response == *"$expected"* ]]; then
        echo -e "${GREEN}✓ 正常${NC}"
        return 0
    else
        echo -e "${RED}✗ 失败${NC}"
        echo "  期望包含: $expected"
        echo "  实际响应: $response"
        return 1
    fi
}

# 1. 检查后端服务
echo "📡 检查后端服务..."
check_service "后端健康检查" "http://localhost:3001/health" "OK"
check_service "后端API信息" "http://localhost:3001/" "TaskMaster API"

# 2. 检查前端服务
echo
echo "🌐 检查前端服务..."
check_service "前端页面" "http://localhost:5173/" "TaskMaster"

# 3. 测试API功能
echo
echo "🔐 测试用户认证..."

# 随机邮箱避免冲突
EMAIL="test$(date +%s)@example.com"
PASSWORD="12345678"

# 注册用户
echo -n "用户注册... "
register_response=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" \
    http://localhost:3001/api/auth/register)

if [[ $register_response == *"token"* ]]; then
    echo -e "${GREEN}✓ 成功${NC}"
    
    # 登录用户
    echo -n "用户登录... "
    login_response=$(curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" \
        http://localhost:3001/api/auth/login)
    
    if [[ $login_response == *"token"* ]]; then
        echo -e "${GREEN}✓ 成功${NC}"
        
        # 提取token
        TOKEN=$(echo $login_response | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
        
        # 测试任务管理
        echo
        echo "📝 测试任务管理..."
        
        # 创建任务
        echo -n "创建任务... "
        create_response=$(curl -s -X POST -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -d '{"title":"验证测试任务","description":"这是系统验证创建的任务","priority":"high"}' \
            http://localhost:3001/api/tasks)
        
        if [[ $create_response == *"Task created successfully"* ]]; then
            echo -e "${GREEN}✓ 成功${NC}"
            
            # 获取任务列表
            echo -n "获取任务列表... "
            tasks_response=$(curl -s -H "Authorization: Bearer $TOKEN" \
                http://localhost:3001/api/tasks)
            
            if [[ $tasks_response == *"验证测试任务"* ]]; then
                echo -e "${GREEN}✓ 成功${NC}"
            else
                echo -e "${RED}✗ 失败${NC}"
            fi
        else
            echo -e "${RED}✗ 失败${NC}"
            echo "  响应: $create_response"
        fi
    else
        echo -e "${RED}✗ 失败${NC}"
        echo "  响应: $login_response"
    fi
else
    echo -e "${RED}✗ 失败${NC}"
    echo "  响应: $register_response"
fi

# 4. 测试前端代理
echo
echo "🔄 测试前端代理..."
check_service "前端API代理" "http://localhost:5173/api/auth/login" "Invalid credentials"

echo
echo "=========================================="
echo -e "${YELLOW}📊 系统状态总览${NC}"
echo "后端服务: http://localhost:3001"
echo "前端服务: http://localhost:5173"
echo "测试页面: http://localhost:5173/test.html"
echo
echo -e "${GREEN}🎉 TaskMaster 系统验证完成！${NC}"
echo "您现在可以访问 http://localhost:5173 开始使用系统"