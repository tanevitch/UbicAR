from sqlalchemy.inspection import inspect
from app.db import db
from datetime import  datetime
from app.models.user import User
from app.helpers.constants import EstadoDenuncia

class Report(db.Model):
    __tablename__ = 'report'
    id_report = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    category = db.Column(db.Integer(), db.ForeignKey('report_category.id_report_category'))
    created_at = db.Column(db.DateTime, nullable = False)
    finished_at = db.Column(db.DateTime)
    description = db.Column(db.String(500), nullable = False)
    coords = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(100), nullable = False)
    assigned_to = db.Column(db.Integer(), db.ForeignKey('user.id_user', ondelete='SET NULL'))
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(16), nullable = False)
    email = db.Column(db.String(100), nullable = False)

    def __init__(self, title, category, description, coords, fname, lname, phone, email):
        
        self.title = title
        self.category = category
        self.created_at = datetime.now()
        self.description = description
        self.coords = coords
        self.status = EstadoDenuncia.SINCONFIRMAR.name
        self.fname = fname
        self.lname = lname
        self.phone = phone
        self.email = email

    @classmethod
    def add(cls, report):
        db.session.add(report)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def filter_by_title(cls, title):
        return cls.query.filter(cls.title.like(title))

    @classmethod
    def filter_by_period(cls, start, end):
        return cls.query.filter(cls.created_at.between(start, end))

    @classmethod
    def filter_by_state(cls, status):
        return cls.query.filter(cls.status == status)

    @classmethod
    def filter_by_assigned_to(cls, user):
        return cls.query.filter(cls.assigned_to == user)

    @classmethod
    def delete(cls, id):
        db.session.delete(cls.get_by_id(id))

    @classmethod
    def get_sortable_fields(cls):
        return [inspect(cls).c.title.name]

    @classmethod
    def get_user_assigned(cls, id):
        return User.get_by_id(cls.get_by_id(id).assigned_to)

    @classmethod
    def get_unassigned(cls):
        return cls.query.filter(cls.assigned_to == None)
        