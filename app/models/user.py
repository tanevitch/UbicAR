from datetime import  datetime
from flask import session
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship
from app.db import db
from app.models.permission import Permission
from app.models.role import Role
from app.models.user_role import user_role
from app.helpers.constants import usuario_change_roles, denuncias_tracing

class User(db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(100), unique=True, nullable = False)
    username = db.Column(db.String(100), unique=True, nullable = False)
    password = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, nullable = False)
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable = False)
    updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    roles = relationship(Role, secondary=user_role, backref=db.backref('users'))
    
    def __init__(self, email, username, password, fname, lname, is_active=1):
        self.email = email
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname 
        self.created_at= datetime.now()
        self.updated_at= datetime.now()
        self.is_active= is_active

    @classmethod
    def get_social_network_registers(cls):
        return cls.query.filter(cls.roles == None)

    @classmethod
    def get_roles(cls, id):
        return cls.get_by_id(id).roles

    @classmethod 
    def filter_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def username_exists(cls, username):
        return cls.query.filter(cls.username.like(username+"%")).all()

    @classmethod 
    def filter_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def filter_by_name(cls, name):
        return cls.query.filter((cls.username.like(name)) & (cls.roles != None))

    @classmethod
    def filter_social_network_by_lname(cls, lname):
        return cls.get_social_network_registers().filter(cls.lname.like(lname))

    @classmethod
    def filter_by_active(cls, is_active):
        return cls.query.filter((cls.is_active==is_active) & (cls.roles != None))

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def delete(cls, id):
        db.session.delete(cls.get_by_id(id))

    @classmethod
    def add(cls, user):
        db.session.add(user)

    @classmethod
    def has_permission(cls, permission):
        roles= cls.get_by_id(session.get("user")).roles
        for rol in roles:
            for permiso in Role.find_by_name(rol.name).permisos:
                if permiso.name == permission:
                    return True
        return False

    @classmethod
    def last_user_with_change_roles_permission(cls, id_user):
        user = db.session.query(cls).join((Role, cls.roles)).join((Permission, Role.permisos)).filter(Permission.name == usuario_change_roles).filter(User.is_active).all()
        if len(list(user)) == 1 and id_user == user[0].id_user: # es el ultimo usuario con posibilidad de cambiar roles
            return True

    @classmethod
    def get_sortable_fields(cls):
        '''
        Devuelve los nombres de las columnas de la tabla por las cuales se puede ordenar el módulo
        '''
        return [inspect(cls).c.username.name, inspect(cls).c.email.name, inspect(cls).c.is_active.name]


    @classmethod
    def get_user_roles_names(cls, id):
        roles_list = []
        for rol in cls.get_roles(id):
            roles_list.append(rol.name)

        return roles_list

    @classmethod
    def users_with_report_manage_permission(cls):
        return db.session.query(cls).join((Role, cls.roles)).join((Permission, Role.permisos)).filter(Permission.name == denuncias_tracing).all()

    @classmethod
    def all(cls):
        return cls.query.filter(cls.roles != None)