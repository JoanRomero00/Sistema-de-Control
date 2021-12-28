from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
    return render_template("index.html")


@app.route('/index1/<string:maquina>')
def index1(maquina):
    complete = 'SELECT TOP 5 idPieza, PIEZA_DESCRIPCION FROM basePiezas ORDER BY ' \
               'fechaLectura' + maquina + ' DESC'
    cursor = con.cursor()
    cursor.execute(complete)
    data = cursor.fetchall()
    cursor.close()
    list = []
    for o in lista_op():
        list.append(o['OP'])
    return render_template("index1.html", maquina=maquina, piezas=data, ops=list)


@app.route('/index2/<string:maquina>')
def index2(maquina):
    if maquina == "HORNO":
        complete = 'SELECT TOP 5 idOrdenManufactura, SO FROM baseModulos ORDER BY ' \
                   'fechaLecturaHorno DESC'
    else:
        complete = 'SELECT TOP 5 idPieza, PIEZA_DESCRIPCION FROM basePiezas ORDER BY ' \
                'fechaLectura' + maquina + ' DESC'
    cursor = con.cursor()
    cursor.execute(complete)
    data = cursor.fetchall()
    cursor.close()
    return render_template("index2.html", maquina=maquina, piezas=data)


@app.route('/index3/<string:maquina>')
def index3(maquina):
    return render_template("index3.html", maquina=maquina)


@app.route('/escanear_codigo/<string:maq>/<string:templete>', methods=['POST'])
def escanear_codigo(maq, templete):
    if request.method == 'POST':
        codigo = request.form['cod_escaneado']
        if verificacion(codigo, maq) == '' or verificacion(codigo, maq) is None:
            if maq == "HORNO":
                complete = 'UPDATE dbo.baseModulos SET fechaLecturaHorno = getdate() WHERE idOrdenManufactura = ?'
            else:
                complete = 'UPDATE dbo.basePiezas SET fechaLectura' + maq + ' = getdate() WHERE idPieza = ?'
            cursor = con.cursor()
            cursor.execute(complete, codigo)
            cursor.commit()
            cursor.close()
            return redirect(url_for(templete, maquina=maq))
        else:
            flash('El codigo ' + codigo + ' ya fue escaneado')
            return redirect(url_for(templete, maquina=maq))


@app.route("/ops", methods=["POST", "GET"])
def ops():
    global OutputArray
    if request.method == 'POST':
        op = request.form['op']
        print(op)
        OutputArray = lista_colores(op)
    return jsonify(OutputArray)


@app.route("/colores",methods=["POST","GET"])
def colores():
    global OutputArray
    if request.method == 'POST':
        color = request.form['color']
        op = request.form['op']
        print(color)
        OutputArray = lista_espesores(color,op)
    return jsonify(OutputArray)


def verificacion(id, maq):
    if maq == "HORNO":
        complete = "SELECT fechaLecturaHorno FROM baseModulos WHERE idOrdenManufactura=?"
    else:
        complete = "SELECT fechaLectura" + maq + " FROM basePiezas WHERE idPieza=?"
    cursor = con.cursor()
    cursor.execute(complete, id)
    data = cursor.fetchone()
    cursor.close()
    return data[0]


def lista_op():
    cursor = con.cursor()
    cursor.execute('SELECT DISTINCT OP FROM basePiezas ORDER BY OP')
    records = cursor.fetchall()
    OutputArray = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        OutputArray.append(dict(zip(columnNames, record)))
    cursor.close()
    return OutputArray


def lista_colores(op):
    cursor = con.cursor()
    cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR FROM basePiezas WHERE OP=? ORDER BY OP", op)
    records = cursor.fetchall()
    OutputArray = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        OutputArray.append(dict(zip(columnNames, record)))
    cursor.close()
    return OutputArray


def lista_espesores(color, op):
    cursor = con.cursor()
    cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR, PIEZA_PROFUNDO FROM basePiezas WHERE OP=? "
                   "AND PIEZA_NOMBRECOLOR=? ORDER BY OP", op, color)
    records = cursor.fetchall()
    OutputArray = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        OutputArray.append(dict(zip(columnNames, record)))
    cursor.close()
    return OutputArray
