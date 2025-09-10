from rest_framework import serializers
from rest_framework.fields import Field
from typing import Dict, Any, Type, List

from .models import Prompt, PromptHistory, PromptStatistics


class PromptSerializer(serializers.ModelSerializer):
    """
    Prompt 模型的完整序列化器，用于提示词的展示和操作

    字段说明:
        id: 提示词唯一标识符
        title: 提示词标题
        content: 提示词内容
        description: 提示词描述
        category: 分类
        tags: 标签，多个标签用逗号分隔
        user: 创建提示词的用户
        usage_count: 使用次数
        average_score: 平均评分
        created_at: 创建时间
        updated_at: 更新时间
        is_public: 是否公开
    """

    class Meta:
        model: Type[Prompt] = Prompt
        fields: List[str] = [
            "id",
            "title",
            "content",
            "description",
            "category",
            "tags",
            "user",
            "usage_count",
            "average_score",
            "created_at",
            "updated_at",
            "is_public",
        ]
        read_only_fields: List[str] = ["id", "created_at", "updated_at"]

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证序列化器数据

        参数:
            data: 待验证的数据

        返回:
            验证后的数据
        """
        # 确保提示词标题和内容不为空
        if "title" in data and not data["title"].strip():
            raise serializers.ValidationError({"title": "提示词标题不能为空"})
        if "content" in data and not data["content"].strip():
            raise serializers.ValidationError({"content": "提示词内容不能为空"})
        return data


class PromptHistorySerializer(serializers.ModelSerializer):
    """
    PromptHistory 模型的序列化器，用于提示词历史记录的展示

    字段说明:
        id: 历史记录唯一标识符
        prompt: 关联的提示词
        content: 历史内容
        operation_type: 操作类型
        user: 操作的用户
        created_at: 创建时间
    """

    prompt: Field = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model: Type[PromptHistory] = PromptHistory
        fields: List[str] = [
            "id",
            "prompt",
            "content",
            "operation_type",
            "user",
            "created_at",
        ]
        read_only_fields: List[str] = ["id", "created_at"]


class PromptStatisticsSerializer(serializers.ModelSerializer):
    """
    PromptStatistics 模型的序列化器，用于提示词统计信息的展示

    字段说明:
        id: 统计信息唯一标识符
        prompt: 关联的提示词
        total_usage: 总使用次数
        daily_usage: 当日使用次数
        weekly_usage: 本周使用次数
        monthly_usage: 本月使用次数
        total_score: 总评分
        score_count: 评分次数
        optimization_count: 优化次数
        average_optimization_improvement: 平均优化提升率
        updated_at: 更新时间
    """

    prompt: Field = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model: Type[PromptStatistics] = PromptStatistics
        fields: List[str] = [
            "id",
            "prompt",
            "total_usage",
            "daily_usage",
            "weekly_usage",
            "monthly_usage",
            "total_score",
            "score_count",
            "optimization_count",
            "average_optimization_improvement",
            "updated_at",
        ]
        read_only_fields: List[str] = ["id", "updated_at"]


class PromptCreateSerializer(serializers.ModelSerializer):
    """
    用于创建 Prompt 的序列化器，专注于创建所需的字段

    字段说明:
        id: 提示词唯一标识符（只读）
        title: 提示词标题
        content: 提示词内容
        description: 提示词描述
        category: 分类
        tags: 标签
        is_public: 是否公开
    """

    class Meta:
        model: Type[Prompt] = Prompt
        fields: List[str] = [
            "id",
            "title",
            "content",
            "description",
            "category",
            "tags",
            "is_public",
        ]
        read_only_fields: List[str] = ["id"]

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证创建提示词的数据

        参数:
            data: 待验证的数据

        返回:
            验证后的数据
        """
        # 确保标题和内容不为空
        if not data.get("title", "").strip():
            raise serializers.ValidationError({"title": "提示词标题不能为空"})
        if not data.get("content", "").strip():
            raise serializers.ValidationError({"content": "提示词内容不能为空"})
        return data


class PromptUpdateSerializer(serializers.ModelSerializer):
    """
    用于更新 Prompt 的序列化器，专注于可更新的字段

    字段说明:
        title: 提示词标题
        content: 提示词内容
        description: 提示词描述
        category: 分类
        tags: 标签
        is_public: 是否公开
    """

    class Meta:
        model: Type[Prompt] = Prompt
        fields: List[str] = [
            "title",
            "content",
            "description",
            "category",
            "tags",
            "is_public",
        ]

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证更新提示词的数据

        参数:
            data: 待验证的数据

        返回:
            验证后的数据
        """
        # 确保如果提供了标题或内容，它们不为空
        if "title" in data and not data["title"].strip():
            raise serializers.ValidationError({"title": "提示词标题不能为空"})
        if "content" in data and not data["content"].strip():
            raise serializers.ValidationError({"content": "提示词内容不能为空"})
        return data
