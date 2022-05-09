from flask import Blueprint
from flask.json import jsonify
from app.models.palette import Palette 
api_colores = Blueprint("color", __name__, url_prefix="/color")

@api_colores.get("/")
def get():
    return jsonify({"color":Palette.get_current_color_public()}), 200