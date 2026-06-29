from datetime import date

import pytest

from app.extensions import db
from app.models import Task, TaskStatus, User, UserProfile
from app.services.task_service import create_task


@pytest.fixture
def users(db_session):
    """Crea un usuario activo y uno inactivo para las pruebas."""
    active_user = User(
        name="Usuario Activo",
        profile=UserProfile.DEVELOPER,
        is_active=True,
    )
    inactive_user = User(
        name="Usuario Inactivo",
        profile=UserProfile.QA,
        is_active=False,
    )

    db.session.add_all([active_user, inactive_user])
    db.session.commit()

    return {
        "active": active_user,
        "inactive": inactive_user,
    }


def test_create_task_creates_valid_task_with_pending_status(db_session, users):
    task = create_task(
        title="Implementar login",
        description="Crear pantalla de acceso",
        user_id=users["active"].id,
        start_date=date(2026, 6, 1),
        end_date=date(2026, 6, 10),
    )

    assert task.id is not None
    assert task.title == "Implementar login"
    assert task.description == "Crear pantalla de acceso"
    assert task.user_id == users["active"].id
    assert task.start_date == date(2026, 6, 1)
    assert task.end_date == date(2026, 6, 10)
    assert task.status == TaskStatus.PENDING
    assert task.is_active is True
    assert task.delivery_date is None

    saved_task = db.session.get(Task, task.id)
    assert saved_task is not None
    assert saved_task.status == TaskStatus.PENDING


def test_create_task_raises_error_when_title_is_empty(db_session, users):
    with pytest.raises(ValueError, match="El título es obligatorio\\."):
        create_task(
            title="   ",
            description="Descripción",
            user_id=users["active"].id,
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 10),
        )


def test_create_task_raises_error_when_end_date_is_before_start_date(db_session, users):
    with pytest.raises(ValueError, match="La fecha de fin debe ser igual o posterior a la fecha de inicio\\."):
        create_task(
            title="Tarea con fechas inválidas",
            description="Descripción",
            user_id=users["active"].id,
            start_date=date(2026, 6, 10),
            end_date=date(2026, 6, 1),
        )


def test_create_task_raises_error_when_assigned_user_does_not_exist(db_session, users):
    with pytest.raises(ValueError, match="El usuario asignado no existe o no está activo\\."):
        create_task(
            title="Tarea sin usuario",
            description="Descripción",
            user_id=9999,
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 10),
        )


def test_create_task_raises_error_when_assigned_user_is_inactive(db_session, users):
    with pytest.raises(ValueError, match="El usuario asignado no existe o no está activo\\."):
        create_task(
            title="Tarea con usuario inactivo",
            description="Descripción",
            user_id=users["inactive"].id,
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 10),
        )


def test_create_task_raises_error_when_there_are_no_active_users(db_session):
    inactive_user = User(
        name="Solo Inactivo",
        profile=UserProfile.DESIGN,
        is_active=False,
    )
    db.session.add(inactive_user)
    db.session.commit()

    with pytest.raises(ValueError, match="El usuario asignado no existe o no está activo\\."):
        create_task(
            title="Tarea sin usuarios activos",
            description="Descripción",
            user_id=inactive_user.id,
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 10),
        )