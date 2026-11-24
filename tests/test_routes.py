import unittest
from main import create_app
from models import db, User, Juego


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_login_page_access(self):
        resp = self.client.get('/auth/login')
        self.assertEqual(resp.status_code, 200)

    def test_register_page_access(self):
        resp = self.client.get('/auth/register')
        self.assertEqual(resp.status_code, 200)

    def test_index_requires_login(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/auth/login', resp.headers['Location'])

    def test_juegos_requires_login(self):
        resp = self.client.get('/juegos')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/auth/login', resp.headers['Location'])

    def test_agregar_juego_requires_login(self):
        resp = self.client.get('/agregar_juego')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/auth/login', resp.headers['Location'])

    def test_register_user(self):
        resp = self.client.post('/auth/register', data={
            'username': 'nuevo',
            'password': '123'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/auth/login', resp.headers['Location'])
        self.assertEqual(User.query.count(), 1)

    def test_login_y_acceso_rutas_protegidas(self):
        user = User(username='miguel', password='password123')
        db.session.add(user)
        db.session.commit()

        resp = self.client.post('/auth/login', data={
            'username': 'miguel',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        resp_index = self.client.get('/')
        self.assertEqual(resp_index.status_code, 200)

        resp_juegos = self.client.get('/juegos')
        self.assertEqual(resp_juegos.status_code, 200)

    def test_login_credenciales_incorrectas(self):
        user = User(username='miguel', password='password123')
        db.session.add(user)
        db.session.commit()

        resp = self.client.post('/auth/login', data={
            'username': 'miguel',
            'password': 'incorrecta'
        })
        self.assertEqual(resp.status_code, 200)

        resp_juegos = self.client.get('/juegos')
        self.assertEqual(resp_juegos.status_code, 302)
        self.assertIn('/auth/login', resp_juegos.headers['Location'])

    def test_agregar_juego_autenticado(self):
        user = User(username='miguel', password='password123')
        db.session.add(user)
        db.session.commit()

        self.client.post('/auth/login', data={
            'username': 'miguel',
            'password': 'password123'
        })

        resp = self.client.post('/agregar_juego', data={
            'nombre': 'Halo',
            'descripcion': 'Shooter',
            'precio': '599.00'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/juegos', resp.headers['Location'])
        self.assertEqual(Juego.query.count(), 1)

    def test_logout(self):
        user = User(username='miguel', password='password123')
        db.session.add(user)
        db.session.commit()

        self.client.post('/auth/login', data={
            'username': 'miguel',
            'password': 'password123'
        })

        resp_logout = self.client.get('/auth/logout')
        self.assertEqual(resp_logout.status_code, 302)
        self.assertIn('/auth/login', resp_logout.headers['Location'])

        resp_juegos = self.client.get('/juegos')
        self.assertEqual(resp_juegos.status_code, 302)


if __name__ == '__main__':
    unittest.main()