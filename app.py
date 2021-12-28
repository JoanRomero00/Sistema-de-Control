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


@app.route("/carbrand",methods=["POST","GET"])
def carbrand():
    if request.method == 'POST':
        category_id = request.form['category_id']
        print(category_id)
        OutputArray = lista_colores(category_id)
    return jsonify(OutputArray)


@app.route("/carcolor",methods=["POST","GET"])
def carcolor():
    if request.method == 'POST':
        color = request.form['color']
        #color = request.form['color']
        print(color)
        OutputArray = lista_espesores(color)#, color)
    return jsonify(OutputArray)

"""
@app.route("/carbrand",methods=["POST","GET"])
def carbrand():
    if request.method == 'POST':
        category_id = request.form['category_id']
        print(category_id)
        type = request.form['type']
        if type == 'carColordata':
            OutputArray = lista_colores(category_id)
        else:
            OutputArray = lista_espesores(category_id)
    return jsonify(OutputArray)
"""
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
    """data = []
    cursor = con.cursor()
    cursor.execute('SELECT DISTINCT OP FROM basePiezas ORDER BY OP')
    for row in cursor:
        indice = str(row).index(",")
        row2 = str(row)[2:indice - 1]
        row3 = row2.replace(" ", "-")
        data.append(row3)
    cursor.close()
    return data"""
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
    """data = []
    cursor = con.cursor()
    cursor.execute('SELECT DISTINCT PIEZA_NOMBRECOLOR FROM basePiezas WHERE OP=? ORDER BY PIEZA_NOMBRECOLOR')
    for row in cursor:
        indice = str(row).index(",")
        row2 = str(row)[2:indice-1]
        row3 = row2.replace(" ", "-")
        data.append(row3)
    cursor.close()
    return data """
    cursor = con.cursor()
    cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR FROM basePiezas WHERE OP=? ORDER BY OP", op)
    records = cursor.fetchall()
    OutputArray = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        OutputArray.append(dict(zip(columnNames, record)))
    cursor.close()
    return OutputArray

def lista_espesores(color):
    """data = []
    cursor = con.cursor()
    cursor.execute('SELECT DISTINCT OP, PIEZA_PROFUNDO WHERE OP=? FROM basePiezas ORDER BY OP', op)
    for row in cursor:
        indice = str(row).index(",")
        row2 = str(row)[1:indice]
        data.append(row2)
    cursor.close()
    return data"""
    cursor = con.cursor()
    #cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR, PIEZA_PROFUNDO FROM basePiezas WHERE OP=? AND"
                   #" PIEZA_NOMBRECOLOR=? ORDER BY OP", op, color)
    cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR, PIEZA_PROFUNDO FROM basePiezas WHERE OP=? "
                   "ORDER BY OP", color)
    records = cursor.fetchall()
    OutputArray = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        OutputArray.append(dict(zip(columnNames, record)))
    cursor.close()
    return OutputArray


