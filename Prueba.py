import pyodbc

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
for row in cursor:
    indice = str(row).index(",")
    fila = str(row)[2:indice-1]
    fila2 = fila.replace(" ","-")
    data.append(fila2)
cursor.close()

print(str(data[1]))
print(data)
print(type(data[1]))
#print(type(data))
#print(str(data[0]).index(","))
#print(str(data[0])[2:16])

data = []
cursor = con.cursor()
cursor.execute('SELECT DISTINCT OP FROM basePiezas ORDER BY OP')
for row in cursor:
    data.append(row)
cursor.close()

print(data)

data = []
cursor = con.cursor()
cursor.execute('SELECT DISTINCT PIEZA_PROFUNDO FROM basePiezas')
for row in cursor:
    indice = str(row).index(",")
    row2 = str(row)[1:indice]
    data.append(row2)
cursor.close()

print(data)