from flask import redirect, render_template, request, url_for, session, abort
from app.helpers.paginator import Paginator
from app.models.meeting_point import Meeting_point
from app import db
from sqlalchemy import asc, desc
from app.helpers.auth import authenticated, check_permission
from flask.helpers import flash
from app.validators.mpValidator import MPValidator
from app.helpers.constants import punto_de_encuentro_destroy, punto_de_encuentro_show, punto_de_encuentro_index, punto_de_encuentro_update, punto_de_encuentro_create, punto_de_encuentro_change_visibility
import json

def index(page):
    if not authenticated(session):
        abort(401)
    
    if not check_permission(punto_de_encuentro_index):
        abort(403)
    
    if request.args.get('mp_name'):   
        buscar = "%{}%".format(request.args.get('mp_name'))
        puntos = Paginator.paginate(Meeting_point.filter_by_name(buscar), Meeting_point, page)
    elif request.args.get('isVisible'):
        puntos= Paginator.paginate(Meeting_point.filter_by_visibility(request.args.get('isVisible')), Meeting_point, page)
    else:
        puntos= Paginator.paginate(Meeting_point.query, Meeting_point, page)
    data={}
    c=0
    for i in puntos.items:
        data[str(c)+'n']=i.name
        data[str(c)+'coords']=i.coords
        c+=1

    return render_template("meeting_point/index.html", puntos = puntos,data=json.dumps(data))


def edit(id):
    if not authenticated(session):
        abort(401)
    
    if not check_permission(punto_de_encuentro_update):
        abort(403)

    meeting_point=Meeting_point.get_by_id(id)
    if (not meeting_point):
        flash("No existe punto de encuentro con ese ID", 'alert-warning')
        return redirect(url_for("mp_index"))

    if request.method == 'GET':
        p={}
        p['coords']=meeting_point.coords

        return render_template("meeting_point/edit.html",id=id,data=meeting_point,coords=json.dumps(p))

    elif request.method == 'POST':
        checkExist = Meeting_point.filter_by_address(request.form.get("direccion"))

        if checkExist and checkExist.id_point != meeting_point.id_point:
            flash("Ya existe un punto de encuentro con esa direccion", 'alert-warning')
            return redirect(url_for('mp_edit', id=id))

        meeting_point.name=request.form.get("nombre")
        meeting_point.address= request.form.get("direccion")
        meeting_point.coords=request.form.get("coords")
        meeting_point.phone= request.form.get("telefono")
        meeting_point.mail=request.form.get("email")
        
        error= MPValidator.emptyFields(meeting_point)
        if error:
            flash(error, 'alert-warning')
            return redirect(url_for('mp_edit', id=id))
        
        error = MPValidator.invalidType(meeting_point)
        if error:
            flash(error, 'alert-warning')
            return redirect(url_for('mp_edit', id=id))
        
        db.save()
        return redirect(url_for("mp_index"))

def info(id):
    if not authenticated(session):
        abort(401)
    
    if not check_permission(punto_de_encuentro_show):
        abort(403)


    mp = Meeting_point.get_by_id(id)

    if mp:
        p={}
        p['coords']=mp.coords
        return render_template("meeting_point/info.html", mp = mp, coords=json.dumps(p))
    else:
        flash("Punto de encuentro inexistente", 'alert-warning')
        return redirect(url_for("mp_index"))
    

def create():
    if not authenticated(session):
        abort(401)
    if not check_permission(punto_de_encuentro_create):
        abort(403)

    if request.method== "GET":
        return render_template("meeting_point/new.html")

    elif request.method == "POST":
        address=request.form.get("direccion")
        checkExist = Meeting_point.filter_by_address(address)
        if (checkExist):
            flash("Ya existe un punto de encuentro con esa direccion", 'alert-warning')
            return render_template("meeting_point/new.html")
        else:
            mp = (Meeting_point(
                name=request.form.get("nombre"),
                address= request.form.get("direccion"),
                coords=request.form.get("coords"),
                phone= request.form.get("telefono"),
                mail=request.form.get("email")
                ))

            error_message_emptyFields= MPValidator.emptyFields(mp)
            if error_message_emptyFields:
                flash(error_message_emptyFields, 'alert-warning')
                return render_template("meeting_point/new.html")
            
            error_message_invalidType= MPValidator.invalidType(mp)
            if error_message_invalidType:
                flash(error_message_invalidType, 'alert-warning')
                return render_template("meeting_point/new.html")
            Meeting_point.add(mp)
            db.save()
        return redirect(url_for("mp_index"))



def changeVisibility(id):
    if not authenticated(session):
        abort(401)

    if not check_permission(punto_de_encuentro_change_visibility):
        abort(403)

    mp = Meeting_point.get_by_id(id)
    if (mp):
        mp.visible = not mp.visible
        db.save()
        if (mp.visible):
            flash("Se cambió la visibilidad del punto a Visible", 'alert-success')
        else:
            flash("Se cambió la visibilidad del punto a No Visible", 'alert-success')
    else:
       flash("No se encontró el punto de encuentro con esa id", 'alert-warning')
        
    return redirect(url_for("mp_index"))


def delete(id):
    if not authenticated(session):
        abort(401)
    
    if not check_permission(punto_de_encuentro_destroy):
        abort(403)
    
    mp = Meeting_point.get_by_id(id)
    if (mp):
        Meeting_point.delete(id)
        db.save()
        flash("Se eliminó el punto de encuentro", 'alert-success')
    else:
        flash("No se encontró el punto de encuentro con esa id", 'alert-warning')
    return redirect(url_for("mp_index"))
