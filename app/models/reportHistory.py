from app.db import db
from datetime import datetime
from flask import session
from app.models.user import User
from sqlalchemy import desc

class ReportHistory(db.Model):
    __tablename__ = 'report_history'
    id_reportHistory = db.Column(db.Integer(), primary_key = True)
    report_id  = db.Column(db.Integer(), db.ForeignKey('report.id_report'))
    description = db.Column(db.String(500), nullable = False)
    author = db.Column(db.Integer(), db.ForeignKey('user.id_user', ondelete='SET NULL'))
    date =  db.Column(db.DateTime, nullable = False)
    origin = db.Column(db.String(20),nullable=False)

    def __init__(self, report_id, description, author, origin):
        self.report_id = report_id
        self.description = description
        self.author = author
        self.origin = origin
        self.date = datetime.now()

    @classmethod
    def add(cls, id_report, description, origin):
        report_history = ReportHistory(id_report, description, session.get("user"), origin)
        db.session.add(report_history)
        db.session.commit()

    @classmethod
    def add_default(cls, id_report, origin, id_user):
        user = User.get_by_id(id_user)
        if user:
            report_history = ReportHistory(id_report, "Se ha cambiado el asignado de seguimiento de la denuncia a "+ user.username, session.get("user"), origin)
        else: 
            report_history = ReportHistory(id_report, "Se ha desasignado la denuncia", session.get("user"), origin)
        db.session.add(report_history)
        db.session.commit()
    
    @classmethod
    def get_report_histories_by_report_id(cls,id_report):
        return db.session.query(User, cls).join(User,User.id_user == cls.author, isouter=True).filter(cls.report_id == id_report).order_by(desc('date')).all()
    
    @classmethod
    def get_external_histories_quantity_by_report_id(cls, id_report):
        return db.session.query(cls).filter(cls.report_id == id_report, cls.origin == "Externo").count()
    

