from flask import Flask
from flask import render_template,request,jsonify
from flask_mysqldb import MySQL
from config import config
from validaciones import *

#Inicializo la aplicacion de flask
app = Flask(__name__, static_folder='static')
#DESDE ACA EMPIEZA LA CONEXION A LA BD
conexion=MySQL(app)

#mysql.init_app(app)
#--------------------------------------



# Ruta de la pagina principal
@app.route('/')
def home():
    return render_template('index.html')
#-------ACA EMPIEZA LA CONEXION API+SQL-----------
#HAY QUE CHEQUEAR ESTO

@app.route('/crud')
def crud():
    return render_template('pages/crud.html')


from flask import render_template

@app.route('/administrar')
def listar_inscriptosv3():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT dni, nombre, apellido, email, curso FROM personasinscriptas ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        print(datos)
        return render_template('pages/crud.html', datos=datos)
    except Exception as ex:
        return f"Error: {str(ex)}"

@app.route('/administrar')
def listar_inscriptosv2():
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT dni, nombre, apellido, email, curso FROM personasinscriptas ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        personas = []
        for fila in datos:
            personasinscriptas = {'dni':fila[0],
                                'nombre':fila[1],
                                'apellido':fila[2],
                                'email':fila[3],
                                'curso':fila[4]
                                }
            personas.append(personasinscriptas)
        return jsonify({'Personas': personas, 'mensaje': "Listado de inscriptos."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


def leer_inscriptoBD(dni):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT dni, nombre, apellido, email, curso FROM personasinscriptas WHERE dni = %s"
        cursor.execute(sql,(dni,))#tupla con un solo valor
        datos = cursor.fetchone()
        if datos != None:
            personas = {'dni':datos[0],
                        'nombre':datos[1],
                        'apellido':datos[2],
                        'email':datos[3],
                        'curso':datos[4]
                        }
            return personas
        else:
            return None
    except Exception as ex:
        raise ex
    
@app.route('/administrar/<dni>',methods=['GET'])
def leer_inscripto(dni):
    try:
        inscripto = leer_inscriptoBD(dni)
        if inscripto != None:
            return jsonify({'inscripto': inscripto, 'mensaje': "Persona encontrada"})
        else:
            return jsonify({'mensaje': "Persona no encontrada."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/administrar',methods=['POST'])
def registrar_persona():
    data = request.json#capturo los datos
    #if(validar_dni(data['dni']) and validar_nombre(data['nombre']) and validar_apellido(data['apellido'])):
    try:
            inscripto = leer_inscriptoBD(data['dni'])
            if inscripto != None:
                return jsonify({'mensaje':"El dni ya existe,no se puede duplicar." }),400
            else: 
                cursor = conexion.connection.cursor()
                sql = "INSERT INTO personasinscriptas (dni, nombre, apellido, email, curso) VALUES (%s,%s,%s,%s,%s)"
                dataInscripto= (data['dni'], data['nombre'], data['apellido'], data['email'], data['curso'])
                cursor.execute(sql,dataInscripto)
                conexion.connection.commit()#confirma la accion de insercion
                return jsonify({'mensaje':"Persona Registrada"}),201
    except Exception as ex:
            return jsonify({'mensaje': "Error"}),500


@app.route('/administrar/<dni>',methods=['PUT'])
def actualizar_inscripto(dni):
    data = request.json#capturo los datos

    try:
            inscripto = leer_inscriptoBD(dni)
            if inscripto != None:
                dataInscripto = (data['nombre'], data['apellido'], data['email'], dni)
                cursor = conexion.connection.cursor()
                sql = """ UPDATE personasinscriptas SET nombre = %s, apellido = %s,email = %s WHERE dni = %s"""
                cursor.execute(sql,dataInscripto)
                conexion.connection.commit()#confrima la actualizacion
                return jsonify({'mensaje': "Persona actualizada."})
            else:
                return jsonify({'mensaje':"Persona no ecnontrada."}),404
    except Exception as ex:
            return jsonify({'mensaje': "ERROR"}),500



@app.route('/administrar/<dni>', methods=['DELETE'])
def eliminar_inscripto(dni):
    try:
        inscripto = leer_inscriptoBD(dni)
        if inscripto is not None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM personasinscriptas WHERE dni = %s"
            cursor.execute(sql, (dni,))
            conexion.connection.commit()
            return jsonify({'mensaje': "Persona eliminada correctamente."}), 200
        else:
            return jsonify({'mensaje': "Persona no encontrada."}), 404
    except Exception as ex:
        return jsonify({'mensaje': "Parametros invalidos...", 'error': str(ex)}), 500



#-------ACA TERMINA LA CONEXION API+SQL-----------


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
#--------------------------------------------------------------
#corre la aplicacion
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()