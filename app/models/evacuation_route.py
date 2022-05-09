from app.db import db
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.inspection import inspect


class Evacuation_Route(db.Model):
    __tablename__ = 'evacuation_route'
    id_eRoute = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(100), nullable = False)
    coords = db.Column(LONGTEXT, nullable = False)
    status = db.Column(db.Boolean, nullable = False, default=True)
    color = db.Column(db.String(7), nullable = False)

    def __init__(self, name, description, coords, color):
        self.name = name
        self.description = description
        self.coords = coords
        self.color = color

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def filter_by_name(cls, name):
        return cls.query.filter(cls.name.like(name))

    @classmethod 
    def filter_by_status(cls, status):
        return cls.query.filter(cls.status == status)

    @classmethod
    def delete(cls, id):
        db.session.delete(Evacuation_Route.get_by_id(id))

    @classmethod
    def add(cls, er):
        db.session.add(er)

    @classmethod
    def get_sortable_fields(cls):

        return [inspect(cls).c.name.name, inspect(cls).c.status.name]