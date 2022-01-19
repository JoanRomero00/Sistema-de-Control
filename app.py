from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import pyodbc
import os
from os import remove
from werkzeug.utils import secure_filename
from dataBase.control import Control
from dataBase.lecturaMasiva import LecturaMasiva
from dataBase.despacho import Despacho
from dataBase.AB_ModulosPiezas import ABM
from dataBase.plano import Plano

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

# setings
app.secret_key = "mysecretkey"


# HOME
@app.route('/')
def index():
    return render_template("index.html")


# Escanear codigo y lectura mavisa de piezas
@app.route('/index1/<string:maquina>/<string:ventana>')
def index1(maquina, ventana):
    piezas = Control()
    ops = LecturaMasiva()
    if ventana == "1":
        display1 = ""
        display2 = "display:None;"
        return render_template("index1.html", maquina=maquina, display1=display1, display2=display2,
                               piezas=piezas.getTabla(maquina), ops=ops.lista_ops(maquina))
    elif ventana == "2":
        display1 = "display:None;"
        display2 = ""
        return render_template("index1.html", maquina=maquina, display1=display1, display2=display2,
                               piezas=piezas.getTabla(maquina), ops=ops.lista_ops(maquina))


@app.route('/index2/<string:maquina>')
def index2(maquina):
    piezas = Control()
    return render_template("index2.html", maquina=maquina, piezas=piezas.getTabla(maquina))


@app.route('/escanear_codigo/<string:maq>/<string:templete>', methods=['POST'])
def escanear_codigo(maq, templete):
    if request.method == 'POST':
        codigo = request.form['cod_escaneado']
        try:
            ver1 = Control()
            ver2 = Control()
            if ver1.verificar_cod(codigo, maq) == 1:
                flash('El codigo ' + codigo + ' ya fue escaneado')
                if templete == "index1":
                    return redirect(url_for(templete, maquina=maq, ventana="1"))
                return redirect(url_for(templete, maquina=maq))
            elif ver2.verificar_cod(codigo, maq) is None:
                flash('El codigo ingresado no existe.')
                if templete == "index1":
                    return redirect(url_for(templete, maquina=maq, ventana="1"))
                return redirect(url_for(templete, maquina=maq))
            else:
                update = Control()
                update.updatePM(codigo, maq)
                if templete == "index1":
                    return redirect(url_for(templete, maquina=maq, ventana="1"))
                return redirect(url_for(templete, maquina=maq))
        except pyodbc.DataError:
            flash("Error: el codigo ingresado es incorrecto. Intente nuevamente")
            if templete == "index1":
                return redirect(url_for(templete, maquina=maq, ventana="1"))
            return redirect(url_for(templete, maquina=maq))


@app.route("/ops", methods=["POST", "GET"])
def ops():
    global OutputArray
    if request.method == 'POST':
        op = request.form['op']
        print(op)
        colores = LecturaMasiva()
        OutputArray = colores.lista_colores(op)
    return jsonify(OutputArray)


@app.route("/colores", methods=["POST", "GET"])
def colores():
    global OutputArray
    if request.method == 'POST':
        color = request.form['color']
        op = request.form['op']
        print(color)
        espesores = LecturaMasiva()
        OutputArray = espesores.lista_espesores(color, op)
    return jsonify(OutputArray)


@app.route("/espesores", methods=["POST", "GET"])
def espesores():
    global piezas
    if request.method == 'POST':
        op = request.form['op']
        color = request.form['color']
        espesor = request.form['espesor']
        print(espesor)
        lectura = LecturaMasiva()
        piezas = lectura.lista_piezas(op, color, espesor)
        print(piezas)
    return jsonify(piezas)


@app.route("/piezas", methods=["POST", "GET"])
def piezas():
    global cantidad
    if request.method == 'POST':
        op = request.form['op']
        color = request.form['color']
        espesor = request.form['espesor']
        pieza = request.form['pieza']
        print(espesor + " , " + color + " , " + op + " , " + pieza)
        lectura = LecturaMasiva()
        cantidad = lectura.calcular_cant(op, color, espesor, pieza)
    return jsonify(cantidad)


@app.route('/lectura_masiva/<string:maq>', methods=['POST'])
def lectura_masiva(maq):
    try:
        if request.method == 'POST':
            pin = request.form['pin']
            log = LecturaMasiva()
            usuario = log.verificar_pin(pin)
            if usuario is None:
                flash("Error: el PIN ingresado es incorrecto", 'danger')
                return redirect(url_for('index1', maquina=maq, ventana=2))
            op = request.form['ops']
            color = request.form['colores']
            espesor = request.form['espesores']
            pieza = request.form['piezas']
            if color == 'Color' or pieza == 'Pieza':
                flash("Error: Por favor ingrese todos los campos", 'danger')
                return redirect(url_for('index1', maquina=maq, ventana=2))
            lectura1 = LecturaMasiva()
            piezas = lectura1.verificar_lectura(op, color, espesor, pieza, maq)
            if piezas == 1:
                flash("Esta lectura masiva ya se a realizado. OP: " + op + " "
                      "| COLOR: " + color + " | ESPESOR: " + espesor + " | PIEZA: " + pieza, 'warning')
                return redirect(url_for('index1', maquina=maq, ventana=2))
            lectura2 = LecturaMasiva()
            lectura2.updateMasivo(piezas, maq)
            log2 = LecturaMasiva()
            log2.log_lecturaMasiva(usuario, op, color, espesor, maq, pieza)
            flash("Lectura masiva realizada con exito. \n OP: " + op + " | COLOR: " + color + " | ESPESOR: " + espesor
                  + " | PIEZA: " + pieza)
            return redirect(url_for('index1', maquina=maq, ventana=2))
    except pyodbc.DataError:
        flash("Error: Por favor ingrese todos los campos", 'danger')
        return redirect(url_for('index1', maquina=maq, ventana=2))


