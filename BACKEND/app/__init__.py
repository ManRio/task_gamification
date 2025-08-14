from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta



db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gamification.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "clave-secreta-super-importante"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)  # o 24h, lo que prefieras

    db.init_app(app)
    jwt.init_app(app)
    CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
        }
    },
    supports_credentials=True,   # no molesta aunque uses Bearer
)

    from .routes.auth import auth_bp
    from .routes.tasks import tasks_bp
    from .routes.students import students_bp
    from .routes.rewards import rewards_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(students_bp, url_prefix="/api/students")
    app.register_blueprint(rewards_bp, url_prefix="/api/rewards")

    with app.app_context():
        db.create_all()

    return app
