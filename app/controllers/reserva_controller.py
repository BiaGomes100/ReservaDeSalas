from flask import Blueprint, jsonify, request, response
from app.Models import reserva
from app.database import db

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/reservas", methods=["POST"])
def solicitar_reserva(data):
    data = request.json
    reserva.criar_reserva(data)
    return jsonify(response), 201

@routes_bp.route("/reservas", methods=["GET"])
def listar_reservas():
    return reserva.query.all()

@routes_bp.route("/reservas/verificar/<sala>/<data>/<hora_inicio>", methods=["GET"])
def verificar_reserva(sala, data, hora_inicio):
    if reserva.existe_reserva(sala, data, hora_inicio):
        return jsonify({"reserva": True})
    else:
        return jsonify({"reserva": False})
    
@routes_bp.route('/reservas/<int:id_turma>', methods=['DELETE'])
def delete_reserva(id_turma):    
    if reserva.excluir_reserva(id_turma):
        return jsonify({"Reserva excluída": True}), 202
    else:
        return jsonify({"Reserva excluída": False}), 204


