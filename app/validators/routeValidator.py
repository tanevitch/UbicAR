from sqlalchemy.sql.expression import desc, true
from app.validators.genericValidator import check_empty_fields, check_limit_100_chars, check_polycoords, check_hex_color
from app.models.evacuation_route import Evacuation_Route

class eRouteValidator():

    @classmethod
    def _route_datatypes_are_right(cls, args):

        msj = check_polycoords(args["coords"])
        if msj:
            return msj

        
        return (
            check_limit_100_chars(args['name'])
            or check_limit_100_chars(args['description'])
            or check_hex_color(args['color'])
        )

    @classmethod
    def _check(cls, args):
        '''
            Un mensaje de error si ocurre un fallo de validación, o None si todo es correcto
        '''
        invalid_fields_error_message= check_empty_fields(args) or cls._route_datatypes_are_right(args)

        return invalid_fields_error_message

    @classmethod
    def check_create(cls, name, description, color, coords):
        msg_error= cls._check({"name":name, "description":description, "color":color, "coords":coords})
        if (msg_error):
            return msg_error