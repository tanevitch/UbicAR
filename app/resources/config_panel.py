from flask import render_template, request, session, abort, flash
from app.models.moduleConfig import Module_config
from app.models.palette import Palette
from app.models.currentConfig import Current_config
from app import db
from app.models.meeting_point import Meeting_point
from app.models.floodable_zone import Floodable_Zone
from app.models.report import Report
from app.models.user import User
from app.models.evacuation_route import Evacuation_Route
from app.helpers.auth import authenticated, check_permission
from app.helpers.constants import configuracion_sistema
from app.validators.configValidator import  ConfigValidator

def index():
    if not authenticated(session):
        abort(401)
    if not check_permission(configuracion_sistema):
        abort(403)

    return render_template(
        "config_panel/index.html",
        paletas = Palette.all(), 
        pagina=Current_config.get_results_per_page(),
        actual_pub= Palette.get_current_color_public(),
        actual_priv= Palette.get_current_color_private(),
        config_modules = Module_config.get_modules_config()
    )

def update():
    if not authenticated(session):
        abort(401)
    if not check_permission(configuracion_sistema):
        abort(403)

    actual = Current_config.get_actual_config()

    if(request.form.get("paginas")):
        config_error_msg = ConfigValidator.check_page_config(request.form)
        if config_error_msg:
            flash(config_error_msg, 'alert-warning')
        else:
            actual.pages = request.form.get("paginas")
            db.save()
            flash("Actualización cantidad de resultados por página exitosa", 'alert-success')

    elif request.form.get("paleta-pub"):    
        msg_paleta_pub= _config_public_color(actual)
        flash(msg_paleta_pub[0], msg_paleta_pub[1])
    elif request.form.get("paleta-priv"):
        msg_paleta_priv = _config_private_color(actual)   
        flash(msg_paleta_priv[0], msg_paleta_priv[1])
    elif request.form.get("ordenacion_user") and request.form.get("campo_user"): 
        msg_user_module= _config_user_module()
        flash(msg_user_module[0], msg_user_module[1])
    elif request.form.get("ordenacion_mp") and request.form.get("campo_mp"): 
        msg_mp_module= _config_mp_module()
        flash(msg_mp_module[0], msg_mp_module[1])
    elif request.form.get("ordenacion_fz") and request.form.get("campo_fz"): 
        msg_fz_module= _config_fz_module()
        flash(msg_fz_module[0], msg_fz_module[1])
    elif request.form.get("ordenacion_report") and request.form.get("campo_report"): 
        msg_fz_module= _config_report_module()
        flash(msg_fz_module[0], msg_fz_module[1])
    elif request.form.get("ordenacion_eRoute") and request.form.get("campo_eRoute"): 
        msg_er_module= _config_eRoute_module()
        flash(msg_er_module[0], msg_er_module[1])
    else:
        flash("Selección inválida", "alert-danger")

    return render_template(
        "config_panel/index.html",
        paletas = Palette.all(), 
        pagina=Current_config.get_results_per_page(),
        actual_pub= Palette.get_current_color_public(),
        actual_priv= Palette.get_current_color_private(),
        config_modules = Module_config.get_modules_config()
    )

def _config_public_color(actual):
    color_elegido_publica = request.form.get("paleta-pub")
    if (color_elegido_publica and ConfigValidator.check_palette_config(color_elegido_publica)):
        actual.currentColor_public = color_elegido_publica
        db.save()
        return "Actualización color paleta pública exitosa", "alert-success"
    else:
        return "Campos inválidos para la configuración de paleta pública", "alert-warning"


def _config_private_color(actual):
    color_elegido_privada = request.form.get("paleta-priv")
    if (color_elegido_privada and ConfigValidator.check_palette_config(color_elegido_privada)):
        actual.currentColor_private= color_elegido_privada
        db.save()
        return "Actualización color paleta privada exitosa", "alert-success"
    else:
        return "Campos inválidos para la configuración de paleta privada", "alert-warning"

def _config_mp_module():
    config_mp = Module_config.get_module_config(f'{Meeting_point.__name__}_module')
    mp_orderby= request.form.get("ordenacion_mp")
    mp_sortfield= request.form.get("campo_mp")
    if ConfigValidator.check_module_config(Meeting_point.get_sortable_fields(), mp_sortfield, mp_orderby):
        config_mp.sort_field= mp_sortfield
        config_mp.order= mp_orderby
        db.save()
        return "Actualización configuración de Módulo  Puntos de Encuentro exitosa", "alert-success"
    else:
        return "Campos inválidos para la configuración de Módulo Puntos de Encuentro", "alert-warning"
        
def _config_fz_module():
    config_fz = Module_config.get_module_config(f'{Floodable_Zone.__name__}_module')
    fz_orderby= request.form.get("ordenacion_fz")
    fz_sortfield= request.form.get("campo_fz")
    if ConfigValidator.check_module_config(["name", "status",], fz_sortfield, fz_orderby):
        config_fz.sort_field= fz_sortfield
        config_fz.order= fz_orderby
        db.save()
        return "Actualización configuración de Módulo  Zonas inundables exitosa", "alert-success"
    else:
        return "Campos inválidos para la configuración de Zonas inundables "

def _config_user_module():
    config_user = Module_config.get_module_config(f'{User.__name__}_module')
    user_orderby= request.form.get("ordenacion_user")
    user_sortfield= request.form.get("campo_user")
    if ConfigValidator.check_module_config(User.get_sortable_fields(),user_sortfield, user_orderby):
        config_user.sort_field= user_sortfield
        config_user.order= user_orderby
        db.save()
        return "Actualización configuración de Módulo Usuarios exitosa", "alert-success"
    else:
        return "Campos inválidos para la configuración de Módulo Usuarios", "alert-warning"

def _config_report_module():
    config_report = Module_config.get_module_config(f'{Report.__name__}_module')
    report_orderby= request.form.get("ordenacion_report")
    report_sortfield= request.form.get("campo_report")
    if ConfigValidator.check_module_config(Report.get_sortable_fields(), report_sortfield, report_orderby):
        config_report.sort_field= report_sortfield
        config_report.order= report_orderby
        db.save()
        return "Actualización configuración de Módulo Denuncias exitosa", "alert-success"
    else:
        return "Campos inválidos para la configuración de Módulo Denuncias", "alert-warning"


def _config_eRoute_module():
    config_report = Module_config.get_module_config(f'{Evacuation_Route.__name__}_module')
    eRoute_orderby= request.form.get("ordenacion_eRoute")
    eRoute_sortfield= request.form.get("campo_eRoute")
    if ConfigValidator.check_module_config(Evacuation_Route.get_sortable_fields(), eRoute_sortfield, eRoute_orderby):
        config_report.sort_field= eRoute_sortfield
        config_report.order= eRoute_orderby
        db.save()
        return "Actualización configuración de Módulo Rutas de evacuación exitosa", "alert-success"
    else:
        return "Campos inválidos para la configuración de Módulo Rutas de evacuación", "alert-warning"
