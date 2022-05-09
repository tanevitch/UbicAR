from sqlalchemy.orm import relationship
from app.db import db

class Permission(db.Model):
    __tablename__ = 'permission'
    id_permission = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100), nullable = False)

    def __init__(self, name):
        self.name= name

         
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()