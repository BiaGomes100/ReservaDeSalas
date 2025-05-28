import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_reserva_sucesso(client):
    reserva = {
        "sala": "101",
        "data": "2025-06-01",
        "horario_inicio": "14:00",
        "horario_fim": "15:00",
        "usuario": "thayane"
    }
    resp = client.post('/reservas', json=reserva)
    assert resp.status_code == 201
    assert resp.get_json()["mensagem"] == "Reserva criada com sucesso"

def test_reserva_com_campo_faltando(client):
    reserva = {
        "sala": "101",
        "data": "2025-06-01",
        "horario_inicio": "14:00",
        "usuario": "thayane"
    }
    resp = client.post('/reservas', json=reserva)
    assert resp.status_code == 400
    assert "faltando" in resp.get_json()["erro"]

def test_reserva_com_conflito_de_horario(client):
    reserva1 = {
        "sala": "101",
        "data": "2025-06-01",
        "horario_inicio": "14:00",
        "horario_fim": "15:00",
        "usuario": "thayane"
    }
    client.post('/reservas', json=reserva1)

    reserva2 = {
        "sala": "101",
        "data": "2025-06-01",
        "horario_inicio": "14:30",
        "horario_fim": "15:30",
        "usuario": "joao"
    }
    resp = client.post('/reservas', json=reserva2)
    assert resp.status_code == 409
    assert "Conflito" in resp.get_json()["erro"]

def test_listar_reservas(client):
    reserva = {
        "sala": "201",
        "data": "2025-06-02",
        "horario_inicio": "10:00",
        "horario_fim": "11:00",
        "usuario": "ana"
    }
    client.post('/reservas', json=reserva)
    resp = client.get('/reservas')
    assert resp.status_code == 200
    lista = resp.get_json()
    assert any(r["sala"] == "201" for r in lista)

def test_cancelar_reserva(client):
    reserva = {
        "sala": "102",
        "data": "2025-06-03",
        "horario_inicio": "09:00",
        "horario_fim": "10:00",
        "usuario": "bia"
    }
    resp = client.post('/reservas', json=reserva)
    reserva_id = resp.get_json()["reserva"]["id"]

    delete_resp = client.delete(f'/reservas/{reserva_id}')
    assert delete_resp.status_code == 200
    assert "cancelada" in delete_resp.get_json()["mensagem"]