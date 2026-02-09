from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import views as api_views
from . import views

router = DefaultRouter()
router.register(r'organizations', api_views.OrganizationViewSet)
router.register(r'bots', api_views.MoltenBotViewSet)
router.register(r'versions', api_views.BotVersionViewSet)
router.register(r'tasks', api_views.TaskViewSet)
router.register(r'executions', api_views.ExecutionViewSet)
router.register(r'logs', api_views.ExecutionLogViewSet)

urlpatterns = [
    # Dashboard and UI
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('bot/<uuid:pk>/', views.BotDetailView.as_view(), name='bot_detail'),
    path('bot/create/', views.BotCreateView.as_view(), name='bot_create'),

    # API
    path('api/', include(router.urls)),
]
