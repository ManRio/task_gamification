# 🏆 Plataforma de Gamificación Educativa

Una aplicación web construida con Flask que permite a profesores crear tareas para sus alumnos, asignar recompensas por su cumplimiento, y fomentar la motivación a través de rankings y estadísticas personalizadas.

---

## ⚙️ Tecnologías utilizadas

- **Python 3** + **Flask**
- **Flask-JWT-Extended** – Autenticación con tokens JWT
- **SQLAlchemy** – ORM para la base de datos
- **Flask-Migrate** – Migraciones con Alembic
- **SQLite** – Base de datos local
- **Flask-CORS** – Habilita CORS para el frontend

---

## 📂 Estructura de directorios

```
flask_gamification_app/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── utils/
│   │   └── auth_helpers.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   ├── students.py
│   │   └── rewards.py
│
├── migrations/
├── run.py
└── README.md
```

---

## 🔐 Autenticación y Roles

- Registro y login con contraseña hasheada
- Roles: `profesor` y `alumno`
- JWT con claims personalizados para control de acceso
- Decorador `@role_required` para proteger endpoints por rol

---

## 📦 Endpoints principales

### 🔐 Autenticación (`/api/auth`)
| Método | Ruta          | Descripción            |
|--------|---------------|------------------------|
| POST   | `/register`   | Registro de usuario    |
| POST   | `/login`      | Login con JWT          |

---

### ✅ Tareas (`/api/tasks`)
| Método | Ruta                     | Rol       | Descripción                         |
|--------|--------------------------|-----------|-------------------------------------|
| POST   | `/create`                | Profesor  | Crear nueva tarea                   |
| GET    | `/`                      | Todos     | Ver todas las tareas                |
| GET    | `/mine`                  | Profesor  | Ver tareas creadas por el profesor  |
| POST   | `/complete/<id>`         | Alumno    | Completar tarea                     |
| GET    | `/completed`             | Alumno    | Ver tareas completadas              |
| PATCH  | `/validate/<id>`         | Profesor  | Validar/aprobar tarea               |

---

### 🎓 Alumnos (`/api/students`)
| Método | Ruta                            | Rol       | Descripción                         |
|--------|----------------------------------|-----------|-------------------------------------|
| POST   | `/create`                        | Profesor  | Crear nuevo alumno                  |
| DELETE | `/<id>`                          | Profesor  | Eliminar alumno                     |
| GET    | `/all`                           | Profesor  | Listar todos los alumnos            |
| GET    | `/me`                            | Alumno    | Ver perfil propio                   |
| GET    | `/stats`                         | Alumno    | Estadísticas personales             |
| GET    | `/ranking`                       | Alumno    | Ver ranking general                 |
| GET    | `/ranking/me`                    | Alumno    | Ver posición personal               |
| GET    | `/stats`                         | Profesor  | Estadísticas globales del sistema   |
| GET    | `/stats/alumno/<id>`             | Profesor  | Estadísticas de un alumno           |
| GET    | `/stats/tarea/<task_id>`         | Profesor  | Estadísticas de una tarea           |

---

### 🎁 Recompensas (`/api/rewards`)
| Método | Ruta                              | Rol       | Descripción                         |
|--------|-----------------------------------|-----------|-------------------------------------|
| POST   | `/create`                         | Profesor  | Crear nueva recompensa              |
| GET    | `/list`                           | Todos     | Ver lista de recompensas            |
| POST   | `/redeem/<reward_id>`             | Alumno    | Canjear recompensa                  |
| GET    | `/history`                        | Alumno    | Historial de canjes                 |
| DELETE | `/delete-redemption/<id>`         | Profesor  | Eliminar canje (reintegro monedas)  |

---

## 🧪 Ejecución local

1. Clona el repositorio:
```bash
git clone https://github.com/tu_usuario/flask_gamification_app.git
cd flask_gamification_app
```

2. Crea entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala dependencias:
```bash
pip install -r requirements.txt
```

4. Inicializa la base de datos:
```bash
flask db init
flask db migrate -m "Inicial"
flask db upgrade
```

5. Ejecuta el servidor:
```bash
python run.py
```

---

## ✨ Próximos pasos

- 🔧 Construcción del **frontend en Vue.js**
- 📊 Paneles de profesor y alumno
- 📱 Interfaz responsiva y accesible

---

## 📄 Licencia

MIT License – libre para usar, modificar y distribuir.

---

## 🙌 Autor

Desarrollado por ManRio
🚀 Proyecto educativo de gamificación