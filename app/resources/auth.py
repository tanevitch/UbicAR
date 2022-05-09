from flask import redirect, render_template, request, url_for, session, flash
from app.helpers.auth import authenticated
from app.models.user import User
from app.validators.authValidator import AuthValidator
import requests
from oauthlib.oauth2 import WebApplicationClient
from app.resources.user import create_google

import json

GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
GOOGLE_DISCOVERY_URL = (
    ""
)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def login_google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    url= "https://admin-grupo1.proyecto2021.linti.unlp.edu.ar/"
    # url= "http://localhost:5000/"
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri= url+ "login/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if not AuthValidator.is_google_validated(userinfo_response):
        flash("Cuenta no verificada por Google", 'alert-error')
    else:
        user = AuthValidator.user_exists(userinfo_response.json()["email"])

        if (user and user.password):
            flash("No se puede realizar el registro con este mail, dado que fue registrado por un administrador", "alert-danger")
        elif (user and not AuthValidator.user_is_active(user)):
            flash("La cuenta está desactivada. Contáctese con un Administrador", 'alert-warning')
        elif (user and AuthValidator.user_is_active(user)):
            session["user"]= user.id_user
            flash("La sesión se inició correctamente.", 'alert-success')
        else: 
            create_google(userinfo_response.json())
            flash("Se ha generado una petición de creación de cuenta. Debe aguardar que un Administrador la verifique para poder utilizar el servicio", 'alert-success')

    return redirect(url_for("dashboard"))

def login():
    if (authenticated(session)):
        return redirect(url_for("dashboard"))
    else:
        return render_template("auth/login.html")


def authenticate():
    error_msg= AuthValidator.check(request.form['email'], request.form['password'])
    if (error_msg):
        flash(error_msg, 'alert-warning')
        return redirect(url_for("auth_login"))
    
    session["user"]= User.filter_by_email(request.form['email']).id_user 
    flash("La sesión se inició correctamente.", 'alert-success')
    
    return redirect(url_for("dashboard"))

def logout():
    if (session.get("user")):
        del session["user"]
        session.clear()
        flash("La sesión se cerró correctamente.", 'alert-success')

    return redirect(url_for("auth_login"))
