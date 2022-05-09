from flask import render_template, request
from flask.json import jsonify


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }

    if (request.path.startswith("/api")):
        return jsonify(kwargs), 404
    else:
        return render_template("error.html", **kwargs), 404


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    if (request.path.startswith("/api")):
        return jsonify(kwargs), 401
    else:
        return render_template("error.html", **kwargs), 401

def forbidden_error(e):
    kwargs = {
        "error_name": "403 Forbidden Error",
        "error_description": "Acceso denegado",
    }
    if (request.path.startswith("/api")):
        return jsonify(kwargs), 403
    else:
        return render_template("error.html", **kwargs), 403

def internal_server_error(e):
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": "Ha ocurrido un error interno en el servidor",
    }
    if (request.path.startswith("/api")):
        return jsonify(kwargs), 500
    else:
        return render_template("error.html", **kwargs), 500
