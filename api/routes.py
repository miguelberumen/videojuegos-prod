from flask import request
from flask_restful import Resource, fields, marshal_with, abort
from models import db, Juego

juego_campos = {
    'id': fields.Integer,
    'nombre': fields.String,
    'descripcion': fields.String,
    'precio': fields.Float
}

class JuegoList(Resource):
    @marshal_with(juego_campos)
    def get(self):
        return Juego.query.all(), 200

    @marshal_with(juego_campos)
    def post(self):
        datos = request.get_json()
        if not datos or 'nombre' not in datos or 'descripcion' not in datos or 'precio' not in datos:
            abort(400, message="Faltan datos obligatorios")
        
        nuevo_juego = Juego(
            nombre=datos['nombre'],
            descripcion=datos['descripcion'],
            precio=datos['precio']
        )
        db.session.add(nuevo_juego)
        db.session.commit()
        return nuevo_juego, 201

class JuegoResource(Resource):
    @marshal_with(juego_campos)
    def get(self, id):
        juego = Juego.query.get(id)
        if not juego:
            abort(404, message="Juego no encontrado")
        return juego, 200

    @marshal_with(juego_campos)
    def put(self, id):
        juego = Juego.query.get(id)
        if not juego:
            abort(404, message="Juego no encontrado")
            
        datos = request.get_json()
        if not datos:
            abort(400, message="Datos no proporcionados")
            
        if 'nombre' in datos:
            juego.nombre = datos['nombre']
        if 'descripcion' in datos:
            juego.descripcion = datos['descripcion']
        if 'precio' in datos:
            juego.precio = datos['precio']
            
        db.session.commit()
        return juego, 200

    def delete(self, id):
        juego = Juego.query.get(id)
        if not juego:
            abort(404, message="Juego no encontrado")
            
        db.session.delete(juego)
        db.session.commit()
        return '', 204