import requests

TURMA_SERVICE_URL = "http://localhost:8000/api/turma"

class TurmaServiceClient:
    @staticmethod
    def verificar_turma(id_turma):
        url = f"{TURMA_SERVICE_URL}/{id_turma}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('turma', False)
        except requests.RequestException as e:
            print(f"Erro ao acessar o turma_service: {e}")
            return False