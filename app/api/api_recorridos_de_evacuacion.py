from flask import Blueprint, request
from flask.json import jsonify
from app.helpers.paginator import Paginator
from app.models.evacuation_route import Evacuation_Route
from app.schemas.EvacuationRouteSchema import eroutes_schema

api_recorridos_de_evacuacion = Blueprint("recorridos_evacuacion", __name__, url_prefix="/recorridos_evacuacion")

@api_recorridos_de_evacuacion.get("/")
def get():
    page = request.args.get("page", 1, type=int)

    recorridos = eroutes_schema.dump(Paginator.paginate(Evacuation_Route.filter_by_status(True), Evacuation_Route, page))
    if not recorridos["recorridos"]:
        return jsonify({"error":"No hay resultados"}), 404

    return jsonify(recorridos), 200