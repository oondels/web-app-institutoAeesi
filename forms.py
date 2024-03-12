from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms import validators

class Cadastro_Form(FlaskForm):
    nome = StringField("Nome:", validators=[validators.DataRequired()])
    data_nascimento = StringField("Data Nascimento:", validators=[validators.Length(min=6, max=35)])
    curso = StringField("Curso:", validators=[validators.DataRequired()])
    idade = StringField("Idade:", validators=[validators.DataRequired(), validators.Length(min=1, max=3)])
    submit = SubmitField("Cadastrar")