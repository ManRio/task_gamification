from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .. import db
from ..models import Task, TaskCompletion, User
from ..utils.auth_helpers import role_required

tasks_bp = Blueprint("tasks", __name__)

# CREACION DE TAREA
@tasks_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required("profesor")
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    reward = data.get("reward")

    if not title or not reward:
        return jsonify({"msg": "Título y recompensa son requeridos"}), 400

    user_id = get_jwt_identity()

    new_task = Task(
        title=title,
        description=description,
        reward=reward,
        created_by=int(user_id)
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"msg": "Tarea creada exitosamente"}), 201

 # OBTENER TODAS LAS TAREAS
@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_tasks():
    tasks = Task.query.all()
    return jsonify([
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "reward": task.reward,
            "created_by": task.created_by
        } for task in tasks
    ]), 200

# OBTENER TAREAS CREADAS SÓLO POR UN PROFESOR
@tasks_bp.route("/mine", methods=["GET"])
@jwt_required()
@role_required("profesor")
def get_my_tasks():
    current_user_id = int(get_jwt_identity())
    tasks = Task.query.filter_by(created_by=current_user_id).all()

    return jsonify([
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "reward": task.reward
        } for task in tasks
    ]), 200

# COMPLETADO DE TAREAS POR ALUMNOS
@tasks_bp.route("/complete/<int:task_id>", methods=["POST"])
@jwt_required()
@role_required("alumno")
def complete_task(task_id):
    user_id = int(get_jwt_identity())

    # Verifica que la tarea existe
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"msg": "Tarea no encontrada"}), 404

    # Verifica que el alumno no haya completado ya esta tarea
    already_done = TaskCompletion.query.filter_by(
        student_id=user_id, task_id=task_id
    ).first()
    if already_done:
        return jsonify({"msg": "Ya has completado esta tarea"}), 400

    # Registrar la tarea como completada
    completion = TaskCompletion(student_id=user_id, task_id=task_id)
    db.session.add(completion)

    db.session.commit()

    return jsonify({"msg": "Tarea completada", "monedas_ganadas": task.reward}), 200

# OBTENER TAREAS COMPLETADAS POR UN ALUMNO
@tasks_bp.route("/completed", methods=["GET"])
@jwt_required()
@role_required("alumno")
def get_completed_tasks():
    user_id = int(get_jwt_identity())

    completions = TaskCompletion.query.filter_by(student_id=user_id).all()

    data = []
    for completion in completions:
        task = Task.query.get(completion.task_id)
        data.append({
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "reward": task.reward,
            "completed_at": completion.completed_at.isoformat(),
            "is_validated": completion.is_validated,
            "is_approved": completion.is_approved
        })

    return jsonify(data), 200

# VALIDAR TAREA COMPLETADA POR UN PROFESOR
@tasks_bp.route("/validate/<int:completion_id>", methods=["PATCH"])
@jwt_required()
@role_required("profesor")
def validate_task(completion_id):
    data = request.get_json()
    approve = data.get("approve")

    if approve is None:
        return jsonify({"msg": "Campo 'approve' requerido (true/false)"}), 400

    completion = TaskCompletion.query.get(completion_id)
    if not completion:
        return jsonify({"msg": "Registro no encontrado"}), 404

    if completion.is_validated:
        return jsonify({"msg": "Esta tarea ya fue validada"}), 400

    completion.is_validated = True
    completion.is_approved = bool(approve)

    if approve:
        student = User.query.get(completion.student_id)
        task = Task.query.get(completion.task_id)
        student.coins += task.reward

    db.session.commit()

    return jsonify({"msg": "Validación registrada correctamente"}), 200