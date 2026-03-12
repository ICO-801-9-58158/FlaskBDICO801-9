from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms

from models import db, Alumnos, Maestros

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf = CSRFProtect(app)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/usuarios",methods=["GET","POST"])
def usuario():
    mat=0
    nom=''
    apa=''
    ama=''
    edad=0
    email=''
    usuarios_class=forms.UserForm(request.form)  

    if request.method=='POST':  
        mat=usuarios_class.matricula.data  
        nom=usuarios_class.nombre.data  
        apa=usuarios_class.apaterno.data  
        ama=usuarios_class.amaterno.data  
        edad=usuarios_class.edad.data  
        email=usuarios_class.correo.data  

    return render_template('usuarios.html',form=usuarios_class,mat=mat,  
                       nom=nom,apa=apa,ama=ama,edad=edad,email=email)  

@app.route("/maestros",methods=["GET","POST"])
def maestro():
    mat=0
    nom=''
    ape=''
    esp=''
    email=''
    cur=''
    maestros_class=forms.MaestroForm(request.form)  

    if request.method=='POST':  
        mat=maestros_class.matricula.data  
        nom=maestros_class.nombre.data  
        ape=maestros_class.apellidos.data  
        esp=maestros_class.especialidad.data  
        email=maestros_class.email.data  
        cur=maestros_class.cursos.data  

    return render_template('maestros.html',form=maestros_class,mat=mat,  
                       nom=nom,ape=ape,esp=esp,email=email,cur=cur)  

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()