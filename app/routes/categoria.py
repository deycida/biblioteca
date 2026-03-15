from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import Categoria, db
from app.forms import CategoriaForm
from functools import wraps
categoria_bp = Blueprint('categoria', __name__, url_prefix='/categoria')
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.rol != 'admin':
            abort(403)
        return func(*args, **kwargs)
    return wrapper
@categoria_bp.route('/')
@login_required
@admin_required
def listar():
    busqueda = request.args.get('busqueda', '')
    categorias = Categoria.query.filter(Categoria.nombre.contains(busqueda)).all()
    return render_template('categoria/listar.html', categorias=categorias, busqueda=busqueda)
@categoria_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear():
    form = CategoriaForm()
    if form.validate_on_submit():
        categoria = Categoria(nombre=form.nombre.data)
        db.session.add(categoria)
        db.session.commit()
        flash('Categoría creada', 'success')
        return redirect(url_for('categoria.listar'))
    return render_template('categoria/crear.html', form=form)
@categoria_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    categoria = Categoria.query.get_or_404(id)
    form = CategoriaForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nombre = form.nombre.data
        db.session.commit()
        flash('Categoría actualizada', 'success')
        return redirect(url_for('categoria.listar'))
    return render_template('categoria/editar.html', form=form)
@categoria_bp.route('/eliminar/<int:id>')
@login_required
@admin_required
def eliminar(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada', 'info')
    return redirect(url_for('categoria.listar'))