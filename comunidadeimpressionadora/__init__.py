from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# TOKEN
app.config['SECRET_KEY'] = 'M2w7hO0Q&x!0x9FH5a*DuXHGNw@4cg'

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
database = SQLAlchemy(app)


# IMPORTANDO AS  ROTAS EMBAIXO PORQUE ELA DEPENDE DA CARIÁVEL "app"
from comunidadeimpressionadora import routes
