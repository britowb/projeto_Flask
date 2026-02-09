from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet

db = SQLAlchemy() #ORM
migrate = Migrate() #Versionamento do banco de dados
bcrypt = Bcrypt() #métodos de hashing e verificação de senha
login_manager = LoginManager() #Gerenciador de login
photos = UploadSet('photos', IMAGES) # Define o tipo de upload permitido
