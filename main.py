from flask import Flask, flash, redirect, render_template, url_for, request
from forms import FormLogin, FormCriarConta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

lista_usuarios = ['Carlos', 'Fulano', 'Ciclano', 'Beutrano']

# TOKEN
app.config['SECRET_KEY'] = 'M2w7hO0Q&x!0x9FH5a*DuXHGNw@4cg'

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
database = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login feito com seucesso no e-mail: {form_login.email.data}', 'alert-success')
        return redirect(url_for('home'))
                
    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        flash(f'Conta criada para o e-mail: {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)


if __name__ == '__main__':
    app.run(debug=True)