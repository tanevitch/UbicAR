from app.db import db
from sqlalchemy.inspection import inspect

class Meeting_point(db.Model):
    __tablename__ = 'meeting_point'
    id_point = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    coords = db.Column(db.String(100), nullable = False)
    visible = db.Column(db.Boolean, nullable = False)
    phone = db.Column(db.String(16), nullable = False)
    mail = db.Column(db.String(100), nullable = False)

    def __init__(self, name,address,coords,phone,mail):
        self.name = name
        self.address = address
        self.coords = coords
        self.phone = phone 
        self.mail = mail 
        self.visible = 1
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def delete(cls, id):
        db.session.delete(Meeting_point.get_by_id(id))

    @classmethod
    def add(cls, mp):
        db.session.add(mp)

    @classmethod 
    def filter_by_visibility(cls, isVisible):
        return cls.query.filter(cls.visible == isVisible)


    @classmethod
    def filter_by_address(cls, address):
        return cls.query.filter(cls.address.like(address)).first()

    @classmethod
    def filter_by_name(cls, name):
        return cls.query.filter(cls.name.like(name))

    @classmethod
    def get_sortable_fields(cls):
        '''
        Devuelve los nombres de las columnas de la tabla por las cuales se puede ordenar el módulo
        '''
        return [inspect(cls).c.name.name, inspect(cls).c.mail.name, inspect(cls).c.visible.name, inspect(cls).c.address.name]