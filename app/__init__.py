from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_admin import Admin
from config import Config
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
admin = Admin(name="Biblioteca Admin", template_mode="bootstrap4")
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    admin.init_app(app)
    from app.routes.auth import auth_bp
    from app.routes.usuario import usuario_bp
    from app.routes.libro import libro_bp
    from app.routes.categoria import categoria_bp
    from app.routes.chatbot import chatbot_bp
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(libro_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(dashboard_bp)
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.dashboard'))
        return """
        <html>
        <head>
            <title>Sistema de Biblioteca</title>
        </head>
        <body>
            <div style='text-align:center; margin-top:100px; font-family:sans-serif;'>
                <h1>Bienvenido al Sistema de Biblioteca</h1>
                <a href='/auth/login' 
                   style='display:inline-block; margin-top:30px; padding:12px 25px; 
                          background-color:#0d6efd; color:white; text-decoration:none; 
                          font-weight:bold; border-radius:5px; font-size:16px;'>
                    Iniciar Sesión
                </a>
            </div>
        </body>
        </html>
        """
    return app