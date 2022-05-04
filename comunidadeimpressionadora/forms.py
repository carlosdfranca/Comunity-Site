from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL, NumberRange, Optional
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    botao_submit_criarconta = SubmitField('Criar Conta')
    
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Cadastre-se com outro e-mail ou faça o Login para continuar.')
            
    
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')
    
class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_photo = FileField('Atualizar foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    phone_number = IntegerField('Número do Telefone', validators=[Optional()])
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    github = StringField('Github')
    
    ling_python = BooleanField('Python')
    ling_php = BooleanField('PHP')
    ling_c = BooleanField('C#')
    ling_java = BooleanField('Java')
    ling_sql = BooleanField('SQL')
    ling_htmlCss = BooleanField('HTML/CSS')
    ling_javascript = BooleanField('JavaScript')
    
    botao_submit_editarperfil = SubmitField('Confirmar Edição')
    
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Esse e-mail já foi cadastrado por outro usuário. Cadastre outro e-mail.')