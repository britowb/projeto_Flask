import os
from flask import Flask, Blueprint, render_template
from flask_uploads import configure_uploads
from extensions import db, migrate, login_manager, bcrypt, photos
from config import config_by_name
from auth.routes import auth_bp
from posts.routes import post_bp
from feed.routes import feed_bp
from coments.routes import comentar_bp
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
    login_manager.login_view = "auth.login" # Define para onde o usuário é redirecionado se não estiver logado
    app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads' # Pasta onde as imagens serão salvas
    configure_uploads(app, photos)

    # Registrar blueprints aqui
    index_bp = Blueprint('Index', __name__)
    @index_bp.route('/')
    def index():
        return render_template('base.html')
    
    app.register_blueprint(feed_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(comentar_bp)
    return app
