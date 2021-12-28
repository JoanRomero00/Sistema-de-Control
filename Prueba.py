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

print(OutputArray)