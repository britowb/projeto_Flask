import os
from flask import Flask
from extensions import db, migrate
from config import config_by_name


def create_app(config_name=None):
    app = Flask(__name__)
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    cfg = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(cfg)

    db.init_app(app)  # Inicializa o SQLAlchemy com a app
    migrate.init_app(app, db)  # Inicializa o Flask-Migrate

    # Importa os modelos para que o migrate os detecte
    from models import User, Endereco, Mensagem, Postagem, Comentario

    # Registrar blueprints aqui
    # app.register_blueprint(...)

    return app
