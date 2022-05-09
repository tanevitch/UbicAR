from app.db import db

class Module_config(db.Model):
    __tablename__ = 'module_config'
    id_module_config = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    order = db.Column(db.String(4), nullable = False)
    sort_field = db.Column(db.String(50), nullable = False)

    def __init__(self, name, order, sort_field):
        self.name = name
        self.order = order
        self.sort_field= sort_field

    @classmethod
    def get_module_config(cls,name):
        return cls.query.filter_by(name = name).first()

    @classmethod
    def get_modules_config(cls):
        dic= {}
        modulos = cls.query.all()
        for modulo in modulos:
            dic[modulo.name]=[modulo.order, modulo.sort_field]

        return dic
