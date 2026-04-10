from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate
from maestros import maestros_bp

from models import db, Alumnos
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros_bp)

db.init_app(app)
csrf = CSRFProtect()
migrate = Migrate(app, db)


@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    create_alumno = forms.UserForm(request.form)
    alumno = Alumnos.query.all()
    return render_template("alumnos/index.html", form=create_alumno, alumno=alumno)


@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST':
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            amaterno=create_form.amaterno.data,
            edad=create_form.edad.data,
            email=create_form.email.data
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("alumnos/crear.html", form=create_form)


@app.route("/alumnos/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.amaterno.data = alum1.amaterno
        create_form.edad.data = alum1.edad
        create_form.email.data = alum1.email

    if request.method == 'POST':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum1.id = id
        alum1.nombre = create_form.nombre.data
        alum1.apaterno = create_form.apaterno.data
        alum1.amaterno = create_form.amaterno.data
        alum1.edad = create_form.edad.data
        alum1.email = create_form.email.data
        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("alumnos/modificar.html", form=create_form)


@app.route('/alumnos/eliminar', methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.amaterno.data = alum1.amaterno
        create_form.edad.data = alum1.edad
        create_form.email.data = alum1.email

    if request.method == 'POST':
        id = request.form.get('id')
        alum = Alumnos.query.get_or_404(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('alumnos/eliminar.html', form=create_form)


@app.route("/alumnos/detalles", methods=['GET', 'POST'])
def detalles():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        id = request.args.get('id')
        nombre = alum1.nombre
        apaterno = alum1.apaterno
        amaterno = alum1.amaterno
        edad = alum1.edad
        email = alum1.email

    return render_template(
        'alumnos/detalles.html',
        id=id,
        nombre=nombre,
        apaterno=apaterno,
        amaterno=amaterno,
        edad=edad,
        email=email
    )


@app.route("/usuarios", methods=["GET", "POST"])
def usuario():
    mat = 0
    nom = ''
    apa = ''
    ama = ''
    edad = 0
    email = ''
    usuarios_clas = forms.UserForm(request.form)
    if request.method == 'POST':
        mat = usuarios_clas.id.data
        nom = usuarios_clas.nombre.data
        apa = usuarios_clas.apaterno.data
        ama = usuarios_clas.amaterno.data
        edad = usuarios_clas.edad.data
        email = usuarios_clas.email.data

    return render_template(
        'usuarios.html',
        form=usuarios_clas,
        mat=mat,
        nom=nom,
        apa=apa,
        ama=ama,
        edad=edad,
        email=email
    )


if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()