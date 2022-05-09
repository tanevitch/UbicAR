from app.helpers.auth import  check_permission
from app.helpers.constants import punto_de_encuentro_index, usuario_index, configuracion_sistema, evacuation_route_index, zonas_inundables_index, denuncias_index
from app.models.palette import Palette  


def get_theme():
    return Palette.get_current_color_private()

def render_buttons():
    botones=[]
    dropdown=[]

    if check_permission(punto_de_encuentro_index):
        dropdown.append(("Modulo puntos de encuentro", "/meetingPoints"))
    if check_permission(zonas_inundables_index):
        dropdown.append(("Modulo zonas inundables", "/floodableZones"))
    if check_permission(evacuation_route_index):
        dropdown.append(("Modulo recorridos de evacuación", "/eRoutes"))    
    if check_permission(usuario_index):
        botones.append(("Modulo usuarios", "/users"))
    if check_permission(denuncias_index):
        botones.append(("Modulo denuncias", "/reports"))
    if check_permission(configuracion_sistema):
        botones.append(("Modulo configuración", "/config"))
    
    render=[botones,dropdown]

    return render

def render_cards_in_private_home_page():
    cards=[]

    if check_permission(usuario_index):
        cards.append(("USUARIOS",
         "Panel de funcionalidades de usuario, con operaciones según permisos (crear, modificar, borrar, deshabilitar)",        
         "users")
        )
    if check_permission(punto_de_encuentro_index):
        cards.append(("PUNTOS DE ENCUENTRO",
         "Panel de funcionalidades de puntos de encuentro, con operaciones según permisos (crear, modificar, borrar, deshabilitar",
         "meetingPoints")
        )
    if check_permission(configuracion_sistema):
        cards.append(("CONFIGURACIÓN", 
        "Panel de configuraciones de administrador. Paleta de colores, criterio de ordenamiento, valores de paginación",
        "config"))
    
    if check_permission(evacuation_route_index):
        cards.append(("RECORRIDOS DE EVACUACIÓN", 
        "Panel de recorridos de evacuación, con operaciones según permisos (crear, modificar, borrar, deshabilitar)",
        "eRoutes"))        

    if check_permission(denuncias_index):
        cards.append(("GESTIÓN DE DENUNCIAS", 
        "Panel de gestión de denuncias, con operaciones según permisos (crear, modificar, borrar, realizar seguimientos)",
        "reports"))
        
    if check_permission(zonas_inundables_index): 
        cards.append(("GESTIÓN DE ZONAS INUNDABLES", 
        "Panel de zonas inundables, con operaciones según permisos (crear, borrar, deshabilitar)",
        "floodableZones"))

        
    return cards




