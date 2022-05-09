from app.db import db

user_role= db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id_user', ondelete="CASCADE"), primary_key=True),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id_role', ondelete="CASCADE"), primary_key=True)
)

