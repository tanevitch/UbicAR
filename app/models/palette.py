from app.db import db

from app.models.currentConfig import Current_config
class Palette(db.Model):
    __tablename__ = 'palette'
    id_palette = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100), nullable = False)

    def __init__(self, name):
        self.name= name

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(id_palette=name).first()

    @classmethod
    def get_current_color_public(cls):
        return cls.query.join(Current_config, Current_config.currentColor_public == cls.id_palette).first().name
    
    @classmethod
    def get_current_color_private(cls):
        return cls.query.join(Current_config, Current_config.currentColor_private == cls.id_palette).first().name
