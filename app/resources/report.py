from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.helpers.auth import authenticated, check_permission
from app.helpers.paginator import Paginator
from app.models.report import Report
from app.helpers.constants import denuncias_index, denuncias_destroy, denuncias_change_assignee, denuncias_tracing, denuncias_create, denuncias_show, denuncias_update, EstadoDenuncia
from app import db
from app.models.report_category import ReportCategory
from app.models.user import User
from app.models.reportHistory import ReportHistory
from app.validators.reportStatesValidator import change_state_abled
from app.validators.reportValidator import ReportValidator
from datetime import datetime
import json


def index(page):
    if not authenticated(session):
        abort(401)
    if not check_permission(denuncias_index):
        abort(403)
    if request.args.get('report_searchtitle'):
        buscar = "%{}%".format(request.args.get('report_searchtitle'))
        reports= Paginator.paginate(Report.filter_by_title(buscar), Report, page)
    elif request.args.get('date_range'):
        period= request.args.get('date_range').split(' - ')
        try:
            d_from = datetime.strptime(period[0], '%d/%m/%Y')
            d_to =  datetime.strptime(period[1], '%d/%m/%Y')
            f = '%Y-%m-%d'
            d_from = d_from.strftime(f)
            d_to = d_to.strftime(f)
        except:
            flash("Fecha inválida", 'alert-warning')
            return redirect(url_for("report_index"))
        reports = Paginator.paginate(Report.filter_by_period(d_from, d_to), Report, page)
    elif request.args.get('report_status'):
        reports = Paginator.paginate(Report.filter_by_state(request.args.get('report_status')), Report, page)
    elif request.args.get('report_unasigned'):
        reports = Paginator.paginate(Report.get_unassigned(), Report, page)
    elif request.args.get('report_self'):
        reports = Paginator.paginate(Report.filter_by_assigned_to(session.get("user")), Report, page)
    else:
        reports = Paginator.paginate(Report.query, Report, page)
    
    data={}
    c=0
    for i in reports.items:
        data[str(c)+'n']=i.title
        data[str(c)+'coords']=i.coords
        c+=1

    return render_template("report/index.html", reports = reports, data=json.dumps(data), estados=EstadoDenuncia)


def create():
    if not authenticated(session):
        abort(401)

    if not check_permission(denuncias_create):
        abort(403)

    if request.method== "GET":
        return render_template("report/new.html", categories= ReportCategory.all()) 

    elif request.method == "POST":
        report = Report(
            request.form.get("title"), 
            request.form.get("category"),
            request.form.get("description"),
            request.form.get("coords"),
            request.form.get("fname"),
            request.form.get("lname"),
            request.form.get("phone"),
            request.form.get("email"),
            )

        error_msg = ReportValidator.check(report)
        if (error_msg):
            flash(error_msg, 'alert-warning')
            return render_template("report/new.html", categories= ReportCategory.all())

        Report.add(report)
        return redirect(url_for("report_index"))


def info(id):
    if not authenticated(session):
        abort(401)
    if not check_permission(denuncias_show):
        abort(403)
    report = Report.get_by_id(id)
    if report:
        p={}
        p['coords']=report.coords

        return render_template(
            "report/info.html", 
            report=report, 
            report_histories=ReportHistory.get_report_histories_by_report_id(id), 
            extHistoriesQuantity=ReportHistory.get_external_histories_quantity_by_report_id(id),
            estados= EstadoDenuncia,
            coords=json.dumps(p)
            )
    else:
        flash("Denuncia inexistente", 'alert-warning')
        return redirect(url_for("report_index"))

