"""
LLM 配置模块
用于配置和初始化 LangChain 和 OpenAI 客户端
"""

from typing import Optional
from langchain_openai import ChatOpenAI
from loguru import logger
from metaprompter import settings


class LLMConfig:
    """
    LLM 配置类，用于统一管理 LLM 相关配置和客户端初始化。

    负责加载 LLM 配置，初始化客户端，并提供配置更新功能。
    """

    def __init__(self) -> None:
        """
        初始化 LLM 配置管理器，加载配置并创建客户端实例。
        """
        # 从 settings.py 加载配置
        self.api_key: str = settings.OPENAI_API_KEY
        self.api_base: str = settings.OPENAI_API_BASE
        self.default_model: str = settings.DEFAULT_LLM_MODEL

        # 初始化 OpenAI 客户端
        self.client: Optional[ChatOpenAI] = self._init_chat_client()

    def _init_chat_client(self) -> Optional[ChatOpenAI]:
        """
        初始化 ChatOpenAI 客户端。

        Returns:
            ChatOpenAI: 初始化成功的客户端实例，如果失败则返回 None
        """
        try:
            return ChatOpenAI(
                api_key=self.api_key,
                base_url=self.api_base,
                model=self.default_model,
                temperature=0.7,  # 设置默认的温度值，控制输出的随机性
                max_tokens=None,  # 默认不限制 tokens 数量
            )
        except Exception as e:
            # 使用 logger 记录错误信息，符合项目规范
            logger.error(f"初始化 OpenAI 客户端失败: {str(e)}")
            return None

    def get_chat_client(self) -> Optional[ChatOpenAI]:
        """
        获取 ChatOpenAI 客户端实例。如果客户端未初始化，则尝试重新初始化。

        Returns:
            ChatOpenAI: 客户端实例，如果初始化失败则返回 None
        """
        if not self.client:
            self.client = self._init_chat_client()
        return self.client

    def update_config(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        """
        更新 LLM 配置并重新初始化客户端。

        Args:
            api_key: 新的 API 密钥
            api_base: 新的 API 基础 URL
            model: 新的默认模型名称
        """
        if api_key:
            self.api_key = api_key
        if api_base:
            self.api_base = api_base
        if model:
            self.default_model = model
        # 重新初始化客户端
        self.client = self._init_chat_client()


# 创建全局 LLM 配置实例
llm_config = LLMConfig()
