from flask import Flask, render_template, request
app = Flask(__name__)

alunos_teste = {"Hendrius":["Jiu-Jitsu",24], "Bruce":["Jiu-Jitsu",25], "Christopher":["Box",24]}


@app.route('/')
def index():
    lista_faixas_teste = {1:"branca",3:"Roxa",4:"Marrom",2:"Azul",5:"Preta"}
    return render_template('home.html', template_faixa=lista_faixas_teste, template_alunos=alunos_teste)

@app.route("/aluno/<aluno_name>")
def alunos(aluno_name):
    return render_template("alunos.html", template_nome_aluno=aluno_name, template_alunos=alunos_teste)

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/cadastrar-aluno", methods=["GET", "POST"])
def cadastro_aluno():
    if request.form:
        alunos_teste[request.form["nome"]] = [request.form["curso"], request.form["idade"]]
    return render_template("cadastro.html")

if __name__ == "__main__":
    app.run(debug=True)