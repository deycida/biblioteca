import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi_clave_secreta'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/biblioteca'
    SQLALCHEMY_TRACK_MODIFICATIONS = False