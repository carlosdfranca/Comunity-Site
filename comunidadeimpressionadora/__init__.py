from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# TOKEN
app.config['SECRET_KEY'] = 'M2w7hO0Q&x!0x9FH5a*DuXHGNw@4cg'
# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
Bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Você precisa fazer o login para acessar esse conteúdo.'
login_manager.login_message_category = 'alert-info'


# IMPORTANDO AS  ROTAS EMBAIXO PORQUE ELA DEPENDE DA CARIÁVEL "app"
from comunidadeimpressionadora import routes
