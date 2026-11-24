import unittest
from main import create_app
from models import db, Juego, User


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_juego_creation(self):
        j = Juego(nombre='Test', descripcion='Desc', precio=9.99)
        db.session.add(j)
        db.session.commit()
        self.assertEqual(Juego.query.count(), 1)

    def test_juego_datos_y_actualizacion(self):
        j = Juego(nombre='Halo', descripcion='Accion', precio=599.50)
        db.session.add(j)
        db.session.commit()
        juego_guardado = Juego.query.first()
        self.assertEqual(juego_guardado.nombre, 'Halo')
        self.assertEqual(float(juego_guardado.precio), 599.50)
        juego_guardado.precio = 499.00
        db.session.commit()
        self.assertEqual(float(Juego.query.first().precio), 499.00)

    def test_user_creation(self):
        u = User(username='miguel', password='clave123')
        db.session.add(u)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'miguel')

    def test_user_password_hashing(self):
        u = User(username='jugador1', password='secreto')
        self.assertIsNotNone(u.password_hash)
        self.assertNotEqual(u.password_hash, 'secreto')
        self.assertTrue(u.verify_password('secreto'))
        self.assertFalse(u.verify_password('incorrecta'))

    def test_user_password_solo_escritura(self):
        u = User(username='jugador2', password='secreto')
        with self.assertRaises(AttributeError):
            u.password


if __name__ == '__main__':
    unittest.main()