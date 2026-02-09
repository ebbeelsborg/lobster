from rest_framework import serializers
from ..models import Organization, MoltenBot, BotVersion, Task, Execution, ExecutionLog

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class BotVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotVersion
        fields = '__all__'

class MoltenBotSerializer(serializers.ModelSerializer):
    versions = BotVersionSerializer(many=True, read_only=True)
    is_overheating = serializers.BooleanField(read_only=True)

    class Meta:
        model = MoltenBot
        fields = ['id', 'name', 'organization', 'description', 'status', 'temperature', 'max_temperature', 'is_overheating', 'versions', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ExecutionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionLog
        fields = '__all__'

class ExecutionSerializer(serializers.ModelSerializer):
    logs = ExecutionLogSerializer(many=True, read_only=True)

    class Meta:
        model = Execution
        fields = ['id', 'bot_version', 'task', 'status', 'started_at', 'finished_at', 'logs']
