# 🎮 Gamification App

Aplicación de gamificación educativa que permite a profesores asignar tareas a sus alumnos, y a los alumnos ganar monedas virtuales al completarlas. Estas monedas pueden ser canjeadas por recompensas, fomentando la participación y el aprendizaje activo.

---

## 📁 Estructura del proyecto

```bash
gamification-app/
│
├── backend/          # API RESTful en Flask
│   ├── app/          # Modelos, rutas y lógica de negocio
│   ├── migrations/   # Archivos de migración de la base de datos
│   ├── run.py        # Punto de entrada de la app
│   ├── requirements.txt
│   └── README.md     # Instrucciones específicas del backend
│
├── frontend/         # Aplicación web (Vue, próximamente)
│   ├── src/
│   ├── public/
│   └── README.md     # Instrucciones específicas del frontend
│
└── README.md         # Este archivo
```

---

## 🧩 Funcionalidades principales

### 👨‍🏫 Profesores

- Crear, listar y validar tareas completadas por los alumnos.
- Crear y administrar recompensas.
- Ver estadísticas globales, por alumno o por tarea.
- Registrar y eliminar alumnos desde el panel.
- Ver historial de canjes y revertirlos si es necesario.

### 🧑‍🎓 Alumnos

- Completar tareas asignadas.
- Consultar historial de tareas completadas.
- Canjear monedas por recompensas.
- Ver estadísticas personales.
- Consultar su posición en el ranking.

---

## 🔧 Tecnologías utilizadas

- **Backend**: Flask, SQLAlchemy, Flask-JWT-Extended, Flask-Migrate, SQLite
- **Frontend**: Vue 3 (próximamente)
- **Autenticación**: JWT (Token-Based)
- **ORM**: SQLAlchemy
- **Base de datos**: SQLite (desarrollo)

---

## 🚀 Cómo empezar

### Requisitos

- Python 3.10+
- Node.js (cuando el frontend esté disponible)

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/gamification-app.git
cd gamification-app
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
flask db upgrade
flask run
```

> Más detalles en `backend/README.md`.

### 3. Frontend

Próximamente en la carpeta `/frontend`.

---

## 📌 Estado del proyecto

✅ Backend funcional  
🚧 Frontend en desarrollo (Vue 3)

---

## 🤝 Contribución

¡Pull requests y sugerencias son bienvenidas!

---

## 📜 Licencia

MIT © 2025 - ManRio
