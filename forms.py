from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class Cadastro_Form(FlaskForm):
    nome = StringField("Nome:", validators=[DataRequired()])
    curso = StringField("Curso:", validators=[DataRequired()])
    idade = StringField("Idade:", validators=[DataRequired()])
    submit = SubmitField("Cadastrar")