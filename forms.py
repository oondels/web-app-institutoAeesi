from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, TextAreaField, RadioField, BooleanField, FileField
from wtforms.validators import DataRequired, Length

cursos = [("Jiu-Jitsu","Jius-Jitsu"), ("RitBox", "RitBox"), ("Box", "Box"), ("Academia", "Academia")]
class Cadastro_Form(FlaskForm):
    nome = StringField("Nome:", validators=[DataRequired()])
    idade = StringField("Idade:", validators=[DataRequired(), Length(min=1, max=3)])
    telefone = StringField("Telefone: ", validators=[Length(min=9, max=14)])
    curso = RadioField("Curso:", choices=cursos)
    descricao = TextAreaField("Descricao:")
    bolsista = BooleanField("Possui Bolsa?")
    submit = SubmitField("Cadastrar")

class Upload_File(FlaskForm):
    file_up = FileField("Arquivo", validators=[FileRequired()])
    submit = SubmitField("Enviar")