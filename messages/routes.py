from extensions import db
from models import User, Mensagem
from sqlalchemy import select, union_all
from datetime import datetime
from flask import Blueprint, redirect, request, url_for, render_template
from flask_login import login_required, current_user
inbox_bp = Blueprint('inbox', __name__)
send_bp = Blueprint('send', __name__)
conversa_bp = Blueprint('conversa', __name__)

@conversa_bp.route('/conversa/<int:id>', methods=['GET'])
@login_required
def conversa(id):

    eu = current_user.id

    mensagem_recebida = select(Mensagem).where(Mensagem.destinatario_id == eu, Mensagem.remetente_id == id)
    mensagem_enviada = select(Mensagem).where(Mensagem.remetente_id == eu, Mensagem.destinatario_id == id)

    mix = mensagem_enviada.union_all(mensagem_recebida).order_by(Mensagem.detalhes)
    conversas = db.session.execute(mix)

    user = db.session.execute(select(User.nome).where(User.id == id)).scalar()
    return render_template('conversas.html', conversa=conversas, quem=user, logado=eu, autenticado=current_user)

@inbox_bp.route('/inbox', methods=['GET'])
@login_required
def inbox():
    eu = current_user.id
    #Aqui eu segrego o ID de quem eu já conversei.
    lista_conversa = select(Mensagem.destinatario_id).where(Mensagem.remetente_id==eu).union(select(Mensagem.remetente_id).where(Mensagem.destinatario_id==eu))
    #Aqui eu pego a instancia do usuario para poder criar meu bate-papo.
    usuarios = db.session.execute(select(User).where(User.id.in_(lista_conversa))).scalars().all()
    return render_template('inbox.html', usuarios=usuarios, autenticado=current_user)


@send_bp.route('/send', methods=['POST', 'GET'])
@login_required
def send():
    if request.method =='GET':
        usuarios = db.session.execute(select(User)).scalars()
        return render_template('send_message.html', users=usuarios, autenticado=current_user)
    else:
        destinatario = request.form.get('destinatario')
        msg = request.form.get('conteudo')
        data = datetime.now()
        mensagem_enviada = Mensagem(conteudo=msg, destinatario_id=destinatario, remetente_id=current_user.id, detalhes=data)
        
        db.session.add(mensagem_enviada)
        db.session.commit()
        print(f'Mensagem de {current_user.nome} ({current_user.id}) para {destinatario}')
        return redirect(url_for('Index.index', autenticado=current_user))
