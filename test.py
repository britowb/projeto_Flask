from models import Mensagem
from app import db, create_app
from sqlalchemy import select, union_all, Select


app = create_app()
with app.app_context():
    eu = 3
#consulta
    mensagem_recebida = select(Mensagem).where(Mensagem.destinatario_id == eu)
    mensagem_enviada = select(Mensagem).where(Mensagem.destinatario_id != eu,   Mensagem.remetente_id == eu)

#União dos resultados da consulta
    conversa = mensagem_enviada.union_all(mensagem_recebida).order_by(Mensagem.detalhes)

#execução e captação dos objetos
    resultado = db.session.execute(conversa)

    for i in resultado:
        print(i.conteudo)
        print(i.detalhes)