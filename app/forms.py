from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Usuario, Categoria
def validar_categoria(form, field):
    if field.data.lower() == "general":
        raise ValidationError("No se permite la categoría 'General'.")
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar_contrasena = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('contrasena')])
    rol = SelectField('Rol', choices=[('usuario', 'Usuario'), ('admin', 'Admin')])
    submit = SubmitField('Registrarse')
    def validate_email(self, email):
        if Usuario.query.filter_by(email=email.data).first():
            raise ValidationError('Email ya registrado.')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')
class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), validar_categoria])
    submit = SubmitField('Guardar')
class LibroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired()])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')
class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    rol = SelectField('Rol', choices=[('usuario', 'Usuario'), ('admin', 'Admin')])
    submit = SubmitField('Guardar')