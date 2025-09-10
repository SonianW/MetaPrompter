"""
LLM 提示词模板管理模块
用于管理各种 LLM 任务的提示词模板
"""

from typing import Optional, Dict
from langchain_core.prompts import ChatPromptTemplate


class PromptTemplateManager:
    """
    提示词模板管理类，用于管理各种 LLM 任务的提示词模板。

    提供模板的获取、添加和更新功能，支持多种提示词任务类型。
    """

    def __init__(self) -> None:
        """
        初始化提示词模板管理器，加载预定义的提示词模板。
        """
        # 初始化模板字典，存储各种任务类型的提示词模板
        self.templates: Dict[str, ChatPromptTemplate] = {
            # Prompt 生成模板
            "prompt_generation": ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "你是一个专业的 LLM 提示词工程师。根据用户的需求，生成高质量的提示词。\n"
                        "请严格按照以下要求进行生成：\n"
                        "1. 提示词应具体、清晰、引导 LLM 产生高质量回复\n"
                        "2. 避免使用模糊、笼统的语言\n"
                        "3. 提示词应有良好的结构，避免语义上的混淆\n"
                        "4. 提示词可包括示例，以帮助 LLM 理解任务需求\n"
                        "5. 直接返回提示词，不要添加任何额外的说明、标记或格式"
                    ),
                    ("human", "请为以下需求生成一个高质量的提示词：\n{requirement}"),
                ]
            ),
            # Prompt 优化模板
            "prompt_optimization": ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        (
                            "你是一个专业的 LLM 提示词优化专家。请严格按照以下要求优化提示词：\n"
                            "1. 仅返回优化后的提示词文本\n"
                            "2. 不要添加任何额外的说明、标记或格式\n"
                            '3. 不要包含"优化后的提示词"等字样\n'
                            "4. 优化后的提示词应更具体、更清晰、更能引导LLM产生高质量回复"
                        ),
                    ),
                    ("human", "请优化以下提示词：\n{prompt}"),
                ]
            ),
            # Prompt 评估模板
            "prompt_evaluation": ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        (
                            "你是一个专业的 LLM 提示词评估专家。根据提示词的质量标准，"
                            "对提示词进行评估和打分。"
                        ),
                    ),
                    (
                        "human",
                        "请评估以下提示词：\n{prompt}\n\n评估标准：清晰度、具体性、引导性、完整性，满分 10 分。",
                    ),
                ]
            ),
        }

    def get_template(self, template_name: str) -> Optional[ChatPromptTemplate]:
        """
        获取指定名称的提示词模板。

        Args:
            template_name: 模板名称

        Returns:
            ChatPromptTemplate: 对应的模板对象，如果不存在则返回 None
        """
        return self.templates.get(template_name)

    def add_template(
        self, template_name: str, template: ChatPromptTemplate
    ) -> None:
        """
        添加新的提示词模板。

        Args:
            template_name: 模板名称
            template: 要添加的模板对象
        """
        self.templates[template_name] = template

    def update_template(
        self, template_name: str, template: ChatPromptTemplate
    ) -> None:
        """
        更新现有的提示词模板。

        Args:
            template_name: 要更新的模板名称
            template: 新的模板对象
        """
        if template_name in self.templates:
            self.templates[template_name] = template


# 创建全局提示词模板管理器实例
prompt_template_manager = PromptTemplateManager()
