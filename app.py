import os
from flask import Flask, render_template, redirect, url_for, flash, request
from forms import Cadastro_Form, Upload_File, Register_User, Login_User, Editar_Form
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from datetime import datetime, date
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime, date
# from dotenv import load_dotenv

# load_dotenv()

path = os.path.abspath(os.path.dirname(__file__))
folder = os.path.join(path, "database/files")

app = Flask(__name__)

app.config["SECRET_KEY"] = "wa0i4Ochu"
app.config["UPLOAD_FOLDER"] = folder

# Teste Local
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wa0i4OchuSql@localhost/geral'
# Mysql DB
# Deploys app
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uftu2hj60jqhe8:p1713e72b5a4b69168f4e9832c3e43912b38be9947621448782b8c750362b9335@c5hilnj7pn10vb.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/deiodn8elck6ib'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key = True)
        nome = db.Column(db.String(200))
        sobrenome = db.Column(db.String(200))
        email = db.Column(db.String(40), unique=True, index=True)
        password_hash = db.Column(db.String(200))
        dev = db.Column(db.Boolean())
        admin = db.Column(db.Boolean())

        def __repr__(self):
            return f'{self.nome}'

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        @property
        def is_admin(self):
            return self.admin
        @property
        def is_dev(self):
            return self.dev
    
