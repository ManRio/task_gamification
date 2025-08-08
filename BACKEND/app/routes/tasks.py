# app/routes/tasks.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Task, TaskCompletion, User
from ..utils.auth_helpers import role_required

tasks_bp = Blueprint("tasks", __name__)

# ----------------------- CREAR / EDITAR / BORRAR / LISTAR -----------------------

@tasks_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required("profesor")
def create_task():
    data = request.get_json() or {}
    title = data.get("title")
    description = data.get("description")
    reward = data.get("reward")

    if not title or reward is None:
        return jsonify({"msg": "Título y recompensa son requeridos"}), 400
    if not isinstance(reward, int) or reward <= 0:
        return jsonify({"msg": "La recompensa debe ser un entero > 0"}), 400

    user_id = int(get_jwt_identity())
    new_task = Task(title=title, description=description, reward=reward, created_by=user_id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"msg": "Tarea creada exitosamente", "id": new_task.id}), 201


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
@role_required("profesor")
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"msg": "Tarea no encontrada"}), 404

    data = request.get_json() or {}
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)

    reward = data.get("reward", task.reward)
    if reward is not None:
        if not isinstance(reward, int) or reward <= 0:
            return jsonify({"msg": "La recompensa debe ser un entero > 0"}), 400
        task.reward = reward

    db.session.commit()
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "reward": task.reward,
        "created_by": task.created_by
    }), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
@role_required("profesor")
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"msg": "Tarea no encontrada"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Tarea eliminada"}), 200


@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": t.id, "title": t.title, "description": t.description, "reward": t.reward, "created_by": t.created_by}
        for t in tasks
    ]), 200


@tasks_bp.route("/mine", methods=["GET"])
@jwt_required()
@role_required("profesor")
def get_my_tasks():
    current_user_id = int(get_jwt_identity())
    tasks = Task.query.filter_by(created_by=current_user_id).all()
    return jsonify([
        {"id": t.id, "title": t.title, "description": t.description, "reward": t.reward}
        for t in tasks
    ]), 200


# ----------------------- COMPLETAR / LISTAR COMPLETADAS (ALUMNO) -----------------------

@tasks_bp.route("/complete/<int:task_id>", methods=["POST"])
@jwt_required()
@role_required("alumno")
def complete_task(task_id):
    user_id = int(get_jwt_identity())
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"msg": "Tarea no encontrada"}), 404

    already_done = TaskCompletion.query.filter_by(student_id=user_id, task_id=task_id).first()
    if already_done:
        return jsonify({"msg": "Ya has completado esta tarea"}), 400

    completion = TaskCompletion(student_id=user_id, task_id=task_id)  # pending por defecto
    db.session.add(completion)
    db.session.commit()
    return jsonify({"msg": "Tarea marcada como completada y pendiente de validación"}), 200


@tasks_bp.route("/completed", methods=["GET"])
@jwt_required()
@role_required("alumno")
def get_completed_tasks():
    """No dependemos de relaciones. Hacemos JOIN explícito."""
    user_id = int(get_jwt_identity())

    rows = db.session.query(
        TaskCompletion.id.label("completion_id"),
        Task.id.label("task_id"),
        Task.title.label("title"),
        Task.description.label("description"),
        Task.reward.label("reward"),
        TaskCompletion.completed_at.label("completed_at"),
        TaskCompletion.is_validated.label("is_validated"),
        TaskCompletion.is_approved.label("is_approved"),
    ).join(Task, Task.id == TaskCompletion.task_id
    ).filter(TaskCompletion.student_id == user_id
    ).all()

    return jsonify([
        {
            "completion_id": r.completion_id,
            "task_id": r.task_id,
            "title": r.title,
            "description": r.description,
            "reward": r.reward,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "is_validated": r.is_validated,
            "is_approved": r.is_approved
        } for r in rows
    ]), 200


# ----------------------- PENDIENTES DE APROBACIÓN (PROFESOR) -----------------------

