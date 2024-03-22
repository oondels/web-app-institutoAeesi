import os
from flask import Flask, render_template, redirect, url_for, flash
from forms import Cadastro_Form, Upload_File, Register_User, Login_User
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user

path = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret" #Editar senha depois
folder = os.path.join(path, "database/files")

app.config['UPLOAD_FOLDER'] = folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(path, 'database/geral.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
   'user_database': 'sqlite:///' + os.path.join(path, 'database/user_database.db'),
   'alunos_database': 'sqlite:///' + os.path.join(path, 'database/alunos_database.db')
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
    __bind_key__ =  "alunos_database"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(20))
    sobrenome = db.Column(db.String(128))
    idade = db.Column(db.Integer())
    curso = db.Column(db.String(128))
    bolsa = db.Column(db.Boolean())

    def __repr__(self):
        return f"{self.nome}"

def admin_acces():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.get_id()).first()
        if user.is_admin:
            return True
        else: return False

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/alunos")
def alunos_cadastrados():
    alunos = Aluno.query.all()
    return render_template('alunos.html', alunos = alunos)

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
            sobrenome = cadastrar_form.sobrenome.data
            idade = cadastrar_form.idade.data
            curso = cadastrar_form.curso.data
            bolsa = cadastrar_form.bolsa.data

            aluno = Aluno(nome=nome, sobrenome=sobrenome, idade=idade, curso=curso, bolsa=bolsa)
            db.session.add(aluno)
            db.session.commit()
            return redirect(url_for("cadastro_aluno", _external=True, _scheme='http'))
    else: return "Acesso Bloqueado"
    return render_template("cadastro.html", template_form=cadastrar_form)

# Finalizar Route
@app.route('/editar_aluno/<aluno_name>/<aluno_id>')
def editar_aluno(aluno_name, aluno_id):
    if admin_acces():
        aluno_edite = Aluno.query.filter_by(id=aluno_id).first()
    return "editando..."

@app.route("/upload-arquivos", methods=["GET", "POST"])
@login_required
def upload_files():
    file_form = Upload_File()

    if file_form.validate_on_submit():
        arquivo = file_form.file_up.data
        filename = secure_filename(arquivo.filename)
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER']+"\comprovantes", filename))
        return redirect(url_for('upload_files'))
    return render_template("upload.html", file_form=file_form)

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

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and check_password_hash(user.password_hash, login_form.password.data):
            login_user(user)
            return redirect(url_for('user_page', user_id=user.id))
        else:
            flash("Falha ao efetuar login. Verifique erro de digitação ou se já esta cadastrado no sistema!")
            return redirect(url_for('login'))
    return render_template("login.html", login_form=login_form)

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

if __name__ == "__main__":
    app.run(debug=True)