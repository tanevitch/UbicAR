from sqlalchemy.inspection import inspect
from app.db import db
from sqlalchemy.dialects.mysql import LONGTEXT

class Floodable_Zone(db.Model):
    __tablename__ = 'floodable_zone'
    id_floodableZone = db.Column(db.Integer(), primary_key = True)
    zone_code = db.Column(db.String(16), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    coords = db.Column(LONGTEXT, nullable = False)
    status = db.Column(db.Boolean(), nullable = False)
    color = db.Column(db.String(7), nullable = False)

    def __init__(self, zone_code, name, coords, status, color):
        self.zone_code = zone_code
        self.name = name
        self.coords = coords
        self.status = status
        self.color = color

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def delete(cls, id):
        db.session.delete(Floodable_Zone.get_by_id(id))

    @classmethod
    def add(cls, fz):
        db.session.add(fz)

    @classmethod 
    def filter_by_status(cls, stat):
        return cls.query.filter(cls.status == stat)

    @classmethod
    def filter_by_name(cls, name):
        return cls.query.filter(cls.name.like(name))
    @classmethod
    def filter_by_zonecode(cls, zonecode):
        return cls.query.filter_by(zone_code = zonecode).first()

        