def update(id):
    if not authenticated(session):
        abort(401)
    if not check_permission(denuncias_update):
        abort(403)
    report = Report.get_by_id(id)
    if not report:
        flash("Denuncia inexistente", 'alert-warning')
        return redirect(url_for("report_index"))
    if report.status == EstadoDenuncia.CERRADA.name or report.status == EstadoDenuncia.RESUELTA.name:
        flash("Acción denegada, no puede editar una denuncia que no esté abierta", 'alert-warning')
        return redirect(url_for("report_index"))
    p={}
    p['coords']=report.coords
    if request.method == "GET":
        return render_template(
            "report/update.html", 
            report=report, 
            seleccionada = report.category,
            categories= ReportCategory.all(), 
            available_asignees=User.users_with_report_manage_permission(), 
            coords=json.dumps(p), 
            estados = EstadoDenuncia
            )
    elif request.method == "POST":

        nuevo_report = Report(
            request.form.get("title"), 
            request.form.get("category"),
            request.form.get("description"),
            request.form.get("coords"),
            request.form.get("fname"),
            request.form.get("lname"),
            request.form.get("phone"),
            request.form.get("email"),
            )

        nuevo_asignado = request.form.get("asignee")

        error_message = ReportValidator.check(nuevo_report)
        if(error_message):
            flash(error_message, 'alert-warning')
            return render_template(
                "report/update.html", 
                report=report, 
                seleccionada = report.category,
                categories= ReportCategory.all(), 
                available_asignees=User.users_with_report_manage_permission(), 
                coords=json.dumps(p)
            )
        
        #tuve que crear doble objeto para evitar fallos en FK de sqlalchemy..
        report.title = nuevo_report.title
        report.category = nuevo_report.category
        report.description = nuevo_report.description
        report.coords = nuevo_report.coords
        report.lname = nuevo_report.lname
        report.fname = nuevo_report.fname
        report.phone = nuevo_report.phone
        report.email = nuevo_report.email

        if (nuevo_asignado and (session.get("user") == report.assigned_to or check_permission(denuncias_change_assignee))):
            error_message = ReportValidator.check_assigned(nuevo_asignado) #evito validar si no modificó
            if (error_message):
                flash (error_message, 'alert-warning')

            elif  nuevo_asignado == "null": #si seleccionó a "Nadie" explicitamente
                if (report.assigned_to == None):
                    flash ("El asignado ya es null. Seleccione otro para cambiarlo, o deje el campo sin seleccionar", 'alert-warning')
                    return render_template(
                        "report/update.html", 
                        report=report, 
                        seleccionada = report.category,
                        categories= ReportCategory.all(), 
                        available_asignees=User.users_with_report_manage_permission(), 
                        coords=json.dumps(p)
                    )
                else:
                    report.assigned_to = None 
                    ReportHistory.add_default(id,"Interno", report.assigned_to)

            elif int(nuevo_asignado) != report.assigned_to: #si seleccionó pasarle el report a otro
            
                report.assigned_to = nuevo_asignado    
                ReportHistory.add_default(id,"Interno", report.assigned_to)
        
        db.save()

    return redirect(url_for("report_index"))

def assign_to(id):
    if not authenticated(session):
        abort(401)
    if not check_permission(denuncias_tracing):
        abort(403)
    report = Report.get_by_id(id)
    if not report:
        flash("Denuncia inexistente", 'alert-warning')
        return redirect(url_for("report_index"))
    if report.assigned_to:
        flash("Acción denegada. Esta denuncia ya se encuentra asignada.", 'alert-warning')
        return redirect(url_for("report_index"))

    report.assigned_to = session.get("user")
    ReportHistory.add_default(id, "Interno", report.assigned_to)
    db.save()
    return redirect(url_for("report_info", id=id))

def tracing(id):
    if not authenticated(session):
        abort(401)
    if not check_permission(denuncias_tracing):
        abort(403)

    descripcion = request.form.get("description")
    error_message= ReportValidator.check_seguimiento(id, descripcion)
    if (error_message):
        flash(error_message, 'alert-warning')
        return redirect(url_for("report_info", id=id))    
        
    report = Report.get_by_id(id)
    # == 2 porque la 3ra es la que va a cargar
    if(ReportHistory.get_external_histories_quantity_by_report_id(id) == 2 and report.status != EstadoDenuncia.ENCURSO.name):
        ReportHistory.add(id,"Se ha cerrado la denuncia por no poder confirmar con denunciante", "Interno")
        report.status = EstadoDenuncia.CERRADA.name
        report.finished_at =  datetime.now()
    
    ReportHistory.add(id, descripcion ,"Externo")
    db.save()  
    return redirect(url_for("report_info", id=id))


def change_status(id):
    
    if not authenticated(session):
        abort(401)
    if not check_permission(denuncias_tracing):
        abort(403)
    
    report = Report.get_by_id(id)
    if not report:
        flash("Denuncia inexistente", 'alert-warning')
        return redirect(url_for("report_info", id=id))   

    status = request.form.get('statusSelect', None)
    puede_actualizarse = change_state_abled(report, status)
    if puede_actualizarse == True:
        if status == EstadoDenuncia.CERRADA.name:
            if not request.form.get('motivoCierre'):
                flash("Para cerrar una denuncia debe indicar un motivo de cierre", 'alert-warning')
                return redirect(url_for("report_info", id=id))   
            ReportHistory.add(id, request.form.get('motivoCierre'), "Externo")
            report.finished_at =  datetime.now()

        if status == EstadoDenuncia.RESUELTA.name:
            report.finished_at =  datetime.now()
            
        ReportHistory.add(id, "El estado de la denuncia a cambiado a: " + status, "Interno")
        report.status = status
        db.save()
    else:
        flash(puede_actualizarse, 'alert-warning')

    return redirect(url_for("report_info", id=id))


def delete(id):
    if not authenticated(session):
        abort(401)

    if not check_permission(denuncias_destroy):
        abort(403)

    if (not Report.get_by_id(id)):
        flash("Denuncia inexistente", 'alert-warning')
        return redirect(url_for("report_index"))
    
    if ReportHistory.get_report_histories_by_report_id(id):
        flash("Solo pueden ser eliminadas las denuncias que no tengan seguimientos iniciados", 'alert-warning')
        return redirect(url_for("report_index"))
        
    Report.delete(id)
    db.save()
    return redirect(url_for("report_index"))
