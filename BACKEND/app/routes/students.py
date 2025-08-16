from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from .. import db
from ..models import User, TaskCompletion, Task, CoinLog
from ..utils.auth_helpers import role_required

students_bp = Blueprint("students", __name__)

# ----------------------- CRUD / STATS / RANKINGS -----------------------

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


@students_bp.route("/all", methods=["GET"])
@jwt_required()
@role_required("profesor")
def list_all_students():
    students = User.query.filter_by(role="alumno").all()
    return jsonify([
        {
            "id": s.id, "username": s.username,
            "first_name": s.first_name, "last_name": s.last_name,
            "email": s.email, "course": s.course, "coins": s.coins
        } for s in students
    ]), 200


@students_bp.route("/me", methods=["GET"])
@jwt_required()
@role_required("alumno")
def view_profile():
    user_id = int(get_jwt_identity())
    student = User.query.get(user_id)
    if not student:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    return jsonify({
        "id": student.id, "username": student.username,
        "first_name": student.first_name, "last_name": student.last_name,
        "email": student.email, "course": student.course,
        "role": student.role, "coins": student.coins
    }), 200


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


@students_bp.route("/ranking", methods=["GET"])
@jwt_required()
@role_required("alumno")
def ranking():
    students = User.query.filter_by(role="alumno").order_by(User.coins.desc()).all()
    return jsonify([
        {"position": idx, "username": s.username, "coins": s.coins}
        for idx, s in enumerate(students, start=1)
    ]), 200


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


@students_bp.route("/stats/alumno/<int:alumno_id>", methods=["GET"])
@jwt_required()
@role_required("profesor")
def stats_alumno(alumno_id):
    alumno = User.query.get(alumno_id)
    if not alumno or alumno.role != "alumno":
        return jsonify({"msg": "Alumno no encontrado"}), 404

    tareas_realizadas = TaskCompletion.query.filter_by(student_id=alumno_id, is_approved=True).count()
    return jsonify({
        "alumno_id": alumno.id, "username": alumno.username,
        "first_name": alumno.first_name, "last_name": alumno.last_name,
        "email": alumno.email, "course": alumno.course,
        "tareas_realizadas": tareas_realizadas,
        "monedas_actuales": alumno.coins
    }), 200


