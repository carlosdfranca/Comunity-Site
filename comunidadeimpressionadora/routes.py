from fileinput import filename
from flask import render_template, redirect, url_for, flash, request
import flask
from comunidadeimpressionadora import app, database, Bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and Bcrypt.check_password_hash(usuario.password, form_login.password.data):
            login_user(usuario)       
            flash(f'Login feito com seucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login. Email ou senha incorretos', 'alert-danger')
                
    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = Bcrypt.generate_password_hash(form_criar_conta.password.data)
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, password=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario)
        flash(f'Conta criada para o e-mail: {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout realizado.', 'alert-primary')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.profile_photo))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    
    return render_template('criarpost.html', form=form)

# método criado para Atualizar a foto de Perfil
def salvar_imagem(imagem):
    
    # tratando o nome
    codigo = secrets.token_hex(8)
    nome, extencao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extencao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    
    # reduzindo imagem
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    
    
    # salvando imagem
    imagem_reduzida.save(caminho_completo)
    
    return nome_arquivo


# Método criado para atualizar os cursos do perfil
def atualizar_cursos(form):
    lista_cursos = []
    # Percorrer o formulário pegando só os campos com "ling_"
    for campo in form:
        if 'ling_' in campo.name:
            # Adicionar o campo.label na lista de cursos os selecionados para
            if campo.data:
                lista_cursos.append(campo.label.text)    
    # transformar a lista numa string separadando os cursos com ";"
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        # Atualizando dados
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.facebook = form.facebook.data
        current_user.instagram = form.instagram.data
        current_user.github = form.github.data
        
        # Atualizando a foto do perfil
        if form.profile_photo.data:
            nome_imagem = salvar_imagem(form.profile_photo.data)
            current_user.profile_photo = nome_imagem
            
        # Atualizando as linguagens conhecidas
        current_user.cursos = atualizar_cursos(form)

        
        # Commitando no banco de dados
        database.session.commit()
        
        flash('Perfil Atualizado com Sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.facebook.data = current_user.facebook
        form.instagram.data = current_user.instagram
        form.github.data = current_user.github
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.profile_photo))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)