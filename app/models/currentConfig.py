from app.db import db

class Current_config(db.Model):
    __tablename__ = 'current_config'
    id_currentConfig = db.Column(db.Integer(), primary_key = True)
    pages = db.Column(db.Integer(), nullable = False)
    currentColor_public = db.Column(db.Integer(), nullable = False)
    currentColor_private = db.Column(db.Integer(), nullable = False)

    def __init__(self, pages,currentColor_public, currentColor_private):
        self.pages = pages
        self.currentColor_public = currentColor_public
        self.currentColor_private = currentColor_private

    @classmethod
    def get_results_per_page(cls):
        return cls.get_actual_config().pages

    @classmethod
    def get_actual_config(cls):
        return cls.query.first()

    