# MetaPrompter 后端项目

MetaPrompter 是一个帮助用户生成与优化 LLM prompt 的工具的后端项目。

## 项目结构

```
backend/
├── metaprompter/         # Django 项目配置目录
│   ├── settings.py       # 项目设置
│   ├── urls.py           # 主 URL 配置
│   └── ...               # 其他配置文件
├── prompt/               # Prompt 管理应用
│   ├── models.py         # 数据模型
│   ├── serializers.py    # 序列化器
│   ├── views.py          # 视图函数
│   └── ...               # 其他应用文件
├── llm/                  # LLM 框架集成应用
│   ├── config.py         # LLM 配置
│   ├── services.py       # LLM 服务实现
│   ├── views.py          # LLM 相关视图
│   └── ...               # 其他应用文件
├── pyproject.toml        # 项目依赖配置
└── manage.py             # Django 管理脚本
```

## 技术栈

- Python 3.10+
- Django 5.2.6
- Django REST Framework 3.15.2
- LangChain 0.2.16
- OpenAI Python SDK 1.40.6
- python-dotenv 1.0.1

## 环境变量配置

在项目根目录创建 `.env` 文件，添加以下配置：

```
# Django 配置
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置
DATABASE_ENGINE=django.db.backends.sqlite3  # 或使用 MySQL: django.db.backends.mysql
DATABASE_NAME=db.sqlite3  # 或 MySQL 数据库名
DATABASE_USER=  # MySQL 用户名
DATABASE_PASSWORD=  # MySQL 密码
DATABASE_HOST=  # MySQL 主机
DATABASE_PORT=  # MySQL 端口

# LLM 配置
OPENAI_API_KEY=your_openai_api_key  # OpenAI API 密钥
OPENAI_API_BASE=https://api.openai.com/v1  # OpenAI API 基础 URL
DEFAULT_LLM_MODEL=gpt-4o-mini  # 默认 LLM 模型
```

## 安装依赖

使用 uv 或 pip 安装项目依赖：

```bash
# 使用 uv
uv pip install -e .

# 或使用 pip
pip install -e .
```

## 数据库迁移

```bash
python manage.py migrate
```

## 运行开发服务器

```bash
python manage.py runserver
```

服务器将在 http://127.0.0.1:8000/ 启动。

## API 端点

### Prompt 管理 API

- `GET /api/prompts/` - 获取所有提示词
- `POST /api/prompts/` - 创建新的提示词
- `GET /api/prompts/<id>/` - 获取单个提示词
- `PUT /api/prompts/<id>/` - 更新提示词
- `DELETE /api/prompts/<id>/` - 删除提示词

### LLM 服务 API

- `GET /api/llm/test/` - 测试 LLM 服务是否正常工作
- `POST /api/llm/generate/` - 根据需求生成提示词
- `POST /api/llm/generate/template/<template_name>/` - 使用指定模板生成提示词
- `POST /api/llm/optimize/` - 优化提示词
- `POST /api/llm/evaluate/` - 评估提示词质量
- `POST /api/llm/compare/` - 比较两个提示词
- `POST /api/llm/analyze/` - 分析提示词质量

## LLM 服务使用指南

### 提示词生成

发送 POST 请求到 `/api/llm/generate/`，请求体包含：

```json
{
  "requirement": "需求描述",
  "model": "可选，指定使用的模型"
}
```

### 提示词优化

发送 POST 请求到 `/api/llm/optimize/`，请求体包含：

```json
{
  "prompt": "需要优化的提示词",
  "model": "可选，指定使用的模型"
}
```

### 提示词评估

发送 POST 请求到 `/api/llm/evaluate/`，请求体包含：

```json
{
  "prompt": "需要评估的提示词",
  "model": "可选，指定使用的模型"
}
```

### 提示词比较

发送 POST 请求到 `/api/llm/compare/`，请求体包含：

```json
{
  "original_prompt": "原始提示词",
  "optimized_prompt": "优化后的提示词",
  "task_description": "任务描述",
  "model": "可选，指定使用的模型"
}
```

### 提示词质量分析

发送 POST 请求到 `/api/llm/analyze/`，请求体包含：

```json
{
  "prompt": "需要分析的提示词",
  "detailed": true,  # 是否需要详细分析
  "model": "可选，指定使用的模型"
}
```

## 测试

运行项目测试：

```bash
python manage.py test
```

## 注意事项

1. 在生产环境中，务必设置 `DEBUG=False` 并配置适当的 `ALLOWED_HOSTS`。
2. 确保保护好你的 API 密钥和敏感配置信息。
3. 在没有 OpenAI API 密钥的情况下，LLM 服务将无法正常工作，但基本的 API 框架仍然可以使用。
4. 可以根据实际需求修改 `DEFAULT_LLM_MODEL` 配置，选择适合的 LLM 模型。