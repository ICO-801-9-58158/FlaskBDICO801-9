from flask import render_template, request, redirect, url_for, flash
from models import db, Curso, Maestros, Alumnos, Inscripcion
import forms
from . import cursos_bp

@cursos_bp.route("/cursos/lista", methods=["GET"])
def lista_cursos():
    cursos = Curso.query.all()
    return render_template("cursos/index.html", cursos=cursos)

@cursos_bp.route("/cursos/nuevo", methods=["GET", "POST"])
def crear_curso():
    create_form = forms.CursoForm(request.form)
    # Populate maestros choices
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros]

    if request.method == 'POST' and create_form.validate():
        curso = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )
        db.session.add(curso)
        db.session.commit()
        flash("Curso registrado exitosamente")
        return redirect(url_for('cursos.lista_cursos'))
    
    return render_template("cursos/crear.html", form=create_form)

@cursos_bp.route("/cursos/modificar", methods=['GET', 'POST'])
def modificar_curso():
    create_form = forms.CursoForm(request.form)
    id = request.args.get('id') or request.form.get('id')
    curso = db.session.get(Curso, id)

    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros]

    if request.method == 'GET':
        if not curso:
            flash("Curso no encontrado")
            return redirect(url_for('cursos.lista_cursos'))
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id

    if request.method == 'POST' and create_form.validate():
        if curso:
            curso.nombre = create_form.nombre.data
            curso.descripcion = create_form.descripcion.data
            curso.maestro_id = create_form.maestro_id.data
            db.session.commit()
            flash("Curso modificado correctamente")
        return redirect(url_for('cursos.lista_cursos'))
        
    return render_template("cursos/modificar.html", form=create_form)

@cursos_bp.route('/cursos/eliminar', methods=['GET', 'POST'])
def eliminar_curso():
    create_form = forms.CursoForm(request.form)
    id = request.args.get('id') or request.form.get('id')
    curso = db.session.get(Curso, id)

    if request.method == 'GET':
        if not curso:
            flash("Curso no encontrado")
            return redirect(url_for('cursos.lista_cursos'))
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre

    if request.method == 'POST':
        if curso:
            db.session.delete(curso)
            db.session.commit()
            flash("Curso eliminado correctamente")
        return redirect(url_for('cursos.lista_cursos'))
        
    return render_template('cursos/eliminar.html', form=create_form)

@cursos_bp.route("/cursos/detalles", methods=['GET', 'POST'])
def detalles_curso():
    id = request.args.get('id')
    curso = db.session.get(Curso, id)
    
    if not curso:
        flash("Curso no encontrado")
        return redirect(url_for('cursos.lista_cursos'))

    return render_template(
        'cursos/detalles.html',
        curso=curso
    )
