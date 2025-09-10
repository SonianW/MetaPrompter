# MetaPrompter

## 项目简介
MetaPrompter 是一个专业的 LLM Prompt 生成与优化工具，旨在帮助用户创建高质量的提示词，提升与大语言模型的交互效果。

## 技术栈
- **前端**：Vue3 + Vite + ElementPlus + TypeScript + Pinia + Vue Router
- **后端**：Django + Django REST Framework + MySQL
- **LLM 应用框架**：LangGraph 或 LangChain
- **依赖管理**：前端使用 npm，后端使用 uv + pyproject.toml

## 核心功能
1. **Prompt 生成**：根据用户需求自动生成高质量的提示词
   - 基于模板的 Prompt 生成
   - 基于需求描述的智能 Prompt 生成
2. **Prompt 优化**：分析现有提示词并提供优化建议
   - 提示词质量评估
   - 智能优化建议
3. **Prompt 管理**：创建、编辑、保存提示词
4. **历史记录**：跟踪和管理使用历史
5. **统计分析**：提供使用数据和效果分析

## 项目架构
前后端分离架构：
- 前端：负责用户交互，提供友好的界面
- 后端：负责业务逻辑和数据处理，集成 LLM 服务
- 通信：通过 RESTful API 进行前后端数据交互

## 开发计划
项目分为四个阶段：
1. **项目初始化与后端架构搭建**（1-3天）
2. **后端核心功能开发**（4-15天），包括 Prompt 管理、LLM 集成、Prompt 生成与优化、历史记录和统计分析
3. **前端开发**（16-25天），包括界面实现、前后端集成和 UI/UX 优化
4. **测试与部署**（26-30天）

## 快速开始
### 环境要求
- Node.js 16+ (前端)
- Python 3.8+ (后端)
- MySQL 8.0+ (数据库)

### 安装指南
1. 克隆项目仓库
   ```bash
   git clone https://github.com/yourusername/MetaPrompter.git
   cd MetaPrompter
   ```

2. 后端安装
   ```bash
   cd backend
   # 使用 uv 安装依赖（推荐）
   uv sync
   # 或者使用 pip
   pip install -r requirements.txt
   ```

3. 前端安装
   ```bash
   cd frontend
   npm install
   ```

## 开发流程
本项目采用 "计划 - 对齐 - 开发" 的工作流程，确保代码质量和项目进度。详细信息请参考项目内的 .plan.md 和 .context.md 文件。

## 贡献指南
欢迎对项目进行贡献！请先阅读项目的开发计划和上下文文档，然后提交 Pull Request。

## 许可证
[MIT License](LICENSE)