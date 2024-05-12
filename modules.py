from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from extension import db
from datetime import datetime, date

class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key = True)
        nome = db.Column(db.String())
        sobrenome = db.Column(db.String())
        email = db.Column(db.String(), unique=True, index=True)
        password_hash = db.Column(db.String())
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
        nome = db.Column(db.String())
        idade = db.Column(db.Integer())
        cpf = db.Column(db.Integer())
        curso = db.Column(db.String())
        telefone = db.Column(db.Integer())
        horario= db.Column(db.String())
        email = db.Column(db.String())
        aniversario = db.Column(db.String())
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