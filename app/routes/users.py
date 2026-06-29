from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.forms import UserForm
from app.models import UserProfile
from app.services.user_service import (
    create_user,
    get_user_or_404,
    list_users,
    set_user_active,
    update_user,
)

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/")
def index():
    active_filter = request.args.get("active", "all")
    if active_filter == "active":
        active = True
    elif active_filter == "inactive":
        active = False
    else:
        active = None

    users = list_users(active=active)
    return render_template(
        "users/list.html",
        users=users,
        active_filter=active_filter,
        profile_labels=dict(UserProfile.choices()),
    )


@users_bp.route("/create", methods=["GET", "POST"])
def create():
    form = UserForm()
    form.profile.choices = UserProfile.choices()

    if form.validate_on_submit():
        try:
            create_user(form.name.data, form.profile.data)
            flash("Usuario creado correctamente.", "success")
            return redirect(url_for("users.index"))
        except ValueError as exc:
            flash(str(exc), "danger")

    return render_template(
        "users/form.html",
        form=form,
        user=None,
        form_title="Registrar usuario",
        submit_label="Crear usuario",
    )


@users_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
def edit(user_id):
    user = get_user_or_404(user_id)
    form = UserForm(obj=user)
    form.profile.choices = UserProfile.choices()

    if request.method == "GET":
        form.profile.data = user.profile.value

    if form.validate_on_submit():
        try:
            update_user(user, form.name.data, form.profile.data)
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("users.index"))
        except ValueError as exc:
            flash(str(exc), "danger")

    return render_template(
        "users/form.html",
        form=form,
        user=user,
        form_title="Editar usuario",
        submit_label="Guardar cambios",
    )


@users_bp.route("/<int:user_id>/activate", methods=["POST"])
def activate(user_id):
    user = get_user_or_404(user_id)
    set_user_active(user, True)
    flash("Usuario activado correctamente.", "success")
    return redirect(url_for("users.index", active=request.args.get("active", "all")))


@users_bp.route("/<int:user_id>/deactivate", methods=["POST"])
def deactivate(user_id):
    user = get_user_or_404(user_id)
    set_user_active(user, False)
    flash("Usuario desactivado correctamente.", "success")
    return redirect(url_for("users.index", active=request.args.get("active", "all")))