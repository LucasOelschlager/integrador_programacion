from flask import render_template, session, flash, redirect, url_for
from sqlalchemy import text

# ==================== RUTAS DE CURSOS ====================


def registrar_rutas_cursos(app, db):

    @app.route('/cursos')
    def cursos():
        return render_template('cursos/cursos.html')
    
    @app.route('/mis-cursos')
    def mis_cursos():
        if 'user_id' not in session:
            flash('Debes iniciar sesión para ver tus cursos.', 'warning')
            return redirect(url_for('login'))
        
        resultado_usuario = db.session.execute(
            text('SELECT nombre, apellido, email, DNI FROM usuarios WHERE DNI = :dni'), 
            {'dni': session['user_id']}
        )
        usuario = resultado_usuario.fetchone()
        
        if not usuario:
            flash('Usuario no encontrado.', 'error')
            return redirect(url_for('index'))
        
        resultado_cursos = db.session.execute(
            text('''
                SELECT c.id_curso, c.nombre, c.fecha_inicio, c.fecha_finalizacion, c.precio,
                       uc.fecha_inicio as fecha_inscripcion, uc.modalidad, uc.estado_activo
                FROM cursos c
                INNER JOIN usuarios_cursos uc ON c.id_curso = uc.id_curso 
                WHERE uc.dni_usuario = :dni AND uc.estado_activo = 1
            '''), 
            {'dni': session['user_id']}
        )
        cursos = resultado_cursos.fetchall()

        return render_template('cursos/mis_cursos.html', usuario=usuario, cursos=cursos)

    @app.route('/inscripcion')
    def inscripcion():
        return render_template('cursos/inscribirse.html')

    @app.route('/curso-cpp')
    def curso_cpp():
        return render_template('cursos/cursoC++.html')

    @app.route('/curso-net')
    def curso_net():
        return render_template('cursos/cursoNet.html')

    @app.route('/curso-php')
    def curso_php():
        return render_template('cursos/cursoPHP.html')

    @app.route('/curso-python')
    def curso_python():
        return render_template('cursos/cursoPython.html')

    @app.route('/curso-java')
    def curso_java():
        return render_template('cursos/cursoJava.html')

    @app.route('/curso-html')
    def curso_html():
        return render_template('cursos/cursohtml.html')

    @app.route('/curso-css')
    def curso_css():
        return render_template('cursos/cursocss.html')

    @app.route('/curso-js')
    def curso_js():
        return render_template('cursos/cursoJs.html')