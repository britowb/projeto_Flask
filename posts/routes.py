from models import Postagem
from extensions import db, photos
from flask_login import current_user, login_required
from flask import Blueprint, request, redirect, render_template, url_for


post_bp = Blueprint('post', __name__, url_prefix='/posts')

@post_bp.route('/post', methods=['GET', 'POST'])
@login_required
def postagem():
    if request.method == 'GET':
        return render_template('post.html')
    
    autor = current_user.id #Só queremos o ID para que a ForeignKey seja válida.
    conteudo = request.form.get('conteudo')
    file = request.files.get('foto')#Só pega se houver.
    if file and file.filename: #Se existir e tiver um nome, então ta válido.
        filename = photos.save(request.files.get['foto'])
        #image_url = url_for('static', filename='uploads/'+filename)
        image_url = photos.url(filename) 

    else:
        image_url = None

    novo_post = Postagem(autor_id=autor, imagem=image_url, conteudo=conteudo)
    db.session.add(novo_post)
    db.session.commit()
    print('Novo post')
    return redirect(url_for('Index.index'))

    