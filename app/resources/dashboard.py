from app.helpers.auth import authenticated
from flask import render_template, session, redirect, url_for

def dashboard():
    if authenticated(session):
        return render_template("dashboard.html")
    else:
        return redirect(url_for("auth_login"))