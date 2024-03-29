from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, TextAreaField, RadioField, BooleanField, FileField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

cursos = [("Jiu-Jitsu","Jius-Jitsu"), ("RitBox", "RitBox"), ("Box", "Box"), ("Academia", "Academia")]
class Cadastro_Form(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()], render_kw={"placeholder":"Nome", "class":"edit"})
    sobrenome = StringField("Sobrenome", validators=[DataRequired()], render_kw={"placeholder":"Sobrenome", "class":"edit"})
    idade = StringField("Idade", validators=[DataRequired()], render_kw={"placeholder":"Idade", "class":"edit"})
    curso = RadioField("Curso:", choices=cursos, render_kw={"class": "lista-cursos"})
    bolsa = BooleanField("Possui Bolsa?")
    submit = SubmitField("Cadastrar", render_kw={"class":"btn"})

class Edite_Form(FlaskForm):
    nome = StringField("Nome:", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome:", validators=[DataRequired()])
    idade = StringField("Idade:", validators=[DataRequired(), Length(min=1, max=3)])
    curso = RadioField("Curso:", choices=cursos)
    bolsa = BooleanField("Possui Bolsa?")
    submit = SubmitField("Cadastrar")   

class Upload_File(FlaskForm):
    file_up = FileField("Arquivo", validators=[FileRequired()], render_kw={"class":"file_up"})
    submit = SubmitField("Enviar", render_kw={"class":"btn"})

class Register_User(FlaskForm):
    nome = StringField("Usuário", validators=[DataRequired()], render_kw={"placeholder":"Nome", "class":"register-form"})
    sobrenome = StringField("Usuário", validators=[DataRequired()], render_kw={"placeholder":"Sobrenome", "class":"register-form"})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email", "class":"register-form"})
    password = PasswordField("Senha", validators=[DataRequired()], render_kw={"placeholder":"Senha", "class":"register-form"})
    password_repeat = PasswordField("Repetir Senha", validators=[DataRequired(),  EqualTo('password')], render_kw={"placeholder":"Repetir Senha", "class":"register-form"})
    submit = SubmitField("Criar Conta", render_kw={"class":"btn"})

class Login_User(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    password = PasswordField("Senha", validators=[DataRequired()], render_kw={"placeholder":"Senha"})
    submit = SubmitField("Entrar", render_kw={"class":"btn"})

class Editar_Form(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()], render_kw={"placeholder":"Nome", "class":"edit"})
    sobrenome = StringField("Sobrenome", validators=[DataRequired()], render_kw={"placeholder":"Sobrenome", "class":"edit"})
    idade = StringField("Idade", validators=[DataRequired()], render_kw={"placeholder":"Idade", "class":"edit"})
    curso = RadioField("Curso:", choices=cursos, render_kw={"class": "lista-cursos"})
    bolsa = BooleanField("Possui Bolsa?")
    submit = SubmitField("Salvar", render_kw={"class":"btn"})