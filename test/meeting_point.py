import unittest
import sys
sys.path.append('../')
from app.models.meeting_point import Meeting_point
from app.db import db 
from app import create_app

create_app()
#TEST CORREN CON python -m unittest nombre_clase.py (parado en la carpeta test)

class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        Meeting_point.add(Meeting_point("Dardo Rocha", "6 y 60", "[-34.914019, -57.949708]", "2214251990", "drocha@gmail.com"))    
        Meeting_point.add(Meeting_point("Catedral", "12 y 51", "[-34.922883, -57.956317]", "2214233931", "catedrallp@gmail.com"))
        db.session.commit()

    def tearDown(self) -> None:
        Meeting_point.query.delete()
        db.session.commit()

    def test_add(self) -> None:
        self.assertEqual(2, len(Meeting_point.query.all()))
        Meeting_point.add(Meeting_point("Facultad de Informática", "50 y 120", "[-34.922883, -57.956317]", "2214233931", "info@gmail.com"))
        db.session.commit()
        self.assertEqual(3, len(Meeting_point.query.all()))

    def test_filter_by_visibility(self) -> None:
        catedral = Meeting_point.filter_by_name("Catedral").first()
        self.assertEqual(2, len(Meeting_point.filter_by_visibility(isVisible=True).all()))
        catedral.visible = False
        db.session.commit()
        self.assertEqual(1, len(Meeting_point.filter_by_visibility(isVisible=True).all()))
        self.assertNotIn(catedral, Meeting_point.filter_by_visibility(isVisible=True))
        self.assertEqual(1, len(Meeting_point.filter_by_visibility(isVisible=False).all()))
        self.assertIn(catedral, Meeting_point.filter_by_visibility(isVisible=False))

    def test_filter_by_adress(self) -> None: 
        self.assertIsNone(Meeting_point.filter_by_address("1 y 60"))
        self.assertEqual("Catedral", Meeting_point.filter_by_address("12 y 51").name)


    def test_delete(self) -> None: 
        self.assertEqual(2, len(Meeting_point.query.all()))
        catedral = Meeting_point.filter_by_address("12 y 51")
        Meeting_point.delete(catedral.id_point)
        db.session.commit()
        self.assertEqual(1, len(Meeting_point.query.all()))