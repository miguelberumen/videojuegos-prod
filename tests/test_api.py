import unittest
import json
from main import create_app
from models import db, Juego


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        juego = Juego(nombre='X', descripcion='Y', precio=1.23)
        db.session.add(juego)
        db.session.commit()
        self.juego_id = juego.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_get_juegos(self):
        resp = self.client.get('/api/juegos')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], 'X')

    def test_get_juego_por_id(self):
        resp = self.client.get(f'/api/juegos/{self.juego_id}')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['nombre'], 'X')
        self.assertEqual(data['descripcion'], 'Y')
        self.assertEqual(data['precio'], 1.23)

    def test_get_juego_no_encontrado(self):
        resp = self.client.get('/api/juegos/999')
        self.assertEqual(resp.status_code, 404)

    def test_post_juego(self):
        nuevo_juego = {
            'nombre': 'Zelda',
            'descripcion': 'Aventura',
            'precio': 1199.50
        }
        resp = self.client.post(
            '/api/juegos',
            data=json.dumps(nuevo_juego),
            content_type='application/json'
        )
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['nombre'], 'Zelda')
        self.assertEqual(Juego.query.count(), 2)

    def test_post_juego_datos_vacios(self):
        resp = self.client.post(
            '/api/juegos',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)

    def test_put_juego(self):
        datos_actualizados = {
            'nombre': 'X Actualizado',
            'precio': 2.50
        }
        resp = self.client.put(
            f'/api/juegos/{self.juego_id}',
            data=json.dumps(datos_actualizados),
            content_type='application/json'
        )
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['nombre'], 'X Actualizado')
        self.assertEqual(data['descripcion'], 'Y')
        self.assertEqual(data['precio'], 2.5)

    def test_delete_juego(self):
        resp = self.client.delete(f'/api/juegos/{self.juego_id}')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Juego.query.count(), 0)

    def test_delete_juego_no_encontrado(self):
        resp = self.client.delete('/api/juegos/999')
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()