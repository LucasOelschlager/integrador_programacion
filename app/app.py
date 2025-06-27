from flask import Flask, render_template

app = Flask(__name__, static_folder='../static')

@app.route('/') 
def index():
    # return 'Hola, desde FLASK!'
    return render_template('index.html')

@app.route('/contactoForm')
def login():
    return render_template('/contactoForm.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)