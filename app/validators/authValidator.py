from flask_bcrypt import Bcrypt
from app.models.user import User
from app.validators.genericValidator import check_empty_fields


class AuthValidator():
    @classmethod
    def check(cls, email, password):
        b_crypt=Bcrypt()
        empty_fields = check_empty_fields([email, password])
        if empty_fields:
            return empty_fields
        
        user = User.filter_by_email(email)
        if (user and user.password == None):
            return "Inicio de sesión inválido. Debe continuar con Google"
            
        if not user or not b_crypt.check_password_hash(user.password, password):
            return "Usuario o clave incorrecto"

        if (not user.is_active):
            return "Cuenta desactivada, contáctese con un administrador para obtener más información"

    @classmethod
    def user_exists(cls, email):
        return User.filter_by_email(email)

    @classmethod
    def user_is_active(cls, user):
        return user.is_active

    @classmethod
    def is_google_validated(cls, userinfo_response):
        return userinfo_response.json().get("email_verified")
