import os
import sys
from app import app
from models import db, Alumnos, Maestros, Curso, Inscripcion

def test_delete_maestro(matricula):
    with app.app_context():
        print(f"--- Testing Deletion of Maestro {matricula} ---")
        maestro = db.session.get(Maestros, matricula)
        if not maestro:
            print("Maestro not found.")
            return

        print(f"Found Maestro: {maestro.nombre} {maestro.apellidos}")
        print(f"Cursos: {[c.nombre for c in maestro.cursos]}")

        try:
            # MANUAL SCORCHED EARTH DELETE
            for curso in maestro.cursos:
                print(f"Cleaning up inscripciones for course: {curso.nombre}")
                Inscripcion.query.filter_by(curso_id=curso.id).delete()
            
            # Now let cascade handle courses if possible, or do it manually
            # To be 100% sure, we delete courses explicitly too
            Curso.query.filter_by(maestro_id=matricula).delete()
            
            db.session.delete(maestro)
            db.session.commit()
            print("Deletion successful!")
        except Exception as e:
            db.session.rollback()
            print(f"FAIL: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_delete_maestro(int(sys.argv[1]))
    else:
        print("Please provide a matricula.")
