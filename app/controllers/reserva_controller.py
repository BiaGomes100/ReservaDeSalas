from flask import Blueprint, jsonify, request, response
from app.Models import reserva
from app.db import db
from app.service.service import TurmaServiceClient

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


@routes_bp.route('/<int:id_reserva>/turma/<int:id_turma>', methods=['GET'])
def obter_reserva_para_turma(id_reserva, id_turma):
    try:
        reserva = reserva.obter_reserva(id_reserva)

        if not TurmaServiceClient.verificar_turma(id_turma):
            return jsonify({'erro': 'Turma não encontrada'}), 404

        return jsonify(reserva.to_dict())
    except reserva.ReservaNotFound:
        return jsonify({'erro': 'Reserva não encontrada'}), 404