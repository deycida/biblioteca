from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistroForm, LoginForm
from app.models import Usuario, db
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))    
    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            rol=form.rol.data
        )
        usuario.set_contrasena(form.contrasena.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario registrado correctamente', 'success')
        return redirect(url_for('auth.login'))    
    return render_template('registro.html', form=form)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_contrasena(form.contrasena.data):
            login_user(usuario)
            flash('Bienvenido', 'success')
            if usuario.rol == 'admin':
                return redirect(url_for('dashboard.dashboard'))
            else:
                return redirect(url_for('libro.listar'))
        else:
            flash('Email o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('auth.login'))