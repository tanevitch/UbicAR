from app.helpers.auth import check_permission
from app.models.user import User
from app.models.role import Role
from app.validators.genericValidator import check_email, check_empty_fields, check_limit_100_chars, check_only_letters
from app.helpers.constants import usuario_change_roles
class UserValidator():
    @classmethod
    def _check_selected_roles(cls, roles):
        if not all(elem in Role.get_all_names() for elem in roles):
            return "Roles inválidos"


    @classmethod
    def _user_datatypes_are_right(cls, args):

        pw_error = None
        try:
            pw_error =  check_limit_100_chars(args["password"])
        except: 
            pass

        return (
            check_only_letters(args["fname"])
            or check_email(args["email"])
            or check_limit_100_chars(args["username"])
            or check_only_letters(args["lname"])
            or pw_error
        )   

    @classmethod
    def _check(cls, args, roles):
        '''
            Un mensaje de error si ocurre un fallo de validación, o None si todo es correcto
        '''
        invalid_fields_error_message= check_empty_fields(args.values()) or cls._user_datatypes_are_right(args) or cls._check_selected_roles(roles)
        
        if invalid_fields_error_message:
            return invalid_fields_error_message
        elif check_permission(usuario_change_roles) and len(roles)==0:
            return "Seleccione al menos un rol"

    @classmethod
    def check_create(cls, email, username, password, fname, lname, roles):
        msg_error= cls._check({"email":email, "fname":fname, "lname":lname, "username":username, "password":password}, roles)
        if (msg_error):
            return msg_error

        if (User.filter_by_email(email)):
            return 'Ya existe un usuario con email '+email
        if (User.filter_by_username(username)):
            return 'Ya existe un usuario con username '+username
        
    @classmethod
    def check_edit(cls, id_user, email, username, password, fname, lname, roles):
        attrs_to_check = {"email":email, "fname":fname, "lname":lname, "username":username}
        if password: # si es null es porque eligió no cambiarla
            attrs_to_check["password"]=password

        msg_error= cls._check(attrs_to_check, roles)
        if (msg_error):
            return msg_error
        
        if (len(roles)!=0 and not check_permission(usuario_change_roles)):
            return "No tenés permiso para editar roles"

        # Si no seleccioné algún rol que tenga permisos para cambiar los roles, y soy el último usuario en el sistema que puede cambiar los roles,
        # la acción se denega porque sino el sistema quedaría inaccesible
        if (len(roles)!=0 and not Role.check_if_any_has_change_roles(roles) and User.last_user_with_change_roles_permission(id_user)):
            return "Sos el ultimo usuario activo con permisos para editar roles. Acción denegada"

        if (User.filter_by_email(email) and User.filter_by_email(email).id_user != id_user):
                return 'Ya existe un usuario con email '+email

        if (User.filter_by_username(username) and User.filter_by_username(username).id_user != id_user):
            return 'Ya existe un usuario con username '+username

