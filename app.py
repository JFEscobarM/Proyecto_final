from flask import Flask,  render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL,MySQLdb 
from os import path 
from notifypy import Notify


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyecto_p'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("contenido.html")    

@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("contenido.html")


@app.route('/login', methods= ["GET", "POST"])
def login():

    notificacion = Notify()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if user!=None:
            if password == user["password"]:
                session['name'] = user['name']
                session['email'] = user['email']
                session['tipo'] = user['id_tip_usu']

                if session['tipo'] == 1:
                    return render_template("docente/home.html")
                elif session['tipo'] == 2:
                    return render_template("estudiante/homeTwo.html")


            else:
                notificacion.title = "Error de Acceso"
                notificacion.message="Correo y/o contraseña incorrectos"
                notificacion.send()
                return render_template("login.html")
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="El usuario no se encuentra registrado"
            notificacion.send()
            return render_template("login.html")
    else:
        return render_template("login.html")



@app.route('/registro', methods = ["GET", "POST"])
def registro():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tip_usu")
    tipo = cur.fetchall()

    notificacion = Notify()
    

    if request.method == 'GET':
        return render_template("registro.html", tipo = tipo)
    
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        tip = request.form['tipo']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, id_tip_usu) VALUES (%s,%s,%s,%s)", (name, email, password,tip,))
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message="Ya se encuentra registrado, por favor inicie sesión para ingresar a la plataforma"
        notificacion.send()
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = "sllave"
    app.run(debug=True)