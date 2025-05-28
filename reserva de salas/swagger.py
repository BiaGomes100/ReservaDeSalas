from flask_restx import Namespace, Resource, fields

reservas_ns = Namespace("reservas", description="Operações relacionadas às reservas de salas")

reserva_input_model = reservas_ns.model("ReservaInput", {
    "sala": fields.String(required=True, description="Número da sala"),
    "data": fields.String(required=True, description="Data da reserva (YYYY-MM-DD)"),
    "horario_inicio": fields.String(required=True, description="Horário de início (HH:MM)"),
    "horario_fim": fields.String(required=True, description="Horário de fim (HH:MM)"),
    "usuario": fields.String(required=True, description="Nome do usuário que reservou"),
})

reserva_output_model = reservas_ns.model("ReservaOutput", {
    "id": fields.Integer(description="ID da reserva"),
    "sala": fields.String(description="Número da sala"),
    "data": fields.String(description="Data da reserva"),
    "horario_inicio": fields.String(description="Horário de início"),
    "horario_fim": fields.String(description="Horário de fim"),
    "usuario": fields.String(description="Usuário que reservou"),
})

mensagem_sucesso_model = reservas_ns.model("MensagemSucesso", {
    "mensagem": fields.String(example="Reserva criada com sucesso")
})

mensagem_erro_model = reservas_ns.model("MensagemErro", {
    "erro": fields.String(example="Horário conflitante com outra reserva")
})


reservas = []
contador = 1

@reservas_ns.route("/")
class ReservasResource(Resource):
    @reservas_ns.doc("listar_reservas")
    @reservas_ns.marshal_list_with(reserva_output_model)
    def get(self):
        """Lista todas as reservas"""
        return reservas

    @reservas_ns.doc("criar_reserva")
    @reservas_ns.expect(reserva_input_model)
    @reservas_ns.response(201, "Reserva criada com sucesso", modelo=mensagem_sucesso_model)
    @reservas_ns.response(400, "Campo obrigatório faltando", modelo=mensagem_erro_model)
    @reservas_ns.response(409, "Conflito de horário", modelo=mensagem_erro_model)
    def post(self):
        """Cria uma nova reserva"""
        global contador
        data = reservas_ns.payload

        campos_obrigatorios = ["sala", "data", "horario_inicio", "horario_fim", "usuario"]
        for campo in campos_obrigatorios:
            if campo not in data:
                return {"erro": f"Campo '{campo}' está faltando"}, 400

        for r in reservas:
            if r["sala"] == data["sala"] and r["data"] == data["data"]:
                if not (data["horario_fim"] <= r["horario_inicio"] or data["horario_inicio"] >= r["horario_fim"]):
                    return {"erro": "Conflito de horário com outra reserva"}, 409

        nova = data.copy()
        nova["id"] = contador
        contador += 1
        reservas.append(nova)
        return {"mensagem": "Reserva criada com sucesso", "reserva": nova}, 201

@reservas_ns.route("/<int:id>")
class CancelarReservaResource(Resource):
    @reservas_ns.response(200, "Reserva cancelada com sucesso")
    @reservas_ns.response(404, "Reserva não encontrada")
    def delete(self, id):
        """Cancela uma reserva pelo ID"""
        global reservas
        for r in reservas:
            if r["id"] == id:
                reservas = [res for res in reservas if res["id"] != id]
                return {"mensagem": "Reserva cancelada com sucesso"}, 200
        return {"erro": "Reserva não encontrada"}, 404