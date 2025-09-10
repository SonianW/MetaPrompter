from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from typing import Optional

# Create your models here.


class Prompt(models.Model):
    """
    Prompt 模型，用于存储用户创建和优化的提示词

    属性:
        id: 主键
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

    # 基本信息
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    title: models.CharField = models.CharField(
        max_length=200, blank=False, null=False, verbose_name="标题"
    )
    content: models.TextField = models.TextField(
        blank=False, null=False, verbose_name="内容"
    )
    description: models.TextField = models.TextField(
        blank=True, null=True, verbose_name="描述"
    )

    # 分类和标签
    category: models.CharField = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="分类"
    )
    tags: models.CharField = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="标签"
    )

    # 关联信息
    user: Optional[models.ForeignKey] = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="用户"
    )

    # 统计信息
    usage_count: models.IntegerField = models.IntegerField(
        default=0, verbose_name="使用次数"
    )
    average_score: models.FloatField = models.FloatField(
        default=0.0, verbose_name="平均评分"
    )

    # 元数据
    created_at: models.DateTimeField = models.DateTimeField(
        default=timezone.now, verbose_name="创建时间"
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True, verbose_name="更新时间"
    )
    is_public: models.BooleanField = models.BooleanField(
        default=False, verbose_name="是否公开"
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "提示词"
        verbose_name_plural = "提示词管理"


class PromptHistory(models.Model):
    """
    Prompt 历史记录模型，用于存储用户对提示词的使用和修改历史

    属性:
        id: 主键
        prompt: 关联的提示词
        content: 历史内容
        operation_type: 操作类型（创建、更新、使用、优化、生成、评估）
        user: 操作的用户
        created_at: 创建时间
    """

    # 基本信息
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    prompt: models.ForeignKey = models.ForeignKey(
        "Prompt", on_delete=models.CASCADE, verbose_name="关联提示词"
    )
    content: models.TextField = models.TextField(
        blank=False, null=False, verbose_name="历史内容"
    )

    # 操作信息
    operation_type: models.CharField = models.CharField(
        max_length=50,
        choices=[
            ("create", "创建"),
            ("update", "更新"),
            ("use", "使用"),
            ("optimize", "优化"),
            ("generate", "生成"),
            ("evaluate", "评估"),
        ],
        verbose_name="操作类型",
    )

    # 关联信息
    user: Optional[models.ForeignKey] = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="用户"
    )

    # 元数据
    created_at: models.DateTimeField = models.DateTimeField(
        default=timezone.now, verbose_name="创建时间"
    )

    def __str__(self) -> str:
        return (
            f"{self.prompt.title} - {self.operation_type} - "
            f"{self.created_at}"
        )

    class Meta:
        verbose_name = "提示词历史"
        verbose_name_plural = "提示词历史记录"


class PromptStatistics(models.Model):
    """
    Prompt 统计数据模型，用于存储提示词的统计信息

    属性:
        id: 主键
        prompt: 关联的提示词（一对一关系）
        total_usage: 总使用次数
        daily_usage: 当日使用次数
        weekly_usage: 本周使用次数
        monthly_usage: 本月使用次数
        total_score: 总评分
        score_count: 评分次数
        optimization_count: 优化次数
        average_optimization_improvement: 平均优化提升率
        generation_count: 生成次数
        updated_at: 更新时间
    """

    # 基本信息
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    prompt: models.OneToOneField = models.OneToOneField(
        "Prompt", on_delete=models.CASCADE, verbose_name="关联提示词"
    )

    # 使用统计
    total_usage: models.IntegerField = models.IntegerField(
        default=0, verbose_name="总使用次数"
    )
    daily_usage: models.IntegerField = models.IntegerField(
        default=0, verbose_name="当日使用次数"
    )
    weekly_usage: models.IntegerField = models.IntegerField(
        default=0, verbose_name="本周使用次数"
    )
    monthly_usage: models.IntegerField = models.IntegerField(
        default=0, verbose_name="本月使用次数"
    )

    # 评分统计
    total_score: models.FloatField = models.FloatField(
        default=0.0, verbose_name="总评分"
    )
    score_count: models.IntegerField = models.IntegerField(
        default=0, verbose_name="评分次数"
    )

    # 优化统计
    optimization_count: models.IntegerField = models.IntegerField(
        default=0, verbose_name="优化次数"
    )
    average_optimization_improvement: models.FloatField = models.FloatField(
        default=0.0, verbose_name="平均优化提升率"
    )

    # 生成统计
    generation_count: models.IntegerField = models.IntegerField(
        default=0, verbose_name="生成次数"
    )

    # 更新时间
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True, verbose_name="更新时间"
    )

    def __str__(self) -> str:
        return f"{self.prompt.title} - 统计信息"

    class Meta:
        verbose_name = "提示词统计"
        verbose_name_plural = "提示词统计数据"
