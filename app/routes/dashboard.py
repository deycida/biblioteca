from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Libro, Categoria
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
@dashboard_bp.route("/")
@login_required
def dashboard():
    if current_user.rol != 'admin':
        return redirect(url_for('libro.listar'))
    total_libros = Libro.query.count()
    total_categorias = Categoria.query.count()
    libro_popular = Libro.query.first()
    nombre_libro_popular = libro_popular.titulo if libro_popular else "Ninguno"
    categorias = Categoria.query.all()
    categorias_nombres = [c.nombre for c in categorias]
    libros_por_categoria = [Libro.query.filter_by(categoria_id=c.id).count() for c in categorias]
    analisis = (
        f"📊 En el sistema hay {total_libros} libros y {total_categorias} categorías.\n"
        f"⭐ El libro destacado es '{nombre_libro_popular}'.\n"
        f"🔍 Predicción: si se agregan más libros de la categoría "
        f"'{libro_popular.categoria.nombre if libro_popular else 'N/A'}', podría ser la categoría más popular."
    )
    return render_template(
        "dashboard.html",
        total_libros=total_libros,
        total_categorias=total_categorias,
        analisis=analisis,
        categorias_nombres=categorias_nombres,
        libros_por_categoria=libros_por_categoria
    )