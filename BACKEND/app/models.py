from . import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'alumno' o 'profesor'
    coins = db.Column(db.Integer, default=0)

    # Datos adicionales
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    course = db.Column(db.String(40), nullable=True)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(200))
    reward = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class TaskCompletion(db.Model):
    __tablename__ = "task_completion"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    # Usa callable para que se evalúe en cada inserción
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_validated = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, nullable=True)
    # NUEVO: cuándo se validó (aprobada o rechazada)
    validated_at = db.Column(db.DateTime, nullable=True)


class Reward(db.Model):
    __tablename__ = "rewards"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    cost = db.Column(db.Integer)
    description = db.Column(db.String(200))


class RewardRedemption(db.Model):
    __tablename__ = "reward_redemptions"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reward_id = db.Column(db.Integer, db.ForeignKey("rewards.id"), nullable=False)
    redeemed_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )


class CoinLog(db.Model):
    __tablename__ = "coin_log"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    coins = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255))
    assigned_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
