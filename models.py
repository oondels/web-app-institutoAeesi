from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key = True)
        nome = db.Column(db.String(200))
        sobrenome = db.Column(db.String(200))
        email = db.Column(db.String(40), unique=True, index=True)
        password_hash = db.Column(db.String(200))
        is_confirmed = db.Column(db.Boolean(), nullable=False, default=False)
        confirmed_on = db.Column(db.DateTime(), nullable=True)
        dev = db.Column(db.Boolean())
        admin = db.Column(db.Boolean())

        def __repr__(self):
            return f'{self.nome}'

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)
    
class Aluno(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        nome = db.Column(db.String(200))
        idade = db.Column(db.Integer())
        cpf = db.Column(db.String(200))
        curso = db.Column(db.String(40))
        telefone = db.Column(db.String(25))
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