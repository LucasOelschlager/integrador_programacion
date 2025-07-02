from flask import render_template

# ==================== RUTAS DE CURSOS ====================


def registrar_rutas_cursos(app):

    @app.route('/cursos')
    def cursos():
        return render_template('cursos/cursos.html')

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