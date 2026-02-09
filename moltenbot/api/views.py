from rest_framework import viewsets, permissions
from ..models import Organization, MoltenBot, BotVersion, Task, Execution, ExecutionLog
from .serializers import (
    OrganizationSerializer, MoltenBotSerializer, BotVersionSerializer,
    TaskSerializer, ExecutionSerializer, ExecutionLogSerializer
)

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

class MoltenBotViewSet(viewsets.ModelViewSet):
    queryset = MoltenBot.objects.all()
    serializer_class = MoltenBotSerializer
    permission_classes = [permissions.IsAuthenticated]

class BotVersionViewSet(viewsets.ModelViewSet):
    queryset = BotVersion.objects.all()
    serializer_class = BotVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExecutionViewSet(viewsets.ModelViewSet):
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExecutionLogViewSet(viewsets.ModelViewSet):
    queryset = ExecutionLog.objects.all()
    serializer_class = ExecutionLogSerializer
    permission_classes = [permissions.IsAuthenticated]
