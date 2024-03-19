from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, TextAreaField, RadioField, BooleanField, FileField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

cursos = [("Jiu-Jitsu","Jius-Jitsu"), ("RitBox", "RitBox"), ("Box", "Box"), ("Academia", "Academia")]
class Cadastro_Form(FlaskForm):
    nome = StringField("Nome:", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome:", validators=[DataRequired()])
    idade = StringField("Idade:", validators=[DataRequired(), Length(min=1, max=3)])
    curso = RadioField("Curso:", choices=cursos)
    bolsa = BooleanField("Possui Bolsa?")

    submit = SubmitField("Cadastrar")

class Upload_File(FlaskForm):
    file_up = FileField("Arquivo", validators=[FileRequired()])
    submit = SubmitField("Enviar")

class Register_User(FlaskForm):
    nome = StringField("Usuário", validators=[DataRequired()], render_kw={"placeholder":"Nome"})
    sobrenome = StringField("Usuário", validators=[DataRequired()], render_kw={"placeholder":"Sobrenome"})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    password = PasswordField("Senha", validators=[DataRequired()], render_kw={"placeholder":"Senha"})
    password_repeat = PasswordField("Repetir Senha", validators=[DataRequired(),  EqualTo('password')], render_kw={"placeholder":"Repetir Senha"})
    
    submit = SubmitField("Criar Conta")

class Login_User(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    password = PasswordField("Senha", validators=[DataRequired()], render_kw={"placeholder":"Senha"})
    
    submit = SubmitField("Entrar")