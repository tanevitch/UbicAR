
from app.resources import user
from app.resources import config_panel
from app.resources import auth
from app.resources import meeting_point
from app.resources import evacuation_route
from app.resources import floodable_zones
from app.resources import report
from app.resources.dashboard import dashboard

class Router():

    @classmethod
    def crearRutas(cls, app):
        app.add_url_rule("/", "dashboard", dashboard) # Home privado
        cls.crearRutasAutenticacion(app)        
        cls.crearRutasUsers(app)
        cls.crearRutasConfiguracion(app)
        cls.crearRutasPuntoDeEncuentro(app)
        cls.crearRutasEvacuation_route(app)
        cls.crearRutasZonasInundables(app)
        cls.crearRutasDenuncias(app)
    
    @classmethod
    def crearRutasPuntoDeEncuentro(cls, app):
        app.add_url_rule("/meetingPoints", "mp_index", meeting_point.index, defaults={"page": 1})
        app.add_url_rule("/meetingPoints/<int:page>", "mp_index", meeting_point.index)
        app.add_url_rule("/meetingPoints/new", "mp_create", meeting_point.create, methods=['GET','POST'])
        app.add_url_rule("/meetingPoints/edit/<id>", "mp_edit", meeting_point.edit, methods=['GET', 'POST'])
        app.add_url_rule("/meetingPoints/disable/<id>", "mp_toogle", meeting_point.changeVisibility)
        app.add_url_rule("/meetingPoints/delete/<id>", "mp_delete", meeting_point.delete)
        app.add_url_rule("/meetingPoints/info/<id>", "mp_info", meeting_point.info, methods=["GET"])

    @classmethod
    def crearRutasConfiguracion(cls, app):
        app.add_url_rule("/config", "config_index", config_panel.index, methods=["GET"] )
        app.add_url_rule("/config", "config_update", config_panel.update, methods=["POST"] )

    @classmethod
    def crearRutasUsers(cls, app):
        app.add_url_rule("/users", "user_index", user.index, defaults={"page": 1})
        app.add_url_rule("/users/<int:page>", "user_index", user.index)
        app.add_url_rule("/users/new", "user_create", user.create, methods=["GET", "POST"])
        app.add_url_rule("/users/update/<id>", "user_update", user.update, methods=["GET", "POST"])
        app.add_url_rule("/users/delete/<id>", "user_delete", user.delete, methods=["GET"])
        app.add_url_rule("/users/toggleAvailability/<id>", "user_activation", user.toggleAvailability,methods=["GET"])
        app.add_url_rule("/users/info/<id>", "user_info", user.info, methods=["GET"])
        app.add_url_rule("/users/approvement", "user_approvement", user.approve, methods=["GET"], defaults={"page": 1})
        app.add_url_rule("/users/approvement/<int:page>", "user_approvement", user.approve)
        app.add_url_rule("/users/approvement/<int:id>", "user_approve", user.post_approve, methods=["POST"])
        
    @classmethod
    def crearRutasAutenticacion(cls, app):
        app.add_url_rule("/login", "auth_login", auth.login)
        app.add_url_rule("/logout", "auth_logout", auth.logout)
        app.add_url_rule("/authenticate", "auth_authenticate", auth.authenticate, methods=["POST"])
        app.add_url_rule("/login_google", "auth_google", auth.login_google)
        app.add_url_rule("/login/callback", "auth_callback", auth.callback, methods=["GET"])

    @classmethod
    def crearRutasZonasInundables(cls, app):
        app.add_url_rule("/floodableZones", "fz_index", floodable_zones.index, defaults={"page": 1})
        app.add_url_rule("/floodableZones/<int:page>", "fz_index", floodable_zones.index)
        app.add_url_rule("/floodableZones/new", "fz_create", floodable_zones.create, methods=['GET', 'POST'])
        app.add_url_rule("/floodableZones/disable/<id>", "fz_toogle", floodable_zones.changeStatus)
        app.add_url_rule("/floodableZones/delete/<id>", "fz_delete", floodable_zones.delete)
        app.add_url_rule("/floodableZones/info/<id>", "fz_info", floodable_zones.info, methods=["GET"])

    @classmethod
    def crearRutasEvacuation_route(cls,app):
        app.add_url_rule("/eRoutes", "eRoutes_index", evacuation_route.index, defaults={"page": 1})
        app.add_url_rule("/eRoutes/<int:page>", "eRoutes_index", evacuation_route.index)
        app.add_url_rule("/eRoutes/new", "eRoutes_create", evacuation_route.create, methods=["GET", "POST"])
        app.add_url_rule("/eRoutes/update/<id>", "eRoutes_update", evacuation_route.update, methods=["GET", "POST"])
        app.add_url_rule("/eRoutes/delete/<id>", "eRoutes_delete", evacuation_route.delete, methods=["GET"])
        app.add_url_rule("/eRoutes/toggleStatus/<id>", "eRoutes_activation", evacuation_route.changeStatus,methods=["GET"])
        app.add_url_rule("/eRoutes/info/<id>", "eRoutes_info", evacuation_route.info, methods=["GET"])

    @classmethod  
    def crearRutasDenuncias(cls, app):
        app.add_url_rule("/reports", "report_index", report.index, defaults={"page": 1})
        app.add_url_rule("/reports/<int:page>", "report_index", report.index)
        app.add_url_rule("/reports/new", "report_create", report.create, methods=['GET', 'POST'])
        app.add_url_rule("/reports/update/<id>", "report_update", report.update, methods=['GET', 'POST'])
        app.add_url_rule("/reports/info/<id>", "report_info", report.info)
        app.add_url_rule("/reports/assignment/<id>", "report_assignment", report.assign_to)
        app.add_url_rule("/reports/delete/<id>", "report_delete", report.delete, methods=["GET"])
        app.add_url_rule("/reports/tracing/<id>", "report_tracing",report.tracing, methods=['POST'])
        app.add_url_rule("/reports/change_status/<id>","report_change_status",report.change_status,  methods=['POST'])
        