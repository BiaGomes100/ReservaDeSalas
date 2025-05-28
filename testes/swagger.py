from flask_restx import Namespace, Resource, fields

atividades_ns = Namespace("atividades", description="Operações relacionadas às atividades")

atividade_input_model = atividades_ns.model("AtividadeInput", {
    "nome": fields.String(required=True, description="Nome da atividade"),
    "descricao": fields.String(required=True, description="Descrição da atividade"),
    "status": fields.String(required=True, description="Status da atividade (ex: pendente, concluída)"),
})

atividade_output_model = atividades_ns.model("AtividadeOutput", {
    "id": fields.Integer(description="ID da atividade"),
    "nome": fields.String(description="Nome da atividade"),
    "descricao": fields.String(description="Descrição da atividade"),
    "status": fields.String(description="Status da atividade"),
})

atividades_db = []
proximo_id = 1

def adicionar_atividade(data):
    global proximo_id
    nova = {
        "id": proximo_id,
        "nome": data["nome"],
        "descricao": data["descricao"],
        "status": data["status"]
    }
    atividades_db.append(nova)
    proximo_id += 1
    return nova, 201

@atividades_ns.route("/")
class AtividadesResource(Resource):
    @atividades_ns.expect(atividade_input_model)
    @atividades_ns.marshal_with(atividade_output_model, code=201)
    def post(self):
        """Cria uma nova atividade"""
        data = atividades_ns.payload
        return adicionar_atividade(data)