from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length
cursos = [("Jiu-Jitsu","Jius-Jitsu"), ("RitBox", "RitBox"), ("Box", "Box"), ("Academia", "Academia")]
class Cadastro_Form(FlaskForm):
    nome = StringField("Nome:", validators=[DataRequired()])
    idade = StringField("Idade:", validators=[DataRequired(), Length(min=1, max=3)])
    telefone = StringField("Telefone: ", validators=[DataRequired(), Length(min=9, max=14)])
    curso = RadioField("Curso:", choices=cursos)
    descricao = TextAreaField("Descricao:")
    bolsista = BooleanField("Possui Bolsa?")
    submit = SubmitField("Cadastrar")
    