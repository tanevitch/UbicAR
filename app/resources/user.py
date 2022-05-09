
from typing import Counter
from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.helpers.paginator import Paginator
from app.validators.userValidator import UserValidator
from app.validators.genericValidator import check_role
from app.models.user import User
from app.models.role import Role
from app.helpers.auth import authenticated, check_permission
from flask_bcrypt import Bcrypt
from app import db
from app.helpers.constants import usuario_aprobacion, usuario_change_roles, usuario_update_others, usuario_update, usuario_index, usuario_toggle_availability, usuario_destroy, usuario_create, usuario_show
from datetime import datetime
b_crypt=Bcrypt()

def index(page):
    if not authenticated(session):
        abort(401)
    if not check_permission(usuario_index):
        abort(403)
    
    
    if request.args.get('username'):
        buscar = "%{}%".format(request.args.get('username'))
        users= Paginator.paginate(User.filter_by_name(buscar), User, page)
    elif request.args.get('is_active'):
        users = Paginator.paginate(User.filter_by_active(request.args.get('is_active')), User, page)
    else:    
        users = Paginator.paginate(User.all(), User, page)
    return render_template("user/index.html", users=users)


def toggleAvailability(id):
    if not authenticated(session): 
        abort(401)
    if not check_permission(usuario_toggle_availability):
        abort(403)

    user = User.get_by_id(id)
    if (not user):
        flash("No se encontró el usuario con ese id", 'alert-warning')
        return redirect(url_for("user_index"))
    
    if (not Role.find_by_name('admin') in User.get_roles(user.id_user) or not user.is_active):
        user.is_active= not user.is_active
        db.save()
    else:
        flash("Usuarios con rol administrador no pueden ser desactivados", 'alert-warning')
    return redirect(url_for("user_index"))

def delete(id):
    if not authenticated(session):
        abort(401)

    if not check_permission(usuario_destroy):
        abort(403)

    if (not User.get_by_id(id)):
        flash("Usuario inexistente", 'alert-warning')
        return redirect(url_for("user_index"))

    if (session.get("user") == User.get_by_id(id).id_user):
        flash("Acción denegada. No puede eliminarse a sí mismo", 'alert-warning')
        return redirect(url_for("user_index"))
    
    session[id] = None
    User.delete(id)
    db.save()
    return redirect(url_for("user_index"))

def info(id):
    if not authenticated(session):
        abort(401)
    if not check_permission(usuario_show):
        abort(403)
    user = User.get_by_id(id)
    if user:
        return render_template("user/info.html", user=user)
    else:
        flash("Usuario inexistente", 'alert-warning')
        return redirect(url_for("user_index"))

def create_google(datos_google):
    '''
    Registra un usuario nuevo con cuenta desactivada, con nombre de usuario la parte izquierda del @ del mail de Google, si no existe en el sistema
    
    Si existe, registra un usuario nuevo con cuenta desactivada, agregandole un número único atrás del nombre de usuario asignado (determinado por el la parte izquierda del @ del mail de google)
    
    Si el mail ya está en uso, la persona se registró de otra manera, por lo que no puede darse de alta con google, deberá ingresar de la manera que corresponda
    '''

    username = datos_google["email"].split("@")[0]
    user = User.filter_by_username(username)

    if not user:
        user = User(
        email=datos_google["email"],
        username= username,
        password= None,
        is_active=False,
        fname=datos_google["given_name"],
        lname=datos_google["family_name"]
        )
        User.add(user)
        db.save()
    else:
        
        users= [user.username for user in User.username_exists(username)]
        bool = True
        aux = 1
        while bool:
            if not username+str(aux) in users:
                bool=False
                user = User(
                email=datos_google["email"],
                username= username+str(aux),
                password= None,
                is_active=False,
                fname=datos_google["given_name"],
                lname=datos_google["family_name"]
                )
                User.add(user)
                db.save()
            aux+=1
        
    

