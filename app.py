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
    data2 = lista_op()
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
        if verificacion(codigo, maq) == '' or verificacion(codigo, maq) == None:
            complete = 'UPDATE dbo.basePiezas SET fechaLectura' + maq + ' = getdate() WHERE idPieza = ?'
            cursor = con.cursor()
            cursor.execute(complete, codigo)
            cursor.commit()
            cursor.close()
            return redirect(url_for(templete, maquina=maq))
        else:
            flash('El codigo ' + codigo + ' ya fue escaneado')
            return redirect(url_for(templete, maquina=maq))


"""@app.route('dar_bajas/<string:maq>', methods=["GET", "POST"])
def dar_bajas(maq):
    cursor = con.cursor()
    cursor.execute('SELECT DISTINCT CODIGO_COLOR FROM basePiezas WHERE OP=?', maq)
    cursor.commit()
    cursor.close() """



def verificacion(id, maq):
    complete = "SELECT fechaLectura" + maq + " FROM basePiezas WHERE idPieza=?"
    cursor = con.cursor()
    cursor.execute(complete, id)
    data = cursor.fetchone()
    cursor.close()
    return data[0]

def lista_op():
    data = []
    cursor = con.cursor()
    cursor.execute('SELECT DISTINCT OP FROM basePiezas ORDER BY OP')
    for row in cursor:
        indice = str(row).index(",")
        row2 = str(row)[2:indice - 1]
        row3 = row2.replace(" ", "-")
        data.append(row3)
    cursor.close()
    return data