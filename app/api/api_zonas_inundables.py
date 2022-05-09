from flask import Blueprint, request
from flask.json import jsonify
from app.helpers.paginator import Paginator
from app.models.floodable_zone import Floodable_Zone
from app.schemas.FloodableZoneSchema import fzone_schema, fzones_schema

api_zonas_inundables = Blueprint("zonas inundables", __name__, url_prefix="/zonas_inundables")

@api_zonas_inundables.get("/<int:id>")
def get_by_id(id):
    zona_inundable= Floodable_Zone.get_by_id(id)
    if (not zona_inundable):
        return jsonify({"error": f"No existe zona con id {id}"}), 404

    zona_inundable= fzone_schema.dump(zona_inundable)
    return jsonify(zona_inundable), 200

@api_zonas_inundables.get("/")
def get():
    page = request.args.get("page", 1, type=int)

    zonas_inundables = fzones_schema.dump(Paginator.paginate(Floodable_Zone.filter_by_status(True), Floodable_Zone, page))
    if not zonas_inundables["zonas"]:
        return jsonify({"error":"No hay resultados"}), 404

    return jsonify(zonas_inundables), 200