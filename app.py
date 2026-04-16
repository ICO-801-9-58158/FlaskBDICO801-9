from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from models import db
from maestros import maestros_bp
from alumnos import alumnos_bp
from cursos import cursos_bp
from inscripciones import inscripciones_bp
import forms

from sqlalchemy import event
from sqlalchemy.engine import Engine

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Enable Foreign Key support for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(maestros_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(inscripciones_bp)

@app.route("/", methods=["GET"])
@app.route("/index")
def index():
    return render_template("bienvenida.html")


    return render_template(
        'usuarios.html',
        form=usuarios_clas,
        mat=mat, nom=nom, apa=apa, ama=ama, edad=edad, email=email
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)