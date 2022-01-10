from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import pyodbc
import os
import datetime
import logic_subidaModulos
import logic_subidaPiezas
from os import remove
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

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


@app.route('/index1/<string:maquina>/<string:ventana>')
def index1(maquina, ventana):
    hoy = fecha()[:10]
    complete = "SELECT TOP 8 idPieza, PIEZA_DESCRIPCION FROM basePiezas " \
              "where CONVERT (DATE, fechaLectura" + maquina + ") = ? ORDER BY fechaLectura" + maquina + " DESC"
    cursor = con.cursor()
    cursor.execute(complete, hoy)
    data = cursor.fetchall()
    cursor.close()
    list = []
    for o in lista_op(maquina):
        list.append(o['OP'])
    if ventana == "1":
        display1=""
        display2="display:None;"
        return render_template("index1.html", maquina=maquina, display1=display1, display2=display2, piezas=data,
                               ops=list)
    elif ventana == "2":
        display1="display:None;"
        display2=""
        return render_template("index1.html", maquina=maquina, display1=display1, display2=display2, piezas=data,
                               ops=list)


@app.route('/index2/<string:maquina>')
def index2(maquina):
    hoy = fecha()[:10]
    if maquina == "HORNO":
        complete = 'SELECT TOP 8 idOrdenManufactura, PT_PRODUCTO FROM baseModulos ' \
                   'where CONVERT (DATE, fechaLecturaHORNO) = ? ORDER BY fechaLecturaHorno DESC'
    else:
        complete = "SELECT TOP 8 idPieza, PIEZA_DESCRIPCION FROM basePiezas " \
                   "where CONVERT (DATE, fechaLectura" + maquina + ") = ? ORDER BY fechaLectura" + maquina + " DESC"
    cursor = con.cursor()
    cursor.execute(complete, hoy)
    data = cursor.fetchall()
    cursor.close()
    return render_template("index2.html", maquina=maquina, piezas=data)


@app.route('/index3/<string:maquina>')
def index3(maquina):
    return render_template("index3.html", maquina=maquina, sos=lista_SO(0), clientes=lista_CF(0))


@app.route('/index4/<string:ventana>')
def index4(ventana):
    list = []
    for o in lista_op2():
        list.append(o['OP'])
    if ventana == "1":
        display1 = ""
        display2 = "display:none;"
        return render_template("index4.html", ops=list, display1=display1, display2=display2)
    elif ventana == "2":
        display1 = "display:none;"
        display2 = ""
        return render_template("index4.html", ops=list, display1=display1, display2=display2)


@app.route('/planos/<string:plano>')
def planos(plano):
    return render_template("planos.html", plano=plano, produccion=produccion_diaria())


@app.route('/buscar_plano/<string:plano>')
def buscar_plano(plano):
    if plano == "0":
        return "BUSCAR PLANO"
    if len(plano) > 12:
        aux = "/" + plano[:3]
        path = 'E:\COMPARTIDOS\Ing de Producto\Productos - VISTAS Y PLANOS\Desenhos' + aux + '/' + plano + '.pdf'
        if os.path.isfile(path):
            return send_from_directory('E:\COMPARTIDOS\Ing de Producto\Productos - VISTAS Y PLANOS\Desenhos' + aux, plano + '.pdf')
        else:
            return "PLANO NO ENCONTRADO"
    else:
        path = 'E:\COMPARTIDOS\Ing de Producto\Productos - VISTAS Y PLANOS\Desenhos' + '/' + plano + '.pdf'
        if os.path.isfile(path):
            return send_from_directory('E:\COMPARTIDOS\Ing de Producto\Productos - VISTAS Y PLANOS\Desenhos', plano + '.pdf')
        else:
            return "PLANO NO ENCONTRADO"



@app.route('/leer_plano', methods=['POST'])
def leer_plano():
    if request.method == 'POST':
        plano = request.form['plano']
        return redirect(url_for('planos', plano=plano))



@app.route('/baja_archivo', methods=['POST'])
def baja_archivo():
    if request.method == 'POST':
        tipo = request.form['tipo']
        op = request.form['op']
        if tipo == 'baseModulos':
            elimar_Modulos(op)
            flash('DatosMODULOS borrados correctamente')
            return redirect(url_for('index4', ventana=2))
        elif tipo == 'basePiezas':
            elimar_Piezas(op)
            flash('DatosPIEZAS borrados correctamente')
            return redirect(url_for('index4', ventana=2))
        elif tipo == 'Ambas':
            elimar_Modulos(op)
            elimar_Piezas(op)
            flash('DatosPIEZAS y DatosMODULOS borrados correctamente')
            return redirect(url_for('index4', ventana=2))


