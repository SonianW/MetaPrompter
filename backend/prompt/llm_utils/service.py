"""
LLM 服务模块
实现与 LLM 相关的核心功能服务
"""

from typing import Optional, Any
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from loguru import logger

from .config import llm_config
from .template_manager import prompt_template_manager


class PromptGenerationService:
    """
    提示词生成服务
    负责根据用户需求生成高质量的提示词
    """

    @staticmethod
    def generate_prompt(requirement: str, model: Optional[str] = None) -> str:
        """
        根据用户需求生成提示词

        参数:
            requirement: 用户需求描述
            model: 可选，指定使用的 LLM 模型

        返回:
            生成的提示词内容
        """
        try:
            # 如果指定了模型，则创建临时客户端
            client: Optional[ChatOpenAI] = None
            if model:
                temp_config = llm_config.__class__()
                temp_config.update_config(model=model)
                client = temp_config.get_chat_client()
            else:
                client = llm_config.get_chat_client()

            # 如果客户端未初始化成功，返回错误信息
            if not client:
                return "LLM 服务初始化失败，请检查配置"

            # 获取提示词生成模板
            template = prompt_template_manager.get_template("prompt_generation")

            # 创建链
            chain = template | client | StrOutputParser()

            # 运行链并返回结果
            result = chain.invoke({"requirement": requirement})
            return result
        except Exception as e:
            logger.error(f"生成提示词失败: {str(e)}")
            return f"生成提示词失败: {str(e)}"

    @staticmethod
    def generate_prompt_from_template(template_name: str, **kwargs: Any) -> str:
        """
        使用指定的模板生成提示词

        参数:
            template_name: 模板名称
            **kwargs: 模板参数

        返回:
            生成的提示词内容
        """
        try:
            # 获取指定的模板
            template = prompt_template_manager.get_template(template_name)

            if not template:
                return f"未找到模板: {template_name}"

            # 获取客户端
            client = llm_config.get_chat_client()

            if not client:
                return "LLM 服务初始化失败，请检查配置"

            # 创建链
            chain = template | client | StrOutputParser()

            # 运行链并返回结果
            result = chain.invoke(kwargs)
            return result
        except Exception as e:
            logger.error(f"使用模板生成提示词失败: {str(e)}")
            return f"使用模板生成提示词失败: {str(e)}"


class PromptOptimizationService:
    """
    提示词优化服务
    负责优化现有提示词，提升其质量
    """

    @staticmethod
    def optimize_prompt(prompt: str, model: Optional[str] = None) -> str:
        """
        优化给定的提示词

        参数:
            prompt: 需要优化的提示词
            model: 可选，指定使用的 LLM 模型

        返回:
            优化后的提示词内容
        """
        try:
            # 如果指定了模型，则创建临时客户端
            client: Optional[ChatOpenAI] = None
            if model:
                temp_config = llm_config.__class__()
                temp_config.update_config(model=model)
                client = temp_config.get_chat_client()
            else:
                client = llm_config.get_chat_client()

            # 如果客户端未初始化成功，返回错误信息
            if not client:
                return "LLM 服务初始化失败，请检查配置"

            # 获取提示词优化模板
            template = prompt_template_manager.get_template("prompt_optimization")

            # 创建链
            chain = template | client | StrOutputParser()

            # 渲染模板以获取实际的消息历史
            messages = template.format_messages(prompt=prompt)
            logger.debug("\n=== 调用模型时的实际消息历史 ===\n")
            for i, message in enumerate(messages):
                logger.debug(f"[{i+1}][{message.type}] {message.content}")
            logger.debug("============================\n")

            # 运行链并返回结果
            result = chain.invoke({"prompt": prompt})

            # 基本的后处理逻辑：由于模板已优化，此处仅保留必要的清理
            # 1. 移除多余空格
            result = result.strip()

            # 2. 如果结果过长，截取前500字符
            if len(result) > 500:
                return result[:500].strip()

            # 3. 简单检查结果是否合理
            if not result or result == "None" or result.lower() == "null":
                return prompt  # 如果结果不合理，返回原始提示词

            return result
        except Exception as e:
            logger.error(f"优化提示词失败: {str(e)}")
            return f"优化提示词失败: {str(e)}"

    @staticmethod
    def evaluate_prompt(prompt: str, model: Optional[str] = None) -> str:
        """
        评估给定的提示词质量

        参数:
            prompt: 需要评估的提示词
            model: 可选，指定使用的 LLM 模型

        返回:
            评估结果和分数
        """
        try:
            # 如果指定了模型，则创建临时客户端
            client: Optional[ChatOpenAI] = None
            if model:
                temp_config = llm_config.__class__()
                temp_config.update_config(model=model)
                client = temp_config.get_chat_client()
            else:
                client = llm_config.get_chat_client()

            # 如果客户端未初始化成功，返回错误信息
            if not client:
                return "LLM 服务初始化失败，请检查配置"

            # 获取提示词评估模板
            template = prompt_template_manager.get_template("prompt_evaluation")

            # 创建链
            chain = template | client | StrOutputParser()

            # 运行链并返回结果
            result = chain.invoke({"prompt": prompt})
            return result
        except Exception as e:
            logger.error(f"评估提示词失败: {str(e)}")
            return f"评估提示词失败: {str(e)}"


