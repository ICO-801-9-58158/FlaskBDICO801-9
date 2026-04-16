from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apaterno = db.Column(db.String(50), nullable=False)
    amaterno = db.Column(db.String(150), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    # Many-to-many relationship (direct to Course via bridge)
    cursos = db.relationship(
        'Curso',
        secondary='inscripciones',
        back_populates='alumnos',
        passive_deletes=True,
        overlaps="inscripciones_list,alumno,curso"
    )

    # Direct relationship to Inscriptions bridge table
    # This is for detailed access (e.g. date_enrolled)
    inscripciones_list = db.relationship(
        'Inscripcion',
        back_populates='alumno',
        cascade="all, delete-orphan",
        passive_deletes=True,
        overlaps="cursos"
    )


class Maestros(db.Model):
    __tablename__ = 'maestros'

    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    cursos = db.relationship(
        'Curso', 
        back_populates='maestro', 
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    maestro_id = db.Column(
        db.Integer,
        db.ForeignKey('maestros.matricula', ondelete="CASCADE"),
        nullable=False
    )

    maestro = db.relationship('Maestros', back_populates='cursos', passive_deletes=True)

    # Many-to-many relationship (direct to Alumnos via bridge)
    alumnos = db.relationship(
        'Alumnos',
        secondary='inscripciones',
        back_populates='cursos',
        passive_deletes=True,
        overlaps="inscripciones_list,alumno,curso"
    )

    # Direct relationship to Inscriptions bridge table
    inscripciones_list = db.relationship(
        'Inscripcion',
        back_populates='curso',
        cascade="all, delete-orphan",
        passive_deletes=True,
        overlaps="alumnos"
    )


class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'

    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(
        db.Integer,
        db.ForeignKey('alumnos.id', ondelete="CASCADE"),
        nullable=False
    )

    curso_id = db.Column(
        db.Integer,
        db.ForeignKey('cursos.id', ondelete="CASCADE"),
        nullable=False
    )

    fecha_inscripcion = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Back-populates provides better control than backref
    alumno = db.relationship('Alumnos', back_populates='inscripciones_list', overlaps="cursos,alumnos")
    curso = db.relationship('Curso', back_populates='inscripciones_list', overlaps="cursos,alumnos")

    __table_args__ = (
        db.UniqueConstraint('alumno_id', 'curso_id', name='uq_alumno_curso'),
    )