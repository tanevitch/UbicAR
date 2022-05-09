from flask import redirect, url_for
from app.models.user import User

def authenticated(session):
    if User.get_by_id(session.get("user")): #además de tener una sesión, tiene que tener una sesión de un usuario que exista en el sistema
        return session.get("user")


def check_permission(permission):
    return User.has_permission(permission)