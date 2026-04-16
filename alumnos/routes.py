from flask import render_template, request, redirect, url_for, flash
from models import db, Alumnos
import forms
from . import alumnos_bp

@alumnos_bp.route("/alumnos/lista", methods=["GET"])
def lista_alumnos():
    alumno = Alumnos.query.all()
    return render_template("alumnos/index.html", alumno=alumno)

@alumnos_bp.route("/alumnos", methods=['GET', 'POST'])
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
        return redirect(url_for('alumnos.lista_alumnos'))
    return render_template("alumnos/crear.html", form=create_form)

@alumnos_bp.route("/alumnos/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)
    id = request.args.get('id') or request.form.get('id')
    alum1 = db.session.get(Alumnos, id)

    if request.method == 'GET':
        if not alum1:
            flash("Alumno no encontrado")
            return redirect(url_for('alumnos.lista_alumnos'))
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
        return redirect(url_for('alumnos.lista_alumnos'))
        
    return render_template("alumnos/modificar.html", form=create_form)

@alumnos_bp.route('/alumnos/eliminar', methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    id = request.args.get('id') or request.form.get('id')
    alum1 = db.session.get(Alumnos, id)

    if request.method == 'GET':
        if not alum1:
            flash("Alumno no encontrado")
            return redirect(url_for('alumnos.lista_alumnos'))
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
        return redirect(url_for('alumnos.lista_alumnos'))
        
    return render_template('alumnos/eliminar.html', form=create_form)

@alumnos_bp.route("/alumnos/detalles", methods=['GET'])
def detalles():
    id = request.args.get('id')
    alum1 = db.session.get(Alumnos, id)
    
    if not alum1:
        flash("Alumno no encontrado")
        return redirect(url_for('alumnos.lista_alumnos'))
        
    return render_template(
        'alumnos/detalles.html',
        id=alum1.id,
        nombre=alum1.nombre,
        apaterno=alum1.apaterno,
        amaterno=alum1.amaterno,
        edad=alum1.edad,
        email=alum1.email
    )
