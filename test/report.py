from datetime import datetime, timedelta
import unittest
import sys

sys.path.append('../')
from app.db import db 
from app import create_app
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from app.models.report_category import ReportCategory
from app.models.report import Report

create_app()
#TEST CORREN CON python -m unittest nombre_clase.py (parado en la carpeta test)

class TestUser(unittest.TestCase):

    def setUp(self) -> None:
        db.session.add(ReportCategory("Fallo o avería"))
        db.session.add(ReportCategory("Alcantarilla tapada"))
        db.session.add(ReportCategory("Pérdida de agua"))
        Report.add(Report("Caño tapado", ReportCategory.find_by_name("Pérdida de agua").id_report_category, "se tapó un caño por basura", "[12323, 12312]", "Luciana", "Tanevitch", "2212223333", "lubatane@gmail.com"))
        Report.add(Report("Alcantarilla obstruida", ReportCategory.find_by_name("Alcantarilla tapada").id_report_category, "se tapó una alcantarilla por basura", "[12323, 12312]", "Luciana", "Tanevitch", "2212223333", "lubatane@gmail.com"))
        Report.add(Report("Baño público tapado", ReportCategory.find_by_name("Fallo o avería").id_report_category, "se tapó el baño de parque saavedra", "[12323, 12312]", "Luciana", "Tanevitch", "2212223333", "lubatane@gmail.com"))
        db.session.commit()

    def tearDown(self) -> None:
        Report.query.delete()
        ReportCategory.query.delete()
        User.query.delete()
        db.session.commit()

    def test_add(self) -> None:
        self.assertEqual(3, len(Report.query.all()))
        self.assertFalse(Report.filter_by_title("Denuncia Prueba").first())
        Report.add(Report("Denuncia Prueba", ReportCategory.find_by_name("Fallo o avería").id_report_category, "descripcion de prueba", "[12323, 12312]", "Luciana", "Tanevitch", "2212223333", "lubatane@gmail.com"))
        self.assertEqual(4, len(Report.query.all()))
        self.assertTrue(Report.filter_by_title("Denuncia Prueba").first())  

    def test_filter_by_title(self) -> None:
        #contiene "tapa"
        self.assertTrue(Report.filter_by_title("%tapa%").all())
        self.assertEqual(2, len(Report.filter_by_title("%tapa%").all()))
        #es "tapa"
        self.assertFalse(Report.filter_by_title("tapa").all())

    def test_filter_by_period(self) -> None:
        self.assertTrue(Report.filter_by_period(datetime.now()- timedelta(days=1), datetime.now()+ timedelta(days=1)).all())
        self.assertFalse(Report.filter_by_period(datetime.now()- timedelta(days=3), datetime.now()- timedelta(days=2)).all())

    def test_filter_by_state(self) -> None:
        self.assertTrue(Report.filter_by_state("SINCONFIRMAR").all())
        self.assertEqual(3, len(Report.filter_by_state("SINCONFIRMAR").all()))
        denuncia = Report.filter_by_title("Caño tapado").first()
        self.assertFalse(Report.filter_by_state("EN CURSO").all())
        denuncia.status = "EN CURSO"
        db.session.commit()
        self.assertTrue(Report.filter_by_state("EN CURSO").all())
        self.assertEqual(2, len(Report.filter_by_state("SINCONFIRMAR").all()))
        self.assertEqual(1, len(Report.filter_by_state("EN CURSO").all()))

    def test_assigned_unasssigned(self) -> None:
        self.assertEqual(3, len(Report.get_unassigned().all()))
        User.add(User("juanperez@gmail.com", "juanperez", "1234", "Juan", "Perez"))
        db.session.commit()
        jp_id= User.filter_by_username("juanperez").id_user
        self.assertTrue(Report.filter_by_assigned_to(jp_id))
        denuncia = Report.filter_by_title("Caño tapado").first()
        denuncia.assigned_to = jp_id
        db.session.commit()
        self.assertTrue(Report.filter_by_assigned_to(jp_id))
        self.assertEqual(2, len(Report.get_unassigned().all()))