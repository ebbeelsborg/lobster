from django.contrib import admin
from django.utils.html import format_html
from .models import Organization, MoltenBot, BotVersion, Task, Execution, ExecutionLog, Secret

class BotVersionInline(admin.TabularInline):
    model = BotVersion
    extra = 1

class ExecutionLogInline(admin.TabularInline):
    model = ExecutionLog
    extra = 0
    readonly_fields = ('timestamp', 'level', 'message')
    can_delete = False

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('members',)

@admin.register(MoltenBot)
class MoltenBotAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'status', 'temp_display', 'is_overheating_display')
    list_filter = ('status', 'organization')
    search_fields = ('name',)
    inlines = [BotVersionInline]
    actions = ['shut_down_bot', 'reheat_bot_core']

    def temp_display(self, obj):
        color = "green"
        if obj.temperature > 500:
            color = "orange"
        if obj.temperature > 800:
            color = "red"
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}🔥</span>',
            color, obj.temperature
        )
    temp_display.short_description = "Temperature"

    def is_overheating_display(self, obj):
        if obj.is_overheating():
            return format_html('<span style="color: red; font-weight: bold;">YES 🔥🔥🔥</span>')
        return "Normal"
    is_overheating_display.short_description = "Overheating?"

    @admin.action(description="Shut down selected bots")
    def shut_down_bot(self, request, queryset):
        queryset.update(status='offline', temperature=25)
        self.message_user(request, "Selected bots have been decommissioned.")

    @admin.action(description="Reheat bot core")
    def reheat_bot_core(self, request, queryset):
        queryset.update(temperature=500, status='idle')
        self.message_user(request, "Bot cores are warming up...")

@admin.register(BotVersion)
class BotVersionAdmin(admin.ModelAdmin):
    list_display = ('bot', 'version_number', 'created_at')
    list_filter = ('bot',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot_version', 'task', 'status', 'started_at')
    list_filter = ('status', 'task')
    inlines = [ExecutionLogInline]

@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = ('key', 'organization', 'created_at')
    list_filter = ('organization',)
