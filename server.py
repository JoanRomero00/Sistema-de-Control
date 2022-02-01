from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import pyodbc
import os
from os import remove
from werkzeug.utils import secure_filename
from waitress import serve
from dataBase.control import Control
from dataBase.lecturaMasiva import LecturaMasiva
from dataBase.despacho import Despacho
from dataBase.AB_ModulosPiezas import ABM
from dataBase.plano import Plano
from dataBase.informes import Informe

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

# setings
app.secret_key = "mysecretkey"


# HOME
@app.route('/')
def index():
    return render_template("index.html")


# Escanear codigo y lectura mavisa de piezas
@app.route('/index1/<string:maquina>/<string:ventana>', methods=["POST", "GET"])
def index1(maquina, ventana):
    if ventana == "1":
        display1 = ""
        display2 = "display:None;"
        display3 = "display:None;"
        return render_template("index1.html", maquina=maquina, display1=display1, display2=display2, display3=display3,
                               piezas=Control().getTabla(maquina), ops=LecturaMasiva().lista_ops(maquina),
                               ops_masivo=LecturaMasiva().getTablaLecturaMasiva(maquina))
    elif ventana == "2":
        display1 = "display:None;"
        display2 = ""
        display3 = "display:None;"
        return render_template("index1.html", maquina=maquina, display1=display1, display2=display2, display3=display3,
                               piezas=Control().getTabla(maquina), ops=LecturaMasiva().lista_ops(maquina),
                               ops_masivo=LecturaMasiva().getTablaLecturaMasiva(maquina))
    elif ventana == "3":
        if maquina in ["NST", "GBM", "CHN", "LEA", "ALU", "INSUMOS", "PLTER", "HORNO", "PLACARD", "PEGADO", "AGUJEREADO"]:
            flash("El informe no se encuentra disponible para esta maquina")
        display1 = "display:None;"
        display2 = "display:None;"
        display3 = ""
        return render_template("index1.html", maquina=maquina, display1=display1, display2=display2, display3=display3,
                               piezas=Control().getTabla(maquina), ops=LecturaMasiva().lista_ops(maquina),
                               piezas_noleidas=Informe().piezas_noleidas(maquina, request.form['op_informe']))


@app.route('/index2/<string:maquina>/<string:ventana>', methods=["POST", "GET"])
def index2(maquina, ventana):
    if ventana == "1":
        display1 = ""
        display2 = "display:None;"
        return render_template("index2.html", maquina=maquina, display1=display1, display2=display2,
                               piezas=Control().getTabla(maquina))
    if ventana == "2":
        if maquina in ["NST", "GBM", "CHN", "LEA", "ALU", "INSUMOS", "PLTER", "HORNO", "PLACARD", "PEGADO", "AGUJEREADO"]:
            flash("El informe no se encuentra disponible para esta maquina")
        display1 = "display:None;"
        display2 = ""
        return render_template("index2.html", maquina=maquina, piezas=Control().getTabla(maquina),
                               display1=display1, display2=display2,
                               piezas_noleidas=Informe().piezas_noleidas(maquina, request.form['op_informe']))


@app.route('/escanear_codigo/<string:maq>/<string:templete>', methods=['POST'])
def escanear_codigo(maq, templete):
    if request.method == 'POST':
        codigo = request.form['cod_escaneado']
        try:
            if Control().verificar_cod(codigo, maq) == 1:
                flash('El codigo ' + codigo + ' ya fue escaneado')
                if templete == "index1":
                    return redirect(url_for(templete, maquina=maq, ventana="1"))
                return redirect(url_for(templete, maquina=maq, ventana="1"))
            elif Control().verificar_cod(codigo, maq) is None:
                flash('El codigo ingresado no existe o la maquina no pertenece a la ruta de la pieza')
                if templete == "index1":
                    return redirect(url_for(templete, maquina=maq, ventana="1"))
                return redirect(url_for(templete, maquina=maq, ventana="1"))
            else:
                Control().updatePM(codigo, maq)
                if templete == "index1":
                    return redirect(url_for(templete, maquina=maq, ventana="1"))
                return redirect(url_for(templete, maquina=maq, ventana="1"))
        except pyodbc.DataError:
            flash("Error: el codigo ingresado es incorrecto. Intente nuevamente")
            if templete == "index1":
                return redirect(url_for(templete, maquina=maq, ventana="1"))
            return redirect(url_for(templete, maquina=maq, ventana="1"))


@app.route("/ops", methods=["POST", "GET"])
def ops():
    global OutputArray
    if request.method == 'POST':
        op = request.form['op']
        maquina = request.form['maquina']
        print(maquina)
        print(op)
        OutputArray = LecturaMasiva().lista_colores(op, maquina)
    return jsonify(OutputArray)


