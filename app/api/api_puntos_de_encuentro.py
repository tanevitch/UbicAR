from flask import Blueprint, request
from flask.json import jsonify
from app.helpers.paginator import Paginator
from app.models.meeting_point import Meeting_point
from app.schemas.MeetingPointSchema import mpoints_schema

api_puntos_de_encuentro = Blueprint("puntos_encuentro", __name__, url_prefix="/puntos_encuentro")

@api_puntos_de_encuentro.get("/")
def get():
    page = request.args.get("page", 1, type=int)

    puntos_de_encuentro = mpoints_schema.dump(Paginator.paginate(Meeting_point.filter_by_visibility(True), Meeting_point, page))
    if not puntos_de_encuentro["puntos_encuentro"]:
        return jsonify({"error":"No hay resultados"}), 404

    return jsonify(puntos_de_encuentro), 200
