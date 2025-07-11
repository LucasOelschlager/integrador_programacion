from routes.cursos_rutas import registrar_rutas_cursos
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
import hashlib
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='../static')


if os.path.exists('.env'):
    load_dotenv()


is_production = os.getenv('VERCEL') == '1'

if is_production:
    DB_HOST = os.getenv('MYSQL_HOST')
    DB_USER = os.getenv('MYSQL_USER')
    DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
    DB_NAME = os.getenv('MYSQL_DB')
    DB_PORT = os.getenv('MYSQL_PORT', '3306')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
else:
    DB_HOST = os.getenv('MYSQL_HOST_LOCAL', 'localhost')
    DB_USER = os.getenv('MYSQL_USER_LOCAL', 'root')
    DB_PASSWORD = os.getenv('MYSQL_PASSWORD_LOCAL')
    DB_NAME = os.getenv('MYSQL_DB_LOCAL', 'rosario_cursos')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')


db = SQLAlchemy(app)


def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()


def verificar_contrasena(contrasena, contrasena_hash):
    return hashlib.sha256(contrasena.encode()).hexdigest() == contrasena_hash


registrar_rutas_cursos(app, db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacto')
def contacto():
    return render_template('contactoForm.html')


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
        documento = request.form['documento']
        dni_check = db.session.execute(text(
            "SELECT COUNT(*) as count FROM usuarios WHERE DNI = :dni"), {'dni': documento})
        dni_existe = dni_check.fetchone().count > 0

        if dni_existe:
            flash(
                f'❌ Error: El DNI {documento} ya está registrado en el sistema. Si ya tienes cuenta, inicia sesión.', 'error')
            return render_template('register.html')
        email_check = db.session.execute(text(
            "SELECT COUNT(*) as count FROM usuarios WHERE email = :email"), {'email': email})
        email_existe = email_check.fetchone().count > 0
        if email_existe:
            flash(
                f'❌ Error: El email {email} ya está registrado. Si ya tienes cuenta, inicia sesión.', 'error')
            return render_template('register.html')
        contrasena_encriptada = encriptar_contrasena(contrasena)
        try:
            db.session.execute(text("""
                INSERT INTO usuarios (DNI, nombre, apellido, email, contrasena_hash, fecha_registro, rol)
                VALUES(:DNI, :nombre, :apellido, :email, :contrasena_hash, :fecha_registro, :rol)
            """), {
                'DNI': documento,
                'nombre': nombre,
                'apellido': apellido,
                'email': email,
                'contrasena_hash': contrasena_encriptada,
                'fecha_registro': datetime.now().date(),
                'rol': 'alumno'
            })
            db.session.commit()
            flash('✅ ¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(
                '❌ Error inesperado al registrar. Por favor, intenta nuevamente.', 'error')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']
        usuario_query = text("SELECT * FROM usuarios WHERE email = :email")
        resultado = db.session.execute(usuario_query, {'email': email})
        usuario = resultado.fetchone()
        if not usuario:
            flash(
                'Este email no está registrado en el sistema. Por favor, regístrate primero.', 'error')
            return render_template('login.html')
        if verificar_contrasena(contrasena, usuario.contrasena_hash):
            session['user_id'] = usuario.DNI
            session['user_name'] = usuario.nombre
            session['user_email'] = usuario.email
            session['user_rol'] = usuario.rol
            session['logged_in'] = True
            flash(f'¡Bienvenido, {usuario.nombre}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(
                'Email o contraseña incorrectos. Por favor, inténtalo de nuevo.', 'error')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/<int:id_curso>/<int:dni>', methods=['PUT', 'DELETE'])
def crud_inscripcion(id_curso, dni):
    if request.method == 'PUT':
        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        email = data.get('email')
        try:
            db.session.execute(
                text(
                    "UPDATE usuarios SET nombre=:nombre, apellido=:apellido, email=:email WHERE DNI=:dni"),
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
                text(
                    "DELETE FROM usuarios_cursos WHERE id_curso=:id_curso AND dni_usuario=:dni"),
                {'id_curso': id_curso, 'dni': dni}
            )
            db.session.commit()
            return {'mensaje': 'Inscripción eliminada correctamente.'}
        except Exception as e:
            db.session.rollback()
            return {'mensaje': f'Error al eliminar: {e}'}, 500


@app.route('/admin')
def admin():
    resultado = db.session.execute(text('''
        SELECT uc.id_curso, uc.dni_usuario, u.nombre, u.apellido, u.email, c.nombre AS curso
        FROM usuarios_cursos uc
        JOIN usuarios u ON uc.dni_usuario = u.DNI
        JOIN cursos c ON uc.id_curso = c.id_curso
    '''))
    datos = resultado.fetchall()
    return render_template('admin/crud.html', datos=datos)


@app.route('/inscribirse/<int:id>', methods=['GET', 'POST'])
def inscribirse(id):
    resultado = db.session.execute(
        text('SELECT * FROM cursos WHERE id_curso = :id'), {'id': id})
    curso = resultado.fetchone()
    if not curso:
        return "Curso no encontrado", 404

    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Debes iniciar sesión para inscribirte.', 'warning')
            return redirect(url_for('login'))
        dni_usuario = session['user_id']

        existe = db.session.execute(
            text("SELECT 1 FROM usuarios_cursos WHERE id_curso = :id_curso AND dni_usuario = :dni_usuario"),
            {'id_curso': id, 'dni_usuario': dni_usuario}
        ).fetchone()
        if existe:
            flash('Ya estás inscripto en este curso.', 'warning')
            return redirect(url_for('dashboard'))

        fecha_inicio = datetime.now().date()
        modalidad = "Online"
        estado_activo = 1

        try:
            db.session.execute(
                text("""
                    INSERT INTO usuarios_cursos (id_curso, dni_usuario, fecha_inicio, modalidad, estado_activo)
                    VALUES (:id_curso, :dni_usuario, :fecha_inicio, :modalidad, :estado_activo)
                """),
                {
                    'id_curso': id,
                    'dni_usuario': dni_usuario,
                    'fecha_inicio': fecha_inicio,
                    'modalidad': modalidad,
                    'estado_activo': estado_activo
                }
            )
            db.session.commit()
            flash('✅ Inscripción realizada con éxito.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error al inscribirse: {e}', 'error')
            return redirect(url_for('inscribirse', id=id))

    return render_template('cursos/inscribirse.html', curso=curso)


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/mi_perfil')
def mi_perfil():

    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a tu perfil.', 'warning')
        return redirect(url_for('login'))

    resultado = db.session.execute(text(
        'SELECT nombre, apellido, email, DNI, fecha_registro FROM usuarios WHERE DNI = :dni'), {'dni': session['user_id']})

    usuario = resultado.fetchone()
    if not usuario:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('index'))

    return render_template('mi_perfil.html', usuario=usuario)


@app.route('/usuarios')
def mostrar_usuarios():
    resultado = db.session.execute(text('SELECT * FROM usuarios'))
    usuarios = resultado.fetchall()
    return str(usuarios)


@app.route('/sobreNosotros')
def sobreNosotros():
    return render_template('sobrenosotros.html')


if __name__ == '__main__':
    app.run(debug=True)
