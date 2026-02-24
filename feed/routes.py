from models import Postagem
from extensions import db, photos
from sqlalchemy import select
from flask_login import current_user, login_required
from flask import Blueprint, request, redirect, render_template, url_for

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/feed', methods=['GET'])
@login_required
def feed():
    post = db.session.execute(select(Postagem).where(Postagem.conteudo.isnot(None)).order_by(Postagem.created_at.desc())).scalars()
    return render_template('feed.html', posts=post, autenticado=current_user)#Coleto os dados e passo para o template.
#    ''for x in post:
#       id = x.id
#        autor = x.autor_id
#       imagem = x.imagem
 #       conteudo = x.conteudo
  #      created_at = x.created_at
   #     is_shared = x.is_shared
    #    reacts = x.reacts
     #   comentarios = x.comentarios
