from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Organization(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_organizations')
    members = models.ManyToManyField(User, related_name='organizations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MoltenBot(models.Model):
    STATUS_CHOICES = [
        ('idle', 'Idle'),
        ('running', 'Running'),
        ('cooling', 'Cooling Down'),
        ('overheated', 'Overheated'),
        ('offline', 'Offline'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='bots')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='idle')
    temperature = models.IntegerField(default=25)  # 0-1000 🔥
    max_temperature = models.IntegerField(default=800)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_overheating(self):
        return self.temperature > (self.max_temperature * 0.8)

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

class BotVersion(models.Model):
    bot = models.ForeignKey(MoltenBot, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50)
    config_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('bot', 'version_number')

    def __str__(self):
        return f"{self.bot.name} v{self.version_number}"

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    required_permissions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Execution(models.Model):
    STATE_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('aborted', 'Aborted'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot_version = models.ForeignKey(BotVersion, on_delete=models.CASCADE, related_name='executions')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='executions')
    started_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATE_CHOICES, default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Execution {self.id} ({self.status})"

class ExecutionLog(models.Model):
    LEVEL_CHOICES = [
        ('info', 'INFO'),
        ('warning', 'WARNING'),
        ('error', 'ERROR'),
        ('molten', 'MOLTEN 🔥'),
    ]

    execution = models.ForeignKey(Execution, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(default=timezone.now)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='info')
    message = models.TextField()

    class Meta:
        ordering = ['timestamp']

class Secret(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='secrets')
    key = models.CharField(max_length=255)
    value = models.TextField()  # In a real app, this would be encrypted
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'key')

    def __str__(self):
        return f"{self.key} ({self.organization.name})"