# DESPACHO
@app.route('/index3/<string:maquina>')
def index3(maquina):
    sos = Despacho()
    clientes = Despacho()
    return render_template("index3.html", maquina=maquina, sos=sos.lista_so(0), clientes=clientes.lista_cf(0))


@app.route("/buscar_cf", methods=["POST", "GET"])
def buscar_cf():
    if request.method == 'POST':
        cf = request.form['op']
        print(cf)
        despacho = Despacho()
        return jsonify(despacho.lista_cf(cf))


@app.route("/buscar_so", methods=["POST", "GET"])
def buscar_so():
    if request.method == 'POST':
        so = request.form['color']
        print(so)
        despacho = Despacho()
        return jsonify(despacho.lista_so(so))


# Alta y Baja de Piezas/Modulos
@app.route('/AB_ModulosPiezas/<string:ventana>')
def index4(ventana):
    ops = ABM()
    if ventana == "1":
        display1 = ""
        display2 = "display:none;"
        return render_template("index4.html", ops=ops.lista_op(), display1=display1, display2=display2)
    elif ventana == "2":
        display1 = "display:none;"
        display2 = ""
        return render_template("index4.html", ops=ops.lista_op(), display1=display1, display2=display2)


@app.route('/subir_archivo', methods=['POST'])
def subir_archivo():
    if request.method == 'POST':
        try:
            tipo = request.form['tipo_subida']
            archivo = request.files['archivo']
            filename = secure_filename(archivo.filename)
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if tipo == 'baseModulos':
                Alta = ABM()
                Alta.Alta_Modulos(archivo.filename)
                flash('Los MODULOS se han subido correctamente')
                return redirect(url_for('index4', ventana=1))
            elif tipo == 'basePiezas':
                Alta = ABM()
                Alta.Alta_Piezas(archivo.filename)
                flash('Las PIEZAS se han subido correctamente')
                return redirect(url_for('index4', ventana=1))
        except PermissionError:
            flash("Error: No se a cargado ningun archivo", 'danger')
            return redirect(url_for('index4', ventana=1))
        except KeyError:
            archivo = request.files['archivo']
            remove(archivo.filename)
            flash("Error: Archivo equivocado, no cumple con el formato establecido", 'danger')
            return redirect(url_for('index4', ventana=1))


@app.route('/baja_archivo', methods=['POST'])
def baja_archivo():
    if request.method == 'POST':
        tipo = request.form['tipo']
        op = request.form['op']
        print("BAJA: " + op)
        if tipo == 'baseModulos':
            delete = ABM()
            delete.elimar_Modulos(op)
            flash('Los MODULOS se han borrado correctamente')
            return redirect(url_for('index4', ventana=2))
        elif tipo == 'basePiezas':
            delete = ABM()
            delete.elimar_Piezas(op)
            flash('Las PIEZAS se han borrado correctamente')
            return redirect(url_for('index4', ventana=2))
        elif tipo == 'Ambas':
            delete1 = ABM()
            delete2 = ABM()
            delete1.elimar_Modulos(op)
            delete2.elimar_Piezas(op)
            flash('PIEZAS y MODULOS se han borrado correctamente')
            return redirect(url_for('index4', ventana=2))


# Planos
@app.route('/planos/<string:plano>')
def planos(plano):
    planos = Plano()
    return render_template("planos.html", plano=plano, produccion=planos.produccion_diaria())


@app.route('/leer_plano', methods=['POST'])
def leer_plano():
    if request.method == 'POST':
        plano = request.form['plano']
        return redirect(url_for('planos', plano=plano))


@app.route('/buscar_plano/<string:plano>')
def buscar_plano(plano):
    if plano == "0":
        return "BUSCAR PLANO"
    if len(plano) > 12:
        aux = "/" + plano[:3]
        path = 'E:\COMPARTIDOS\Ing de Producto\Productos - VISTAS Y PLANOS\Desenhos' + aux + '/' + plano + '.pdf'
        if os.path.isfile(path):
            return send_from_directory('E:\COMPARTIDOS\Ing de Producto\Productos - VISTAS Y PLANOS\Desenhos' + aux,
                                       plano + '.pdf')
        else:
            return "PLANO NO ENCONTRADO"
    else:
        path = 'E:\COMPARTIDOS\Ing de Producto\Productos - VISTAS Y PLANOS\Desenhos' + '/' + plano + '.pdf'
        if os.path.isfile(path):
            return send_from_directory('E:\COMPARTIDOS\Ing de Producto\Productos - VISTAS Y PLANOS\Desenhos',
                                       plano + '.pdf')
        else:
            return "PLANO NO ENCONTRADO"
