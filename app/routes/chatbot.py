from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.models import Libro, Categoria
chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")
@chatbot_bp.route("/", methods=["POST"])
@login_required
def chat():
    pregunta = request.json.get("mensaje", "").lower()
    if "cuantos libros" in pregunta or "número de libros" in pregunta:
        total = Libro.query.count()
        return jsonify({"respuesta": f"Hay {total} libros registrados."})
    if "listar libros" in pregunta or "mostrar libros" in pregunta:
        libros = Libro.query.limit(5).all()
        if libros:
            titulos = ", ".join([libro.titulo for libro in libros])
            return jsonify({"respuesta": f"Algunos libros disponibles son: {titulos}"})
        return jsonify({"respuesta": "No hay libros registrados."})
    if "libro más popular" in pregunta or "destacado" in pregunta:
        libro = Libro.query.first()
        if libro:
            return jsonify({"respuesta": f"El libro destacado es '{libro.titulo}'."})
        return jsonify({"respuesta": "No hay libros registrados."})
    if "categorías" in pregunta or "categorias" in pregunta:
        categorias = Categoria.query.all()
        if categorias:
            nombres = ", ".join([c.nombre for c in categorias])
            return jsonify({"respuesta": f"Las categorías disponibles son: {nombres}"})
        return jsonify({"respuesta": "No hay categorías registradas."})
    if "recomiendame un libro" in pregunta:
        libro = Libro.query.first()
        if libro:
            return jsonify({"respuesta": f"Te recomiendo el libro '{libro.titulo}'."})
        return jsonify({"respuesta": "No hay libros registrados para recomendar."})
    return jsonify({"respuesta": "No entendí tu pregunta. Prueba con '¿Cuántos libros hay?' o 'Mostrar libros'."})
@chatbot_bp.route("/interfaz")
@login_required
def interfaz():
    return render_template("chatbot.html")