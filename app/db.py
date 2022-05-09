from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

def save():
    db.session.commit()

def init_db(app):
    db.init_app(app)
    db.app= app
    from app.models import user
    from app.models import meeting_point
    from app.models import palette
    from app.models import currentConfig
    from app.models import permission
    from app.models import role
    from app.models import moduleConfig
    from app.models import report
    from app.models import report_category
    from app.models import floodable_zone
    from app.models import reportHistory
    db.create_all()

def seed():
    from app.models.user import User
    from app.models.role import Role
    from app.models.palette import Palette
    from app.models.currentConfig import Current_config
    from app.models.permission import Permission
    from app.models.moduleConfig import Module_config
    from app.models.meeting_point import Meeting_point
    from app.models.report_category import ReportCategory
    from flask_bcrypt import Bcrypt

    db.session.add(ReportCategory("Fallo o avería"))
    db.session.add(ReportCategory("Alcantarilla tapada"))
    db.session.add(ReportCategory("Pérdida de agua"))

    db.session.add(Meeting_point("Dardo Rocha", "6 y 60", "[-34.914019, -57.949708]", "2214251990", "drocha@gmail.com"))    
    db.session.add(Meeting_point("Catedral", "12 y 51", "[-34.922883, -57.956317]", "2214233931", "catedrallp@gmail.com"))

    b_crypt= Bcrypt()
    user_admin= User('mariar@example.com', 'mariar',  b_crypt.generate_password_hash('1234'), 'Maria', 'Rosa')
    user_operador= User('juanp@example.com', "juanp", b_crypt.generate_password_hash('1234'), 'Juan', 'Perez')
    user_con_ambos= User('marcosg@example.com', "marcosg", b_crypt.generate_password_hash('1234'), 'Marcos', 'Gomez')
    rol_admin= Role('admin')
    rol_operario= Role('operario')
    user_admin.roles.append(rol_admin)

    user_con_ambos.roles.append(rol_admin)
    user_con_ambos.roles.append(rol_operario)
    
    user_operador.roles.append(rol_operario)
    
    db.session.add(Palette('indigo-theme'))
    db.session.add(Palette('modern-theme'))
    db.session.add(Palette('ocean-theme'))

    db.session.add(Current_config(2,1,2))
    db.session.add(Module_config("Meeting_point_module","asc","name"))
    db.session.add(Module_config("User_module","asc","email"))
    db.session.add(Module_config("Report_module","asc","title"))
    db.session.add(Module_config("Floodable_Zone_module","asc","name"))
    db.session.add(Module_config("Evacuation_Route_module","asc","name"))
    db.session.add(user_admin)   
    db.session.add(user_con_ambos)   
    db.session.add(user_operador)   

    #user permissions
    usuario_toggle_availability = Permission("usuario_toggle_availability")
    usuario_index = Permission("usuario_index")
    usuario_update = Permission("usuario_update") 
    usuario_create = Permission("usuario_create")
    usuario_show = Permission("usuario_show")
    usuario_destroy = Permission("usuario_destroy")
    usuario_change_roles = Permission("usuario_change_roles")
    usuario_update_others = Permission("usuario_update_others")
    usuario_aprobacion = Permission("usuario_aprobacion")

    #puntos de encuentro permissions
    punto_encuentro_index = Permission("punto_de_encuentro_index")
    punto_encuentro_destroy = Permission("punto_de_encuentro_destroy")
    punto_encuentro_update = Permission("punto_de_encuentro_update")
    punto_encuentro_show = Permission("punto_de_encuentro_show")
    punto_encuentro_create = Permission("punto_de_encuentro_create")
    punto_encuentro_change_visibility = Permission("punto_de_encuentro_change_visibility")

    #evacuation route permission
    evacuation_route_index = Permission("evacuation_route_index")
    evacuation_route_destroy = Permission("evacuation_route_destroy")
    evacuation_route_update = Permission("evacuation_route_update")
    evacuation_route_show = Permission("evacuation_route_show")
    evacuation_route_create = Permission("evacuation_route_create")
    evacuation_route_change_status = Permission("evacuation_route_change_status")
    
    #floodable zones permissions
    zonas_inundables_index = Permission("zonas_inundables_index")
    zonas_inundables_create = Permission("zonas_inundables_create")
    zonas_inundables_destroy = Permission("zonas_inundables_destroy")
    # zonas_inundables_update = Permission("zonas_inundables_update")
    zonas_inundables_show = Permission("zonas_inundables_show")
    zonas_inundables_change_status = Permission("zonas_inundables_change_status")

    report_index = Permission("denuncias_index")
    report_create = Permission("denuncias_create")
    report_show = Permission("denuncias_show")
    report_update = Permission("denuncias_update")
    report_change_assignee = Permission("denuncias_change_assignee")
    report_tracing = Permission("denuncias_tracing")
    report_destroy = Permission("denuncias_destroy")
    #configuracion
    configuracion_sistema = Permission("configuracion_sistema")


    ## roles Admin ##

    rol_admin.permisos.append(usuario_toggle_availability)
    rol_admin.permisos.append(usuario_index)
    rol_admin.permisos.append(usuario_update)
    rol_admin.permisos.append(usuario_create)
    rol_admin.permisos.append(usuario_show)
    rol_admin.permisos.append(usuario_destroy)
    rol_admin.permisos.append(usuario_aprobacion)

    rol_admin.permisos.append(punto_encuentro_index)
    rol_admin.permisos.append(punto_encuentro_destroy)
    rol_admin.permisos.append(punto_encuentro_update)
    rol_admin.permisos.append(punto_encuentro_show)
    rol_admin.permisos.append(punto_encuentro_create)
    rol_admin.permisos.append(punto_encuentro_change_visibility)

    rol_admin.permisos.append(evacuation_route_index)
    rol_admin.permisos.append(evacuation_route_destroy)
    rol_admin.permisos.append(evacuation_route_update)
    rol_admin.permisos.append(evacuation_route_show)
    rol_admin.permisos.append(evacuation_route_create)
    rol_admin.permisos.append(evacuation_route_change_status)

    rol_admin.permisos.append(configuracion_sistema)
    rol_admin.permisos.append(usuario_change_roles)

    rol_admin.permisos.append(zonas_inundables_index)
    rol_admin.permisos.append(zonas_inundables_create)
    rol_admin.permisos.append(zonas_inundables_destroy)
    rol_admin.permisos.append(zonas_inundables_show)
    rol_admin.permisos.append(zonas_inundables_change_status)
    rol_admin.permisos.append(usuario_update_others)

    rol_admin.permisos.append(report_index)
    rol_admin.permisos.append(report_show)
    rol_admin.permisos.append(report_update)
    rol_admin.permisos.append(report_create)
    rol_admin.permisos.append(report_change_assignee)
    rol_admin.permisos.append(report_tracing)
    rol_admin.permisos.append(report_destroy)


    ## roles Operario ##

    rol_operario.permisos.append(usuario_index)
    rol_operario.permisos.append(usuario_update)
    rol_operario.permisos.append(usuario_show)

    rol_operario.permisos.append(punto_encuentro_index)
    rol_operario.permisos.append(punto_encuentro_update)
    rol_operario.permisos.append(punto_encuentro_show)
    rol_operario.permisos.append(punto_encuentro_create)
    rol_operario.permisos.append(punto_encuentro_change_visibility)

    rol_operario.permisos.append(evacuation_route_index)
    rol_operario.permisos.append(evacuation_route_update)
    rol_operario.permisos.append(evacuation_route_show)
    rol_operario.permisos.append(evacuation_route_create)
    rol_operario.permisos.append(evacuation_route_change_status)

    rol_operario.permisos.append(zonas_inundables_index)
    rol_operario.permisos.append(zonas_inundables_create)
    rol_operario.permisos.append(zonas_inundables_show)
    rol_operario.permisos.append(zonas_inundables_change_status)
    
    rol_operario.permisos.append(report_index)
    rol_operario.permisos.append(report_show)
    rol_operario.permisos.append(report_update)
    rol_operario.permisos.append(report_create)
    rol_operario.permisos.append(report_tracing)

    db.session.add(rol_admin)
    db.session.add(rol_operario)
    db.session.commit()
