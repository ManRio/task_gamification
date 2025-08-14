from app import create_app, db
from app.models import User, Task, TaskCompletion, Reward, RewardRedemption, CoinLog
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Profesor
    profe = User(
        username="profe1",
        password=generate_password_hash("123456"),
        role="profesor",
        first_name="Manuel",
        last_name="Gómez",
        email="profe1@cole.com",
        course="6ºA",
        coins=0
    )
    db.session.add(profe)

    # Alumnos
    alumnos = []
    monedas = [10, 50, 30, 70, 5, 25]
    for i, coins in enumerate(monedas):
        alumno = User(
            username=f"alumno{i+1}",
            password=generate_password_hash("123456"),
            role="alumno",
            first_name=f"Nombre{i+1}",
            last_name=f"Apellido{i+1}",
            email=f"alumno{i+1}@cole.com",
            course="6ºA",
            coins=coins
        )
        alumnos.append(alumno)
        db.session.add(alumno)

    db.session.commit()

    # Tareas creadas por el profesor
    tareas = [
        Task(title="Tarea 1", description="Sumas y restas", reward=10, created_by=profe.id),
        Task(title="Tarea 2", description="Redacción creativa", reward=20, created_by=profe.id),
        Task(title="Tarea 3", description="Mapa de España", reward=15, created_by=profe.id),
        Task(title="Tarea 4", description="Historia siglo XX", reward=25, created_by=profe.id),
        Task(title="Tarea 5", description="El ciclo del agua", reward=5, created_by=profe.id),
    ]
    db.session.add_all(tareas)
    db.session.commit()

    # Completado de tareas (con validated_at en aprobadas/rechazadas)
    completadas = [
        TaskCompletion(
            student_id=alumnos[0].id,
            task_id=tareas[0].id,
            is_validated=True,
            is_approved=True,
            completed_at=datetime.now(timezone.utc) - timedelta(days=3),
            validated_at=datetime.now(timezone.utc) - timedelta(days=3)
        ),
        TaskCompletion(
            student_id=alumnos[1].id,
            task_id=tareas[1].id,
            is_validated=True,
            is_approved=True,
            completed_at=datetime.now(timezone.utc) - timedelta(days=2),
            validated_at=datetime.now(timezone.utc) - timedelta(days=2)
        ),
        TaskCompletion(
            student_id=alumnos[2].id,
            task_id=tareas[2].id,
            is_validated=True,
            is_approved=False,
            completed_at=datetime.now(timezone.utc) - timedelta(days=1),
            validated_at=datetime.now(timezone.utc) - timedelta(days=1)
        ),
        TaskCompletion(
            student_id=alumnos[3].id,
            task_id=tareas[3].id,
            completed_at=datetime.now(timezone.utc) - timedelta(hours=6)
        ),
        TaskCompletion(
            student_id=alumnos[4].id,
            task_id=tareas[4].id,
            completed_at=datetime.now(timezone.utc) - timedelta(hours=1)
        ),
    ]
    db.session.add_all(completadas)
    db.session.commit()

    # Recompensas
    recompensa1 = Reward(name="5 min extra de patio", cost=10, description="Disfruta de un recreo extendido")
    recompensa2 = Reward(name="Escoger juego", cost=20, description="Elige el juego del día")
    db.session.add_all([recompensa1, recompensa2])
    db.session.commit()

    # Canjes de recompensas
    canjes = [
        RewardRedemption(
            student_id=alumnos[1].id,
            reward_id=recompensa1.id,
            redeemed_at=datetime.now(timezone.utc) - timedelta(days=2)
        ),
        RewardRedemption(
            student_id=alumnos[2].id,
            reward_id=recompensa2.id,
            redeemed_at=datetime.now(timezone.utc) - timedelta(days=1)
        ),
    ]
    db.session.add_all(canjes)

    # Ejemplos de asignaciones manuales (CoinLog)
    coin_logs = [
        CoinLog(
            student_id=alumnos[0].id,
            coins=5,
            reason="Participación en clase",
            assigned_by=profe.id,
            timestamp=datetime.now(timezone.utc) - timedelta(hours=5)
        ),
        CoinLog(
            student_id=alumnos[1].id,
            coins=10,
            reason="Ayuda a un compañero",
            assigned_by=profe.id,
            timestamp=datetime.now(timezone.utc) - timedelta(hours=3)
        )
    ]
    db.session.add_all(coin_logs)

    db.session.commit()
    print("✅ Base de datos poblada con éxito.")
    print("👉 Pruebas manuales sugeridas:")
    print("   - GET  /tasks/pending_approval            (como profesor)")
    print("   - POST /tasks/validate/<completion_id>    (aprueba una pendiente)")
    print("   - POST /tasks/reject/<completion_id>      (rechaza una pendiente)")
    print("   - POST /students/add-coins {student_id, coins, reason}")
