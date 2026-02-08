from flask import Blueprint, request, redirect, url_for, render_template
from models import User
from extensions import db
import datetime
from werkzeug.security import generate_password_hash
auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # Define o blueprint de autenticação. Blueprint('auth' é o nome do blueprint, __name__ é o nome do módulo atual, url_prefix define o prefixo de URL para todas as rotas neste blueprint.)

@auth_bp.route('/login', methods=['GET', 'POST']) #GET é quando o usuário acessa. POST é quando o usuário preenche as infos e submete.
def login():
    if request.method == 'POST':
        return "página de login"

@auth_bp.route('/logout')
def logout():
    return "logout"

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #abaixo nós resgatamos as informações obtidas no formulário, para poder salvar no BD.
        nome = request.form['nome']
        #Recebe a data de nascimento que virá em String YYYY-MM-DD
        nascimento_str = request.form['nascimento']
        #Converte em objeto pythonico para que o BD aceite (pois o campo dt de nascimento é db.date)
        nascimento = datetime.strptime(nascimento_str, '%Y-%m-%d').date
        email = request.form['email']
        # Verificar se o email já existe no banco antes de cadastrar.

        #Conferir se a senha atende critérios (mínimo de caracteres, complexidade).

        #Normalizar dados (ex.: transformar email em minúsculas).

        #Garantir que não haja SQL injection ou manipulação maliciosa.
        username = request.form['username']
        password = request.form['password']
        #Criptografar a senha antes de salvar.
        hashed_password = generate_password_hash(password)
        #Agora vamos criar o objeto novo_user da classe User (nosso model), para salvar.
        novo_user = User(nome=nome, nascimento=nascimento, username=username, email=email, password_hash=hashed_password)
        # Agora vamos adicionar esse objeto ao nosso banco de dados e comitar ele.
        db.session.add(novo_user)
        db.session.commit()
        return redirect(url_for('auth.login')) # redireciona para login após cadastro  
    return render_template('user_form.html')
