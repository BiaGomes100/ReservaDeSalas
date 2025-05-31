from flask import Blueprint, jsonify, request
from Models.reserva import (
    Reserva,
    criar_reserva,
    existe_reserva,
    obter_reserva,
    excluir_reserva,
    ReservaNotFound,
)
from service.service import TurmaServiceClient

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/reservas", methods=["POST"])
def solicitar_reserva():
    data = request.json
    try:
        nova_reserva = criar_reserva(data)
        return jsonify(nova_reserva.to_dict()), 201
    except ReservaNotFound as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor"}), 500

@routes_bp.route("/reservas", methods=["GET"])
def listar_reservas():
    reservas = Reserva.query.all()
    return jsonify([r.to_dict() for r in reservas]), 200

@routes_bp.route("/reservas/verificar/<sala>/<data>/<hora_inicio>", methods=["GET"])
def verificar_reserva(sala, data, hora_inicio):
    existe = existe_reserva(sala, data, hora_inicio)
    return jsonify({"reserva": existe}), 200

@routes_bp.route('/reservas/<int:id_reserva>', methods=['DELETE'])
def delete_reserva(id_reserva):
    sucesso = excluir_reserva(id_reserva)
    if sucesso:
        return jsonify({"mensagem": "Reserva excluída com sucesso"}), 202
    else:
        return jsonify({"mensagem": "Reserva não encontrada"}), 404

@routes_bp.route('/<int:id_reserva>/turma/<int:id_turma>', methods=['GET'])
def obter_reserva_para_turma(id_reserva, id_turma):
    try:
        reserva = obter_reserva(id_reserva)

        if not TurmaServiceClient.verificar_turma(id_turma):
            return jsonify({'erro': 'Turma não encontrada'}), 404

        return jsonify(reserva.to_dict()), 200
    except ReservaNotFound:
        return jsonify({'erro': 'Reserva não encontrada'}), 404
    except Exception:
        return jsonify({'erro': 'Erro interno do servidor'}), 500
