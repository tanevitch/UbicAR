from sqlalchemy.orm import relation, relationship
from app.db import db
from app.models.role_permission import role_permission
from app.models.permission import Permission

class Role(db.Model):
    __tablename__ = 'role'
    id_role = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(15), nullable = False)
    permisos = relationship(Permission, secondary=role_permission, backref=db.backref('roles'))

    def __init__(self, name):
        self.name= name

    @classmethod
    def all(cls):
        return cls.query.all()
        
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_name_by_id(cls, id):
        return cls.query.get(id).name

    @classmethod
    def get_all_names(cls):
        return list(map(lambda role: role.name, cls.all()))

    @classmethod
    def check_if_any_has_change_roles(cls, roles):
        for role in roles:
            selected_role_with_change_role_permission = cls.query.filter_by(name=role).join((Permission, cls.permisos)).filter(Permission.name == "usuario_change_roles").all()
            if selected_role_with_change_role_permission: #Si seleccionó un rol que tiene permisos para cambiar los roles
                return True