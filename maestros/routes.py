from flask import render_template, request, redirect, url_for, flash
from models import db, Maestros
import forms
from . import maestros_bp

@maestros_bp.route("/maestros", methods=["GET", "POST"])
def maestros():
    create_form = forms.MaestrosForm(request.form)
    maestros = Maestros.query.all()
    return render_template("maestros/index.html", form=create_form, maestros=maestros)

@maestros_bp.route("/maestros/nuevo", methods=["GET", "POST"])
def maestros_nuevo():
    create_form = forms.MaestrosForm(request.form)

    if request.method == 'POST':
        if not create_form.validate():
            flash("Te faltan datos o hay campos inválidos")
            return render_template("maestros/crear.html", form=create_form)

        try:
            matricula_int = int(create_form.matricula.data)
        except ValueError:
            flash("La matrícula debe ser numérica")
            return render_template("maestros/crear.html", form=create_form)

        existe_maestro = db.session.query(Maestros).filter(
            Maestros.matricula == matricula_int
        ).first()

        if existe_maestro:
            flash("No se puede registrar porque la matrícula ya existe")
            return render_template("maestros/crear.html", form=create_form)

        maestro = Maestros(
            matricula=matricula_int,
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data
        )
        db.session.add(maestro)
        db.session.commit()
        flash("Maestro registrado correctamente")
        return redirect(url_for('maestros.maestros'))

    return render_template("maestros/crear.html", form=create_form)

@maestros_bp.route("/maestros/modificar", methods=['GET', 'POST'])
def maestros_modificar():
    create_form = forms.MaestrosForm(request.form)

    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        create_form.matricula.data = maestro1.matricula
        create_form.nombre.data = maestro1.nombre
        create_form.apellidos.data = maestro1.apellidos
        create_form.especialidad.data = maestro1.especialidad
        create_form.email.data = maestro1.email

    if request.method == 'POST':
        if not create_form.validate():
            flash("Te faltan datos o hay campos inválidos")
            return render_template("maestros/modificar.html", form=create_form)

        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        maestro1.matricula = matricula
        maestro1.nombre = create_form.nombre.data
        maestro1.apellidos = create_form.apellidos.data
        maestro1.especialidad = create_form.especialidad.data
        maestro1.email = create_form.email.data
        db.session.add(maestro1)
        db.session.commit()
        flash("Maestro modificado correctamente")
        return redirect(url_for('maestros.maestros'))

    return render_template("maestros/modificar.html", form=create_form)

@maestros_bp.route('/maestros/eliminar', methods=['GET', 'POST'])
def maestros_eliminar():
    create_form = forms.MaestrosForm(request.form)

    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        create_form.matricula.data = maestro1.matricula
        create_form.nombre.data = maestro1.nombre
        create_form.apellidos.data = maestro1.apellidos
        create_form.especialidad.data = maestro1.especialidad
        create_form.email.data = maestro1.email

    if request.method == 'POST':
        matricula = request.form.get('matricula')
        maestro = Maestros.query.get_or_404(matricula)
        db.session.delete(maestro)
        db.session.commit()
        flash("Maestro eliminado correctamente")
        return redirect(url_for('maestros.maestros'))

    return render_template('maestros/eliminar.html', form=create_form)

@maestros_bp.route("/maestros/detalles", methods=['GET', 'POST'])
def maestros_detalles():
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        matricula = request.args.get('matricula')
        nombre = maestro1.nombre
        apellidos = maestro1.apellidos
        especialidad = maestro1.especialidad
        email = maestro1.email

    return render_template(
        'maestros/detalles.html',
        matricula=matricula,
        nombre=nombre,
        apellidos=apellidos,
        especialidad=especialidad,
        email=email
    )