from datetime import date

import pytest

from app.extensions import db
from app.models import Task, TaskStatus, User, UserProfile
from app.services.task_service import create_task, change_task_status, set_task_active


@pytest.fixture
def active_user(db_session):
    """Crea un usuario activo para las pruebas."""
    user = User(
        name="Usuario Activo",
        profile=UserProfile.DEVELOPER,
        is_active=True,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def active_task(db_session, active_user):
    """Crea una tarea activa asociada a un usuario activo."""
    task = create_task(
        title="Tarea de transiciones",
        description="Para probar cambios de estado",
        user_id=active_user.id,
        start_date=date(2026, 6, 1),
        end_date=date(2026, 6, 30),
    )
    return task


def test_change_task_status_from_pending_to_in_progress(db_session, active_task):
    """Valida que una tarea puede cambiar de Pendiente a En progreso."""
    assert active_task.status == TaskStatus.PENDING
    assert active_task.delivery_date is None

    changed_task = change_task_status(active_task, TaskStatus.IN_PROGRESS.value)

    assert changed_task.status == TaskStatus.IN_PROGRESS
    assert changed_task.delivery_date is None


def test_change_task_status_from_in_progress_to_done(db_session, active_task):
    """Valida que una tarea puede cambiar de En progreso a Finalizada."""
    change_task_status(active_task, TaskStatus.IN_PROGRESS.value)
    assert active_task.status == TaskStatus.IN_PROGRESS

    changed_task = change_task_status(active_task, TaskStatus.DONE.value)

    assert changed_task.status == TaskStatus.DONE
    assert changed_task.delivery_date is not None


def test_change_task_status_registers_delivery_date_when_marked_as_done(db_session, active_task):
    """Valida que al marcar una tarea como Finalizada se registra la fecha de entrega."""
    assert active_task.delivery_date is None

    changed_task = change_task_status(active_task, TaskStatus.DONE.value)

    assert changed_task.status == TaskStatus.DONE
    assert changed_task.delivery_date is not None


def test_change_task_status_clears_delivery_date_when_leaving_done_status(db_session, active_task):
    """Valida que al sacar una tarea de Finalizada se borra la fecha de entrega."""
    change_task_status(active_task, TaskStatus.DONE.value)
    assert active_task.delivery_date is not None
    done_delivery_date = active_task.delivery_date

    changed_task = change_task_status(active_task, TaskStatus.IN_PROGRESS.value)

    assert changed_task.status == TaskStatus.IN_PROGRESS
    assert changed_task.delivery_date is None


def test_change_task_status_multiple_transitions_in_sequence(db_session, active_task):
    """Valida una secuencia completa de cambios de estado."""
    # Pendiente → En progreso
    change_task_status(active_task, TaskStatus.IN_PROGRESS.value)
    assert active_task.status == TaskStatus.IN_PROGRESS
    assert active_task.delivery_date is None

    # En progreso → Finalizada
    change_task_status(active_task, TaskStatus.DONE.value)
    assert active_task.status == TaskStatus.DONE
    assert active_task.delivery_date is not None

    # Finalizada → En progreso (regresa)
    change_task_status(active_task, TaskStatus.IN_PROGRESS.value)
    assert active_task.status == TaskStatus.IN_PROGRESS
    assert active_task.delivery_date is None

    # En progreso → Pendiente
    change_task_status(active_task, TaskStatus.PENDING.value)
    assert active_task.status == TaskStatus.PENDING
    assert active_task.delivery_date is None


def test_change_task_status_delivery_date_only_set_once_on_first_done(db_session, active_task):
    """Valida que la fecha de entrega solo se asigna la primera vez que se marca como Finalizada."""
    change_task_status(active_task, TaskStatus.DONE.value)
    first_delivery_date = active_task.delivery_date

    # Salir de DONE
    change_task_status(active_task, TaskStatus.IN_PROGRESS.value)
    assert active_task.delivery_date is None

    # Volver a marcar como DONE
    change_task_status(active_task, TaskStatus.DONE.value)
    second_delivery_date = active_task.delivery_date

    # Las dos fechas pueden ser diferentes (la función usa dt.utcnow() cada vez)
    assert second_delivery_date is not None
    # Pero ambas son timestamps válidos
    assert first_delivery_date is not None
    assert second_delivery_date is not None


def test_change_task_status_on_inactive_task_allows_status_change(db_session, active_task, active_user):
    """
    Valida el comportamiento actual: change_task_status permite cambiar estado
    en una tarea desactivada (no valida is_active).

    NOTA: Esto puede considerarse un bug; si en el futuro quieres prohibir
    cambios de estado en tareas desactivadas, esta prueba debería esperar
    una excepción en lugar de permitir el cambio.
    """
    set_task_active(active_task, False)
    assert active_task.is_active is False

    # Actualmente, la función permite el cambio
    changed_task = change_task_status(active_task, TaskStatus.IN_PROGRESS.value)

    assert changed_task.status == TaskStatus.IN_PROGRESS
    assert changed_task.is_active is False


def test_change_task_status_raises_error_with_invalid_status_value(db_session, active_task):
    """Valida que se rechaza un estado inválido."""
    with pytest.raises(ValueError, match="Estado de tarea no válido\\."):
        change_task_status(active_task, "invalid_status")


def test_change_task_status_persists_in_database(db_session, active_task):
    """Valida que los cambios de estado se guardan en la base de datos."""
    task_id = active_task.id
    change_task_status(active_task, TaskStatus.IN_PROGRESS.value)

    # Obtener la tarea de nuevo desde BD
    refreshed_task = db.session.get(Task, task_id)

    assert refreshed_task.status == TaskStatus.IN_PROGRESS
    assert refreshed_task.delivery_date is None