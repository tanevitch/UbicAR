from flask import Blueprint, request
from flask.json import jsonify
from app.helpers.constants import EstadoDenuncia
from app.models.report import Report
from app.schemas.ReportSchema import report_schema, reports_schema
from app.validators.reportValidator import ReportValidator
from app.helpers.paginator import Paginator


api_denuncias = Blueprint("denuncias", __name__, url_prefix="/denuncias")

@api_denuncias.post("/")
def create():
    json= request.get_json()
    validado = ReportValidator.check_api(json)
    if (validado):
        return jsonify(validado), 400
    
    attrs_to_check = {
        "title": json["titulo"],
        "category": json["categoria_id"], 
        "description": json["descripcion"], 
        "coords": "["+json["coordenadas"]+"]", 
        "fname": json["nombre_denunciante"], 
        "lname": json["apellido_denunciante"], 
        "phone": json["telcel_denunciante"], 
        "email": json["email_denunciante"]
    }
    
    error_msg = ReportValidator.validate(attrs_to_check)
    if error_msg:
        return jsonify({"error": error_msg}), 400
    
    nueva_denuncia = Report(
        *attrs_to_check.values()
    )
    Report.add(nueva_denuncia)

    denuncia = report_schema.dump(nueva_denuncia)
    return jsonify(denuncia), 201

@api_denuncias.get("/")
def get():
    page = request.args.get("page", 1, type=int)

    denuncias = reports_schema.dump(Paginator.paginate(Report.filter_by_state(EstadoDenuncia.ENCURSO.name), Report, page))
    if not denuncias["denuncias"]:
        return jsonify({"error":"No hay resultados"}), 404


    return jsonify(denuncias), 200