def create():
    if not authenticated(session):
        abort(401)

    if not check_permission(usuario_create):
        abort(403)

    if request.method== "GET":
        return render_template("user/new.html", roles=Role.get_all_names())

    elif request.method == "POST":
        email= request.form.get("email")
        username= request.form.get("username")
        password= request.form.get("password")
        fname=request.form.get("fname")
        lname=request.form.get("lname")
        roles_form= request.form.getlist('roles')

        
        error_message= UserValidator.check_create(email, username, password, fname, lname, roles_form)

        if (error_message):
            flash(error_message, 'alert-warning')
            return render_template("user/new.html", roles=Role.get_all_names())   
        else:
            u= User(
                email=email,
                username= username,
                password= b_crypt.generate_password_hash(password),
                fname=fname,
                lname=lname
                )
            
            for selected_role in roles_form:
                rol= Role.find_by_name(selected_role)
                u.roles.append(rol)

            User.add(u)
            db.save()

        return redirect(url_for("user_index"))


def update(id):
    if not authenticated(session):
        abort(401)

    if not check_permission(usuario_update):
        abort(403)


    user = User.get_by_id(id)
    if (not user):
        flash("Usuario inexistente", 'alert-warning')
        return redirect(url_for("user_index"))

    if(session.get("user") != user.id_user and not check_permission(usuario_update_others)):
        flash("Acción denegada. No tiene permiso para editar a este usuario", 'alert-warning')
        return redirect(url_for("user_index"))


    roles=get_roles_for_checkbox(id)
    if request.method== "GET":
        return render_template("user/update.html", 
            roles_que_tiene=roles[0], 
            user=user, 
            roles_que_no_tiene=roles[1] 
        )
    
    elif request.method == "POST":          
        email= request.form.get("email")
        username= request.form.get("username")
        password= request.form.get("password")
        fname=request.form.get("fname")
        lname=request.form.get("lname")

        seleccionados= request.form.getlist('roles') 

        if user.password == None: #se registro por red social
            email= user.email

        error_message= UserValidator.check_edit(user.id_user, email, username, password, fname, lname, seleccionados)
        if (error_message):
            flash(error_message, 'alert-warning')
            return render_template("user/update.html", 
                roles_que_tiene=roles[0], 
                user=user, 
                roles_que_no_tiene=roles[1] 
            )
        else:
            user.email = email
            user.username = username
            user.fname = fname
            user.lname = lname
            user.updated_at = datetime.now()

            if password:
                user.password = b_crypt.generate_password_hash(password)

            if(seleccionados and set(seleccionados) != set(User.get_user_roles_names(user.id_user))): #si selecciono los mismos que tiene, que no escriba de nuevo
                user.roles.clear()
                for selected_role in seleccionados:
                    rol= Role.find_by_name(selected_role)
                    user.roles.append(rol)

            db.save()
        return redirect(url_for("user_index"))

def get_roles_for_checkbox(id):
    '''
    Devolverá por separardo la lista de roles que el usuario a editar tiene, de los que no tiene.
    Así, se marcará como "seleccionado" el checkbox correspondiente al rol que sí tenga, y el resto no
    '''
    roles_que_tiene= User.get_user_roles_names(id)
    roles_que_no_tiene= list((Counter(Role.get_all_names()) - Counter(roles_que_tiene)).elements())
    return roles_que_tiene, roles_que_no_tiene

def approve(page):
    if not authenticated(session):
        abort(401)

    if not check_permission(usuario_aprobacion) or not check_permission(usuario_change_roles):
        abort(403)

    if request.args.get('lname'):
        buscar = "%{}%".format(request.args.get('lname'))
        users= Paginator.paginate(User.filter_social_network_by_lname(buscar), User, page)
    else:    
        users = Paginator.paginate(User.get_social_network_registers(), User, page)
    
    return render_template("user/approve.html", users=users, roles=Role.get_all_names())


def post_approve(id):
    if not authenticated(session):
        abort(401)

    if not check_permission(usuario_aprobacion) or not check_permission(usuario_change_roles):
        abort(403)

    user = User.get_by_id(id)
    if not user:
        flash("No se encontró el usuario con ese id", 'alert-warning')
        return redirect(url_for("user_approvement"))
    
    roles_form= request.form.getlist('roles')
    if len(roles_form) == 0:
        flash("Debe seleccionar al menos un rol para aprobar un usuario", 'alert-warning')
        return redirect(url_for("user_approvement"))

    for selected_role in roles_form:
        rol = check_role(selected_role)
        if not rol:
            flash("Ha seleccionado un rol inválido. Seleccione roles válidos e inténtelo nuevamente", 'alert-warning')
            return redirect(url_for("user_approvement"))
        user.roles.append(rol)

    user.is_active= True 
    db.save()
    return redirect(url_for("user_approvement"))