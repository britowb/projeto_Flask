from config import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users' #boa prática para garantir bom entendimento da tabela

#Campos de identificação
    id = db.Column(db.Integer, primary_key=True) # definimos que id será inteiro e chave primária.
    email = db.Column(db.String(120), unique=True)#Limite de 80 caracteres
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))

#Status da conta
    is_active = db.Column(db.Boolean(), default=True)
    email_verified_at = db.Column(db.DateTime)

# Campos de auditoria
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)
    last_login = db.Column(db.DateTime())

#Dados pessoais
    nome = db.Column(db.String(80))#Nome tem limite de 80 caracteres
    nascimento = db.Column(db.Date)
    telefone = db.Column(db.String(20), unique=True)

#Relacionamento 
    endereco = db.relationship('Endereco', backref='user', uselist=False)
    postagens = db.relationship('Postagem', backref='autor')

class Endereco(db.Model):
    __tablename__ = 'enderecos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #Declaro que user_id será inteiro E chave estrangeira. Ligando endereço ao usuário através do ID de user
    country = db.Column(db.String)
    state = db.Column(db.String(2))
    city = db.Column(db.String)
    bairro = db.Column(db.String(80))


class Mensagem(db.Model):
    __tablename__ = 'mensagens'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    detalhes = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    remetente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    remetente = db.relationship('User', foreign_keys=[remetente_id], backref='mensagens_enviadas')
    destinatario = db.relationship('User', foreign_keys=[destinatario_id], backref='mensagens_recebidas')


# Postagens

class Postagem(db.Model):
    __tablename__ = 'postagens'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id')) #Uso chave estrangeira para gravar como autor aquele que estiver logado como user.
    # essa FK é a backref que nomearei no relationship. Relationship primeiro pede a classe e depois a backref que será essa.


    created_at = db.Column(db.DateTime(), default=datetime.now)
    is_shared = db.Column(db.Boolean())
    comentarios = db.relationship('Comentario', backref='postagem') # Aqui eu defino que Uma postagem pode ter multiplos comentarios. E podem ser acessados como "postagens.comentario"

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True) # O id unico do comentario
    post_id = db.Column(db.Integer, db.Forei0 gnKey('postagens.id')) #Aqui eu garanto a conexão do comentário com a postagem.
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Aqui eu armazenarei o autor do comentario, definido pelo user em questão. 
    reacts = db.Column(db.Integer, default=0) #Aqui armazenarei a quantidade de likes

    autor = db.relationship('User', backref='comentarios') #Forma pythonica de acessar o objeto User
    
    # comentario.postagem - acessar a postagem do comentário
    # comentario.autor - acessar o autor do comentário
    # user.comentarios - acessar todos comentários de um usuário
    # postagem.comentarios - acessar todos comentários de uma postagem

    #O autor_id é necessário porque:

    #É a coluna física no banco de dados
    #Armazena o ID do usuário que fez o comentário
    #É a chave estrangeira que mantém a integridade referencial
    #O relationship é necessário porque:

    #Permite acessar o objeto User diretamente: comentario.autor
    #Cria a referência reversa: user.comentarios
    #Facilita o trabalho com os objetos em Python

        # Elaborar em algum momento uma forma de ver quem curtiu o que.



    