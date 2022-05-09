from app.helpers.constants import EstadoDenuncia
from app.models.user import User
from app.validators.genericValidator import check_email,check_empty_fields, check_limit_100_chars, check_limit_500_chars, check_only_letters, check_phone, check_coords
from app.models.report_category import ReportCategory
from app.models.report import Report

class ReportValidator():
    @classmethod
    def _category_not_exists(cls, category):
        if not ReportCategory.find_by_id(category):
            return "Categoría de reporte inválida"

    @classmethod
    def check_api(cls, args):
        '''
        Mensaje de error si es inválido, o None si no hay errores
        
        Ejemplo de cómo se espera el input:
        {
            "categoria_id": 2,
            "coordenadas": "41.40338, 2.17403",
            "apellido_denunciante": "Fulanito",
            "nombre_denunciante": "Cosme",
            "telcel_denunciante": "2218436754",
            "email_denunciante": "juan.perez@gmail.com",
            "titulo": "Alcantarilla tapada",
            "descripcion": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut non erat non ligula efficitur tincidunt eu ac justo. Donec eu nunc purus. Mauris commodo lacus ex, vitae vehicula dui pellentesque at. Nam sollicitudin ut nunc eu imperdiet. Donec in elit fringilla, molestie ligula at, commodo massa. Curabitur quis erat nec odio fringilla hendrerit. Morbi in malesuada dolor, quis auctor nisi."
        }
        '''
        if not args:
            return {"error" : "Datos obligatorios"}
        attributes_that_should_have= ['titulo', 'categoria_id', 'descripcion', 'coordenadas', 'nombre_denunciante', 'apellido_denunciante', 'telcel_denunciante', 'email_denunciante']
        if set(attributes_that_should_have) != set(args.keys()):
            return {"error": "JSON debe tener los campos titulo, categoria_id, descripcion, coordenadas, nombre_denunciante, apellido_denunciante, telcel_denunciante, email_denunciante"}


    @classmethod    
    def validate(cls, args):
        return (
            check_empty_fields(args.values()) 
            or check_email(args['email']) 
            or check_phone(args['phone']) 
            or check_only_letters(args['fname'])
            or check_only_letters(args['lname'])
            or check_limit_100_chars(args['title'])
            or check_coords(args['coords'])
            or check_limit_500_chars(args['description'])
            or cls._category_not_exists(args['category'])
        )
    
    @classmethod 
    def check(cls, report):
        try:
            report.category = int(report.category)
        except:
            return "Categoría debe ser numérica"
        attrs_to_check = {"title": report.title, "category": report.category, "description": report.description, "coords": report.coords, "fname": report.fname, "lname": report.lname, "phone": report.phone, "email": report.email}
        return cls.validate(attrs_to_check)

    @classmethod
    def check_seguimiento(cls, id_denuncia, descripcion):
        try:
            id_denuncia = int(id_denuncia)
        except:
            return "Id inválido"
            
        denuncia = Report.get_by_id(id_denuncia)
        if not denuncia:
            return "Denuncia inexistente"
                
        elif not (denuncia.assigned_to != None and (denuncia.status == EstadoDenuncia.ENCURSO.name or denuncia.status == EstadoDenuncia.SINCONFIRMAR.name)):     
            return "Para hacer seguimientos, la denuncia debe estar asignada, y en estado sin confirmar o en curso"

        return check_empty_fields([descripcion]) 

    @classmethod
    def check_assigned(cls, selected_assigned):
        if selected_assigned != "null":
            try:
                selected_assigned= int(selected_assigned)
            except:
                return "Valor inválido para selección de asignado"

            if not User.get_by_id(selected_assigned):
                return "Usuario inexistente"
            
            if not User.get_by_id(selected_assigned) in User.users_with_report_manage_permission():
                return "Usuario no tiene permiso para realizar seguimientos"


    