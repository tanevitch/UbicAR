from app.db import db

class ReportCategory(db.Model):
    __tablename__ = 'report_category'
    id_report_category = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100), unique = True)

    def __init__(self, name):
        self.name= name

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()