@students_bp.route("/stats/tarea/<int:task_id>", methods=["GET"])
@jwt_required()
@role_required("profesor")
def stats_tarea(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({"msg": "Tarea no encontrada"}), 404

    completadas = TaskCompletion.query.filter_by(task_id=task_id).count()
    aprobadas = TaskCompletion.query.filter_by(task_id=task_id, is_approved=True).count()
    return jsonify({
        "task_id": task.id, "title": task.title,
        "veces_completada": completadas, "veces_aprobada": aprobadas
    }), 200


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


@students_bp.route("/ranking/all", methods=["GET"])
@jwt_required()
@role_required("profesor")
def ranking_profesor():
    students = User.query.filter_by(role="alumno").order_by(User.coins.desc()).all()
    return jsonify([
        {"position": idx, "username": s.username, "coins": s.coins}
        for idx, s in enumerate(students, start=1)
    ]), 200


# ----------------------- ASIGNACIÓN MANUAL + FEEDS -----------------------

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

    student = db.session.get(User, student_id)
    if not student or student.role != "alumno":
        return jsonify({"msg": "Alumno no encontrado"}), 404

    student.coins += coins

    admin_id = int(get_jwt_identity())
    db.session.add(CoinLog(
        student_id=student.id,
        coins=coins,
        reason=reason or "asignación manual",
        assigned_by=admin_id
    ))

    db.session.commit()
    return jsonify({
        "msg": "Monedas asignadas correctamente",
        "student_id": student.id,
        "new_balance": student.coins
    }), 200


# Feed global para profesor (ya lo tenías)
@students_bp.route("/coin-events", methods=["GET"])
@jwt_required()
@role_required("profesor")
def coin_events():
    try:
        limit = int(request.args.get("limit", 10))
    except ValueError:
        limit = 10

    events = []

    ts_col = TaskCompletion.validated_at if hasattr(TaskCompletion, "validated_at") else TaskCompletion.completed_at
    rows = db.session.query(
        TaskCompletion.id.label("completion_id"),
        TaskCompletion.student_id.label("student_id"),
        User.username.label("username"),
        Task.title.label("task_title"),
        Task.reward.label("coins"),
        ts_col.label("ts"),
    ).join(User, User.id == TaskCompletion.student_id
    ).join(Task, Task.id == TaskCompletion.task_id
    ).filter(
        TaskCompletion.is_validated == True,
        TaskCompletion.is_approved == True
    ).order_by(ts_col.desc()
    ).limit(limit * 2).all()

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

    events.sort(key=lambda e: e["timestamp"], reverse=True)
    return jsonify(events[:limit]), 200


# NUEVO: feed personal del alumno
@students_bp.route("/coin-events/me", methods=["GET"])
@jwt_required()
@role_required("alumno")
def my_coin_events():
    user_id = int(get_jwt_identity())
    try:
        limit = int(request.args.get("limit", 10))
    except ValueError:
        limit = 10

    events = []

    ts_col = TaskCompletion.validated_at if hasattr(TaskCompletion, "validated_at") else TaskCompletion.completed_at
    rows = db.session.query(
        TaskCompletion.id.label("completion_id"),
        Task.title.label("task_title"),
        Task.reward.label("coins"),
        ts_col.label("ts"),
    ).join(Task, Task.id == TaskCompletion.task_id
    ).filter(TaskCompletion.student_id == user_id,
             TaskCompletion.is_validated == True,
             TaskCompletion.is_approved == True
    ).order_by(ts_col.desc()).limit(limit * 2).all()

    for r in rows:
        ts = r.ts or datetime.now(timezone.utc)
        events.append({
            "type": "task",
            "timestamp": ts.isoformat(),
            "coins": r.coins,
            "detail": r.task_title
        })

    mrows = db.session.query(
        CoinLog.coins, CoinLog.reason, CoinLog.timestamp
    ).filter(CoinLog.student_id == user_id
    ).order_by(CoinLog.timestamp.desc()).limit(limit * 2).all()

    for c, reason, ts in mrows:
        ts = ts or datetime.now(timezone.utc)
        events.append({
            "type": "manual",
            "timestamp": ts.isoformat(),
            "coins": c,
            "detail": reason or "asignación manual"
        })

    events.sort(key=lambda e: e["timestamp"], reverse=True)
    return jsonify(events[:limit]), 200

# --- ALIAS PARA COMPATIBILIDAD CON EL FRONT (/students/stats/me) ---
@students_bp.route("/stats/me", methods=["GET"])
@jwt_required()
@role_required("alumno")
def stats_me_alias():
    # reutiliza la función real
    return view_stats()

# --- RESUMEN PARA DASHBOARD DEL ALUMNO ---
from datetime import datetime, timezone
from ..models import RewardRedemption, Reward, Task, TaskCompletion, User

@students_bp.route("/summary", methods=["GET"])
@jwt_required()
@role_required("alumno")
def student_summary():
    user_id = int(get_jwt_identity())
    try:
        limit = int(request.args.get("limit", 5))
    except ValueError:
        limit = 5

    student = db.session.get(User, user_id)
    coins = student.coins if student else 0

    # Tareas aprobadas
    ts_col = TaskCompletion.validated_at if hasattr(TaskCompletion, "validated_at") else TaskCompletion.completed_at
    tasks_q = db.session.query(
        TaskCompletion.id.label("completion_id"),
        Task.title.label("task_title"),
        Task.reward.label("task_reward"),
        ts_col.label("ts"),
    ).join(Task, Task.id == TaskCompletion.task_id
    ).filter(
        TaskCompletion.student_id == user_id,
        TaskCompletion.is_validated == True,
        TaskCompletion.is_approved == True
    ).order_by(ts_col.desc())

    tasks_completed = tasks_q.count()
    tasks_rows = tasks_q.limit(limit).all()

    ultimas_tareas = [{
        "id": r.completion_id,
        "task_title": r.task_title,
        "task_reward": r.task_reward,
        "completed_at": (r.ts or datetime.now(timezone.utc)).isoformat()
    } for r in tasks_rows]

    # Canjes
    red_q = db.session.query(
        RewardRedemption.id.label("id"),
        Reward.name.label("reward_name"),
        Reward.cost.label("reward_cost"),
        RewardRedemption.redeemed_at.label("redeemed_at"),
    ).join(Reward, Reward.id == RewardRedemption.reward_id
    ).filter(RewardRedemption.student_id == user_id
    ).order_by(RewardRedemption.redeemed_at.desc())

    rewards_redeemed = red_q.count()
    red_rows = red_q.limit(limit).all()

    ultimos_canjes = [{
        "id": r.id,
        "reward_name": r.reward_name,
        "reward_cost": r.reward_cost,
        "redeemed_at": (r.redeemed_at or datetime.now(timezone.utc)).isoformat()
    } for r in red_rows]

    return jsonify({
        "estadisticas": {
            "coins": coins,
            "tasks_completed": tasks_completed,
            "rewards_redeemed": rewards_redeemed
        },
        "ultimasTareas": ultimas_tareas,
        "ultimosCanjes": ultimos_canjes
    }), 200

