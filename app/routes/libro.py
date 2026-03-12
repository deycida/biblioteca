from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import Libro, Categoria, db
from app.forms import LibroForm
from functools import wraps

libro_bp = Blueprint('libro', __name__, url_prefix='/libro')

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.rol != 'admin':
            abort(403)
        return func(*args, **kwargs)
    return wrapper

@libro_bp.route('/')
@login_required
def listar():
    busqueda = request.args.get('busqueda', '')
    libros = Libro.query.filter(Libro.titulo.contains(busqueda)).all()
    return render_template('libro/listar.html', libros=libros, busqueda=busqueda)

@libro_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear():
    form = LibroForm()
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    if form.validate_on_submit():
        libro = Libro(titulo=form.titulo.data, autor=form.autor.data, categoria_id=form.categoria_id.data)
        db.session.add(libro)
        db.session.commit()
        flash('Libro creado', 'success')
        return redirect(url_for('libro.listar'))
    return render_template('libro/crear.html', form=form)

@libro_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    libro = Libro.query.get_or_404(id)
    form = LibroForm(obj=libro)
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    if form.validate_on_submit():
        libro.titulo = form.titulo.data
        libro.autor = form.autor.data
        libro.categoria_id = form.categoria_id.data
        db.session.commit()
        flash('Libro actualizado', 'success')
        return redirect(url_for('libro.listar'))
    return render_template('libro/editar.html', form=form)

@libro_bp.route('/eliminar/<int:id>')
@login_required
@admin_required
def eliminar(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    flash('Libro eliminado', 'info')
    return redirect(url_for('libro.listar'))