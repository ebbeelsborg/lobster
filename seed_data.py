import os
import django
import uuid
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lobster_project.settings')
django.setup()

from django.contrib.auth.models import User
from moltenbot.models import Organization, MoltenBot, BotVersion, Task, Execution, ExecutionLog

def seed():
    # 1. Create User
    admin = User.objects.filter(username='admin').first()
    if not admin:
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    # 2. Create Organization
    org, _ = Organization.objects.get_or_create(
        name="Magma Corp",
        slug="magma-corp",
        owner=admin
    )
    org.members.add(admin)

    # 3. Create Tasks
    task1, _ = Task.objects.get_or_create(name="Core Diagnostics", description="Run basic unit health check.")
    task2, _ = Task.objects.get_or_create(name="Lava Mining", description="Extract resources from sub-surface layers.")
    task3, _ = Task.objects.get_or_create(name="Core Containment", description="Prevent thermal runaway.")

    # 4. Create Bots
    bots_data = [
        {"name": "Blaze-V1", "status": "idle", "temp": 120, "desc": "Standard exploration unit."},
        {"name": "Inferno-X", "status": "running", "temp": 650, "desc": "Heavy-duty mining unit. High heat tolerance."},
        {"name": "Frost-Bite", "status": "cooling", "temp": 45, "desc": "Experimental cooling prototype."},
        {"name": "Meltdown", "status": "overheated", "temp": 950, "desc": "WARNING: Thermal runaway detected."},
    ]

    for b in bots_data:
        bot, created = MoltenBot.objects.get_or_create(
            name=b['name'],
            organization=org,
            defaults={
                'status': b['status'],
                'temperature': b['temp'],
                'description': b['desc']
            }
        )
        
        # Add a version
        version, _ = BotVersion.objects.get_or_create(
            bot=bot,
            version_number="1.0.0",
            defaults={'config_json': {'mode': 'aggressive', 'safety': 'off'}}
        )

        # Add some executions
        if created:
            for i in range(3):
                exec_obj = Execution.objects.create(
                    bot_version=version,
                    task=task1 if i == 0 else task2,
                    started_by=admin,
                    status='success' if i < 2 else 'failed',
                    started_at=timezone.now() - timedelta(hours=i*2),
                    finished_at=timezone.now() - timedelta(hours=i*2 - 1)
                )
                
                # Add logs
                ExecutionLog.objects.create(execution=exec_obj, level='info', message="Initializing core components...")
                if bot.name == "Meltdown":
                    ExecutionLog.objects.create(execution=exec_obj, level='molten', message="🔥 CORE TEMPERATURE RISING RAPIDLY 🔥")
                    ExecutionLog.objects.create(execution=exec_obj, level='error', message="Thermal containment failed.")
                else:
                    ExecutionLog.objects.create(execution=exec_obj, level='info', message="Operation continuing within parameters.")

    print("Database seeded successfully with Moltenbot data!")

if __name__ == '__main__':
    seed()
