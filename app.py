import os
from flask import Flask, render_template, redirect, url_for, flash, request
from forms import Cadastro_Form, Upload_File, Register_User, Login_User, Editar_Form
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from datetime import datetime

path = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret" #Editar senha depois
folder = os.path.join(path, "database/files")

app.config['UPLOAD_FOLDER'] = folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(path, 'database/geral.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
   'user_database': 'sqlite:///' + os.path.join(path, 'database/user_database.db'),
   'aluno_database': 'sqlite:///' + os.path.join(path, 'database/aluno_database.db')
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
  return redirect(url_for('login'))

db = SQLAlchemy(app)

# Classe para databse do usuário
class User(UserMixin, db.Model):
    __bind_key__ = 'user_database'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(120))
    sobrenome = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
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
    __bind_key__ =  "aluno_database"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(20))
    idade = db.Column(db.Integer())
    cpf = db.Column(db.Integer())
    curso = db.Column(db.String(128))
    telefone = db.Column(db.Integer())
    horario= db.Column(db.String(128))
    email = db.Column(db.String(128))
    aniversario = db.Column(db.String(128))
    bolsa = db.Column(db.Boolean())
    pagamento = db.relationship('Pagamento', backref='aluno', lazy='dynamic')

    def __repr__(self):
        return f"{self.nome}"

class Pagamento(db.Model):
    __bind_key__ =  "aluno_database"
    id = db.Column(db.Integer, primary_key=True)
    pagamento = db.Column(db.Boolean())
    mes = db.Column(db.DateTime, default=datetime.utcnow)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'))

    def __repr__(self):
        return self.pagamento

def admin_acces():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.get_id()).first()
        if user.is_admin:
            return True
        else: return False

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/alunos", methods=["GET", "POST"])
def alunos_cadastrados():
    alunos = Aluno.query.all()
    return render_template('alunos.html', alunos = alunos)

#corrigir depois
@app.route("/pesquisa")
def pesquisa():
    pesquisa = request.args.get("q")
    if pesquisa:
        print(pesquisa)
        results = Aluno.query.filter(Aluno.nome.icontains(pesquisa)).order_by(Aluno.nome.asc()).limit(100).all()
    else: 
        results = []
    return render_template("pesquisa_aluno.html", results=results)

@app.route("/aluno/<aluno_id>")
@login_required
def aluno(aluno_id):
    if admin_acces():
        aluno = Aluno.query.filter_by(id=aluno_id).first()
        return render_template("aluno.html", aluno=aluno)
    return "Acesso Bloqueado"

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
            db.session.add(aluno)
            db.session.commit()
            return redirect(url_for("cadastro_aluno", _external=True, _scheme='http'))
    else: return "Acesso Bloqueado"
    return render_template("cadastro.html", template_form=cadastrar_form)

# Finalizar Route
@app.route('/editar_aluno/<aluno_name>/<aluno_id>', methods=["GET", "POST"])
@login_required
def editar_aluno(aluno_name, aluno_id):
    editar_form = Editar_Form()
    aluno_edite = Aluno.query.filter_by(id=aluno_id).first()
    if admin_acces():
        if editar_form.validate_on_submit():
            aluno_edite.pagamento = editar_form.pagamento.data

            db.session.commit()
            return redirect(url_for("alunos_cadastrados", _external=True, _scheme='http'))
    else: return "Acesso bloqueado!"
    return render_template("editar.html", editar_form=editar_form, aluno_edite = aluno_edite)

@app.route("/cursos")
def cursos():
    return render_template("cursos.html")

@app.route("/pagamentos", methods=["GET", "POST"])
@login_required
def pagamentos():
    file_form = Upload_File()
    if file_form.validate_on_submit():
        selection = file_form.directory.data
        arquivo = file_form.file_up.data
        filename = secure_filename(arquivo.filename)
        try:
            arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'] + f"/{selection}", filename))
        except:
            new_path = os.path.join(app.config['UPLOAD_FOLDER'] + f"/{selection}")
            os.mkdir(new_path)
            arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'] + f"/{selection}", filename))
        return redirect(url_for('pagamentos'))
    return render_template("pagamentos.html", file_form=file_form)

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
    if current_user.get_id() == user_id:
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
    users = User.query.all()
    admin = User.query.filter_by(id=current_user.id).first()
    if current_user.admin == 1:
        return render_template("admin.html", users=users, admin=admin, alunos=alunos, reversed=reversed)
    else:
        flash("Você não possui acesso a esta página!")
        return(redirect(url_for('home')))

@app.route("/user/<user_id>")
@login_required
def edit_user(user_id):
    user_edit = User.query.filter_by(id = user_id).first()
    if current_user.dev == 1:
        return render_template("edit_user.html", user_edit=user_edit)
    else:
        flash("Você não possui acesso a esta página!")
        return(redirect(request.referrer))

if __name__ == "__main__":
    app.run(debug=True)