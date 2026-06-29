from datetime import datetime as dt, date

from sqlalchemy import select

from app.extensions import db
from app.models import Task, TaskStatus, User


def count_active_users():
    stmt = select(db.func.count(User.id)).where(User.is_active.is_(True))
    count = db.session.scalar(stmt)
    return count or 0


def get_active_users():
    stmt = select(User).where(User.is_active.is_(True)).order_by(User.name.asc())
    return db.session.scalars(stmt).all()


def list_tasks(active=None):
    stmt = select(Task).order_by(Task.created_at.desc())
    if active is True:
        stmt = stmt.where(Task.is_active.is_(True))
    elif active is False:
        stmt = stmt.where(Task.is_active.is_(False))

    return db.session.scalars(stmt).all()


def get_task_or_404(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        from flask import abort
        abort(404)
    return task


def validate_task_data(title, user_id, start_date, end_date):
    if not title or not title.strip():
        raise ValueError("El título es obligatorio.")

    user = db.session.get(User, user_id)
    if user is None or not user.is_active:
        raise ValueError("El usuario asignado no existe o no está activo.")

    if isinstance(start_date, str):
        try:
            start_date = dt.strptime(start_date, "%Y-%m-%d").date()
        except (ValueError, AttributeError):
            raise ValueError("Formato de fecha de inicio inválido.")

    if isinstance(end_date, str):
        try:
            end_date = dt.strptime(end_date, "%Y-%m-%d").date()
        except (ValueError, AttributeError):
            raise ValueError("Formato de fecha de fin inválido.")

    if end_date < start_date:
        raise ValueError("La fecha de fin debe ser igual o posterior a la fecha de inicio.")

    return start_date, end_date


def create_task(title, description, user_id, start_date, end_date):
    start_date, end_date = validate_task_data(title, user_id, start_date, end_date)

    task = Task(
        title=title.strip(),
        description=description.strip() if description else None,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        status=TaskStatus.PENDING,
        delivery_date=None,
        is_active=True,
    )
    db.session.add(task)
    db.session.commit()
    return task


def update_task(task, title, description, user_id, start_date, end_date):
    start_date, end_date = validate_task_data(title, user_id, start_date, end_date)

    task.title = title.strip()
    task.description = description.strip() if description else None
    task.user_id = user_id
    task.start_date = start_date
    task.end_date = end_date
    db.session.commit()
    return task


def set_task_active(task, active):
    task.is_active = active
    db.session.commit()
    return task


def validate_task_status(status_value):
    if status_value not in {item.value for item in TaskStatus}:
        raise ValueError("Estado de tarea no válido.")


def change_task_status(task, status_value):
    validate_task_status(status_value)

    new_status = TaskStatus(status_value)
    task.status = new_status

    if new_status == TaskStatus.DONE:
        if task.delivery_date is None:
            task.delivery_date = dt.utcnow()
    else:
        task.delivery_date = None

    db.session.commit()
    return task


def is_task_overdue(task):
    return task.is_active and task.status != TaskStatus.DONE and task.end_date < date.today()