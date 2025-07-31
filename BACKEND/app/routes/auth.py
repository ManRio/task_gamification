from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta

from ..models import User
from .. import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data.get("username") or not data.get("password") or not data.get("role"):
        return jsonify({"msg": "Faltan campos requeridos"}), 400

    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"msg": "El nombre de usuario ya está en uso"}), 409

    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        username=data["username"],
        password=hashed_password,
        role=data["role"]
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario registrado exitosamente"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data.get("username") or not data.get("password"):
        return jsonify({"msg": "Faltan campos requeridos"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    # CORREGIDO: solo pasamos el ID como identity y el rol como claim extra
    access_token = create_access_token(
        identity=str(user.id),  # ⚠️ Solo ID
        additional_claims={"role": user.role},  # ⚠️ Role como claim adicional
        expires_delta=timedelta(hours=2)
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    })