class LLMEvaluationService:
    """
    LLM 评估服务
    负责评估提示词的效果和质量
    """

    @staticmethod
    def compare_prompts(
        original_prompt: str,
        optimized_prompt: str,
        task_description: str,
        model: Optional[str] = None,
    ) -> str:
        """
        比较两个提示词在特定任务上的效果

        参数:
            original_prompt: 原始提示词
            optimized_prompt: 优化后的提示词
            task_description: 任务描述
            model: 可选，指定使用的 LLM 模型

        返回:
            比较结果
        """
        try:
            # 如果指定了模型，则创建临时客户端
            client: Optional[ChatOpenAI] = None
            if model:
                temp_config = llm_config.__class__()
                temp_config.update_config(model=model)
                client = temp_config.get_chat_client()
            else:
                client = llm_config.get_chat_client()

            # 如果客户端未初始化成功，返回错误信息
            if not client:
                return "LLM 服务初始化失败，请检查配置"

            # 创建比较模板
            compare_template = (
                "你是一个专业的 LLM 提示词评估专家。请比较以下两个提示词在完成特定任务时的效果。\n"
                f"任务描述: {task_description}\n\n"
                f"原始提示词: {original_prompt}\n\n"
                f"优化提示词: {optimized_prompt}\n\n"
                "请从清晰度、具体性、引导性、完整性等方面进行比较，并给出详细分析。"
            )

            # 发送请求
            result = client.invoke(compare_template)
            return result.content
        except Exception as e:
            logger.error(f"比较提示词失败: {str(e)}")
            return f"比较提示词失败: {str(e)}"

    @staticmethod
    def analyze_prompt_quality(
        prompt: str, detailed: bool = True, model: Optional[str] = None
    ) -> str:
        """
        分析提示词的质量，提供详细或简要的分析报告

        参数:
            prompt: 需要分析的提示词
            detailed: 是否提供详细分析
            model: 可选，指定使用的 LLM 模型

        返回:
            分析报告
        """
        try:
            # 如果指定了模型，则创建临时客户端
            client: Optional[ChatOpenAI] = None
            if model:
                temp_config = llm_config.__class__()
                temp_config.update_config(model=model)
                client = temp_config.get_chat_client()
            else:
                client = llm_config.get_chat_client()

            # 如果客户端未初始化成功，返回错误信息
            if not client:
                return "LLM 服务初始化失败，请检查配置"

            # 创建分析模板
            if detailed:
                analysis_template = (
                    "你是一个专业的 LLM 提示词分析专家。请详细分析以下提示词的质量。\n"
                    f"提示词: {prompt}\n\n"
                    "请从以下几个方面进行分析：\n"
                    "1. 清晰度：提示词是否表达清晰，易于理解\n"
                    "2. 具体性：提示词是否足够具体，避免模糊表述\n"
                    "3. 引导性：提示词是否能够有效引导 LLM 产生高质量回复\n"
                    "4. 完整性：提示词是否包含了完成任务所需的所有信息\n"
                    "5. 建议：针对不足之处提出具体的改进建议"
                )
            else:
                analysis_template = (
                    "你是一个专业的 LLM 提示词分析专家。请简要分析以下提示词的质量。\n"
                    f"提示词: {prompt}\n\n"
                    "请给出总体评价和主要建议。"
                )

            # 发送请求
            result = client.invoke(analysis_template)
            return result.content
        except Exception as e:
            logger.error(f"分析提示词质量失败: {str(e)}")
            return f"分析提示词质量失败: {str(e)}"


# 创建服务实例
prompt_generation_service = PromptGenerationService()
prompt_optimization_service = PromptOptimizationService()
llm_evaluation_service = LLMEvaluationService()
