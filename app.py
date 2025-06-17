from flask import Flask
from flask import render_template,request
from flask_mysqldb import MySQL

#Inicializo la aplicacion de flash
app = Flask(__name__, static_folder='static')
#DESDE ACA EMPIEZA LA CONEXION A LA BD
mysql=MySQL()
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'Administrador'
app.config['MYSQL_PASSWORD']= '1234'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_DB']= 'tpi_programacion'
mysql.init_app(app)




# Ruta de la pagina principal
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('pages/contactoForm.html')
#aca hago el formulario para que conecte con la base de datos
@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['nombre']
    _apellido=request.form['apellido']
    _email=request.form['email']
    _consulta=request.form['consulta']
    sql ="INSERT INTO `formcontacto` (`id`, `nombre`, `apellido`, `email`, `consulta`) VALUES (NULL, %s, %s, %s, %s);"
    datos=(_nombre,_apellido,_email,_consulta)
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('index.html')


@app.route('/cursos')
def cursos():
    return render_template('pages/cursos.html')

@app.route('/inscripcion')
def inscripcion():
    return render_template('pages/Inscripcion.html')




@app.route('/curso-cpp')
def curso_cpp():
    return render_template('pages/cursosPages/cursoC++.html')

@app.route('/curso-net')
def curso_net():
    return render_template('pages/cursosPages/cursoNet.html')

@app.route('/curso-php')
def curso_php():
    return render_template('pages/cursosPages/cursoPHP.html')

@app.route('/curso-python')
def curso_python():
    return render_template('pages/cursosPages/cursoPython.html')

@app.route('/curso-java')
def curso_java():
    return render_template('pages/cursosPages/cursoJava.html')

@app.route('/curso-html')
def curso_html():
    return render_template('pages/cursosPages/cursohtml.html')

@app.route('/curso-css')
def curso_css():
    return render_template('pages/cursosPages/cursocss.html')


@app.route('/curso-js')
def curso_js():
    return render_template('pages/cursosPages/cursoJs.html')

#corre la aplicacion
if __name__ == '__main__':
    app.run(debug=True)