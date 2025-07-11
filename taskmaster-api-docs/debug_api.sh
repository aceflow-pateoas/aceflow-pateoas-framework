#!/bin/bash

echo "🧪 前端API代理测试"
echo "==================="

# 测试登录
echo "1. 测试登录..."
LOGIN_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"12345678"}' \
  http://localhost:5173/api/auth/login)

echo "登录响应: $LOGIN_RESPONSE"

if [[ $LOGIN_RESPONSE == *"token"* ]]; then
  echo "✅ 登录成功"
  
  # 提取token
  TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
  echo "Token: ${TOKEN:0:50}..."
  
  # 测试创建任务（通过前端代理）
  echo ""
  echo "2. 测试任务创建（通过前端代理）..."
  
  CREATE_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"title":"前端代理测试任务","description":"通过前端代理创建的任务","priority":"high"}' \
    http://localhost:5173/api/tasks)
  
  echo "创建响应: $CREATE_RESPONSE"
  
  if [[ $CREATE_RESPONSE == *"successfully"* ]]; then
    echo "✅ 任务创建成功"
  else
    echo "❌ 任务创建失败"
    # 检查是否是400错误
    if [[ $CREATE_RESPONSE == *"errors"* ]]; then
      echo "📋 验证错误详情: $CREATE_RESPONSE"
    fi
  fi
  
  # 测试获取任务列表
  echo ""
  echo "3. 测试获取任务列表..."
  TASKS_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" \
    http://localhost:5173/api/tasks)
  
  echo "任务列表响应: $TASKS_RESPONSE"
  
else
  echo "❌ 登录失败: $LOGIN_RESPONSE"
fi

echo ""
echo "测试完成！"