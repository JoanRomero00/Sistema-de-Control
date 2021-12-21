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


@app.route('/escanear_codigo', methods=['POST'])
def escanear_codigo():
    if request.method == 'POST':
        maquina = request.form['maquina']
        codigo = request.form['cod_escaneado']
        cursor = con.cursor()
        cursor.execute('SELECT idPieza, PIEZA_DESCRIPCION FROM dbo.basePiezas WHERE idPieza=?', int(codigo))
        data2 = cursor.fetchall()
        cursor.close()
        flash('Codigo escaneado correctamente')
        return redirect(url_for(maquina.lower()))


@app.route('/dar_id')
def dar_id(id2):
    id = id2
    return redirect(url_for(id.lower()))


@app.route('/plantilla1')
def plantilla1():
    return render_template('plantilla1.html')


@app.route('/GBN1')
def gbn1():
    if request.method == 'POST':
        maquina = request.form['maquina']
        codigo = request.form['cod_escaneado']
        cursor = con.cursor()
        cursor.execute('SELECT TOP 5 idPieza, PIEZA_DESCRIPCION FROM dbo.basePiezas '
                       'WHERE fechaLecturaPEGADO is not null ORDER BY fechaLecturaPEGADO')
        data2 = cursor.fetchall()
        cursor.close()
        flash('Codigo escaneado correctamente')
        return render_template('Corte/GBN1.html', piezas=data2)


@app.route('/SLC')
def slc():
    return render_template('Corte/SLC.html')


@app.route('/NST')
def nst():
    return render_template('Corte/NST.html')


@app.route('/GBM')
def gbm():
    return render_template('Corte/GBM.html')


@app.route('/STF')
def stf():
    return render_template('Pegado/STF.html')


@app.route('/MRT1')
def mrt1():
    return render_template('Pegado/MRT1.html')


@app.route('/MRT2')
def mrt2():
    return render_template('Pegado/MRT2.html')


@app.route('/MRT3')
def mrt3():
    return render_template('Pegado/MRT3.html')


@app.route('/MRT4')
def mrt4():
    return render_template('Pegado/MRT4.html')


@app.route('/IDM')
def idm():
    return render_template('Pegado/IDM.html')


@app.route('/RVR')
def rvr():
    return render_template('Agujereado/RVR.html')


@app.route('/CHN')
def chn():
    return render_template('Agujereado/CHN.html')


@app.route('/FTAL1')
def ftal1():
    return render_template('Agujereado/FTAL1.html')


@app.route('/KBT1')
def kbt1():
    return render_template('Agujereado/KBT1.html')


@app.route('/KBT2')
def kbt2():
    return render_template('Agujereado/KBT2.html')


@app.route('/VTP1')
def vtp1():
    return render_template('Agujereado/VTP1.html')


@app.route('/LEA')
def lea():
    return render_template('Frentes/LEA.html')


@app.route('/PRS')
def prs():
    return render_template('Frentes/PRS.html')


@app.route('/ALU')
def alu():
    return render_template('Frentes/ALU.html')


@app.route('/INSUMOS')
def insumos():
    return render_template('Armado/INSUMOS.html')


@app.route('/PLTER')
def plter():
    return render_template('Armado/PLTER.html')


@app.route('/HORNO')
def horno():
    return render_template('Armado/HORNO.html')


@app.route('/PLACARD')
def placard():
    return render_template('Control/PLACARD.html')


@app.route('/PEGADO')
def pegado():
    return render_template('Control/PEGADO.html')


@app.route('/AGUJEREADO')
def agujereado():
    return render_template('Control/AGUJEREADO.html')


@app.route('/DESPACHO')
def despacho():
    return render_template('Informes/DESPACHO.html')


if __name__ == '__main__':
    app.run(debug=True)
