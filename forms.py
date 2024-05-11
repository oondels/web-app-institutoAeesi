from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, IntegerField, RadioField, BooleanField, FileField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

cursos = [("Jiu-Jitsu","Jius-Jitsu"), ("RitBox", "RitBox"), ("Box", "Box"), ("Academia", "Academia")]
class Cadastro_Form(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()], render_kw={"placeholder":"Nome", "class":"edit"})
    idade = StringField("Idade", validators=[DataRequired()], render_kw={"placeholder":"Idade", "class":"edit", "required pattern":"[0-9]{2,3}"})
    cpf_aluno = StringField("Cpf", validators=[DataRequired()], render_kw={"placeholder":"Cpf", "class":"edit"})
    curso = RadioField("Curso:", choices=cursos, render_kw={"class": "lista-cursos"})
    telefone = IntegerField("Idade", validators=[DataRequired()], render_kw={"placeholder":"Telefone", "class":"edit"})
    horario = StringField("Horário", validators=[DataRequired()], render_kw={"placeholder":"Horário", "class":"edit"})
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder":"Email", "class":"edit"})
    aniversario = StringField("Aniversário", validators=[DataRequired()], render_kw={"placeholder":"Aniversário", "class":"edit"})
    bolsa = BooleanField("Possui Bolsa?")
    submit = SubmitField("Cadastrar", render_kw={"class":"btn"})

class Upload_File(FlaskForm):
    option = [("comprovantes", "comprovantes"), ("foto", "foto")]
    directory = RadioField("directory", choices=option)
    file_up = FileField("Arquivo", validators=[FileRequired()], render_kw={"class":"input-up"})
    submit = SubmitField("Enviar", render_kw={"class":"btn"})

class Register_User(FlaskForm):
    nome = StringField("Usuário", validators=[DataRequired()], render_kw={"placeholder":"Nome"})
    sobrenome = StringField("Usuário", validators=[DataRequired()], render_kw={"placeholder":"Sobrenome"})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    password = PasswordField("Senha", validators=[DataRequired()], render_kw={"placeholder":"Senha"})
    password_repeat = PasswordField("Repetir Senha", validators=[DataRequired(),  EqualTo('password')], render_kw={"placeholder":"Repetir Senha"})
    submit = SubmitField("Criar Conta", render_kw={"class":"btn"})

class Login_User(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    password = PasswordField("Senha", validators=[DataRequired()], render_kw={"placeholder":"Senha"})
    submit = SubmitField("Entrar", render_kw={"class":"btn"})

class Editar_Form(FlaskForm):
    email = StringField("Email",render_kw={"placeholder":"Email"})
    telefone = StringField("Telefone", render_kw={"placeholder":"Telefone"})
    horario = StringField("Horario", render_kw={"placeholder":"Horário"})
    curso = RadioField("Curso:", choices=cursos)
    bolsa = BooleanField("Possui Bolsa?")
    submit = SubmitField("Salvar", render_kw={"class":"btn"})