#!/bin/bash

echo "🔄 测试任务状态更新"
echo "=================="

# 获取token
LOGIN_RESP=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"12345678"}' \
  http://localhost:3001/api/auth/login)

if [[ $LOGIN_RESP == *"token"* ]]; then
  TOKEN=$(echo $LOGIN_RESP | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
  echo "✅ 登录成功"
  
  # 获取任务列表
  echo "📋 获取任务列表..."
  TASKS_RESP=$(curl -s -H "Authorization: Bearer $TOKEN" \
    http://localhost:3001/api/tasks)
  
  # 提取第一个任务的ID
  TASK_ID=$(echo $TASKS_RESP | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
  echo "🎯 测试任务ID: $TASK_ID"
  
  if [[ -n "$TASK_ID" ]]; then
    echo ""
    echo "🧪 测试1: 包含所有字段的更新（模拟前端发送的数据）"
    UPDATE_RESP1=$(curl -s -X PUT -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d '{
        "id": '$TASK_ID',
        "title": "测试任务",
        "description": "测试描述",
        "status": "in_progress",
        "priority": "high",
        "due_date": null,
        "created_at": "2025-07-10 15:28:01",
        "updated_at": "2025-07-10 15:28:01"
      }' \
      http://localhost:3001/api/tasks/$TASK_ID)
    
    echo "响应1: $UPDATE_RESP1"
    
    echo ""
    echo "🧪 测试2: 只包含必要字段的更新"
    UPDATE_RESP2=$(curl -s -X PUT -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d '{
        "status": "completed"
      }' \
      http://localhost:3001/api/tasks/$TASK_ID)
    
    echo "响应2: $UPDATE_RESP2"
    
  else
    echo "❌ 未找到可测试的任务"
  fi
  
else
  echo "❌ 登录失败: $LOGIN_RESP"
fi