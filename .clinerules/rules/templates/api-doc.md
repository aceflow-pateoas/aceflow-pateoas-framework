# API文档模板

# [接口业务名称] - [HTTP Method] [Endpoint Short URL]

> **版本:** 1.0.0
> **维护者:** @AI assistant
> **最后更新:** 2025-06-28

## 1. 功能描述

(清晰地描述此API的业务目的和核心功能。例如：用于创建新用户，并将其基本信息存入数据库。)

## 2. 接口定义

- **Method:** `POST`
- **URL:** `/api/v1/users`
- **Content-Type:** `application/json`

## 3. 认证与授权

- **认证方式:** Bearer Token
- **所需权限:** `user:create` (或说明需要什么角色)

## 4. 请求参数

### 路径参数 (Path Parameters)

| 参数名 | 类型 | 描述 | 示例 |
| :--- | :--- | :--- | :--- |
| `tenantId` | `string` | 租户的唯一标识符 | `t_12345` |

### 请求体 (Request Body)

```json
{
  "username": "string",
  "email": "string",
  "age": "integer",
  "tags": ["string"]
}
```

**字段详细说明:**

| 字段名 | 类型 | 必填 | 描述与约束 |
| :--- | :--- | :--- | :--- |
| `username` | `string` | 是 | 用户名，必须是3-20个字符的字母数字组合。 |
| `email` | `string` | 是 | 用户的电子邮箱，必须符合RFC 5322标准。 |
| `age` | `integer`| 否 | 用户年龄，范围必须在18-99之间。 |
| `tags` | `array` | 否 | 用户标签，数组内每个元素为字符串。 |

## 5. 响应格式

### 成功响应 (Code 201 Created)

```json
{
  "code": 0,
  "message": "User created successfully",
  "data": {
    "userId": "u_a1b2c3d4",
    "username": "newuser",
    "createdAt": "2025-06-28T12:00:00Z"
  }
}
```

### 失败响应 (示例)

请参考全局错误码定义。

## 6. 全局错误码

| HTTP状态 | 业务错误码 | 说明 | 处理建议 |
| :--- | :--- | :--- | :--- |
| `400` | `40001` | 参数校验失败 | 检查请求体参数是否符合约束。 |
| `401` | `40101` | Token无效或过期 | 用户需要重新登录获取Token。 |
| `403` | `40301` | 权限不足 | 确认当前用户角色是否拥有操作权限。 |
| `409` | `40901` | 用户名或邮箱已存在 | 提示用户更换用户名或邮箱。 |
| `500` | `50001` | 服务器内部错误 | 请联系技术支持并提供Trace ID。 |

## 7. 请求示例 (JavaScript)

```javascript
async function createUser(userData) {
  const response = await fetch('/api/v1/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_AUTH_TOKEN'
    },
    body: JSON.stringify(userData)
  });
  
  if (!response.ok) {
    // 处理错误情况
    const errorData = await response.json();
    console.error('API Error:', errorData);
    throw new Error(errorData.message);
  }

  return await response.json();
}

// 使用示例
const newUser = {
  username: "newuser",
  email: "newuser@example.com",
  age: 30
};

try {
  const result = await createUser(newUser);
  console.log('User created:', result.data);
} catch (error) {
  // ...
}
```

## 8. 变更历史

| 版本 | 变更日期 | 变更内容 | 作者 |
| :--- | :--- | :--- | :--- |
| 1.0.0 | 2025-06-28 | 初始版本创建。 | @AI assistant |