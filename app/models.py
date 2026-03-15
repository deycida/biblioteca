from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='usuario')
    def set_contrasena(self, contrasena):
        self.contrasena = generate_password_hash(contrasena)
    def check_contrasena(self, contrasena):
        return check_password_hash(self.contrasena, contrasena)
@login_manager.user_loader
def load_usuario(usuario_id):
    return Usuario.query.get(int(usuario_id))
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    libros = db.relationship('Libro', backref='categoria', lazy=True)
class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)