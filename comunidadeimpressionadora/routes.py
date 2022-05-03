from fileinput import filename
from flask import render_template, redirect, url_for, flash, request
import flask
from comunidadeimpressionadora import app, database, Bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required

lista_usuarios = ['Carlos', 'Fulano', 'Ciclano', 'Beutrano']

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
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

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.profile_photo))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)