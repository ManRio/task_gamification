from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Reward, User, RewardRedemption
from ..utils.auth_helpers import role_required

rewards_bp = Blueprint("rewards", __name__)

# CREACIÓN DE RECOMPENSAS
@rewards_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required("profesor")
def create_reward():
    data = request.get_json()
    name = data.get("name")
    cost = data.get("cost")
    description = data.get("description")

    if not name or cost is None:
        return jsonify({"msg": "Nombre y coste son requeridos"}), 400

    reward = Reward(name=name, cost=cost, description=description)
    db.session.add(reward)
    db.session.commit()

    return jsonify({"msg": "Recompensa creada correctamente"}), 201

# ELIMINAR UNA RECOMPENSA
@rewards_bp.route("/<int:reward_id>", methods=["DELETE"])
@jwt_required()
@role_required("profesor")
def delete_reward(reward_id):
    reward = Reward.query.get(reward_id)
    if not reward:
        return jsonify({"msg": "Recompensa no encontrada"}), 404

    db.session.delete(reward)
    db.session.commit()
    return jsonify({"msg": "Recompensa eliminada"}), 200

# EDITAR UNA RECOMPENSA
@rewards_bp.route("/<int:reward_id>", methods=["PUT"])
@jwt_required()
@role_required("profesor")
def update_reward(reward_id):
    reward = Reward.query.get(reward_id)
    if not reward:
        return jsonify({"msg": "Recompensa no encontrada"}), 404

    data = request.get_json()
    reward.name = data.get("name", reward.name)
    reward.description = data.get("description", reward.description)
    reward.cost = data.get("cost", reward.cost)

    db.session.commit()
    return jsonify({
        "id": reward.id,
        "name": reward.name,
        "description": reward.description,
        "cost": reward.cost
    }), 200

# HISTORIAL DE CANJES PARA PROFESOR
@rewards_bp.route("/history/all", methods=["GET"])
@jwt_required()
@role_required("profesor")
def full_redemption_history():
    redemptions = RewardRedemption.query.all()
    result = []

    for redemption in redemptions:
        student = User.query.get(redemption.student_id)
        reward = Reward.query.get(redemption.reward_id)

        result.append({
            "id": redemption.id,
            "student_id": student.id,
            "student_name": student.username,
            "reward_name": reward.name,
            "reward_cost": reward.cost,
            "redeemed_at": redemption.redeemed_at.isoformat()
        })

    return jsonify(result), 200

# LISTADO DE RECOMPENSAS
@rewards_bp.route("/list", methods=["GET"])
@jwt_required()
def list_rewards():
    rewards = Reward.query.all()
    return jsonify([
        {
            "id": reward.id,
            "name": reward.name,
            "cost": reward.cost,
            "description": reward.description
        } for reward in rewards
    ]), 200

# CANJEO DE RECOMPENSAS
@rewards_bp.route("/redeem/<int:reward_id>", methods=["POST"])
@jwt_required()
@role_required("alumno")
def redeem_reward(reward_id):
    user_id = int(get_jwt_identity())

    # Obtener al alumno y la recompensa
    student = User.query.get(user_id)
    reward = Reward.query.get(reward_id)

    if not reward:
        return jsonify({"msg": "Recompensa no encontrada"}), 404

    if student.coins < reward.cost:
        return jsonify({"msg": "No tienes suficientes monedas"}), 400

    # Descontar monedas y guardar
    student.coins -= reward.cost
    redemption = RewardRedemption(student_id=student.id, reward_id=reward.id)
    db.session.add(redemption)
    db.session.commit()

    return jsonify({
        "msg": "Recompensa canjeada correctamente",
        "monedas_restantes": student.coins
    }), 200

# HISTORIAL CANJEO DE RECOMPENSAS POR ALUMNO
@rewards_bp.route("/history", methods=["GET"])
@jwt_required()
@role_required("alumno")
def redemption_history():
    user_id = int(get_jwt_identity())

    redemptions = RewardRedemption.query.filter_by(student_id=user_id).all()

    result = []
    for redemption in redemptions:
        reward = Reward.query.get(redemption.reward_id)
        result.append({
            "id": redemption.id,                 # ← añade id
            "reward_name": reward.name,          # ← nombres coherentes con el front
            "reward_cost": reward.cost,
            "redeemed_at": redemption.redeemed_at.isoformat()
        })
    return jsonify(result), 200                  # ← NO [result]

# ELIMINAR UN CANJE DE RECOMPENSA (SÓLO PROFESOR)
@rewards_bp.route("/delete-redemption/<int:redemption_id>", methods=["DELETE"])
@jwt_required()
@role_required("profesor")
def delete_redemption(redemption_id):
    redemption = RewardRedemption.query.get(redemption_id)
    if not redemption:
        return jsonify({"msg": "Canje no encontrado"}), 404

    student = User.query.get(redemption.student_id)
    reward = Reward.query.get(redemption.reward_id)

    if not student or not reward:
        return jsonify({"msg": "Datos asociados no válidos"}), 400

    # Devolver las monedas
    student.coins += reward.cost

    # Eliminar el canje
    db.session.delete(redemption)
    db.session.commit()

    return jsonify({"msg": "Canje eliminado y monedas devueltas"}), 200

# --- ALIAS PARA COMPATIBILIDAD CON EL FRONT (/rewards/history/me) ---
@rewards_bp.route("/history/me", methods=["GET"])
@jwt_required()
@role_required("alumno")
def history_me_alias():
    return redemption_history()
