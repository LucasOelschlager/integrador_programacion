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
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_NAME = os.getenv('MYSQL_DB', 'rosario_cursos')

if not DB_PASSWORD:
    raise ValueError(
        "La variable de entorno MYSQL_PASSWORD no está configurada.")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'clave_por_defecto_desarrollo')

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


if __name__ == '__main__':
    app.run(debug=True)