@app.route("/colores", methods=["POST", "GET"])
def colores():
    global OutputArray
    if request.method == 'POST':
        color = request.form['color']
        op = request.form['op']
        maquina = request.form['maquina']
        print(color)
        OutputArray = LecturaMasiva().lista_espesores(color, op, maquina)
    return jsonify(OutputArray)


@app.route("/espesores", methods=["POST", "GET"])
def espesores():
    global piezas
    if request.method == 'POST':
        op = request.form['op']
        color = request.form['color']
        espesor = request.form['espesor']
        maquina = request.form['maquina']
        print(espesor)
        piezas = LecturaMasiva().lista_piezas(op, color, espesor, maquina)
    return jsonify(piezas)


@app.route("/espesores_cantidad", methods=["POST", "GET"])
def espesores_cantidad():
    global cantidad
    if request.method == 'POST':
        op = request.form['op']
        color = request.form['color']
        espesor = request.form['espesor']
        maquina = request.form['maquina']
        cantidad = LecturaMasiva().calcular_cant(op, color, espesor, 1, maquina)
    return jsonify(cantidad)


@app.route("/piezas", methods=["POST", "GET"])
def piezas():
    global cantidad
    if request.method == 'POST':
        op = request.form['op']
        color = request.form['color']
        espesor = request.form['espesor']
        pieza = request.form['pieza']
        maquina = request.form['maquina']
        print(espesor + " , " + color + " , " + op + " , " + pieza)
        cantidad = LecturaMasiva().calcular_cant(op, color, espesor, pieza, maquina)
    return jsonify(cantidad)


@app.route('/lectura_masiva/<string:maq>', methods=['POST'])
def lectura_masiva(maq):
    try:
        if request.method == 'POST':
            pin = request.form['pin']
            usuario = LecturaMasiva().verificar_pin(pin)
            if usuario is None:
                flash("Error: el PIN ingresado es incorrecto", 'danger')
                return redirect(url_for('index1', maquina=maq, ventana=2))
            op = request.form['ops']
            color = request.form['colores']
            espesor = request.form['espesores']
            pieza = request.form['piezas']
            if color == 'Color':
                flash("Error: Por favor ingrese todos los campos 1", 'danger')
                return redirect(url_for('index1', maquina=maq, ventana=2))
            piezas = LecturaMasiva().verificar_lectura(op, color, espesor, pieza, maq)
            if piezas == 1:
                flash("Esta lectura masiva ya se a realizado. OP: " + op + " "
                      "| COLOR: " + color + " | ESPESOR: " + espesor + " | PIEZA: " + pieza,
                      'warning')
                return redirect(url_for('index1', maquina=maq, ventana=2))
            LecturaMasiva().updateMasivo(piezas, maq)
            if pieza == 'Pieza':
                LecturaMasiva().log_lecturaMasiva(usuario, op, color, espesor, maq, None)
            else:
                LecturaMasiva().log_lecturaMasiva(usuario, op, color, espesor, maq, pieza)
            flash("Lectura masiva realizada con exito. \n OP: " + op + " | COLOR: " + color + " | ESPESOR: " + espesor
                  + " | PIEZA: " + pieza)
            return redirect(url_for('index1', maquina=maq, ventana=2))
    except pyodbc.DataError:
        flash("Error: Por favor ingrese todos los campos 2", 'danger')
        return redirect(url_for('index1', maquina=maq, ventana=2))


# DESPACHO
@app.route('/index3/<string:maquina>')
def index3(maquina):
    return render_template("index3.html", maquina=maquina, sos=Despacho().lista_so(0), clientes=Despacho().lista_cf(0))


@app.route("/buscar_cf", methods=["POST", "GET"])
def buscar_cf():
    if request.method == 'POST':
        cf = request.form['op']
        print(cf)
        return jsonify(Despacho().lista_cf(cf))


@app.route("/buscar_so", methods=["POST", "GET"])
def buscar_so():
    if request.method == 'POST':
        so = request.form['color']
        print(so)
        return jsonify(Despacho().lista_so(so))


# Alta y Baja de Piezas/Modulos
@app.route('/AB_ModulosPiezas/<string:ventana>')
def index4(ventana):
    if ventana == "1":
        display1 = ""
        display2 = "display:none;"
        display3 = "display:none;"
        return render_template("index4.html", ops_modulos=ABM().lista_opModulos(), ops_piezas=ABM().lista_opPiezas(),
                               display1=display1, display2=display2, display3=display3, logs=ABM().getLogAB())
    elif ventana == "2":
        display1 = "display:none;"
        display2 = ""
        display3 = "display:none;"
        return render_template("index4.html", ops_modulos=ABM().lista_opModulos(), ops_piezas=ABM().lista_opPiezas(),
                               display1=display1, display2=display2, display3=display3, logs=ABM().getLogAB())


