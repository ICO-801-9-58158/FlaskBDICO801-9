from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from maestros import maestros_bp
from models import db, Alumnos
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(maestros_bp)

@app.route("/", methods=["GET"])
@app.route("/index")
def index():
    return render_template("bienvenida.html")

@app.route("/alumnos/lista", methods=["GET"])
def lista_alumnos():
    alumno = Alumnos.query.all()
    return render_template("alumnos/index.html", alumno=alumno)

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST' and create_form.validate():
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            amaterno=create_form.amaterno.data,
            edad=create_form.edad.data,
            email=create_form.email.data
        )
        db.session.add(alum)
        db.session.commit()
        flash("Alumno registrado exitosamente")
        return redirect(url_for('lista_alumnos'))
    return render_template("alumnos/crear.html", form=create_form)

@app.route("/alumnos/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)
    id = request.args.get('id') or request.form.get('id')
    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

    if request.method == 'GET':
        if not alum1:
            flash("Alumno no encontrado")
            return redirect(url_for('lista_alumnos'))
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.amaterno.data = alum1.amaterno
        create_form.edad.data = alum1.edad
        create_form.email.data = alum1.email

    if request.method == 'POST' and create_form.validate():
        if alum1:
            alum1.nombre = create_form.nombre.data
            alum1.apaterno = create_form.apaterno.data
            alum1.amaterno = create_form.amaterno.data
            alum1.edad = create_form.edad.data
            alum1.email = create_form.email.data
            db.session.commit()
            flash("Alumno modificado correctamente")
        return redirect(url_for('index'))
        
    return render_template("alumnos/modificar.html", form=create_form)

@app.route('/alumnos/eliminar', methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    id = request.args.get('id') or request.form.get('id')
    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

    if request.method == 'GET':
        if not alum1:
            flash("Alumno no encontrado")
            return redirect(url_for('index'))
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.amaterno.data = alum1.amaterno
        create_form.edad.data = alum1.edad
        create_form.email.data = alum1.email

    if request.method == 'POST':
        if alum1:
            db.session.delete(alum1)
            db.session.commit()
            flash("Alumno eliminado correctamente")
        return redirect(url_for('index'))
        
    return render_template('alumnos/eliminar.html', form=create_form)

@app.route("/alumnos/detalles", methods=['GET'])
def detalles():
    id = request.args.get('id')
    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
    
    if not alum1:
        flash("Alumno no encontrado")
        return redirect(url_for('lista_alumnos'))
        
    return render_template(
        'alumnos/detalles.html',
        id=alum1.id,
        nombre=alum1.nombre,
        apaterno=alum1.apaterno,
        amaterno=alum1.amaterno,
        edad=alum1.edad,
        email=alum1.email
    )

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