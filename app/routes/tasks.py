from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.forms import TaskForm
from app.models import TaskStatus
from app.services.task_service import (
    count_active_users,
    create_task,
    get_active_users,
    get_task_or_404,
    list_tasks,
    set_task_active,
    update_task,
)

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("/")
def index():
    active_filter = request.args.get("active", "all")
    if active_filter == "active":
        active = True
    elif active_filter == "inactive":
        active = False
    else:
        active = None

    tasks = list_tasks(active=active)
    return render_template(
        "tasks/list.html",
        tasks=tasks,
        active_filter=active_filter,
        status_labels=dict(TaskStatus.choices()),
    )


@tasks_bp.route("/create", methods=["GET", "POST"])
def create():
    if count_active_users() == 0:
        flash(
            "No puedes crear tareas: necesitas al menos un usuario activo.",
            "warning",
        )
        return redirect(url_for("tasks.index"))

    form = TaskForm()
    active_users = get_active_users()
    form.user_id.choices = [(user.id, user.name) for user in active_users]

    if form.validate_on_submit():
        try:
            create_task(
                form.title.data,
                form.description.data,
                form.user_id.data,
                form.start_date.data,
                form.end_date.data,
            )
            flash("Tarea creada correctamente.", "success")
            return redirect(url_for("tasks.index"))
        except ValueError as exc:
            flash(str(exc), "danger")

    return render_template(
        "tasks/form.html",
        form=form,
        task=None,
        active_users=active_users,
        form_title="Crear tarea",
        submit_label="Crear tarea",
    )


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
def edit(task_id):
    task = get_task_or_404(task_id)
    form = TaskForm()
    active_users = get_active_users()
    form.user_id.choices = [(user.id, user.name) for user in active_users]

    if request.method == "GET":
        form.title.data = task.title
        form.description.data = task.description
        form.user_id.data = task.user_id
        form.start_date.data = task.start_date
        form.end_date.data = task.end_date

    if form.validate_on_submit():
        try:
            update_task(
                task,
                form.title.data,
                form.description.data,
                form.user_id.data,
                form.start_date.data,
                form.end_date.data,
            )
            flash("Tarea actualizada correctamente.", "success")
            return redirect(url_for("tasks.index"))
        except ValueError as exc:
            flash(str(exc), "danger")

    return render_template(
        "tasks/form.html",
        form=form,
        task=task,
        active_users=active_users,
        form_title="Editar tarea",
        submit_label="Guardar cambios",
    )


@tasks_bp.route("/<int:task_id>/deactivate", methods=["POST"])
def deactivate(task_id):
    task = get_task_or_404(task_id)
    set_task_active(task, False)
    flash("Tarea desactivada correctamente.", "success")
    return redirect(url_for("tasks.index", active=request.args.get("active", "all")))


@tasks_bp.route("/<int:task_id>/activate", methods=["POST"])
def activate(task_id):
    task = get_task_or_404(task_id)
    set_task_active(task, True)
    flash("Tarea activada correctamente.", "success")
    return redirect(url_for("tasks.index", active=request.args.get("active", "all")))