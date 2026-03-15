from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import Usuario, db
from app.forms import UsuarioForm
from functools import wraps
usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.rol != 'admin':
            abort(403)
        return func(*args, **kwargs)
    return wrapper
@usuario_bp.route('/')
@login_required
@admin_required
def listar():
    busqueda = request.args.get('busqueda', '')
    usuarios = Usuario.query.filter(Usuario.nombre.contains(busqueda)).all()
    return render_template('usuario/listar.html', usuarios=usuarios, busqueda=busqueda)
@usuario_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear():
    form = UsuarioForm()
    if form.validate_on_submit():
        usuario = Usuario(nombre=form.nombre.data, email=form.email.data, rol=form.rol.data)
        usuario.set_contrasena('123456')
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario creado', 'success')
        return redirect(url_for('usuario.listar'))
    return render_template('usuario/crear.html', form=form)
@usuario_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nombre = form.nombre.data
        usuario.email = form.email.data
        usuario.rol = form.rol.data
        db.session.commit()
        flash('Usuario actualizado', 'success')
        return redirect(url_for('usuario.listar'))
    return render_template('usuario/editar.html', form=form)
@usuario_bp.route('/eliminar/<int:id>')
@login_required
@admin_required
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado', 'info')
    return redirect(url_for('usuario.listar'))