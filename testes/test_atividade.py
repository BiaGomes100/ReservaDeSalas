import pytest
import json
from app import create_app  

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_criar_atividade(client):
    nova_atividade = {
        "nome": "Estudar Pytest",
        "descricao": "Aprender a testar APIs com Pytest",
        "status": "pendente"
    }

    response = client.post('/atividades', data=json.dumps(nova_atividade), content_type='application/json')

    assert response.status_code == 201

    dados_resposta = response.get_json()
    assert dados_resposta['nome'] == nova_atividade['nome']
    assert dados_resposta['descricao'] == nova_atividade['descricao']
    assert dados_resposta['status'] == nova_atividade['status']