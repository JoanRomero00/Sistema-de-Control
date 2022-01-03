import pyodbc
import pandas
import datetime
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

def rellenar_fila(indice):
    tabla.iloc[i]['ORDEN_MANUFACTURA']

#print(lista_CF('Branson'))

tabla = pandas.read_excel('baseModulos.xlsx')
del(tabla['Unnamed: 28'])
del(tabla['Unnamed: 29'])
del(tabla['Unnamed: 30'])
del(tabla['Unnamed: 31'])

tabla.insert(0, "idModulo", None, allow_duplicates=False)
tabla.insert(1, "idOrdenManufactura", None, allow_duplicates=False)
tabla.insert(2, "repeticion", None, allow_duplicates=False)


tabla.insert(31, "lecturaHorno", None, allow_duplicates=False)
tabla.insert(32, "fechalecturaHorno", None, allow_duplicates=False)
tabla.insert(33, "fechaCarga", None, allow_duplicates=False)

#tabla.to_excel('example.xlsx')
#print(tabla)

ids = []
ids_OM = []
repeticiones = []
resto_info = []
tabla_final = pandas.DataFrame()
id = 280187
for i in range(0, len(tabla.index)):
    cant = tabla.iloc[i]['PT_CANTIDAD']
    if cant == 1:
        complete = tabla.iloc[i]['ORDEN_MANUFACTURA'] + '/0'
        id = id + 1
        resto_info = {'idModulo': id, 'idOrdenManufactura': complete, 'repeticion': 0,
                      'ORDEN_MANUFACTURA': tabla.iloc[i]['ORDEN_MANUFACTURA'],
                      'SO': tabla.iloc[i]['SO'],
                      'FECHA_CONFIRMACION': tabla.iloc[i]['FECHA_CONFIRMACION'],
                      'FECHA_ENTREGA': tabla.iloc[i]['FECHA_ENTREGA'],
                      'PT_PRODUCTO': tabla.iloc[i]['PT_PRODUCTO'],
                      'lecturaHorno': None, 'fechaLecturaHorno': None,
                      "fechaCarga": datetime.datetime.now()
                      }
        tabla_final = tabla_final.append(resto_info, ignore_index=True)
    else:
        for j in range(0,cant):
            complete = tabla.iloc[i]['ORDEN_MANUFACTURA'] + '/' + str(j)
            id = id + 1
            resto_info = {'idModulo': id, 'idOrdenManufactura': complete, 'repeticion': j,
                          'ORDEN_MANUFACTURA': tabla.iloc[i]['ORDEN_MANUFACTURA'],
                          'SO': tabla.iloc[i]['SO'],
                          'FECHA_CONFIRMACION': tabla.iloc[i]['FECHA_CONFIRMACION'],
                          'FECHA_ENTREGA': tabla.iloc[i]['FECHA_ENTREGA'],
                          'PT_PRODUCTO': tabla.iloc[i]['PT_PRODUCTO'],
                          'lecturaHorno': None, 'fechaLecturaHorno': None,
                          "fechaCarga": datetime.datetime.now()
                          }
            tabla_final = tabla_final.append(resto_info, ignore_index=True)





#tabla_final['idModulo'] = ids
#tabla_final['idOrdenManufactura'] = ids_OM
#tabla_final['repeticion'] = repeticiones

#tabla_final.insert(8, "lecturaHorno", None, allow_duplicates=False)
#tabla_final.insert(9, "fechalecturaHorno", None, allow_duplicates=False)
#tabla_final.insert(10, "fechaCarga", datetime.datetime.now(), allow_duplicates=False)
#print(tabla.iloc[2]['PT_CANTIDAD'])
print(tabla_final)
tabla_final.to_excel('example.xlsx')