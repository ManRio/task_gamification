from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from .. import db
from ..models import User, TaskCompletion, Task
from ..utils.auth_helpers import role_required
from datetime import datetime, timezone

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
            "id": s.id,
            "username": s.username,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "email": s.email,
            "course": s.course,
            "coins": s.coins
        } for s in students
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

# RANKING GENERAL DE ALUMNOS (vista alumno)
@students_bp.route("/ranking", methods=["GET"])
@jwt_required()
@role_required("alumno")
def ranking():
    students = User.query.filter_by(role="alumno").order_by(User.coins.desc()).all()
    return jsonify([
        {"position": idx, "username": s.username, "coins": s.coins}
        for idx, s in enumerate(students, start=1)
    ]), 200

# MI POSICIÓN EN EL RANKING
@students_bp.route("/ranking/me", methods=["GET"])
@jwt_required()
@role_required("alumno")
def my_position():
    user_id = int(get_jwt_identity())
    students = User.query.filter_by(role="alumno").order_by(User.coins.desc()).all()
    for idx, s in enumerate(students, start=1):
        if s.id == user_id:
            return jsonify({"position": idx, "username": s.username, "coins": s.coins}), 200
    return jsonify({"msg": "Alumno no encontrado"}), 404

# ESTADÍSTICAS GLOBALES (solo profesor)
@students_bp.route("/stats/global", methods=["GET"])
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
    return jsonify({
        "alumno_id": alumno.id,
        "username": alumno.username,
        "first_name": alumno.first_name,
        "last_name": alumno.last_name,
        "email": alumno.email,
        "course": alumno.course,
        "tareas_realizadas": tareas_realizadas,
        "monedas_actuales": alumno.coins
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

# RANKING GENERAL DE ALUMNOS (para el profesor)
@students_bp.route("/ranking/all", methods=["GET"])
@jwt_required()
@role_required("profesor")
def ranking_profesor():
    students = User.query.filter_by(role="alumno").order_by(User.coins.desc()).all()
    return jsonify([
        {"position": idx, "username": s.username, "coins": s.coins}
        for idx, s in enumerate(students, start=1)
    ]), 200

# ASIGNAR MONEDAS MANUALMENTE (solo profesor)
@students_bp.route("/add-coins", methods=["POST"])
@jwt_required()
@role_required("profesor")
def add_coins():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    coins = data.get("coins")
    reason = (data.get("reason") or "").strip()

    if not isinstance(student_id, int) or not isinstance(coins, int):
        return jsonify({"msg": "Campos 'student_id' (int) y 'coins' (int) requeridos"}), 400
    if coins <= 0:
        return jsonify({"msg": "El número de monedas debe ser mayor que 0"}), 400

    student = User.query.get(student_id)
    if not student or student.role != "alumno":
        return jsonify({"msg": "Alumno no encontrado"}), 404

    student.coins += coins

    # (Opcional) registrar en CoinLog si existe el modelo
    try:
        from ..models import CoinLog  # si no existe, este import fallará
        admin_id = int(get_jwt_identity())
        log = CoinLog(
            student_id=student.id,
            coins=coins,
            reason=reason or "asignación manual",
            assigned_by=admin_id,
        )
        db.session.add(log)
    except Exception:
        # Silencioso si no existe CoinLog; no interrumpe la asignación de monedas
        pass

    db.session.commit()
    return jsonify({
        "msg": "Monedas asignadas correctamente",
        "student_id": student.id,
        "new_balance": student.coins
    }), 200

@students_bp.route("/coin-events", methods=["GET"])
@jwt_required()
@role_required("profesor")
def coin_events():
    """Últimos movimientos de monedas (aprobaciones de tareas + asignaciones manuales)."""
    try:
        limit = int(request.args.get("limit", 10))
    except ValueError:
        limit = 10

    events = []

    # ---- Aprobaciones de tareas ----
    # Nota: usamos completed_at como timestamp de referencia (si tienes validated_at, úsalo).
    rows = db.session.query(
        TaskCompletion.id.label("completion_id"),
        TaskCompletion.student_id.label("student_id"),
        User.username.label("username"),
        Task.title.label("task_title"),
        Task.reward.label("coins"),
        TaskCompletion.completed_at.label("ts"),
    ).join(User, User.id == TaskCompletion.student_id
    ).join(Task, Task.id == TaskCompletion.task_id
    ).filter(
        TaskCompletion.is_validated == True,
        TaskCompletion.is_approved == True
    ).order_by(TaskCompletion.completed_at.desc()
    ).limit(limit * 2).all()  # pedimos un poco más por si luego mezclamos con manuales

    for r in rows:
        ts = r.ts or datetime.now(timezone.utc)
        events.append({
            "type": "task",
            "timestamp": ts.isoformat(),
            "student_id": r.student_id,
            "username": r.username,
            "coins": r.coins,
            "detail": r.task_title,
            "ref": f"completion:{r.completion_id}"
        })

    # ---- Asignaciones manuales (si existe CoinLog) ----
    try:
        from ..models import CoinLog
        mrows = db.session.query(
            CoinLog.id.label("log_id"),
            CoinLog.student_id.label("student_id"),
            User.username.label("username"),
            CoinLog.coins.label("coins"),
            CoinLog.reason.label("reason"),
            CoinLog.timestamp.label("ts"),
        ).join(User, User.id == CoinLog.student_id
        ).order_by(CoinLog.timestamp.desc()
        ).limit(limit * 2).all()

        for r in mrows:
            ts = r.ts or datetime.now(timezone.utc)
            events.append({
                "type": "manual",
                "timestamp": ts.isoformat(),
                "student_id": r.student_id,
                "username": r.username,
                "coins": r.coins,
                "detail": r.reason or "asignación manual",
                "ref": f"coinlog:{r.log_id}"
            })
    except Exception:
        # Si no hay CoinLog, simplemente omitimos manuales
        pass

    # Mezcla y recorte final
    events.sort(key=lambda e: e["timestamp"], reverse=True)
    events = events[:limit]

    return jsonify(events), 200