from wtforms import form
from wtforms import StringField, IntegerField, EmailField, PasswordField
from wtforms import validators

class UserForm(form):
    nombre = StringField('Nombre')
    apellido_paterno = StringField('Apellido Paterno')
    apellido_materno = StringField('Apellido Materno')
    edad = IntegerField("Edad")
    email = EmailField('Correo')