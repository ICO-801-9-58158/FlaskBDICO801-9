from flask_sqlalchemy import SQLAlchemy #ORM
import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apaterno = db.Column(db.String(50), nullable=False)
    amaterno = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    correo = db.Column(db.String(100), nullable=False)



class Maestros(db.Model):
    __tablename__ = 'maestros'
    id_maestro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    especialidad = db.Column(db.String(50))
    email = db.Column(db.String(50))
    cursos = db.relationship('Curso', back_populates='maestro')