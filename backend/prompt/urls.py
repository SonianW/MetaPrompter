from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PromptViewSet,
    PromptHistoryViewSet,
    PromptStatisticsViewSet,
    PublicPromptListView,
)

# 创建路由器
router = DefaultRouter()
# 注册 Prompt 视图集，生成 CRUD 接口
router.register(r"prompts", PromptViewSet)
# 注册 PromptHistory 视图集，提供只读接口
router.register(
    r"histories", PromptHistoryViewSet, basename="prompthistory"
)
# 注册 PromptStatistics 视图集，提供只读接口
router.register(r"statistics", PromptStatisticsViewSet, basename="promptstatistics")

# 额外的 URL 模式
urlpatterns = [
    # 包含路由器生成的 URL
    path("", include(router.urls)),
    # 公开提示词列表接口
    path(
        "public-prompts/", PublicPromptListView.as_view(), name="public-prompts"
    ),
]
