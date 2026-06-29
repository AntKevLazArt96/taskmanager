from enum import Enum

from app.extensions import db


class UserProfile(str, Enum):
    DEVELOPER = "developer"
    QA = "qa"
    DESIGN = "design"

    @classmethod
    def choices(cls):
        return [
            (cls.DEVELOPER.value, "Desarrollador"),
            (cls.QA.value, "QA"),
            (cls.DESIGN.value, "Diseño"),
        ]

    @classmethod
    def label(cls, value):
        labels = dict(cls.choices())
        return labels.get(value, value)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    profile = db.Column(db.Enum(UserProfile), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<User {self.id} {self.name}>"