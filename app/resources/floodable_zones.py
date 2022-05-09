from flask import redirect, render_template, request, url_for, session, abort
from app.models.floodable_zone import Floodable_Zone
from app import db
from app.validators.fzValidator import FZValidator
from app.helpers.auth import authenticated, check_permission
from app.helpers.paginator import Paginator
from flask.helpers import flash
from app.helpers.constants import zonas_inundables_destroy, zonas_inundables_show, zonas_inundables_create, zonas_inundables_index, zonas_inundables_update, zonas_inundables_change_status
import json
import pandas as pd

from app.validators.genericValidator import check_empty_fields
def index(page):
    if not authenticated(session):
        abort(401)
    
    if not check_permission(zonas_inundables_index):
        abort(403)

    if request.args.get('fz_name'):   
        buscar = "%{}%".format(request.args.get('fz_name'))
        zonas = Paginator.paginate(Floodable_Zone.filter_by_name(buscar), Floodable_Zone, page)
       
    elif request.args.get('isVisible'):
        zonas=Paginator.paginate(Floodable_Zone.filter_by_status(request.args.get('isVisible')), Floodable_Zone, page)
    else:
        zonas= Paginator.paginate(Floodable_Zone.query, Floodable_Zone, page)
        # 
    #formateo en json para que me lo tome el js
    data={}
    c=0
    for i in zonas.items:
        data[str(c)+'name']=i.name
        data[str(c)+'coords']=i.coords
        data[str(c)+'color']=i.color
        c+=1
    return render_template("floodable_zones/index.html", puntos = zonas,data=json.dumps(data))

def info(id):
    if not authenticated(session):
        abort(401)
    
    if not check_permission(zonas_inundables_show):
        abort(403)

    fz = Floodable_Zone.get_by_id(id)
    if fz:
        data={}
        c=0
        data[str(c)+'name']=fz.name
        data[str(c)+'coords']=fz.coords
        data[str(c)+'color']=fz.color
        coordsIniciales=json.loads(fz.coords)[0]
        cantidad=len(json.loads(fz.coords))
        return render_template("floodable_zones/info.html", mp = fz,data=json.dumps(data),inicio=json.dumps(coordsIniciales),cant=cantidad)

def delete(id):
    if not authenticated(session):
        abort(401)
    
    if not check_permission(zonas_inundables_destroy):
        abort(403)
    
    fz = Floodable_Zone.get_by_id(id)
    if (fz):
        Floodable_Zone.delete(id)
        db.save()
        flash("Se eliminó la zona inundable", 'alert-success')
    else:
        flash("No se encontró la zona inundable con ese id", 'alert-warning')
    return redirect(url_for("fz_index"))


def changeStatus(id):
    if not authenticated(session):
        abort(401)

    if not check_permission(zonas_inundables_change_status):
        abort(403)

    fz = Floodable_Zone.get_by_id(id)
    if (fz):
        fz.status = not fz.status
        db.save()
        if (fz.status):
            flash("Se cambió el estado a publicado", 'alert-success')
        else:
            flash("Se cambió el estado a no publicado", 'alert-success')
    else:
       flash("No se encontró la zona con esa id", 'alert-warning')
        
    return redirect(url_for("fz_index"))


def create():
    if not authenticated(session):
        abort(401)
    if not check_permission(zonas_inundables_create):
        abort(403)
    try:
        if request.method== "GET":
            return render_template("floodable_zones/new.html")
    
        elif request.method == "POST":
            uploaded_file = request.files['file']
            error_message= check_empty_fields([uploaded_file.filename])
            if (error_message):
                flash(error_message, 'alert-warning')
                return render_template("floodable_zones/new.html")

            #leo el input csv: si subio el archhivo proceso archivo sino subio archivo no hago nada :) --> informo error
            #el csv va a contener todos los datos que pide    
            try:
                read = pd.read_csv(uploaded_file)
                if (len(read.columns)!=5):
                    flash("Error Archivo no valido, debe contener: name,area,codigo_area,color,publicado",'alert-warning')
                    return redirect(url_for("fz_index"))

            except:
                flash("Error Archivo no valido",'alert-warning')
                return redirect(url_for("fz_index"))
        
            nombres=[]
            coords=[]#chequear que sean pares[lat,long]
            datosInvalido=False
        #proceso archivo: leo cada fila(row) del archivo y me fijo si almenos tiene 3 o mas de 3 puntos para que sea valido
        #si el nombre de zona existe actualizo la tupla de la bd
            for row in range(0,len(read.index)):
                    
                msj_coord_inv = FZValidator.check_coordsList(json.loads(read.iloc[row][1]))
                if (msj_coord_inv):
                    flash(msj_coord_inv+ " en : "+read.iloc[row][0],'alert-warning')
                    return redirect(url_for("fz_index"))

                nombres.append(read.iloc[row][0])
                coords.append(read.iloc[row][1])
                if (str(read.iloc[row][4])=="True"):
                    status=True
                else:
                    status=False
                    
                checkExist = Floodable_Zone.filter_by_zonecode(read.iloc[row][2])
                
                if (FZValidator.check_lenght(json.loads(read.iloc[row][1]))):
                    if checkExist:
                    #si existe lo tengo que actualizar
                        checkExist.name=read.iloc[row][0]
                        checkExist.coords=read.iloc[row][1]
                        checkExist.zone_code=read.iloc[row][2]
                        checkExist.color=read.iloc[row][3]
                        checkExist.status=status
                        Floodable_Zone.add(checkExist)       
                    else:
                        fz = (Floodable_Zone(
                        name=read.iloc[row][0],
                        coords=read.iloc[row][1],
                        zone_code=read.iloc[row][2],
                        color=read.iloc[row][3],
                        status=status,
                        ))
                        Floodable_Zone.add(fz)
                else:
                    datosInvalido=True
                    dato=read.iloc[row][0]
                    break      

            db.save()
            if (datosInvalido):
                flash("Error "+dato+" es invalido tiene menos de 3 coordenadas. Corríjalo para resubir el archivo",'alert-warning')
            return redirect(url_for("fz_index"))
    except:
        flash("El archivo es invalido por tipos o hay algun dato que es invalido",'alert-warning')
        return redirect(url_for("fz_index"))