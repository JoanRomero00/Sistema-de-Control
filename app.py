from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)

# pyodbc
con = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=ANDRESPC;"
    "DataBase=Prueba;"
    "Trusted_Connection=yes;"
)

# setings
app.secret_key = "mysecretkey"


@app.route('/')
def index():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM dbo.Persons')
    data = cursor.fetchall()
    cursor.close()
    return render_template("index.html", contacts=data)


@app.route('/index1/<string:maquina>')
def index1(maquina):
    complete = 'SELECT TOP 5 idPieza, PIEZA_DESCRIPCION FROM basePiezas ORDER BY ' \
               'fechaLectura' + maquina + ' DESC'
    cursor = con.cursor()
    cursor.execute(complete)
    data = cursor.fetchall()
    cursor.close()
    cursor = con.cursor()
    cursor.execute('SELECT DISTINCT OP FROM basePiezas ORDER BY OP')
    data2 = cursor.fetchall()
    cursor.close()
    return render_template("index1.html", maquina=maquina, piezas=data, ops=data2)


@app.route('/index2/<string:maquina>')
def index2(maquina):
    complete = 'SELECT TOP 5 idPieza, PIEZA_DESCRIPCION FROM basePiezas ORDER BY ' \
               'fechaLectura' + maquina + ' DESC'
    cursor = con.cursor()
    cursor.execute(complete)
    data = cursor.fetchall()
    cursor.close()
    return render_template("index2.html", maquina=maquina, piezas=data)


@app.route('/index3/<string:maquina>')
def index3(maquina):
    cursor = con.cursor()
    cursor.execute('SELECT * FROM dbo.Persons')
    data = cursor.fetchall()
    cursor.close()
    return render_template("index3.html", maquina=maquina)


@app.route('/escanear_codigo/<string:maq>/<string:templete>', methods=['POST'])
def escanear_codigo(maq, templete):
    if request.method == 'POST':
        codigo = request.form['cod_escaneado']
        complete = 'UPDATE dbo.basePiezas SET fechaLectura' + maq + ' = getdate() WHERE idPieza = ?'
        cursor = con.cursor()
        cursor.execute(complete , codigo)
        cursor.commit()
        cursor.close()
        flash('Codigo escaneado correctamente')
        return redirect(url_for(templete, maquina=maq))


@app.route('/list_op')
def list_op(id):
    maq = id
    cursor = con.cursor()
    cursor.execute('select distinct op from basePiezas')
    cursor.commit()
    cursor.close()
    return redirect(url_for(maq.lower()))
