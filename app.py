from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from models import db
from maestros import maestros_bp
from alumnos import alumnos_bp
from cursos import cursos_bp
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(maestros_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(cursos_bp)

@app.route("/", methods=["GET"])
@app.route("/index")
def index():
    return render_template("bienvenida.html")

@app.route("/usuarios", methods=["GET", "POST"])
def usuario():
    usuarios_clas = forms.UserForm(request.form)
    mat, nom, apa, ama, edad, email = 0, '', '', '', 0, ''
    
    if request.method == 'POST' and usuarios_clas.validate():
        mat = usuarios_clas.id.data
        nom = usuarios_clas.nombre.data
        apa = usuarios_clas.apaterno.data
        ama = usuarios_clas.amaterno.data
        edad = usuarios_clas.edad.data
        email = usuarios_clas.email.data
        flash("Usuario procesado correctamente")

    return render_template(
        'usuarios.html',
        form=usuarios_clas,
        mat=mat, nom=nom, apa=apa, ama=ama, edad=edad, email=email
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)