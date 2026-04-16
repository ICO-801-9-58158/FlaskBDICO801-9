from flask import render_template, request, redirect, url_for, flash
from models import db, Maestros, Curso, Inscripcion
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

    if request.method == 'POST' and create_form.validate():
        try:
            matricula_int = int(create_form.matricula.data)
        except (ValueError, TypeError):
            flash("La matrícula debe ser numérica")
            return render_template("maestros/crear.html", form=create_form)

        existe_maestro = db.session.get(Maestros, matricula_int)
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
    matricula = request.args.get('matricula') or request.form.get('matricula')
    maestro1 = db.session.get(Maestros, matricula)

    if request.method == 'GET':
        if not maestro1:
            flash("Maestro no encontrado")
            return redirect(url_for('maestros.maestros'))
        create_form.matricula.data = maestro1.matricula
        create_form.nombre.data = maestro1.nombre
        create_form.apellidos.data = maestro1.apellidos
        create_form.especialidad.data = maestro1.especialidad
        create_form.email.data = maestro1.email

    if request.method == 'POST' and create_form.validate():
        if maestro1:
            maestro1.nombre = create_form.nombre.data
            maestro1.apellidos = create_form.apellidos.data
            maestro1.especialidad = create_form.especialidad.data
            maestro1.email = create_form.email.data
            db.session.commit()
            flash("Maestro modificado correctamente")
        return redirect(url_for('maestros.maestros'))

    return render_template("maestros/modificar.html", form=create_form)

@maestros_bp.route('/maestros/eliminar', methods=['GET', 'POST'])
def maestros_eliminar():
    create_form = forms.MaestrosForm(request.form)
    matricula = request.args.get('matricula') or request.form.get('matricula')
    try:
        matricula_id = int(matricula) if matricula else None
    except (ValueError, TypeError):
        flash("Matrícula inválida")
        return redirect(url_for('maestros.maestros'))

    maestro1 = db.session.get(Maestros, matricula_id)
    
    if not maestro1:
        flash("Maestro no encontrado")
        return redirect(url_for('maestros.maestros'))

    # Check if maestro has courses
    cursos_asociados = maestro1.cursos
    has_courses = len(cursos_asociados) > 0

    if request.method == 'GET':
        create_form.matricula.data = maestro1.matricula
        create_form.nombre.data = maestro1.nombre
        create_form.apellidos.data = maestro1.apellidos
        create_form.especialidad.data = maestro1.especialidad
        create_form.email.data = maestro1.email

    if request.method == 'POST':
        try:
            # Re-fetch or ensure it's in session 
            maestro1 = db.session.get(Maestros, matricula_id)
            if maestro1:
                # SCORCHED EARTH: Manual cleanup to avoid IntegrityErrors
                # 1. Clear enrollments for all courses of this teacher
                for curso in maestro1.cursos:
                    Inscripcion.query.filter_by(curso_id=curso.id).delete()
                
                # 2. Clear courses of this teacher
                Curso.query.filter_by(maestro_id=matricula_id).delete()
                
                # 3. Finally delete the teacher
                db.session.delete(maestro1)
                db.session.commit()
                
                # Check if it was really deleted (safety check)
                check = db.session.get(Maestros, matricula_id)
                if not check:
                    flash("Maestro y registros asociados eliminados correctamente")
                else:
                    flash("Advertencia: El maestro sigue en la base de datos (error inesperado)")
            else:
                flash("El maestro ya ha sido eliminado o no existe.")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al eliminar: {str(e)}")
        
        return redirect(url_for('maestros.maestros'))

    return render_template('maestros/eliminar.html', form=create_form, has_courses=has_courses, cursos=cursos_asociados)

@maestros_bp.route("/maestros/detalles", methods=['GET'])
def maestros_detalles():
    matricula = request.args.get('matricula')
    maestro1 = db.session.get(Maestros, matricula)
    
    if not maestro1:
        flash("Maestro no encontrado")
        return redirect(url_for('maestros.maestros'))

    return render_template(
        'maestros/detalles.html',
        matricula=maestro1.matricula,
        nombre=maestro1.nombre,
        apellidos=maestro1.apellidos,
        especialidad=maestro1.especialidad,
        email=maestro1.email
    )