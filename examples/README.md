# MetaPrompter 示例代码

这个目录包含了 MetaPrompter 项目的示例代码，用于演示如何使用 MetaPrompter 的 API 接口。

## 目录结构

```
examples/
├── README.md          # 本说明文件
└── example_usage.py   # API 调用示例代码
```

## 示例代码说明

### example_usage.py

这是一个完整的 Python 脚本，演示了如何使用 `requests` 库调用 MetaPrompter 的所有主要 API 端点。

**主要功能**：
- 使用面向对象的方式封装了所有 API 调用功能
- 包含详细的错误处理机制
- 提供了完整的使用流程示例，从创建提示词到优化、评估和查看统计信息
- 包含丰富的注释，便于理解和使用

## 如何运行示例代码

1. 确保 MetaPrompter 后端服务器正在运行：
   ```bash
   cd /path/to/MetaPrompter/backend
   python manage.py runserver
   ```

2. 安装必要的依赖：
   ```bash
   pip install requests
   ```

3. 运行示例代码：
   ```bash
   cd /path/to/MetaPrompter/examples
   python example_usage.py
   ```

   或者添加执行权限后直接运行：
   ```bash
   chmod +x example_usage.py
   ./example_usage.py
   ```

## 自定义示例

您可以根据自己的需求修改 `example_usage.py` 文件，添加或调整 API 调用功能。示例代码中包含了所有 MetaPrompter API 的封装方法，您可以直接使用这些方法来构建自己的应用程序。

## 注意事项

- 示例代码默认连接到本地开发服务器 (`http://localhost:8000/api`)，如果您的服务器运行在其他地址或端口，请修改代码中的 `base_url` 参数。
- 示例代码会创建和删除测试数据，请确保您了解代码的执行逻辑，避免意外删除重要数据。
- 如果您遇到 API 调用错误，请检查服务器是否正常运行，并查看错误消息以获取详细信息。