class Aluno(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        nome = db.Column(db.String(200))
        idade = db.Column(db.Integer())
        cpf = db.Column(db.Integer())
        curso = db.Column(db.String(40))
        telefone = db.Column(db.Integer())
        horario= db.Column(db.String(200))
        email = db.Column(db.String(200))
        aniversario = db.Column(db.String(200))
        bolsa = db.Column(db.Boolean())
        pagamento = db.relationship('Pagamento', backref='aluno', lazy='dynamic')

        def __repr__(self):
            return f"{self.nome}"

class Pagamento(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        pagamento = db.Column(db.Boolean())
        mes = db.Column(db.DateTime, default=date.today())
        aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'))

        def __repr__(self):
            return f'<{self.pagamento}>'

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
  return redirect(url_for('login'))

def admin_acces():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.get_id()).first()
        if user.is_admin:
            return True
        else: return False

# Tratar erros de url - 404
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/alunos", methods=["GET", "POST"])
def alunos_cadastrados():
    if admin_acces():
        alunos = Aluno.query.all()
        return render_template('alunos.html', alunos = alunos)
    else:
        flash("Você não possui acesso a esta página!")
        return(redirect(url_for('home')))

@app.route("/pesquisa")
def pesquisa():
    pesquisa = request.args.get("q")
    if pesquisa:
        results = Aluno.query.filter(Aluno.nome.icontains(pesquisa)).order_by(Aluno.nome.asc()).limit(100).all()
    else: 
        results = []
    return render_template("pesquisa_aluno.html", results=results)

@app.route("/aluno/<aluno_id>")
@login_required
def aluno(aluno_id):
    if admin_acces():
        aluno = Aluno.query.filter_by(id=aluno_id).first()
        # Pegar pagamento do aluno -> Colocar no arquivo .html
        for pag in aluno.pagamento:
            print(pag.pagamento)
        return render_template("aluno.html", aluno=aluno)
    else:
        flash("Você não possui acesso a esta página!")
        return(redirect(url_for('home')))

@app.route("/cadastrar-aluno", methods=["GET", "POST"])
@login_required
def cadastro_aluno():
    cadastrar_form = Cadastro_Form()
    if admin_acces():
        if cadastrar_form.validate_on_submit():
            nome = cadastrar_form.nome.data
            idade = cadastrar_form.idade.data
            cpf_aluno = cadastrar_form.cpf_aluno.data
            curso = cadastrar_form.curso.data
            telefone = cadastrar_form.telefone.data
            horario = cadastrar_form.horario.data
            email = cadastrar_form.email.data
            aniversario = cadastrar_form.aniversario.data
            bolsa = cadastrar_form.bolsa.data

            aluno = Aluno(nome=nome, idade=idade, cpf=cpf_aluno, curso=curso, telefone=telefone, horario=horario, email=email, aniversario=aniversario, bolsa=bolsa)
            pag_aluno = Pagamento(pagamento=False, mes=date.today(), aluno=aluno)
            db.session.add(pag_aluno)
            db.session.add(aluno)
            db.session.commit()
            return redirect(url_for("cadastro_aluno", _external=True, _scheme='http'))
    else:
        flash("Você não possui acesso a esta página!")
        return(redirect(url_for('home')))
    return render_template("cadastro.html", template_form=cadastrar_form)

# Finalizar Route
@app.route('/editar_aluno/<aluno_name>/<aluno_id>', methods=["GET", "POST"])
@login_required
def editar_aluno(aluno_name, aluno_id):
    editar_form = Editar_Form()
    aluno_edite = Aluno.query.filter_by(id=aluno_id).first()
    if admin_acces():
        if editar_form.validate_on_submit():
            aluno_edite.email = editar_form.email.data
            aluno_edite.telefone = editar_form.telefone.data
            aluno_edite.horario = editar_form.horario.data
            aluno_edite.curso = editar_form.curso.data
            aluno_edite.bolsa = editar_form.bolsa.data
            db.session.commit()
            return redirect(url_for("alunos_cadastrados", _external=True, _scheme='http'))
    else:
        flash("Você não possui acesso a esta página!")
        return(redirect(url_for('home')))
    return render_template("editar.html", editar_form=editar_form, aluno_edite = aluno_edite)

@app.route("/cursos")
def cursos():
    return render_template("cursos.html")

@app.route("/cursos/<nameCourse>")
def curso(nameCourse):
    return render_template("curso.html", curso=nameCourse)

# Rota para registrar pagamento de alunos e upload de comprovantes/fotos
@app.route("/pagamentos", methods=["GET", "POST"])
@login_required
def pagamentos():
    if admin_acces():     
        file_form = Upload_File()
        alunos = Aluno.query.all()

        # Resetando pagamento de todos os alunos para falso no primeiro dia do mês (Menos bolsistas)
        if date.today().day == 1:
            for aluno in alunos:
                if aluno.bolsa == False:
                    for pag in aluno.pagamento:
                        pag.pagamento = False
                        db.session.commit()

        # Verificando se tem envio de dados
        if file_form.validate_on_submit():
            selection = file_form.directory.data
            arquivo = file_form.file_up.data
            filename = secure_filename(arquivo.filename)
            mes_pagamento = request.form.get("mes-pagamento").replace("/", "-").strip()

            # Formarto de Data
            format = "%d-%m-%Y"
            try:
                # Verificando se o formato de dato é válido
                datetime.strptime(mes_pagamento, format)

                # Verificando se um aluno foi selecionado para fazer pagamento
                if request.method == "POST":
                # Atualizando informação de pagamento
                    try:
                        aluno_pesquisado = Aluno.query.filter_by(id=int(request.form.get("aluno-pesquisa"))).first()
                        for pay in aluno_pesquisado.pagamento:
                            pay.pagamento = True
                            db.session.commit() 
                    except:
                        flash("Erro ao efetuar pagamento do aluno!")

                # Verificando se existe o caminho, caso contrário criando o folder
                save_path = os.path.join(app.config['UPLOAD_FOLDER'] + f"/{selection}" + f"/{aluno_pesquisado.nome}-{aluno_pesquisado.id}" + f"/{mes_pagamento}")
                if os.path.exists(save_path):
                    arquivo.save(os.path.join(save_path, filename))
                else:
                    os.makedirs(save_path)
                    arquivo.save(os.path.join(save_path, filename))
                    flash("Arquivo enviado")
            
            except:
                flash("Formato de Data inválido - Utilize o formato <Dia/Mês/Ano>") 
            return redirect(url_for('pagamentos'))

        return render_template("pagamentos.html", file_form=file_form, alunos=alunos)
    else:
        flash("Você não possui acesso a esta página!")
        return(redirect(url_for('home')))

@app.route("/professores")
def professores():
    return render_template("professores.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = Register_User(csrf_enabled=False)
    if register_form.validate_on_submit():
        user = User(nome=register_form.nome.data, sobrenome = register_form.sobrenome.data,
                    email=register_form.email.data, admin=False, dev=False)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template("register.html", register_form=register_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = Login_User()
    if not current_user.is_authenticated:
        if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user and check_password_hash(user.password_hash, login_form.password.data):
                login_user(user)
                return redirect(url_for('user_page', user_id=user.id))
            else:
                flash("Falha ao efetuar login. Verifique erro de digitação ou se já esta cadastrado no sistema!")
                return redirect(url_for('login'))
                
        return render_template("login.html", login_form=login_form)
    else:
        flash("Você já está autenticado!")
        return redirect(request.referrer)

@app.route('/user_page/<user_id>')
@login_required
def user_page(user_id):
    if (current_user.get_id() == user_id) or (current_user.dev == 1):
        user = User.query.filter_by(id=user_id).first()
        return render_template('user_page.html', user=user)
    else: 
        return redirect(url_for('home'))

@app.route("/logout")
def logout():
   logout_user()
   return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    alunos = Aluno()
    # Contagem de Alunos que já pagaram
    pago = 0
    alunos_query = Aluno.query.all()
    for aluno in alunos_query:
        if not aluno.bolsa:
            for pay in aluno.pagamento:
                if pay.pagamento == True:
                    pago += 1

    porcentagem_bolsa = 0
    alunoPago = 0

    if alunos.query.count() != 0:
        alunoPago = round((pago/alunos.query.filter_by(bolsa=0).count() * 100), 2)
        # Porcentagem de Bolsistaas
        porcentagem_bolsa = round((alunos.query.filter_by(bolsa=True).count()/alunos.query.count())*100,2)

    users = User.query.all()
    admin = User.query.filter_by(id=current_user.id).first()
    
    if current_user.admin == 1:
        return render_template("admin.html", users=users, admin=admin, alunos=alunos, 
                               reversed=reversed, porcentagem_bolsa=porcentagem_bolsa, alunoPago=alunoPago)
    else:
        flash("Você não possui acesso a esta página!")
        return(redirect(url_for('home')))

@app.route("/admin/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/user/<user_id>")
@login_required
def edit_user(user_id):
    if (current_user.get_id() == user_id) or (current_user.dev == 1):
        user_edit = User.query.filter_by(id = user_id).first()
        return render_template("edit_user.html", user_edit=user_edit)
    else:
        flash("Você não possui acesso a esta página!")
        return(redirect(url_for('home')))

if __name__ == "__main__":
    app.run(debug=True)
