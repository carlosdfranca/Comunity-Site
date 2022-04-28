from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora.models import Usuario

lista_usuarios = ['Carlos', 'Fulano', 'Ciclano', 'Beutrano']

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login feito com seucesso no e-mail: {form_login.email.data}', 'alert-success')
        return redirect(url_for('home'))
                
    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, password=form_criar_conta.password.data)
        database.session.add(usuario)
        database.session.commit()
        
        flash(f'Conta criada para o e-mail: {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)