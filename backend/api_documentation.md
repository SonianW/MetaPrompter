# MetaPrompter API 文档

本文档提供了 MetaPrompter 项目所有 API 端点的详细说明和调用示例。

## 基础 URL
所有 API 端点的基础 URL 为：`http://localhost:8000/api/`

## 目录

- [Prompt 管理 API](#prompt-管理-api)
  - [创建提示词](#创建提示词)
  - [获取提示词列表](#获取提示词列表)
  - [获取单个提示词](#获取单个提示词)
  - [更新提示词](#更新提示词)
  - [删除提示词](#删除提示词)
  - [使用提示词](#使用提示词)
- [AI 增强功能 API](#ai-增强功能-api)
  - [生成提示词](#生成提示词-1)
  - [评估提示词质量](#评估提示词质量)
  - [优化提示词](#优化提示词)
- [历史记录与统计 API](#历史记录与统计-api)
  - [查看历史记录](#查看历史记录)
  - [查看统计信息](#查看统计信息)
  - [公开提示词列表](#公开提示词列表)

## Prompt 管理 API

### 创建提示词

**请求**:
- 方法: POST
- 端点: `/api/prompts/`
- 认证: 可选
- 请求体:
  ```json
  {
    "name": "提示词名称",
    "description": "提示词描述",
    "content": "提示词内容"
  }
  ```

**响应**:
- 状态码: 201 Created
- 响应体:
  ```json
  {
    "id": 1,
    "name": "提示词名称",
    "description": "提示词描述",
    "content": "提示词内容",
    "created_at": "2025-09-10T13:45:00Z",
    "updated_at": "2025-09-10T13:45:00Z",
    "created_by": null
  }
  ```

### 获取提示词列表

**请求**:
- 方法: GET
- 端点: `/api/prompts/`
- 认证: 可选

**响应**:
- 状态码: 200 OK
- 响应体:
  ```json
  [
    {
      "id": 1,
      "name": "提示词名称",
      "description": "提示词描述",
      "content": "提示词内容",
      "created_at": "2025-09-10T13:45:00Z",
      "updated_at": "2025-09-10T13:45:00Z",
      "created_by": null
    },
    ...
  ]
  ```

### 获取单个提示词

**请求**:
- 方法: GET
- 端点: `/api/prompts/{id}/`
- 认证: 可选

**响应**:
- 状态码: 200 OK
- 响应体:
  ```json
  {
    "id": 1,
    "name": "提示词名称",
    "description": "提示词描述",
    "content": "提示词内容",
    "created_at": "2025-09-10T13:45:00Z",
    "updated_at": "2025-09-10T13:45:00Z",
    "created_by": null
  }
  ```

### 更新提示词

**请求**:
- 方法: PUT/PATCH
- 端点: `/api/prompts/{id}/`
- 认证: 可选
- 请求体 (PUT):
  ```json
  {
    "name": "新的提示词名称",
    "description": "新的提示词描述",
    "content": "新的提示词内容"
  }
  ```

**响应**:
- 状态码: 200 OK
- 响应体:
  ```json
  {
    "id": 1,
    "name": "新的提示词名称",
    "description": "新的提示词描述",
    "content": "新的提示词内容",
    "created_at": "2025-09-10T13:45:00Z",
    "updated_at": "2025-09-10T14:00:00Z",
    "created_by": null
  }
  ```

### 删除提示词

**请求**:
- 方法: DELETE
- 端点: `/api/prompts/{id}/`
- 认证: 可选

**响应**:
- 状态码: 204 No Content

### 使用提示词

**请求**:
- 方法: POST
- 端点: `/api/prompts/{id}/use/`
- 认证: 可选

**响应**:
- 状态码: 200 OK
- 响应体:
  ```json
  {
    "status": "success",
    "message": "Prompt used successfully"
  }
  ```

## AI 增强功能 API

### 生成提示词

**请求**:
- 方法: POST
- 端点: `/api/prompts/generate/`
- 认证: 可选
- 请求体:
  ```json
  {
    "requirement": "请生成一个用于撰写周报的提示词",
    "model": "gpt-4o-mini",  // 可选参数
    "name": "周报提示词",    // 可选参数
    "description": "用于自动生成周报的提示词"  // 可选参数
  }
  ```

**响应**:
- 状态码: 201 Created
- 响应体:
  ```json
  {
    "status": "success",
    "message": "Prompt generated successfully",
    "prompt": {
      "id": 2,
      "name": "周报提示词",
      "description": "用于自动生成周报的提示词",
      "content": "你是一个周报撰写助手。请根据以下要点撰写一份专业、简洁的周报：\n1. 本周完成的主要工作和成果\n2. 遇到的问题和解决方案\n3. 下周计划和目标\n请确保内容真实、客观，语言流畅自然。",
      "created_at": "2025-09-10T14:15:00Z",
      "updated_at": "2025-09-10T14:15:00Z",
      "created_by": null
    }
  }
  ```

### 评估提示词质量

**请求**:
- 方法: POST
- 端点: `/api/prompts/{id}/evaluate/`
- 认证: 可选
- 请求体:
  ```json
  {
    "detailed": true,  // 是否提供详细分析，默认为true
    "model": "gpt-4o-mini"  // 可选参数
  }
  ```

**响应**:
- 状态码: 200 OK
- 响应体:
  ```json
  {
    "status": "success",
    "message": "Prompt evaluated successfully",
    "evaluation_result": "这是一份关于提示词质量的详细评估报告..."
  }
  ```

### 优化提示词

**请求**:
- 方法: POST
- 端点: `/api/prompts/{id}/optimize/`
- 认证: 可选
- 请求体:
  ```json
  {
    "model": "gpt-4o-mini"  // 可选参数
  }
  ```

**响应**:
- 状态码: 200 OK
- 响应体:
  ```json
  {
    "id": 1,
    "name": "提示词名称",
    "description": "提示词描述",
    "content": "优化后的提示词内容",
    "created_at": "2025-09-10T13:45:00Z",
    "updated_at": "2025-09-10T14:30:00Z",
    "created_by": null
  }
  ```

## 历史记录与统计 API

### 查看历史记录

**请求**:
- 方法: GET
- 端点: `/api/histories/`
- 认证: 可选

**响应**:
- 状态码: 200 OK
- 响应体:
  ```json
  [
    {
      "id": 1,
      "prompt": 1,
      "content": "提示词内容",
      "operation_type": "create",
      "created_at": "2025-09-10T13:45:00Z",
      "user": null
    },
    ...
  ]
  ```

### 查看统计信息

**请求**:
- 方法: GET
- 端点: `/api/statistics/`
- 认证: 可选

**响应**:
- 状态码: 200 OK
- 响应体:
  ```json
  [
    {
      "id": 1,
      "prompt": 1,
      "total_usage": 5,
      "daily_usage": 2,
      "weekly_usage": 5,
      "monthly_usage": 5,
      "optimization_count": 1,
      "average_optimization_improvement": 0.1,
      "generation_count": 0
    },
    ...
  ]
  ```

### 公开提示词列表

**请求**:
- 方法: GET
- 端点: `/api/public-prompts/`
- 认证: 可选

**响应**:
- 状态码: 200 OK
- 响应体:
  ```json
  [
    {
      "id": 3,
      "name": "公开提示词名称",
      "description": "公开提示词描述",
      "content": "公开提示词内容",
      "created_at": "2025-09-10T14:45:00Z",
      "updated_at": "2025-09-10T14:45:00Z",
      "created_by": null
    },
    ...
  ]
  ```

## Python 调用示例

下面是使用 Python 的 `requests` 库调用 API 的示例代码：

```python
import requests
import json

# 基础 URL
base_url = "http://localhost:8000/api"

# 1. 生成提示词
def generate_prompt():
    url = f"{base_url}/prompts/generate/"
    data = {
        "requirement": "请生成一个用于撰写周报的提示词",
        "model": "gpt-4o-mini",
        "name": "周报提示词",
        "description": "用于自动生成周报的提示词"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 201:
        result = response.json()
        print(f"生成成功! 提示词ID: {result['prompt']['id']}")
        print(f"提示词内容: {result['prompt']['content']}")
        return result['prompt']['id']
    else:
        print(f"生成失败: {response.status_code}")
        print(response.text)
        return None

# 2. 评估提示词质量
def evaluate_prompt(prompt_id):
    url = f"{base_url}/prompts/{prompt_id}/evaluate/"
    data = {
        "detailed": True,
        "model": "gpt-4o-mini"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"评估结果: {result['evaluation_result']}")
    else:
        print(f"评估失败: {response.status_code}")
        print(response.text)

# 3. 优化提示词
def optimize_prompt(prompt_id):
    url = f"{base_url}/prompts/{prompt_id}/optimize/"
    data = {
        "model": "gpt-4o-mini"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"优化成功!")
        print(f"优化后内容: {result['content']}")
    else:
        print(f"优化失败: {response.status_code}")
        print(response.text)

# 4. 获取提示词列表
def get_prompt_list():
    url = f"{base_url}/prompts/"
    response = requests.get(url)
    
    if response.status_code == 200:
        prompts = response.json()
        print(f"共找到 {len(prompts)} 个提示词")
        for prompt in prompts:
            print(f"{prompt['id']}. {prompt['name']}")
    else:
        print(f"获取列表失败: {response.status_code}")
        print(response.text)

# 5. 获取单个提示词详情
def get_prompt_detail(prompt_id):
    url = f"{base_url}/prompts/{prompt_id}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        prompt = response.json()
        print(f"提示词详情:")
        print(f"ID: {prompt['id']}")
        print(f"名称: {prompt['name']}")
        print(f"描述: {prompt['description']}")
        print(f"内容: {prompt['content']}")
        print(f"创建时间: {prompt['created_at']}")
    else:
        print(f"获取详情失败: {response.status_code}")
        print(response.text)

# 示例使用流程
if __name__ == "__main__":
    print("1. 获取提示词列表")
    get_prompt_list()
    
    print("\n2. 生成新提示词")
    new_prompt_id = generate_prompt()
    
    if new_prompt_id:
        print(f"\n3. 查看新生成的提示词详情 (ID: {new_prompt_id})")
        get_prompt_detail(new_prompt_id)
        
        print(f"\n4. 评估提示词质量 (ID: {new_prompt_id})")
        evaluate_prompt(new_prompt_id)
        
        print(f"\n5. 优化提示词 (ID: {new_prompt_id})")
        optimize_prompt(new_prompt_id)
        
        print(f"\n6. 再次查看优化后的提示词详情 (ID: {new_prompt_id})")
        get_prompt_detail(new_prompt_id)
```

## 错误处理

API 可能返回以下常见错误状态码：

- 400 Bad Request: 请求参数错误或不完整
- 401 Unauthorized: 需要认证但未提供
- 403 Forbidden: 没有权限执行请求的操作
- 404 Not Found: 请求的资源不存在
- 500 Internal Server Error: 服务器内部错误

所有错误响应都包含一个描述性的错误消息，可以帮助排查问题。