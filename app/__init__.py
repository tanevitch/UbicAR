from os import environ
from flask import Flask, Blueprint, request
from flask_session import Session
from app.routes.router import Router
from app.api.api_denuncias import api_denuncias
from app.api.api_zonas_inundables import api_zonas_inundables
from app.api.api_puntos_de_encuentro import api_puntos_de_encuentro
from app.api.api_recorridos_de_evacuacion import api_recorridos_de_evacuacion
from app.api.api_categorias import api_categorias
from app.api.api_colores import api_colores
from config import config
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import general as helper_general
from app import db
from flask_wtf.csrf import CSRFProtect
from flask_marshmallow import Marshmallow
from flask_cors import CORS

csrf = CSRFProtect()

def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    app.secret_key="hola mundo"
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    csrf.init_app(app)
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    Marshmallow(app)
    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    #db config
    db.init_db(app)
    # db.seed() # DESCOMENTAR PRIMERA VEZ 

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(render_buttons=helper_general.render_buttons)
    app.jinja_env.globals.update(render_cards=helper_general.render_cards_in_private_home_page)
    app.jinja_env.globals.update(check_permission = helper_auth.check_permission)

    app.jinja_env.globals.update(get_theme=helper_general.get_theme)

    Router.crearRutas(app)

    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(api_denuncias)
    api.register_blueprint(api_zonas_inundables)
    api.register_blueprint(api_puntos_de_encuentro)
    api.register_blueprint(api_recorridos_de_evacuacion)
    api.register_blueprint(api_colores)
    api.register_blueprint(api_categorias)
    app.register_blueprint(api)
    
    app.before_request(disable_csrf)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(403, handler.forbidden_error)
    app.register_error_handler(500, handler.internal_server_error)

    # Retornar la instancia de app configurada
    return app

def disable_csrf():
    if not request.path.startswith("/api"):
        csrf.protect()