@app.route('/subir_archivo', methods=['POST'])
def subir_archivo():
    if request.method == 'POST':
        try:
            tipo = request.form['tipo_subida']
            archivo = request.files['archivo']
            filename = secure_filename(archivo.filename)
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if tipo == 'baseModulos':
                ABM().Alta_Modulos(archivo.filename)
                ABM().setLogAB("ALTA", "Modulo", 0, 0)
                print("OPERACION SUBIDA DE DATOS: COMPLETADA")
                flash('Los MODULOS se han subido correctamente')
                return redirect(url_for('index4', ventana=1))
            elif tipo == 'basePiezas':
                ABM().Alta_Piezas(archivo.filename)
                ABM().setLogAB("ALTA", "Pieza", 0, 0)
                print("OPERACION SUBIDA DE DATOS:  COMPLETADA")
                flash('Las PIEZAS se han subido correctamente')
                return redirect(url_for('index4', ventana=1))
        except PermissionError:
            print("OPERACION SUBIDA DE DATOS:  CANCELADA")
            flash("Error: No se a cargado ningun archivo", 'danger')
            return redirect(url_for('index4', ventana=1))
        except KeyError:
            archivo = request.files['archivo']
            remove(archivo.filename)
            print("OPERACION SUBIDA DE DATOS:  CANCELADA")
            flash("Error: Archivo equivocado, no cumple con el formato establecido", 'danger')
            return redirect(url_for('index4', ventana=1))
        except pyodbc.IntegrityError as error:
            archivo = request.files['archivo']
            tipo = request.form['tipo_subida']
            remove(archivo.filename)
            if tipo == 'basePiezas':
                remove('basePiezasLimpia.xlsx')
            elif tipo == 'baseModulos':
                remove('baseModulosLimpia.xlsx')
                remove('baseModulosDesglosada.xlsx')
            print("OPERACION SUBIDA DE DATOS:  CANCELADA")
            flash(error.args[1] + " | LA OPERACION SE CANCELO, NO SE SUBIO NINGUN DATO", 'warning')
            return redirect(url_for('index4', ventana=1))


@app.route('/baja_modulos', methods=['POST'])
def baja_modulos():
    if request.method == 'POST':
        borrar_todo = request.form['borrar_todo']
        op = request.form['op_modulo']
        if borrar_todo == 'NO':
            cantidad = ABM().getCant("Modulo", op)
            ABM().elimar_Modulos(op)
            ABM().setLogAB("BAJA", "Modulo", op, cantidad)
            print("BAJA MODULOS | OP: " + op)
            flash('Los MODULOS se han borrado correctamente')
            return redirect(url_for('index4', ventana=2))
        elif borrar_todo == 'SI':
            cant_modulos = ABM().getCant("Modulo", op)
            cant_piezas = ABM().getCant("Pieza", op)
            ABM().elimar_Modulos(op)
            ABM().elimar_Piezas(op)
            ABM().setLogAB("BAJA", "Modulo", op, cant_modulos)
            ABM().setLogAB("BAJA", "Pieza", op, cant_piezas)
            print("BAJA MODULOS Y PIEZAS | OP: " + op)
            flash('PIEZAS y MODULOS se han borrado correctamente')
            return redirect(url_for('index4', ventana=2))


@app.route('/baja_piezas', methods=['POST'])
def baja_piezas():
    if request.method == 'POST':
        op = request.form['op_pieza']
        cantidad = ABM().getCant("Pieza", op)
        ABM().elimar_Piezas(op)
        ABM().setLogAB("BAJA", "Pieza", op, cantidad)
        print("BAJA PIEZAS | OP: " + op)
        flash('Las PIEZAS se han borrado correctamente')
        return redirect(url_for('index4', ventana=2))


# Planos
@app.route('/planos/<string:plano>')
def planos(plano):
    return render_template("planos.html", plano=plano, produccion=Plano().produccion_diaria())


@app.route('/leer_plano', methods=['POST'])
def leer_plano():
    if request.method == 'POST':
        plano = request.form['plano']
        if "/" in plano:
            return redirect(url_for('planos', plano=1))
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


serve(app, host='0.0.0.0', port=5000, threads=6) # WAITRESS!

# starting the app
# if __name__ == "__main__":
#    app.run(port=3000, debug=True)
