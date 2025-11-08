from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv() #carrega o .env para que o os.environ.get possa funcionar

app = Flask(__name__) #instanciamos o Flask
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///projeto.db' #Configuramos o Flask com o ORM
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #É ativado em situações específicas de desenvolvimento e debugging. Tem alto custo de performance.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') #Configura nossa secret key

# Configurar nullable=False como padrão. Assim meus campos serão sempre obrigatórios
class CustomSQLAlchemy(SQLAlchemy):
    def Column(self, *args, **kwargs):
        if 'nullable' not in kwargs:
            kwargs['nullable'] = False
        return super().Column(*args, **kwargs)

db = SQLAlchemy(app) #Instancia o SQLAlchemy conectando ele ao Flask.
#Precisa ser alterado depois quando formos trabalhar com Flask-migrate, ambientes de teste, produção, etc.

