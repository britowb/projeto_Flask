from extensions import db
from datetime import datetime
from app import bcrypt, login_manager
from flask_login import  UserMixin #Adiciona implementações padrão que o flask espera nas instancias de usuario

class Mensagem(db.Model):
    __tablename__ = 'mensagens'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    detalhes = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    remetente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    remetente = db.relationship('User', foreign_keys=[remetente_id], back_populates='mensagem_enviada')
    destinatario = db.relationship('User', foreign_keys=[destinatario_id], back_populates='mensagem_recebida')

#Uma mensagem precisa ter obrigatoriamente uma origem e um destino. 
#back_populates='nome do objeto a conectar'

class User(db.Model, UserMixin):
    __tablename__ = 'users' #boa prática para garantir bom entendimento da tabela

#Campos de identificação
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))

#Funções auxiliares de classe (métodos)
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)#hash da senha, senha digitada. Retorna True/False
    
    @login_manager.user_loader #login_manager é a instancia que criamos em app.py
    def load_user(user_id): #Função para pegar o ID nos cookies e autenticar nosso usuario a cada requisicao
        return User.query.get(int(user_id)) #aqui ele pega o ID e pesquisa no banco de dados

#Status da conta
    is_active = db.Column(db.Boolean(), default=True)
    email_verified_at = db.Column(db.DateTime)

# Campos de auditoria
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    last_login = db.Column(db.DateTime())

#Dados pessoais
    nome = db.Column(db.String(80))
    nascimento = db.Column(db.Date)
    telefone = db.Column(db.String(20), unique=True)


#Relacionamento 
    endereco = db.relationship('Endereco', backref='user', uselist=False)
    postagens = db.relationship('Postagem', backref='autor')
    comentarios = db.relationship('Comentario', backref='autor')
    mensagem_enviada = db.relationship('Mensagem', foreign_keys=[Mensagem.remetente_id], back_populates='remetente')
    mensagem_recebida = db.relationship('Mensagem', foreign_keys=[Mensagem.destinatario_id], back_populates='destinatario')

class Endereco(db.Model):
    __tablename__ = 'enderecos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #Declaro que user_id será inteiro E chave estrangeira. Ligando endereço ao usuário através do ID de user
    country = db.Column(db.String)
    state = db.Column(db.String(2))
    city = db.Column(db.String)
    bairro = db.Column(db.String(80))



# Postagens

class Postagem(db.Model):
    __tablename__ = 'postagens'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id')) 

    imagem = db.Column(db.String(200)) # guarda o caminho da imagem
    conteudo = db.Column(db.Text)

    created_at = db.Column(db.DateTime(), default=datetime.now)
    is_shared = db.Column(db.Boolean(), default=False)
    reacts = db.Column(db.Integer, default=0)
    comentarios = db.relationship('Comentario', backref='postagem')

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True) # O id unico do comentario
    post_id = db.Column(db.Integer, db.ForeignKey('postagens.id'))
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    conteudo = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.now)  
    reacts = db.Column(db.Integer, default=0)