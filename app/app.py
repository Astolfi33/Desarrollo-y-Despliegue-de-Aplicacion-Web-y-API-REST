from flask import Flask, render_template, request, send_from_directory
import os
from methodOverride import MethodOverrideMiddleware
from database import db
from sqlalchemy_utils import create_database, database_exists
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import Equipo
import click
from flask_cors import CORS
from flask.cli import with_appcontext
from flasgger import Swagger
from logger import logger
import logging


app = Flask(__name__,static_folder='public', static_url_path="" ,template_folder='templates')
CORS(app)
app.logger.handlers.clear()
for handler in logger.handlers:
    app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.handlers.clear()
for handler in logger.handlers:
    werkzeug_logger.addHandler(handler)
werkzeug_logger.setLevel(logging.INFO)

app.config['SWAGGER']={
    'title':'API de Equipos',
    'uiversion': 3,
    'openapi':'3.0.3'
}
swagger = Swagger(app, template_file='openapi.yaml')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'assets','images')
app.config['THUMBNAIL_FOLDER'] = os.path.join(app.root_path, 'assets', 'thumbnails')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = '1234'
app.wsgi_app = MethodOverrideMiddleware(app.wsgi_app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:DAstolfi06%40@localhost/p4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(os.path.join(app.root_path, 'assets/images'), filename)

@app.route('/thumbnail/<filename>')
def thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

import blueprints

app.register_blueprint(blueprints.equipos_bp, url_prefix='/equipos')
app.register_blueprint(blueprints.usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(blueprints.auth_bp, url_prefix='/auth')
app.register_blueprint(blueprints.bp_api_equipos, url_prefix='/api/v1/equipos')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():    
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error500.html'), 500

@click.command(name='seed')
@with_appcontext
def seed():
    from models.seeders import seedEquipo, seedUsuario
    #seedEquipo()
    seedUsuario()
    
app.cli.add_command(seed)

if __name__ == '__main__':
    app.run(debug=True)