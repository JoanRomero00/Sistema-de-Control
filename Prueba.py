import pyodbc
import pandas
import datetime
import os
import xlrd
from flask import send_from_directory
con = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=ANDRESPC;"
    "DataBase=Prueba;"
    "Trusted_Connection=yes;"
)

def verificacion(id, maq):
    complete = "SELECT fechaLectura" + maq + " FROM basePiezas WHERE idPieza=?"
    cursor = con.cursor()
    cursor.execute(complete, id)
    data = cursor.fetchone()
    cursor.close()
    return data[0]

#print("Output:")
#print(verificacion(503442, "SLC"))
#print(verificacion(1091140, "SLC"))
#print(verificacion(417524, "SLC"))
#print(verificacion(417523, "SLC"))

data = []
cursor = con.cursor()
cursor.execute('SELECT DISTINCT OP FROM basePiezas ORDER BY OP')
records = cursor.fetchall()
OutputArray = []
columnNames = [column[0] for column in cursor.description]

for record in records:
    OutputArray.append( dict( zip( columnNames , record ) ) )
cursor.close()

#print(str(data[1]))
#for o in OutputArray:
#    print(o['OP'])
#print(OutputArray[0]['OP'])
#print(outputObj[1])
#print(type(data[1]))
#print(type(data))
#print(str(data[0]).index(","))
#print(str(data[0])[2:16])

data = []
cursor = con.cursor()
cursor.execute('SELECT DISTINCT OP, PIEZA_PROFUNDO FROM basePiezas ORDER BY OP')
for row in cursor:
    data.append(row)
cursor.close()

#print(data)

data = []
cursor = con.cursor()
cursor.execute('SELECT DISTINCT PIEZA_PROFUNDO FROM basePiezas')
for row in cursor:
    indice = str(row).index(",")
    row2 = str(row)[1:indice]
    data.append(row2)
cursor.close()

#print(data)

cursor = con.cursor()
cursor.execute('SELECT DISTINCT OP FROM basePiezas ORDER BY OP')
records = cursor.fetchall()
OutputArray = []
columnNames = [column[0] for column in cursor.description]

for record in records:
    OutputArray.append(dict(zip(columnNames, record)))
cursor.close()

#print(OutputArray)

list = []
for o in OutputArray:
    list.append(o['OP'])
#print(list)
#print(list[0])

data = []
cursor = con.cursor()
cursor.execute('SELECT DISTINCT OP FROM basePiezas ORDER BY OP')
for row in cursor:
    data.append(row)
cursor.close()

#print(data)
#print(data[0])

cursor = con.cursor()
cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR, PIEZA_PROFUNDO FROM basePiezas WHERE OP='W19-2105-05-UNIF' AND"
                " PIEZA_NOMBRECOLOR='BLANCO OPACO' ORDER BY OP")
records = cursor.fetchall()
OutputArray = []
columnNames = [column[0] for column in cursor.description]
for record in records:
    OutputArray.append(dict(zip(columnNames, record)))
cursor.close()

#print(OutputArray)
#print(OutputArray[0]['OP'])


op = 'W50-2112-ADELANTO_IDEAS'
color = 'BLANCO'
espesor = 18
cursor = con.cursor()
cursor.execute("SELECT idPieza FROM basePiezas WHERE OP=? "
                 "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=?", op, color, espesor)
records = cursor.fetchall()
ids = []
columnNames = [column[0] for column in cursor.description]
for record in records:
    ids.append(dict(zip(columnNames, record)))
cursor.close()
#print(records)
#print(ids)




cursor = con.cursor()
op='W50-2112-ADELANTO_IDEAS'
color='BLANCO'
cursor.execute("SELECT idPieza FROM basePiezas WHERE OP='W50-2112-ADELANTO_IDEAS' AND PIEZA_NOMBRECOLOR='BLANCO' AND PIEZA_PROFUNDO=15")
records = cursor.fetchall()
OutputArray = []
columnNames = [column[0] for column in cursor.description]
for record in records:
    OutputArray.append(dict(zip(columnNames, record)))
cursor.close()

#print(OutputArray)
#for id in OutputArray:
    #print(id['idPieza'])

def lista_CF(op):
    cursor = con.cursor()
    if op == 0:
        cursor.execute("SELECT DISTINCT CLIENTE_FINAL FROM baseModulos")
    else:
        cursor.execute("SELECT FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP FROM baseModulos WHERE CLIENTE_FINAL=?", op)
    records = cursor.fetchall()
    data = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        data.append(dict(zip(columnNames, record)))
    cursor.close()
    return data

#print(lista_CF('Branson'))

fecha = datetime.datetime.now()
print(fecha.strftime("%c"))
print(fecha.strftime("%x") + ' ' + fecha.strftime("%X"))

a = 'CAJ000000006268A'
b = '\0'
a2 = b[:1] + a[:3]
print(a2)

def lista_op2():
    cursor = con.cursor()
    cursor.execute('SELECT * FROM ProduccionDiariaModulosTablero')
    records = cursor.fetchall()
    OutputArray = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        OutputArray.append(dict(zip(columnNames, record)))
    cursor.close()
    return OutputArray

print(lista_op2())
path = 'E:\COMPARTIDOS\Ing de Producto\Productos - VISTAS Y PLANOS\Desenhos/KPI.pdf'

# Check whether the
# specified path is
# an existing file
isFile = os.path.isfile(path)
print(isFile)


today = datetime.datetime.now()
fecha = today.strftime("%x") + ' ' + today.strftime("%X")
print(today.strftime("%c"))
print(fecha)
print(type(fecha))

print(fecha[:8])

if fecha[:8] == '01/07/22':
    print("Igual")

def fecha():
    today = datetime.datetime.now()
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    return fecha

def comparar_fecha(fecha):
    if fecha == fecha():
        return True
    else:
        return False


print(fecha())