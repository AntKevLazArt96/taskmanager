from datetime import datetime
from enum import Enum

from app.extensions import db


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"

    @classmethod
    def choices(cls):
        return [
            (cls.PENDING.value, "Pendiente"),
            (cls.IN_PROGRESS.value, "En progreso"),
            (cls.DONE.value, "Completada"),
        ]

    @classmethod
    def label(cls, value):
        labels = dict(cls.choices())
        return labels.get(value, value)


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref="tasks")

    def __repr__(self):
        return f"<Task {self.id} {self.title}>"