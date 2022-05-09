from app.db import db

role_permission= db.Table('role_permission',
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id_role', ondelete="CASCADE"), primary_key=True),
    db.Column('permission_id', db.Integer(), db.ForeignKey('permission.id_permission', ondelete="CASCADE"), primary_key=True)
)
