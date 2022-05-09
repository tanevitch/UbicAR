from flask import redirect, render_template, request, url_for, session, abort
from app.models.evacuation_route import Evacuation_Route
from app import db
from app.helpers.auth import authenticated, check_permission
from flask.helpers import flash
from app.helpers.constants import evacuation_route_index, evacuation_route_destroy, evacuation_route_update, evacuation_route_show, evacuation_route_create, evacuation_route_change_status
from app.helpers.paginator import Paginator
from app.validators.routeValidator import eRouteValidator

import json


def index(page):
    if not authenticated(session):
        abort(401)
    
    if not check_permission(evacuation_route_index):
        abort(403)
    
    if request.args.get('er_name'):   
        buscar = "%{}%".format(request.args.get('er_name'))
        routes = Paginator.paginate(Evacuation_Route.filter_by_name(buscar), Evacuation_Route, page)
    elif request.args.get('status'):
        if (request.args.get('status') == '0' or request.args.get('status') == '1'):
            routes= Paginator.paginate(Evacuation_Route.filter_by_status(int(request.args.get('status'))), Evacuation_Route, page)
        else:
            flash("Error en filtro de búsqueda por estado, parámetro inválido", 'alert-warning')
            return redirect(url_for("eRoutes_index"))
    else:
        routes= Paginator.paginate(Evacuation_Route.query, Evacuation_Route, page)

    data={}
    c=0
    for r in routes.items:
        data[str(c)+'name']=r.name
        data[str(c)+'coords']=r.coords
        data[str(c)+'color']=r.color
        c+=1

    return render_template("evacuation_route/index.html", routes = routes,data=json.dumps(data))

def create():
    
    if not authenticated(session):
        abort(401)

    if not check_permission(evacuation_route_create):
        abort(403)

    if request.method== "GET":
        return render_template("evacuation_route/new.html")
    
    elif request.method == "POST":
        name=request.form.get("name")
        er = (Evacuation_Route(
            name=name,
            description=request.form.get("description"),
            color= request.form.get("color"),
            coords= request.form.get("latAndLong")
            ))
        error_message= eRouteValidator.check_create(er.name, er.description, er.color, er.coords)
        if (error_message):
            flash(error_message, 'alert-warning')
            return render_template("evacuation_route/new.html") 
        Evacuation_Route.add(er)
        db.save()
        flash("Ruta creada", 'alert-success')
        return redirect(url_for("eRoutes_index"))

def info(id):

    if not authenticated(session):
        abort(401)
    
    if not check_permission(evacuation_route_show):
        abort(403)


    er = Evacuation_Route.get_by_id(id)
    if er:
        data={}
        data['name']=er.name
        data['coords']="[" + er.coords + "]"
        data['color']=er.color
        coordsIniciales=json.loads(data['coords'])[0]
        return render_template("evacuation_route/info.html", er = er,data=json.dumps(data),inicio=json.dumps(coordsIniciales))

    if er:
        return render_template("evacuation_route/info.html", er=er)
    else:
        flash("Ruta de evacuación inexistente", 'alert-warning')
        return redirect(url_for("eRoutes_index"))
    


def update(id):
    if not authenticated(session):
        abort(401)
    if not check_permission(evacuation_route_update):
        abort(403)
    eRoute = Evacuation_Route.get_by_id(id)
    if not eRoute:
        flash("Ruta inexistente", 'alert-warning')
        return redirect(url_for("eRoutes_index"))

    if request.method == 'GET':
        e={}
        e['coords']="[" + eRoute.coords + "]"
        e['color'] = eRoute.color
        coordsIniciales=json.loads( e['coords'])[0]

        return render_template("evacuation_route/update.html",id=id,data=eRoute,coords=json.dumps(e),inicio=json.dumps(coordsIniciales))
    if request.method == 'POST':
        error_message= eRouteValidator.check_create(request.form.get("name"), request.form.get("description"), request.form.get("color"), request.form.get("latAndLong"))
        if (error_message):
            flash(error_message, 'alert-warning')
            return redirect(url_for("eRoutes_index"))
        eRoute.name = request.form.get("name")
        eRoute.description = request.form.get("description")
        eRoute.color = request.form.get("color")
        eRoute.coords = request.form.get("latAndLong")
        db.save()
    flash("Ruta actualizada", 'alert-success')
    return redirect(url_for("eRoutes_index"))


def changeStatus(id):
    
    if not authenticated(session):
        abort(401)

    if not check_permission(evacuation_route_change_status):
        abort(403)

    eRoute = Evacuation_Route.get_by_id(id)
    if (eRoute):
        eRoute.status = not eRoute.status
        db.save()
        if (eRoute.status):
            flash("Se cambió el estado de la ruta a publicado", 'alert-success')
        else:
            flash("Se cambió el estado de la ruta a no publicado", 'alert-success')
    else:
       flash("No se encontró una ruta con ese id", 'alert-warning')
        
    return redirect(url_for("eRoutes_index"))

def delete(id):
    
    if not authenticated(session):
        abort(401)
    
    if not check_permission(evacuation_route_destroy):
        abort(403)
    
    er = Evacuation_Route.get_by_id(id)
    if (er):
        Evacuation_Route.delete(id)
        db.save()
        flash("Se eliminó la ruta de evacuación", 'alert-success')
    else:
        flash("No se encontró la ruta de evacuación con ese id", 'alert-warning')
    return redirect(url_for("eRoutes_index"))