# Diagrama Relacional Resultante

A continuación se muestra el diagrama del modelo relacional resultante, basado en los modelos implementados con SQLAlchemy para Flask (Maestros, Alumnos, Cursos e Inscripciones).

```mermaid
erDiagram
    MAESTROS ||--o{ CURSOS : "imparte (1:N)"
    ALUMNOS ||--o{ INSCRIPCIONES : "tiene (1:N)"
    CURSOS ||--o{ INSCRIPCIONES : "tiene (1:N)"
    
    MAESTROS {
        int matricula PK
        varchar_50 nombre
        varchar_50 apellidos
        varchar_50 especialidad
        varchar_50 email
    }
    
    ALUMNOS {
        int id PK
        varchar_50 nombre
        varchar_50 apaterno
        varchar_50 email
        datetime created_date
    }
    
    CURSOS {
        int id PK
        varchar_150 nombre
        text descripcion
        int maestro_id FK "References MAESTROS.matricula"
    }
    
    INSCRIPCIONES {
        int id PK
        int alumno_id FK "References ALUMNOS.id"
        int curso_id FK "References CURSOS.id"
        datetime fecha_inscripcion
    }
```

## Detalles de las Relaciones
* **Uno a Muchos (Maestros - Cursos):** Un maestro puede impartir varios cursos, pero un curso pertenece a un único maestro. Esto se representa con `maestro_id` como clave foránea en la tabla `CURSOS`.
* **Muchos a Muchos (Alumnos - Cursos):** Un alumno puede inscribirse en varios cursos y un curso puede tener varios alumnos. Esto se logra mediante la tabla intermedia `INSCRIPCIONES`, la cual contiene las claves foráneas `alumno_id` y `curso_id`. Esta tabla también cuenta con una restricción de unicidad (`uq_alumno_curso`) para evitar que un alumno se inscriba dos veces al mismo curso.
