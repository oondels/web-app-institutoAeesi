from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from forms import Cadastro_Form

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

alunos_teste = {"Hendrius":["Jiu-Jitsu",24], "Bruce":["Jiu-Jitsu",25], "Christopher":["Box",24]}

@app.route('/')
def home():
    lista_faixas_teste = {1:"branca",3:"Roxa",4:"Marrom",2:"Azul",5:"Preta"}
    return render_template('home.html', template_faixa=lista_faixas_teste, template_alunos=alunos_teste)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/aluno/<aluno_name>")
def alunos(aluno_name):
    return render_template("alunos.html", template_nome_aluno=aluno_name, template_alunos=alunos_teste)

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/cadastrar-aluno", methods=["GET", "POST"])
def cadastro_aluno():
    # Formulario pelo Flask e HTML
    # if request.form:
        # alunos_teste[request.form["nome"]] = [request.form["curso"], request.form["idade"]]
    cadastrar_form = Cadastro_Form()
    new_aluno = cadastrar_form.nome.data
    new_telefone = cadastrar_form.telefone.data
    new_curso = cadastrar_form.curso.data
    new_idade = cadastrar_form.idade.data
    
    if cadastrar_form.validate_on_submit():
        if new_aluno:
            alunos_teste[new_aluno] = [new_curso, new_idade, new_telefone]

    return render_template("cadastro.html", template_form=cadastrar_form)

if __name__ == "__main__":
    app.run(debug=True)