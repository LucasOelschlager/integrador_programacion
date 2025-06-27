from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__, static_folder='../static')

#CONFIGURACION DE LA BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lucas1889@localhost/rosario_cursos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/usuarios')
def mostrar_usuarios():
    resultado = db.session.execute(text('SELECT * FROM usuarios'))
    usuarios = resultado.fetchall()
    return str(usuarios)  

@app.route('/') 
def index():
    # return 'Hola, desde FLASK!'
    return render_template('index.html')

@app.route('/contactoForm')
def login():
    return render_template('/contactoForm.html')

@app.route('/registro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            nombre = request.form['name']
            apellido = request.form['apellido']
            email = request.form['email']
            contrasena = request.form['contrasena']
            documento = request.form['documento']
           
            insert_query = text("""
                INSERT INTO usuarios
                VALUES(:DNI, :nombre, :apellido, :email, :contrasena, :fecha_registro, :rol)
            """)
            db.session.execute(insert_query, {
                 'DNI': documento,
                 'nombre': nombre,
                 'apellido': apellido,
                 'email': email,
                 'contrasena': contrasena,
                 'fecha_registro': datetime.now().date(),
                 'rol': 'alumno'
            })
            db.session.commit()
            return "¡Datos recibidos!"
    return render_template('/register.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)