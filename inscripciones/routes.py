from flask import render_template, request, redirect, url_for, flash
from models import db, Curso, Maestros, Alumnos, Inscripcion
import forms
from . import inscripciones_bp

@inscripciones_bp.route("/inscripciones", methods=["GET"])
def lista_inscripciones():
    inscripciones = Inscripcion.query.all()
    return render_template("inscripciones/index.html", inscripciones=inscripciones)

@inscripciones_bp.route("/inscripciones/nueva", methods=["GET", "POST"])
def nueva_inscripcion():
    enroll_form = forms.InscripcionForm(request.form)
    
    # Populate cursos and alumnos for the form
    cursos = Curso.query.all()
    alumnos = Alumnos.query.all()
    
    # Since InscripcionForm.curso_id is HiddenField in original forms.py, 
    # I might want to change it to SelectField or keep it if I use a specific flow.
    # Looking at forms.py, curso_id is HiddenField. 
    # I'll modify the form choices dynamically or create a dedicated form if needed.
    
    # Let's see if I can use the existing form or if I should adjust it.
    # To make it "separate", it's better to select BOTH student and course.
    
    if request.method == 'GET':
        # If passed from a curso page
        curso_id = request.args.get('curso_id')
        if curso_id:
            enroll_form.curso_id.data = curso_id

    # For a general "New Inscription" page, we need to choose the course too.
    # I'll monkey-patch the form to have a SelectField for curso_id if it's the general page
    # OR better yet, just use the request.form directly for curso_id if it's not in the form object.
    
    # Actually, let's just use the form classes we have.
    # I'll update forms.py later if needed, but for now I'll handle it here.
    
    if request.method == 'POST':
        alumno_id = request.form.get('alumno_id')
        curso_id = request.form.get('curso_id')
        
        if not alumno_id or not curso_id:
            flash("Debe seleccionar alumno y curso")
        else:
            # Check if already exists
            existe = Inscripcion.query.filter_by(alumno_id=alumno_id, curso_id=curso_id).first()
            if existe:
                flash("El alumno ya está inscrito en este curso")
            else:
                nueva = Inscripcion(alumno_id=alumno_id, curso_id=curso_id)
                db.session.add(nueva)
                db.session.commit()
                flash("Inscripción realizada con éxito")
                return redirect(url_for('inscripciones.lista_inscripciones'))

    return render_template(
        "inscripciones/crear.html", 
        form=enroll_form, 
        cursos=cursos, 
        alumnos=alumnos
    )

@inscripciones_bp.route("/inscripciones/eliminar", methods=["POST"])
def eliminar_inscripcion():
    alumno_id = request.form.get('alumno_id')
    curso_id = request.form.get('curso_id')
    
    inscripcion = Inscripcion.query.filter_by(alumno_id=alumno_id, curso_id=curso_id).first()
    if inscripcion:
        db.session.delete(inscripcion)
        db.session.commit()
        flash("Inscripción eliminada correctamente")
    else:
        flash("Inscripción no encontrada")
        
    return redirect(url_for('inscripciones.lista_inscripciones'))

@inscripciones_bp.route("/consultas", methods=["GET"])
def consultas():
    query = request.args.get('search', '').strip()
    
    # Statistics (usually unaffected by specific search for counts, 
    # but we can filter detailed lists below)
    total_alumnos = Alumnos.query.count()
    total_maestros = Maestros.query.count()
    total_cursos = Curso.query.count()
    total_inscripciones = Inscripcion.query.count()
    
    # Detailed data for tables with optional filtering
    if query:
        cursos = Curso.query.filter(Curso.nombre.ilike(f"%{query}%")).all()
        maestros = Maestros.query.filter(
            (Maestros.nombre.ilike(f"%{query}%")) | 
            (Maestros.apellidos.ilike(f"%{query}%"))
        ).all()
    else:
        cursos = Curso.query.all()
        maestros = Maestros.query.all()
    
    alumnos = Alumnos.query.all()
    
    return render_template(
        "inscripciones/consultas.html",
        total_alumnos=total_alumnos,
        total_maestros=total_maestros,
        total_cursos=total_cursos,
        total_inscripciones=total_inscripciones,
        cursos=cursos,
        maestros=maestros,
        alumnos=alumnos,
        search_query=query
    )
