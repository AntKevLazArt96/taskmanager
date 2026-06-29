from sqlalchemy import select

from app.extensions import db
from app.models import User, UserProfile


def list_users(active=None):
    stmt = select(User).order_by(User.name.asc())
    if active is True:
        stmt = stmt.where(User.is_active.is_(True))
    elif active is False:
        stmt = stmt.where(User.is_active.is_(False))

    return db.session.scalars(stmt).all()


def get_user_or_404(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        from flask import abort
        abort(404)
    return user


def create_user(name, profile_value):
    if profile_value not in {item.value for item in UserProfile}:
        raise ValueError("Perfil de usuario no válido")

    user = User(
        name=name.strip(),
        profile=UserProfile(profile_value),
        is_active=True,
    )
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user, name, profile_value):
    if profile_value not in {item.value for item in UserProfile}:
        raise ValueError("Perfil de usuario no válido")

    user.name = name.strip()
    user.profile = UserProfile(profile_value)
    db.session.commit()
    return user


def set_user_active(user, active):
    user.is_active = active
    db.session.commit()
    return user