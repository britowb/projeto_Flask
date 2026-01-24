from flask import Blueprint, request, 
auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # Define o blueprint de autenticação. Blueprint('auth' é o nome do blueprint, __name__ é o nome do módulo atual, url_prefix define o prefixo de URL para todas as rotas neste blueprint.)

@auth_bp.route('/login', methods=['GET', 'POST']) #GET é quando o usuário acessa. POST é quando o usuário preenche as infos e submete.
def login():
    if request.method == 'POST':
        return "página de login"

@auth_bp.route('/logout')
def logout():
    return "logout"

@auth_bp.route('/register')
def register():
    return "registro"
