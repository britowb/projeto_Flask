from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import select
from extensions import db
from models import Comentario
comentar_bp = Blueprint('Comentario', __name__)
@comentar_bp.route('/Comentar', methods=['POST'])
@login_required
def comentar():
    if request.method == 'POST':
        user = current_user.id #ID do usuario
        comentario = request.form.get('comentario') #Comentario resgatado do formulário
        post_id = request.form.get('id')
        novo_comentario = Comentario(post_id = post_id, autor_id = user, conteudo=comentario)
        db.session.add(novo_comentario)
        db.session.commit()
        print(f'Comentário do user_id: {user}')
        return redirect(url_for('feed.feed'))