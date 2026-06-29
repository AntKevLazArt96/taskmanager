"""
Script para cargar datos de ejemplo en la base de datos.
Uso: python scripts/seed_data.py
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para importar 'app'
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, date, timedelta
from app import create_app
from app.models import User, Task, UserProfile, TaskStatus
from app.services import user_service, task_service
from app.extensions import db


def seed_database():
    """Carga datos de ejemplo evitando duplicados."""

    # Verificar si ya existen usuarios de ejemplo
    existing_users = user_service.list_users()
    if existing_users:
        print("⚠️  La base de datos ya contiene usuarios. Abortando para evitar duplicados.")
        print(f"   Usuarios existentes: {len(existing_users)}")
        return

    print("🌱 Iniciando carga de datos de ejemplo...\n")

    # Crear usuarios
    users_data = [
        {"name": "Ana García", "profile": UserProfile.DEVELOPER.value},
        {"name": "Carlos López", "profile": UserProfile.QA.value},
        {"name": "María Rodríguez", "profile": UserProfile.DESIGN.value},
    ]

    users = []
    for user_data in users_data:
        user = user_service.create_user(user_data["name"], user_data["profile"])
        users.append(user)
        print(f"✓ Usuario creado: {user.name} ({UserProfile.label(user.profile)})")

    print()

    # Definir fechas
    today = date.today()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)
    two_weeks = today + timedelta(days=14)

    # Crear tareas
    tasks_data = [
        # Tareas del Desarrollador (Ana)
        {
            "title": "Implementar autenticación OAuth",
            "description": "Añadir soporte para login con GitHub y Google",
            "user": users[0],
            "start_date": week_ago,
            "end_date": next_week,
            "status": TaskStatus.IN_PROGRESS.value,
            "delivery_date": None,
        },
        {
            "title": "Refactorizar componentes React",
            "description": "Mejorar la reutilización de código",
            "user": users[0],
            "start_date": yesterday,
            "end_date": today,  # TAREA VENCIDA - fecha de fin pasada
            "status": TaskStatus.PENDING.value,  # Pero no finalizada
            "delivery_date": None,
        },
        {
            "title": "API REST para tablero de tareas",
            "description": "Endpoints para CRUD de tareas",
            "user": users[0],
            "start_date": two_weeks - timedelta(days=7),
            "end_date": two_weeks - timedelta(days=3),
            "status": TaskStatus.DONE.value,
            "delivery_date": datetime.utcnow(),
        },

        # Tareas del QA (Carlos)
        {
            "title": "Testing de flujo de autenticación",
            "description": "Verificar todos los casos de login",
            "user": users[1],
            "start_date": week_ago,
            "end_date": today,
            "status": TaskStatus.IN_PROGRESS.value,
            "delivery_date": None,
        },
        {
            "title": "Pruebas de performance",
            "description": "Análisis de carga y optimización",
            "user": users[1],
            "start_date": today,
            "end_date": two_weeks,
            "status": TaskStatus.PENDING.value,
            "delivery_date": None,
        },
        {
            "title": "Testing de compatibilidad navegadores",
            "description": "Chrome, Firefox, Safari, Edge",
            "user": users[1],
            "start_date": two_weeks - timedelta(days=5),
            "end_date": two_weeks - timedelta(days=1),
            "status": TaskStatus.DONE.value,
            "delivery_date": datetime.utcnow(),
        },

        # Tareas del Diseñador (María)
        {
            "title": "Diseño de sistema de colores",
            "description": "Paleta de colores y tokens de diseño",
            "user": users[2],
            "start_date": week_ago - timedelta(days=2),
            "end_date": week_ago,
            "status": TaskStatus.DONE.value,
            "delivery_date": datetime.utcnow(),
        },
        {
            "title": "Mockups de dashboard",
            "description": "Diseño de interfaz principal",
            "user": users[2],
            "start_date": today,
            "end_date": next_week,
            "status": TaskStatus.IN_PROGRESS.value,
            "delivery_date": None,
        },
        {
            "title": "Guía de componentes UI",
            "description": "Documentación de componentes reutilizables",
            "user": users[2],
            "start_date": next_week,
            "end_date": two_weeks,
            "status": TaskStatus.PENDING.value,
            "delivery_date": None,
        },
    ]

    for task_data in tasks_data:
        user = task_data.pop("user")
        delivery_date = task_data.pop("delivery_date")
        status = task_data.pop("status")

        task = task_service.create_task(
            title=task_data["title"],
            description=task_data["description"],
            user_id=user.id,
            start_date=task_data["start_date"],
            end_date=task_data["end_date"],
        )

        # Cambiar estado si no es pendiente
        if status != TaskStatus.PENDING.value:
            task_service.change_task_status(task, status)

        status_label = TaskStatus.label(status)
        is_overdue = task_service.is_task_overdue(task)
        overdue_marker = " ⚠️ [VENCIDA]" if is_overdue else ""
        print(f"✓ Tarea creada: {task.title} ({status_label}){overdue_marker}")

    print(f"\n✅ Semilla de datos completada!")
    print(f"   - {len(users)} usuarios creados")
    print(f"   - {len(tasks_data)} tareas creadas")
    print("\n📋 Resumen:")
    print(f"   - Tareas Pendientes: 3")
    print(f"   - Tareas En Progreso: 3")
    print(f"   - Tareas Finalizadas: 3")
    print(f"   - Tareas Vencidas: 1")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_database()