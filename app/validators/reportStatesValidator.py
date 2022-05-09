from app.helpers.constants import EstadoDenuncia

def _could_be_closed(report):
    return report.status == EstadoDenuncia.ENCURSO.name

def _could_be_confirmed(report):
    return report.status == EstadoDenuncia.SINCONFIRMAR.name and report.assigned_to != None

def _could_be_resolved(report):
    return report.status == EstadoDenuncia.ENCURSO.name

def change_state_abled(report, status):
    if status == EstadoDenuncia.CERRADA.name:
        if not _could_be_closed(report):
            return "La denuncia debe estar en curso para que pueda ser cerrada"
    elif status == EstadoDenuncia.ENCURSO.name:
        if not _could_be_confirmed(report):
            return "La denuncia debe estar sin confirmar y asignada para que pueda ser confirmada"
    elif status == EstadoDenuncia.RESUELTA.name:
        if not _could_be_resolved(report):
            return "La denuncia debe estar en curso para que pueda ser resuelta"
    elif status == EstadoDenuncia.SINCONFIRMAR.name:
        return "No puede cambiarse a estado sin confirmar"
    elif status == report.status:
        return "No puede cambiarse la denuncia al mismo estado que tiene actualmente"
    elif not status in EstadoDenuncia._value2member_map_:
        return "Estado inválido. Seleccione uno válido"
    
    return True

