import os
from flask import Flask, render_template, redirect, url_for, request
from forms import Cadastro_Form, Upload_File
from werkzeug.utils import secure_filename

path = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"
folder = os.path.join(path, "database/files")
app.config['UPLOAD_FOLDER'] = folder

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
    cadastrar_form = Cadastro_Form()
    
    if cadastrar_form.validate_on_submit():
        new_aluno = cadastrar_form.nome.data
        new_telefone = cadastrar_form.telefone.data
        new_idade = cadastrar_form.idade.data
        new_curso = cadastrar_form.curso.data
        #new_descricao = cadastrar_form.descricao.data
        #new_bolsista = cadastrar_form.bolsista.data
        if new_aluno:
            alunos_teste[new_aluno] = [new_curso, new_idade, new_telefone]
            return redirect(url_for("cadastro_aluno", _external=True, _scheme='http'))
    return render_template("cadastro.html", template_form=cadastrar_form)

# Corrigir
@app.route("/upload-arquivos", methods=["GET", "POST"])
def upload_files():
    file_form = Upload_File()

    if file_form.validate_on_submit():
        arquivo = file_form.file_up.data
        filename = secure_filename(arquivo.filename)
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(arquivo.filename)))
        return 'Arquivo enviado'
    return render_template("upload.html", file_form=file_form)

if __name__ == "__main__":
    app.run(debug=True)