from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.db.models import QuerySet
from django.utils import timezone
from datetime import timedelta
from typing import Optional

from .models import Prompt, PromptHistory, PromptStatistics
from .serializers import (
    PromptSerializer,
    PromptHistorySerializer,
    PromptStatisticsSerializer,
    PromptCreateSerializer,
    PromptUpdateSerializer,
)


# Create your views here.


class PromptViewSet(viewsets.ModelViewSet):
    """
    Prompt 模型的视图集，提供完整的 CRUD 操作和提示词使用、生成、评估、优化功能

    操作：
        - list: 获取提示词列表
        - retrieve: 获取单个提示词
        - create: 创建新的提示词
        - update: 更新提示词
        - partial_update: 部分更新提示词
        - destroy: 删除提示词
        - use: 标记提示词被使用并更新使用统计
        - generate: 根据用户需求生成新的提示词
        - evaluate: 评估提示词质量
        - optimize: 优化提示词内容
    """

    queryset: QuerySet[Prompt] = Prompt.objects.all()
    permission_classes = [permissions.AllowAny]  # 简化起见，允许所有用户访问

    def get_serializer_class(self) -> type[Serializer]:
        """
        根据请求方法选择合适的序列化器

        返回:
            序列化器类
        """
        if self.action == "create":
            return PromptCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return PromptUpdateSerializer
        return PromptSerializer

    def perform_create(self, serializer: Serializer) -> Prompt:
        """
        创建新的提示词时，自动记录历史

        参数:
            serializer: 序列化器实例

        返回:
            创建的提示词实例
        """
        prompt = serializer.save()
        # 创建历史记录
        PromptHistory.objects.create(
            prompt=prompt,
            content=prompt.content,
            operation_type="create",
            user=(self.request.user if self.request.user.is_authenticated else None),
        )
        # 创建统计记录
        PromptStatistics.objects.create(prompt=prompt)
        return prompt

    def perform_update(self, serializer: Serializer) -> Prompt:
        """
        更新提示词时，自动记录历史

        参数:
            serializer: 序列化器实例

        返回:
            更新后的提示词实例
        """
        prompt = serializer.save()
        # 创建历史记录
        PromptHistory.objects.create(
            prompt=prompt,
            content=prompt.content,
            operation_type="update",
            user=(self.request.user if self.request.user.is_authenticated else None),
        )
        return prompt

    @action(detail=True, methods=["post"])
    def use(self, request: Request, pk: Optional[str] = None) -> Response:
        """
        标记提示词被使用，并更新使用统计

        参数:
            request: 请求对象
            pk: 提示词的主键

        返回:
            操作结果响应
        """
        prompt = self.get_object()
        prompt.usage_count += 1
        prompt.save()

        # 创建历史记录
        PromptHistory.objects.create(
            prompt=prompt,
            content=prompt.content,
            operation_type="use",
            user=(self.request.user if self.request.user.is_authenticated else None),
        )

        # 更新统计信息
        try:
            stats = prompt.promptstatistics
            stats.total_usage += 1

            # 计算日期边界
            now = timezone.now()
            today_start = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            week_start = today_start - timedelta(days=now.weekday())
            month_start = today_start.replace(day=1)

            # 获取今日、本周、本月的使用次数
            today_count = PromptHistory.objects.filter(
                prompt=prompt,
                operation_type="use",
                created_at__gte=today_start,
            ).count()
            week_count = PromptHistory.objects.filter(
                prompt=prompt,
                operation_type="use",
                created_at__gte=week_start,
            ).count()
            month_count = PromptHistory.objects.filter(
                prompt=prompt,
                operation_type="use",
                created_at__gte=month_start,
            ).count()

            stats.daily_usage = today_count
            stats.weekly_usage = week_count
            stats.monthly_usage = month_count
            stats.save()
        except PromptStatistics.DoesNotExist:
            # 如果统计记录不存在，则创建
            PromptStatistics.objects.create(
                prompt=prompt,
                total_usage=1,
                daily_usage=1,
                weekly_usage=1,
                monthly_usage=1,
            )

        return Response(
            {
                "status": "success",
                "message": "Prompt used successfully",
            }
        )

    @action(detail=False, methods=["post"])
    def generate(self, request: Request) -> Response:
        """
        根据用户需求生成新的提示词

        参数:
            request: 请求对象，包含生成需求和可选参数

        返回:
            新创建的提示词响应
        """
        from prompt.llm_utils.service import prompt_generation_service

        # 获取用户需求和可选参数
        requirement = request.data.get("requirement", "")
        model = request.data.get("model", None)
        title = request.data.get("title", "Generated Prompt")
        description = request.data.get("description", "Automatically generated prompt")

        if not requirement:
            return Response(
                {
                    "status": "error",
                    "message": "Requirement is required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 使用LLM服务生成提示词
        generated_content = prompt_generation_service.generate_prompt(
            requirement, model=model
        )

        # 创建新的提示词对象
        new_prompt = Prompt.objects.create(
            title=title,
            description=description,
            content=generated_content,
            user=request.user if request.user.is_authenticated else None,
        )

        # 创建历史记录
        PromptHistory.objects.create(
            prompt=new_prompt,
            content=generated_content,
            operation_type="generate",
            user=request.user if request.user.is_authenticated else None,
        )

        # 创建统计信息
        PromptStatistics.objects.create(
            prompt=new_prompt,
            generation_count=1,
        )

        # 使用序列化器返回新创建的提示词
        serializer = PromptSerializer(new_prompt)
        return Response(
            {
                "status": "success",
                "message": "Prompt generated successfully",
                "prompt": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def evaluate(self, request: Request, pk: Optional[str] = None) -> Response:
        """
        评估提示词的质量

        参数:
            request: 请求对象，包含评估参数
            pk: 提示词的主键

        返回:
            评估结果响应
        """
        from prompt.llm_utils.service import llm_evaluation_service

        prompt = self.get_object()
        detailed = request.data.get("detailed", True)
        model = request.data.get("model", None)

        # 使用LLM服务评估提示词质量
        evaluation_result = llm_evaluation_service.analyze_prompt_quality(
            prompt.content,
            detailed=detailed,
            model=model,
        )

        # 记录评估操作（可选）
        if self.request.user.is_authenticated:
            PromptHistory.objects.create(
                prompt=prompt,
                content=f"Evaluation: {evaluation_result[:100]}...",
                operation_type="evaluate",
                user=self.request.user,
            )

        return Response(
            {
                "status": "success",
                "message": "Prompt evaluated successfully",
                "evaluation_result": evaluation_result,
            }
        )

    @action(detail=True, methods=["post"])
    def optimize(self, request: Request, pk: Optional[str] = None) -> Response:
        """
        优化提示词的接口
        使用LLM服务对提示词进行智能优化

        参数:
            request: 请求对象，包含优化参数
            pk: 提示词的主键

        返回:
            优化结果响应，包含原始和优化后的内容
        """
        from prompt.llm_utils.service import prompt_optimization_service

        prompt = self.get_object()
        # 记录优化前的内容
        original_content = prompt.content

        # 使用LLM服务进行实际的提示词优化
        model = request.data.get("model", None)  # 可选参数，指定使用的模型
        optimized_content = prompt_optimization_service.optimize_prompt(
            original_content, model=model
        )

        # 更新提示词内容
        prompt.content = optimized_content
        prompt.save()

        # 创建历史记录
        PromptHistory.objects.create(
            prompt=prompt,
            content=optimized_content,
            operation_type="optimize",
            user=(self.request.user if self.request.user.is_authenticated else None),
        )

        # 更新统计信息
        try:
            stats = prompt.promptstatistics
            stats.optimization_count += 1
            # 计算优化提升率，这里只是一个示例
            improvement = 0.1  # 假设每次优化提升 10%
            stats.average_optimization_improvement = (
                (
                    stats.average_optimization_improvement
                    * (stats.optimization_count - 1)
                )
                + improvement
            ) / stats.optimization_count
            stats.save()
        except PromptStatistics.DoesNotExist:
            # 如果统计记录不存在，则创建
            PromptStatistics.objects.create(
                prompt=prompt,
                optimization_count=1,
                average_optimization_improvement=0.1,
            )

        return Response(
            {
                "status": "success",
                "message": "Prompt optimized successfully",
                "original_content": original_content,
                "optimized_content": optimized_content,
            }
        )


class PromptHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    PromptHistory 模型的视图集，提供只读操作
    """

    queryset = PromptHistory.objects.all()
    serializer_class = PromptHistorySerializer
    permission_classes = [permissions.AllowAny]  # 简化起见，允许所有用户访问

    def get_queryset(self):
        """
        根据 prompt_id 参数过滤历史记录
        """
        queryset = super().get_queryset()
        prompt_id = self.request.query_params.get("prompt_id")
        if prompt_id:
            queryset = queryset.filter(prompt_id=prompt_id)
        return queryset


class PromptStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    PromptStatistics 模型的视图集，提供只读操作
    """

    queryset = PromptStatistics.objects.all()
    serializer_class = PromptStatisticsSerializer
    permission_classes = [permissions.AllowAny]  # 简化起见，允许所有用户访问

    def get_queryset(self):
        """
        根据 prompt_id 参数过滤统计信息
        """
        queryset = super().get_queryset()
        prompt_id = self.request.query_params.get("prompt_id")
        if prompt_id:
            queryset = queryset.filter(prompt_id=prompt_id)
        return queryset


# 对于不需要完整视图集功能的简单视图，可以使用泛型视图
class PublicPromptListView(generics.ListAPIView):
    """
    公开提示词列表视图
    """

    serializer_class = PromptSerializer
    permission_classes = [permissions.AllowAny]  # 简化起见，允许所有用户访问

    def get_queryset(self):
        """
        获取公开的提示词列表
        """
        # 获取公开的提示词并按使用频率排序（前10个）
        # 修复了不存在的last_used_at字段和OneToOne关系查询问题
        return Prompt.objects.filter(
            is_public=True
        ).select_related('promptstatistics').order_by("-promptstatistics__weekly_usage")[:10]