@tasks_bp.route("/pending_approval", methods=["GET"])
@jwt_required()
@role_required("profesor")
def pending_approval():
    """Lista entregas pendientes. Sin relaciones; JOIN a Task y User."""
    prof_id = int(get_jwt_identity())
    show_all = (request.args.get("all", "false").lower() == "true")

    q = db.session.query(
        TaskCompletion.id.label("completion_id"),
        User.id.label("student_id"),
        User.username.label("student_username"),
        Task.id.label("task_id"),
        Task.title.label("task_title"),
        Task.reward.label("task_reward"),
        TaskCompletion.completed_at.label("completed_at"),
    ).join(Task, Task.id == TaskCompletion.task_id
    ).join(User, User.id == TaskCompletion.student_id
    ).filter(TaskCompletion.is_validated == False)

    if not show_all:
        q = q.filter(Task.created_by == prof_id)

    q = q.order_by(TaskCompletion.completed_at.asc())

    rows = q.all()

    return jsonify([
        {
            "completion_id": r.completion_id,
            "student_id": r.student_id,
            "student_username": r.student_username,
            "task_id": r.task_id,
            "task_title": r.task_title,
            "task_reward": r.task_reward,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None
        } for r in rows
    ]), 200


# ----------------------- VALIDAR / RECHAZAR (PROFESOR) -----------------------

def _apply_validation(completion_id: int, approve: bool):
    """Evita relaciones: carga todo con Session.get y actualiza."""
    completion = db.session.get(TaskCompletion, completion_id)
    if not completion:
        return None, (jsonify({"msg": "Registro no encontrado"}), 404)

    if completion.is_validated:
        return None, (jsonify({"msg": "Esta tarea ya fue validada"}), 400)

    completion.is_validated = True
    completion.is_approved = bool(approve)

    student = None
    if approve:
        task = db.session.get(Task, completion.task_id)
        student = db.session.get(User, completion.student_id)
        if not task or not student:
            db.session.rollback()
            return None, (jsonify({"msg": "Datos asociados no encontrados"}), 400)

        student.coins += task.reward

        # (Opcional) CoinLog, si existe
        try:
            from ..models import CoinLog
            admin_id = int(get_jwt_identity())
            db.session.add(CoinLog(
                student_id=student.id,
                coins=task.reward,
                reason=f"aprobación tarea #{task.id}",
                assigned_by=admin_id,
            ))
        except Exception:
            pass

    db.session.commit()
    return (completion, student), None


@tasks_bp.route("/validate/<int:completion_id>", methods=["POST"])
@jwt_required()
@role_required("profesor")
def validate_task_post(completion_id):
    result, error = _apply_validation(completion_id, approve=True)
    if error:
        return error
    completion, student = result
    return jsonify({
        "msg": "Tarea aprobada",
        "completion_id": completion.id,
        "student_id": student.id if student else db.session.get(TaskCompletion, completion.id).student_id,
        "new_balance": student.coins if student else None
    }), 200


@tasks_bp.route("/reject/<int:completion_id>", methods=["POST"])
@jwt_required()
@role_required("profesor")
def reject_task_post(completion_id):
    result, error = _apply_validation(completion_id, approve=False)
    if error:
        return error
    completion, _ = result
    return jsonify({
        "msg": "Tarea rechazada",
        "completion_id": completion.id
    }), 200


# Alias PATCH (compatibilidad con tu front previo)
@tasks_bp.route("/validate/<int:completion_id>", methods=["PATCH"])
@jwt_required()
@role_required("profesor")
def validate_task_patch(completion_id):
    data = request.get_json() or {}
    approve = data.get("approve")
    if approve is None:
        return jsonify({"msg": "Campo 'approve' requerido (true/false)"}), 400
    _, error = _apply_validation(completion_id, approve=bool(approve))
    if error:
        return error
    return jsonify({"msg": "Validación registrada correctamente"}), 200
