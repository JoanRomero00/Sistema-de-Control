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
        complete = 'SELECT TOP 5 idOrdenManufactura, PT_PRODUCTO FROM baseModulos ORDER BY ' \
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
    return render_template("index3.html", maquina=maquina, sos=lista_SO(0), clientes=lista_CF(0))


@app.route('/escanear_codigo/<string:maq>/<string:templete>', methods=['POST'])
def escanear_codigo(maq, templete):
    if request.method == 'POST':
        codigo = request.form['cod_escaneado']
        if verificacion(codigo, maq) == 1:
            flash('El codigo ' + codigo + ' ya fue escaneado')
            return redirect(url_for(templete, maquina=maq))
        elif verificacion(codigo, maq) == None:
            flash('Codigo ingresado incorrecto. Intente de nuevo')
            return redirect(url_for(templete, maquina=maq))
        else:
            if maq == "HORNO":
                complete = 'UPDATE dbo.baseModulos SET fechaLecturaHorno = getdate(), lecturaHorno = 1 WHERE idOrdenManufactura = ?'
            else:
                complete = 'UPDATE dbo.basePiezas SET fechaLectura' + maq + ' = getdate(), lectura' + maq + ' = 1 WHERE idPieza = ?'
            cursor = con.cursor()
            cursor.execute(complete, codigo)
            cursor.commit()
            cursor.close()
            return redirect(url_for(templete, maquina=maq))


@app.route('/lectura_masiva/<string:maq>', methods=['POST'])
def lectura_masiva(maq):
    if request.method == 'POST':
        op = request.form['ops']
        color = request.form['colores']
        espesor = request.form['espesores']
        cursor = con.cursor()
        cursor.execute("SELECT idPieza FROM basePiezas WHERE OP=? "
                       "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=?", op, color, espesor)
        records = cursor.fetchall()
        ids = []
        columnNames = [column[0] for column in cursor.description]
        for record in records:
            ids.append(dict(zip(columnNames, record)))
        cursor.close()
        for id in ids:
            complete = 'UPDATE dbo.basePiezas SET fechaLectura' + maq + ' = getdate(), lectura' + maq + ' = 1 WHERE idPieza = ?'
            cursor = con.cursor()
            cursor.execute(complete, id['idPieza'])
            cursor.commit()
            cursor.close()
        flash("Lectura masiva realizada con exito. \n OP: " + op + " | COLOR: " + color + " | ESPESOR: " + espesor)
        return redirect(url_for('index1', maquina=maq))


@app.errorhandler(500)
def access_error(error):
    return render_template('error.html'), 500


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


@app.route("/espesores",methods=["POST","GET"])
def espesores():
    global OutputArray
    if request.method == 'POST':
        op = request.form['op']
        color = request.form['color']
        espesor = request.form['espesor']
        print(espesor + " , " + color + " , " + op )
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(idPieza) as CANTIDAD FROM basePiezas WHERE OP=? "
                       "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=?", op, color, espesor)
        records = cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        cursor.close()
    return jsonify(OutputArray)


@app.route("/buscar_cf", methods=["POST", "GET"])
def buscar_cf():
    if request.method == 'POST':
        op = request.form['op']
        print(op)
        return jsonify(lista_CF(op))


@app.route("/buscar_so", methods=["POST", "GET"])
def buscar_so():
    if request.method == 'POST':
        color = request.form['color']
        print(color)
        return jsonify(lista_SO(color))


"""@app.route("/buscar_cf", methods=["POST", "GET"])
def buscar_cf():
    if request.method == 'POST':
        op = request.form['op']
        print(op)
        return jsonify(lista_SO(op))"""


def verificacion(id, maq):
    if maq == "HORNO":
        complete = "SELECT (CASE WHEN lecturahorno >= 1 THEN 1 ELSE 0 END) as VER FROM baseModulos WHERE idOrdenManufactura=?"
    else:
        complete = "SELECT (CASE WHEN lectura" + maq + " >= 1 THEN 1 ELSE 0 END) FROM basePiezas WHERE idPieza=?"
    cursor = con.cursor()
    cursor.execute(complete, id)
    data = cursor.fetchone()
    print(type(data))
    cursor.close()
    if data is not None:
        data = data[0]
    return data


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

def lista_CF(op):
    cursor = con.cursor()
    if op == 0:
        cursor.execute("SELECT DISTINCT CLIENTE_FINAL FROM baseModulos ORDER BY CLIENTE_FINAL")
    else:
        cursor.execute("SELECT FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP, COUNT(idOrdenManufactura) AS TOTAL, "
                       "SUM(CASE WHEN lecturahorno >= 1 THEN 1 ELSE 0 END) AS TERMINADOS, "
                       "SUM(CASE WHEN (NOT lecturahorno >= 1) OR (lecturaHorno is Null) THEN 1 ELSE 0 END) AS PENDIENTES "
                       "FROM baseModulos GROUP BY FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP "
                       "HAVING   (CLIENTE_FINAL = ?)", op)
    records = cursor.fetchall()
    data = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        data.append(dict(zip(columnNames, record)))
    cursor.close()
    return data

"""def lista_Fr(op):
    cursor = con.cursor()
    if op == 0:
        cursor.execute("SELECT DISTINCT FRANQUICIA FROM baseModulos")
    else:
        cursor.execute("SELECT FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP FROM baseModulos WHERE FRANQUICIA=?", op)
    records = cursor.fetchall()
    data = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        data.append(dict(zip(columnNames, record)))
    cursor.close()
    return data"""

def lista_SO(op):
    cursor = con.cursor()
    if op == 0:
        cursor.execute("SELECT DISTINCT SO FROM baseModulos ORDER BY SO")
    else:
        cursor.execute("SELECT FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP, COUNT(idOrdenManufactura) AS TOTAL, "
                       "SUM(CASE WHEN lecturahorno >= 1 THEN 1 ELSE 0 END) AS TERMINADOS, "
                       "SUM(CASE WHEN (NOT lecturahorno >= 1) OR (lecturaHorno is Null) THEN 1 ELSE 0 END) AS PENDIENTES "
                       "FROM baseModulos GROUP BY FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP "
                       "HAVING   (SO = ?)", op)
    records = cursor.fetchall()
    data = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        data.append(dict(zip(columnNames, record)))
    cursor.close()
    return data