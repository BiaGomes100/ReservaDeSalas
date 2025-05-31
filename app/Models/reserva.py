from db import db
from flask import Blueprint, jsonify
import requests

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    turma_id = db.Column(db.Integer, nullable=False)
    sala = db.Column(db.String(50), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    hora_inicio = db.Column(db.String(10), nullable=False)
    hora_fim = db.Column(db.String(10), nullable=False)

    def __init__(self, turma_id,sala, data, hora_inicio,hora_fim):
        self.turma_id = turma_id
        self.sala = sala
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim

    def to_dict(self):
        return {
            'id': self.id,
            'turma_id': self.turma_id,
            'sala': self.sala,
            'data': self.data,
            'hora_inicio': self.hora_inicio,
            'hora_fim': self.hora_fim
        }



routes = Blueprint("routes", __name__)

class ReservaNotFound(Exception):
    pass

def validar_turma(turma_id):
    resp = requests.get(f"http://localhost:8000/api/turmas/{turma_id}") #URL da nossa aplicação
    return resp.status_code == 200



def criar_reserva(reserva_data):
    turma_id = reserva_data.get("turma_id")

    if not validar_turma(turma_id):
        raise ReservaNotFound("Turma não encontrada")

    reserva_nova = Reserva(
        turma_id=reserva_data['turma_id'],
        sala=reserva_data['sala'],
        data=reserva_data['data'],
        hora_inicio=reserva_data['hora_inicio'],
        hora_fim=reserva_data['hora_fim']
    )

    db.session.add(reserva_nova)
    db.session.commit()

    return reserva_nova 

def listar_reservas():
    reservas = Reserva.query.all()
    return jsonify([r.to_dict() for r in reservas])

def obter_reserva(id_reserva):
    reserva = Reserva.query.get(id_reserva)
    if not reserva:
        raise ReservaNotFound()
    return reserva

def existe_reserva(sala, data, hora_inicio):
    return Reserva.query.filter_by(sala=sala, data=data, hora_inicio=hora_inicio).first() is not None


def excluir_reserva(id_reserva):
    reserva = Reserva.query.get(id_reserva)
    if not reserva:
        return False
    db.session.delete(reserva)
    db.session.commit()
    return True