@app.route('/subir_archivo', methods=['POST'])
def subir_archivo():
    if request.method == 'POST':
        try:
            tipo = request.form['tipo_subida']
            archivo = request.files['archivo']
            filename = secure_filename(archivo.filename)
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if tipo == 'baseModulos':
                logic_subidaModulos.cargar_archivo(archivo.filename)
                flash('DatosMODULOS subidos correctamente')
                return redirect(url_for('index4', ventana=1))
            elif tipo == 'basePiezas':
                logic_subidaPiezas.cargar_archivo(archivo.filename)
                flash('DatosPIEZAS subidos correctamente')
                return redirect(url_for('index4', ventana=1))
        except PermissionError:
            flash("Error: No se a cargado ningun archivo", 'danger')
            return redirect(url_for('index4', ventana=1))
        except KeyError:
            archivo = request.files['archivo']
            remove(archivo.filename)
            flash("Error: Archivo equivocado", 'danger')
            return redirect(url_for('index4', ventana=1))





@app.route('/escanear_codigo/<string:maq>/<string:templete>', methods=['POST'])
def escanear_codigo(maq, templete):
    if request.method == 'POST':
        codigo = request.form['cod_escaneado']
        try:
            if verificacion(codigo, maq) == 1:
                flash('El codigo ' + codigo + ' ya fue escaneado')
                if templete == "index1":
                    return redirect(url_for(templete, maquina=maq, ventana="1"))
                return redirect(url_for(templete, maquina=maq))
            elif verificacion(codigo, maq) == None:
                flash('El codigo ingresado no existe.')
                if templete == "index1":
                    return redirect(url_for(templete, maquina=maq, ventana="1"))
                return redirect(url_for(templete, maquina=maq))
            else:
                if maq == "HORNO":
                    complete = 'UPDATE dbo.baseModulos SET fechaLecturaHorno = ?, lecturaHorno = 1 WHERE idOrdenManufactura = ?'
                else:
                    complete = 'UPDATE dbo.basePiezas SET fechaLectura' + maq + ' = ?, lectura' + maq + ' = 1 WHERE idPieza = ?'
                cursor = con.cursor()
                cursor.execute(complete, fecha(),codigo)
                cursor.commit()
                cursor.close()
                if templete == "index1":
                    return redirect(url_for(templete, maquina=maq, ventana="1"))
                return redirect(url_for(templete, maquina=maq))
        except pyodbc.DataError:
            flash("Error: el codigo ingresado es incorrecto. Intente nuevamente")
            if templete == "index1":
                return redirect(url_for(templete, maquina=maq, ventana="1"))
            return redirect(url_for(templete, maquina=maq))


@app.route('/lectura_masiva/<string:maq>', methods=['POST'])
def lectura_masiva(maq):
    try:
        if request.method == 'POST':
            op = request.form['ops']
            color = request.form['colores']
            espesor = request.form['espesores']
            if color == 'Color':
                flash("Error: Por favor ingrese todos los campos", 'danger')
                return redirect(url_for('index1', maquina=maq, ventana=2))

            cursor = con.cursor()
            complete = "SELECT idPieza FROM basePiezas WHERE OP=? " \
                       "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=? AND lectura" + maq + " = 0"
            cursor.execute(complete, op, color, espesor)
            records = cursor.fetchall()
            if records == []:
                flash("Esta lectura masiva ya se a realizado. OP: " + op + " | COLOR: " + color + " | ESPESOR: " + espesor, 'warning')
                return redirect(url_for('index1', maquina=maq, ventana=2))

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
            return redirect(url_for('index1', maquina=maq, ventana=2))
    except pyodbc.DataError:
        flash("Error: Por favor ingrese todos los campos", 'danger')
        return redirect(url_for('index1', maquina=maq, ventana=2))


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


@app.route("/limpiar_so", methods=["POST", "GET"])
def limpiar_cf():
    if request.method == 'POST':
        return jsonify(lista_SO(0))


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


def lista_op(maquina):
    cursor = con.cursor()
    cursor.execute('SELECT DISTINCT OP FROM basePiezas WHERE lectura' + maquina + ' = 0 ORDER BY OP')
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

def elimar_Modulos(op):
    cursor = con.cursor()
    cursor.execute("DELETE FROM baseModulos WHERE OP = ?", op)
    cursor.commit()
    cursor.close()

def elimar_Piezas(op):
    cursor = con.cursor()
    cursor.execute("DELETE FROM basePiezas WHERE OP = ?", op)
    cursor.commit()
    cursor.close()


def lista_op2():
    cursor = con.cursor()
    cursor.execute('(SELECT DISTINCT OP FROM basePiezas) UNION (SELECT DISTINCT OP FROM baseModulos) ORDER BY OP')
    records = cursor.fetchall()
    OutputArray = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        OutputArray.append(dict(zip(columnNames, record)))
    cursor.close()
    return OutputArray

def produccion_diaria():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM ProduccionDiariaModulosTablero')
    records = cursor.fetchall()
    OutputArray = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        OutputArray.append(dict(zip(columnNames, record)))
    cursor.close()
    return OutputArray


def fecha():
    today = datetime.datetime.now()
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    return fecha

def comparar_fecha(fecha):
    if fecha == fecha():
        return True
    else:
        return False

