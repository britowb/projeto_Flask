import os
from flask import Flask, Blueprint, render_template
from extensions import db, migrate, login_manager, bcrypt
from config import config_by_name
from auth.routes import auth_bp
    # Importa os modelos para que o migrate os detecte
from models import User, Endereco, Mensagem, Postagem, Comentario


def create_app(config_name=None):
    app = Flask(__name__)
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    cfg = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(cfg)

    db.init_app(app)  # Inicializa o SQLAlchemy com a app
    migrate.init_app(app, db)  # Inicializa o Flask-Migrate
    bcrypt.init_app(app) #inicializa a criptografia
    login_manager.init_app(app)

    # Define para onde o usuário é redirecionado se não estiver logado
    login_manager.login_view = "auth.login"
    # Registrar blueprints aqui
    index_bp = Blueprint('index', __name__)
    @index_bp.route('/')
    def index():
        return render_template('base.html')
    
    app.register_blueprint(auth_bp)
    return app
