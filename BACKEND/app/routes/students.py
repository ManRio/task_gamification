from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from .. import db
from ..models import User, TaskCompletion, Task
from ..utils.auth_helpers import role_required

students_bp = Blueprint("students", __name__)

# CREAR UN NUEVO ALUMNO (sólo profesor)
@students_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required("profesor")
def create_student():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    course = data.get("course")

    if not username or not password:
        return jsonify({"msg": "Username y password requeridos"}), 400

    # Verificar si ya existe
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Este usuario ya existe"}), 409

    hashed_pw = generate_password_hash(password)
    new_user = User(
        username=username,
        password=hashed_pw,
        role="alumno",
        first_name=first_name,
        last_name=last_name,
        email=email,
        course=course,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Alumno creado exitosamente"}), 201


# LISTADO DE TODOS LOS ALUMNOS (solo profesor)
@students_bp.route("/all", methods=["GET"])
@jwt_required()
@role_required("profesor")
def list_all_students():
    students = User.query.filter_by(role="alumno").all()

    return jsonify([
        {
            "id": student.id,
            "username": student.username,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "course": student.course,
            "coins": student.coins
        } for student in students
    ]), 200

# VER PERFIL DEL ALUMNO
@students_bp.route("/me", methods=["GET"])
@jwt_required()
@role_required("alumno")
def view_profile():
    user_id = int(get_jwt_identity())
    student = User.query.get(user_id)

    if not student:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    return jsonify({
        "id": student.id,
        "username": student.username,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
        "course": student.course,
        "role": student.role,
        "coins": student.coins
    }), 200

# VER ESTADÍSTICAS DEL ALUMNO
@students_bp.route("/stats", methods=["GET"])
@jwt_required()
@role_required("alumno")
def view_stats():
    user_id = int(get_jwt_identity())

    total_tasks = TaskCompletion.query.filter_by(student_id=user_id).count()
    validated = TaskCompletion.query.filter_by(student_id=user_id, is_validated=True).count()
    approved = TaskCompletion.query.filter_by(student_id=user_id, is_validated=True, is_approved=True).count()

    return jsonify({
        "total_completadas": total_tasks,
        "validadas": validated,
        "aprobadas": approved
    }), 200

# RANKING GENERAL DE ALUMNOS
@students_bp.route("/ranking", methods=["GET"])
@jwt_required()
@role_required("alumno")
def ranking():
    students = User.query.filter_by(role="alumno").order_by(User.coins.desc()).all()

    ranking_list = []
    for idx, student in enumerate(students, start=1):
        ranking_list.append({
            "position": idx,
            "username": student.username,
            "coins": student.coins
        })

    return jsonify(ranking_list), 200

# MI POSICIÓN EN EL RANKING
@students_bp.route("/ranking/me", methods=["GET"])
@jwt_required()
@role_required("alumno")
def my_position():
    user_id = int(get_jwt_identity())

    students = User.query.filter_by(role="alumno").order_by(User.coins.desc()).all()
    
    for idx, student in enumerate(students, start=1):
        if student.id == user_id:
            return jsonify({
                "position": idx,
                "username": student.username,
                "coins": student.coins
            }), 200

    return jsonify({"msg": "Alumno no encontrado"}), 404

# ESTADÍSTICAS GLOBALES (solo profesor)
@students_bp.route("/stats", methods=["GET"])
@jwt_required()
@role_required("profesor")
def global_stats():
    total_users = User.query.count()
    total_alumnos = User.query.filter_by(role="alumno").count()
    total_profesores = User.query.filter_by(role="profesor").count()
    total_tareas = Task.query.count()
    total_completadas = TaskCompletion.query.count()
    monedas_totales = db.session.query(db.func.sum(User.coins)).scalar() or 0

    return jsonify({
        "total_usuarios": total_users,
        "total_alumnos": total_alumnos,
        "total_profesores": total_profesores,
        "tareas_creadas": total_tareas,
        "tareas_completadas": total_completadas,
        "monedas_en_sistema": monedas_totales
    }), 200

# ESTADÍSTICAS DE UN ALUMNO POR SU ID (solo profesor)
@students_bp.route("/stats/alumno/<int:alumno_id>", methods=["GET"])
@jwt_required()
@role_required("profesor")
def stats_alumno(alumno_id):
    alumno = User.query.get(alumno_id)
    if not alumno or alumno.role != "alumno":
        return jsonify({"msg": "Alumno no encontrado"}), 404

    tareas_realizadas = TaskCompletion.query.filter_by(student_id=alumno_id, is_approved=True).count()
    monedas_actuales = alumno.coins

    return jsonify({
        "alumno_id": alumno.id,
        "username": alumno.username,
        "first_name": alumno.first_name,
        "last_name": alumno.last_name,
        "email": alumno.email,
        "course": alumno.course,
        "tareas_realizadas": tareas_realizadas,
        "monedas_actuales": monedas_actuales
    }), 200

# ESTADÍSTICAS DE UNA TAREA (solo profesor)
@students_bp.route("/stats/tarea/<int:task_id>", methods=["GET"])
@jwt_required()
@role_required("profesor")
def stats_tarea(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"msg": "Tarea no encontrada"}), 404

    completadas = TaskCompletion.query.filter_by(task_id=task_id).count()
    aprobadas = TaskCompletion.query.filter_by(task_id=task_id, is_approved=True).count()

    return jsonify({
        "task_id": task.id,
        "title": task.title,
        "veces_completada": completadas,
        "veces_aprobada": aprobadas
    }), 200

# EDITAR PERFIL DEL ALUMNO (profesor)
@students_bp.route("/<int:student_id>", methods=["PUT"])
@jwt_required()
@role_required("profesor")
def update_student(student_id):
    data = request.get_json()
    student = User.query.get(student_id)

    if not student or student.role != "alumno":
        return jsonify({"msg": "Alumno no encontrado"}), 404

    # Campos editables
    student.first_name = data.get("first_name", student.first_name)
    student.last_name = data.get("last_name", student.last_name)
    student.email = data.get("email", student.email)
    student.course = data.get("course", student.course)

    db.session.commit()

    return jsonify({"msg": "Alumno actualizado correctamente"}), 200

@students_bp.route("/<int:student_id>", methods=["DELETE"])
@jwt_required()
@role_required("profesor")
def delete_student(student_id):
    student = User.query.get(student_id)

    if not student or student.role != "alumno":
        return jsonify({"msg": "Alumno no encontrado"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({"msg": "Alumno eliminado correctamente"}), 200