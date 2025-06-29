from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
import hashlib
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables de entorno desde el archivo .env

app = Flask(__name__, static_folder='../static')

# CONFIGURACION DE LA BASE DE DATOS
DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_USER = os.getenv('MYSQL_USER', 'root')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'lucas1889')
DB_NAME = os.getenv('MYSQL_DB', 'rosario_cursos')

if not DB_PASSWORD:
    raise ValueError(
        "La variable de entorno MYSQL_PASSWORD no está configurada.")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'lucas1889')

db = SQLAlchemy(app)


def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()


def verificar_contrasena(contrasena, contrasena_hash):
    return hashlib.sha256(contrasena.encode()).hexdigest() == contrasena_hash


@app.route('/usuarios')
def mostrar_usuarios():
    resultado = db.session.execute(text('SELECT * FROM usuarios'))
    usuarios = resultado.fetchall()
    return str(usuarios)


@app.route('/')
def index():
    # return 'Hola, desde FLASK!'
    return render_template('index.html')


@app.route('/contacto')
def contacto():
    return render_template('contactoForm.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']

        # Debug: imprimir datos recibidos
        print(f"Email recibido: {email}")
        print(f"Contraseña recibida: {contrasena}")

        usuario_query = text("SELECT * FROM usuarios WHERE email = :email")
        resultado = db.session.execute(usuario_query, {'email': email})
        usuario = resultado.fetchone()

        # Debug: verificar si encontró el usuario
        if usuario:
            print(f"Usuario encontrado: {usuario.nombre}")
            print(f"Hash en BD: {usuario.contrasena_hash}")
            print(f"Hash generado: {encriptar_contrasena(contrasena)}")
        else:
            print("Usuario no encontrado en la base de datos")

        if usuario and verificar_contrasena(contrasena, usuario.contrasena_hash):
            session['user_id'] = usuario.DNI
            session['user_name'] = usuario.nombre
            session['logged_in'] = True
            flash('¡Bienvenido! Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        flash('Debes iniciar sesión para acceder al dashboard.', 'warning')
        return redirect(url_for('login'))

    return render_template('dashboard.html', user_name=session.get('user_name'))


@app.route('/registro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['name']
        apellido = request.form['apellido']
        email = request.form['email']
        contrasena = request.form['contrasena']
        contrasena_confirm = request.form.get('contrasenaConfirm', '')
        documento = request.form['documento']

        # Debug: imprimir datos recibidos
        print(f"Datos recibidos:")
        print(f"Nombre: {nombre}")
        print(f"Apellido: {apellido}")
        print(f"Email: {email}")
        print(f"Documento: {documento}")
        print(f"Contraseña: {'*' * len(contrasena)}")

        # Validar que las contraseñas coincidan
        if contrasena != contrasena_confirm:
            print("Las contraseñas no coinciden.")
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('register.html')

        print("Las contraseñas coinciden, procediendo con el registro...")
        contrasena_encriptada = encriptar_contrasena(contrasena)
        print(f"Contraseña encriptada: {contrasena_encriptada}")

        insert_query = text("""
            INSERT INTO usuarios (DNI, nombre, apellido, email, contrasena_hash, fecha_registro, rol)
            VALUES(:DNI, :nombre, :apellido, :email, :contrasena_hash, :fecha_registro, :rol)
        """)
        try:
            print("Ejecutando la consulta de inserción...")
            db.session.execute(insert_query, {
                'DNI': documento,
                'nombre': nombre,
                'apellido': apellido,
                'email': email,
                'contrasena_hash': contrasena_encriptada,
                'fecha_registro': datetime.now().date(),
                'rol': 'alumno'
            })
            db.session.commit()
            print("Usuario registrado exitosamente.")
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
            flash(f'Error al registrar el usuario: error')
            db.session.rollback()
    return render_template('register.html')

@app.route('/admin/<int:dni>', methods=['PUT', 'DELETE'])
def crud(dni):
        if request.method == 'PUT':
                data = request.get_json()
                nombre = data.get('nombre')
                apellido = data.get('apellido')
                email = data.get('email')
                try:
                    db.session.execute(
                        text("UPDATE usuarios SET nombre=:nombre, apellido=:apellido, email=:email WHERE DNI=:dni"),
                        {'nombre': nombre, 'apellido': apellido, 'email': email, 'dni': dni}
                    )
                    db.session.commit()
                    return {'mensaje': 'Usuario actualizado correctamente.'}
                except Exception as e:
                    db.session.rollback()
                    return {'mensaje': f'Error al actualizar: {e}'}, 500

        if request.method == 'DELETE':
            try:
                db.session.execute(
                    text("DELETE FROM usuarios WHERE DNI=:dni"),
                    {'dni': dni}
                )
                db.session.commit()
                return {'mensaje': 'Inscripción eliminada correctamente.'}
            except Exception as e:
                db.session.rollback()
                return {'mensaje': f'Error al eliminar: {e}'}, 500
@app.route('/admin')
def admin():
    resultado = db.session.execute(text('SELECT DNI, nombre, apellido, email FROM usuarios'))
    datos = resultado.fetchall()
    return render_template('crud.html', datos=datos)


@app.route('/cursos')
def cursos():
    return render_template('cursos.html')
@app.route('/inscripcion')
def inscripcion():
    return render_template('pages/Inscripcion.html')

@app.route('/curso-cpp')
def curso_cpp():
    return render_template('cursoC++.html')

@app.route('/curso-net')
def curso_net():
    return render_template('cursoNet.html')

@app.route('/curso-php')
def curso_php():
    return render_template('cursoPHP.html')

@app.route('/curso-python')
def curso_python():
    return render_template('cursoPython.html')

@app.route('/curso-java')
def curso_java():
    return render_template('cursoJava.html')

@app.route('/curso-html')
def curso_html():
    return render_template('cursohtml.html')

@app.route('/curso-css')
def curso_css():
    return render_template('cursocss.html')


@app.route('/curso-js')
def curso_js():
    return render_template('cursoJs.html')

if __name__ == '__main__':
    app.run(debug=True)
