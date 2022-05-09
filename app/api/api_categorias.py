from flask import Blueprint
from flask.json import jsonify
from app.models.report_category import ReportCategory 
api_categorias = Blueprint("categorias", __name__, url_prefix="/categorias")

@api_categorias.get("/")
def get():
    categorias = {}
    for categoria in ReportCategory.all():
        categorias[categoria.id_report_category] = categoria.name
    return jsonify(categorias), 200