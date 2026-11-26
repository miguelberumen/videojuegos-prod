import os
import time
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api
from models import db, User, Juego
from auth import auth as auth_blueprint
import controllers
from api.routes import JuegoList, JuegoResource


def create_app(config_name='default'):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_desarrollo_local')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///videojuegos.db')

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = 'strong'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    api = Api(app)
    api.add_resource(JuegoList, '/api/juegos')
    api.add_resource(JuegoResource, '/api/juegos/<int:id>')

    @app.route('/')
    @app.route('/juegos')
    @login_required
    def juegos():
        lista_juegos = controllers.obtener_juegos()
        return render_template('juegos.html', juegos=lista_juegos)

    @app.route('/agregar_juego', methods=['GET', 'POST'])
    @login_required
    def agregar_juego():
        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio = request.form['precio']
            controllers.insertar_juego(nombre, descripcion, precio)
            return redirect(url_for('juegos'))
        return render_template('agregar_juego.html')

    @app.route('/editar_juego/<int:id>')
    @login_required
    def editar_juego(id):
        juego = controllers.obtener_juego_por_id(id)
        return render_template('editar_juego.html', juego=juego)

    @app.route('/actualizar_juego', methods=['POST'])
    @login_required
    def actualizar_juego():
        id = request.form['id']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        controllers.actualizar_juego(id, nombre, descripcion, precio)
        return redirect(url_for('juegos'))

    @app.route('/eliminar_juego/<int:id>')
    @login_required
    def eliminar_juego(id):
        controllers.eliminar_juego(id)
        return redirect(url_for('juegos'))

    with app.app_context():
        for _ in range(10):
            try:
                db.create_all()
                if not User.query.filter_by(username='admin').first():
                    admin_user = User(username='admin', password='admin123')
                    db.session.add(admin_user)
                    db.session.commit()
                break
            except Exception:
                time.sleep(3)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)