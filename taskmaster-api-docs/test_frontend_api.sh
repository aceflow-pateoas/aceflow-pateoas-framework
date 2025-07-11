#!/bin/bash

echo "测试前端保存功能..."

# 测试是否能访问任务页面
echo "1. 测试页面访问..."
response=$(curl -s http://localhost:5173/tasks)
if [[ $response == *"任务管理"* ]]; then
    echo "✅ 任务页面可以访问"
else
    echo "❌ 任务页面访问失败"
fi

# 测试API代理
echo "2. 测试API代理..."
login_response=$(curl -s -X POST -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"12345678"}' \
    http://localhost:5173/api/auth/login)

if [[ $login_response == *"token"* ]]; then
    echo "✅ API代理正常工作"
    TOKEN=$(echo $login_response | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    
    # 测试创建任务
    echo "3. 测试任务创建API..."
    create_response=$(curl -s -X POST -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"title":"前端测试任务","description":"通过脚本创建","priority":"high"}' \
        http://localhost:5173/api/tasks)
    
    if [[ $create_response == *"Task created successfully"* ]]; then
        echo "✅ 任务创建API正常"
    else
        echo "❌ 任务创建API失败: $create_response"
    fi
else
    echo "❌ API代理失败: $login_response"
fi

echo "测试完成！"