import unittest
import sys
sys.path.append('../')
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.db import db 
from app import create_app
from sqlalchemy.exc import IntegrityError

create_app()
#TEST CORREN CON python -m unittest nombre_clase.py (parado en la carpeta test)

class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        ivan = User("ivanscopel@gmail.com", "iscopel", "1234", "Ivan", "Scopel")
        juli = User("julidelleville@gmail.com", "jdelleville", "1234", "Juli", "Delle Ville")
        rol_operario = Role("operario")
        rol_admin = Role("admin")
        permiso_crear_user = Permission("crear_user")
        permiso_listar_user = Permission("listar_user")
        rol_operario.permisos.append(permiso_crear_user)
        rol_admin.permisos.append(permiso_crear_user)
        rol_admin.permisos.append(permiso_listar_user)
        juli.roles.append(rol_admin)
        ivan.roles.append(rol_admin)
        ivan.roles.append(rol_operario)
        User.add(ivan)
        User.add(juli)
        db.session.commit()

    def tearDown(self) -> None:
        User.query.delete()
        Role.query.delete()
        db.session.commit()

    def test_add(self) -> None:
        #caso feliz
        self.assertIsNone(User.filter_by_email("juanperez@gmail.com"))
        User.add(User("juanperez@gmail.com", "juanperez", "1234", "Juan", "Perez"))
        db.session.commit()
        self.assertTrue(User.filter_by_email("juanperez@gmail.com"))

        #mismo mail y user
        User.add(User("juanperez@gmail.com", "juanperez", "1234", "Juan", "Perez"))
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        #mismo mail distinto user
        User.add(User("juanperez@gmail.com", "otrojuanperez", "1234", "Juan", "Perez"))
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        
        #distinto mail mismo user
        User.add(User("otrojuanperez@gmail.com", "juanperez", "1234", "Juan", "Perez"))
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        #distinto mail distinto user
        User.add(User("otrojuanperez@gmail.com", "otrojuanperez", "1234", "Juan", "Perez"))
        db.session.commit()
        self.assertTrue(User.filter_by_email("otrojuanperez@gmail.com"))


    def test_update(self) -> None:
        #caso feliz
        self.assertTrue(User.filter_by_email("ivanscopel@gmail.com"))
        user_a_editar = User.filter_by_email("ivanscopel@gmail.com")
        user_a_editar.email= "iscopel@gmail.com"
        db.session.commit()
        self.assertIsNone(User.filter_by_email("ivanscopel@gmail.com"))
        self.assertTrue(User.filter_by_email("iscopel@gmail.com"))

        #mail existente
        user_a_editar = User.filter_by_email("julidelleville@gmail.com")
        user_a_editar.email= "iscopel@gmail.com"
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        #username existente
        user_a_editar.username= "iscopel"
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()


    def test_filter_by_username(self) -> None:
        self.assertTrue(User.filter_by_username("jdelleville"))
        self.assertFalse(User.filter_by_username("ltanevitch"))

    def test_filter_by_email(self) -> None:
        self.assertTrue(User.filter_by_email("julidelleville@gmail.com"))
        self.assertFalse(User.filter_by_email("ltanevitch@gmail.com"))

    def test_delete(self) -> None:
        juli = User.filter_by_username("jdelleville")
        self.assertTrue(juli)
        User.delete(juli.id_user)
        self.assertFalse(User.filter_by_username("jdelleville"))

    def test_filter_by_active(self) -> None:
        juli = User.filter_by_username("jdelleville")
        self.assertIn(juli, User.filter_by_active(is_active=True))
        juli.is_active= False
        db.session.commit()
        self.assertNotIn(juli, User.filter_by_active(is_active=True))
        self.assertIn(juli, User.filter_by_active(is_active=False))
    
    def test_get_roles(self) -> None:
        ivi = User.filter_by_username("iscopel")
        admin = Role.find_by_name("admin")
        operario = Role.find_by_name("operario")
        self.assertIn(admin, ivi.roles)
        self.assertIn(operario, ivi.roles)
        self.assertNotIn("estudiante", ivi.roles)


