import pyodbc
import pandas
import xlrd
from os import remove
import app


def cargar_archivo(nombre_archivo):

    con = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=ANDRESPC;"
        "DataBase=Prueba;"
        "Trusted_Connection=yes;"
    )


    #Ordeno Tabla
    tabla = pandas.read_excel(nombre_archivo)
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

    tabla.to_excel('baseModulosLimpia.xlsx')


    #Desglose
    def resto_info(id, complete, repeticion, tabla, i):
        resto_info = {'idModulo': id, 'idOrdenManufactura': complete, 'repeticion': repeticion,
                      'ORDEN_MANUFACTURA': tabla.iloc[i]['ORDEN_MANUFACTURA'],
                      'SO': tabla.iloc[i]['SO'],
                      'FECHA_CONFIRMACION': tabla.iloc[i]['FECHA_CONFIRMACION'],
                      'FECHA_ENTREGA': tabla.iloc[i]['FECHA_ENTREGA'],
                      'FRANQUICIA': tabla.iloc[i]['FRANQUICIA'],
                      'CLIENTE_FINAL': tabla.iloc[i]['CLIENTE_FINAL'],
                      'TIPO_OPORTUNIDAD': tabla.iloc[i]['TIPO_OPORTUNIDAD'],
                      'PRODUCTO_GENERICO': tabla.iloc[i]['PRODUCTO_GENERICO'],
                      'PT_PRODUCTO': tabla.iloc[i]['PT_PRODUCTO'],
                      'PT_CODIGO': tabla.iloc[i]['PT_CODIGO'],
                      'PT_CATEGORIA': tabla.iloc[i]['PT_CATEGORIA'],
                      'PT_CANTIDAD': tabla.iloc[i]['PT_CANTIDAD'],
                      'PT_UNIDAD': tabla.iloc[i]['PT_UNIDAD'],
                      'PT_ANCHO': tabla.iloc[i]['PT_ANCHO'],
                      'PT_ALTO': tabla.iloc[i]['PT_ALTO'],
                      'PT_PROFUNDO': tabla.iloc[i]['PT_PROFUNDO'],
                      'PT_NOMBRECOLOR': tabla.iloc[i]['PT_NOMBRECOLOR'],
                      'PT_NOMBREDISTRIBUCION': tabla.iloc[i]['PT_NOMBREDISTRIBUCION'],
                      'PT_NOMBREFAMILIA': tabla.iloc[i]['PT_NOMBREFAMILIA'],
                      'PT_NOMBRELINEA': tabla.iloc[i]['PT_NOMBRELINEA'],
                      'PT_NOMBREMATERIAL': tabla.iloc[i]['PT_NOMBREMATERIAL'],
                      'PT_NOMBREMODELO': tabla.iloc[i]['PT_NOMBREMODELO'],
                      'PT_NOMBREMODOCONSTRUCCION': tabla.iloc[i]['PT_NOMBREMODOCONSTRUCCION'],
                      'PT_NOMBREMODOSUSTENTACION': tabla.iloc[i]['PT_NOMBREMODOSUSTENTACION'],
                      'PT_NOMBRETIPOENTIDAD': tabla.iloc[i]['PT_NOMBRETIPOENTIDAD'],
                      'PT_NOMBRETIPOMUEBLE': tabla.iloc[i]['PT_NOMBRETIPOMUEBLE'],
                      'DocumentoOrigen': tabla.iloc[i]['DocumentoOrigen'],
                      'OP': tabla.iloc[i]['OP'],
                      'lecturaHorno': None, 'fechaLecturaHorno': None,
                      "fechaCarga": app.fecha()
                      }
        return resto_info


    tabla_final = pandas.DataFrame()
    cursor = con.cursor()
    cursor.execute("SELECT MAX(idModulo) FROM baseModulos")
    max = cursor.fetchone()
    id = max[0]
    for i in range(0, len(tabla.index)):
        cant = tabla.iloc[i]['PT_CANTIDAD']
        if cant == 1:
            complete = tabla.iloc[i]['ORDEN_MANUFACTURA'] + '/0'
            id = id + 1
            fila = resto_info(id, complete, 0, tabla, i)
            tabla_final = tabla_final.append(fila, ignore_index=True)
        else:
            for j in range(0,cant):
                complete = tabla.iloc[i]['ORDEN_MANUFACTURA'] + '/' + str(j)
                id = id + 1
                fila = resto_info(id, complete, j, tabla, i)
                tabla_final = tabla_final.append(fila, ignore_index=True)


    #subir a la BD
    tabla_final.to_excel('baseModulosDesglosada.xlsx')

    book = xlrd.open_workbook("baseModulosDesglosada.xlsx")
    sheet = book.sheet_by_name("Sheet1")

    query = """
    INSERT INTO dbo.baseModulos (
        idModulo, 
        idOrdenManufactura, 
        repeticion,
        ORDEN_MANUFACTURA,
        SO,
        FECHA_CONFIRMACION,
        FECHA_ENTREGA,
        FRANQUICIA,
        CLIENTE_FINAL,
        TIPO_OPORTUNIDAD,
        PRODUCTO_GENERICO,
        PT_PRODUCTO,
        PT_CODIGO,
        PT_CATEGORIA,
        PT_CANTIDAD,
        PT_UNIDAD,
        PT_ANCHO,
        PT_ALTO,
        PT_PROFUNDO,
        PT_NOMBRECOLOR,
        PT_NOMBREDISTRIBUCION,
        PT_NOMBREFAMILIA,
        PT_NOMBRELINEA,
        PT_NOMBREMATERIAL,
        PT_NOMBREMODELO,
        PT_NOMBREMODOCONSTRUCCION,
        PT_NOMBREMODOSUSTENTACION,
        PT_NOMBRETIPOENTIDAD,
        PT_NOMBRETIPOMUEBLE,
        DocumentoOrigen,
        OP,
        lecturaHorno,
        fechaLecturaHorno,
        fechaCarga
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    cursor = con.cursor()

    for r in range(1, sheet.nrows):
        idModulo = sheet.cell(r,1).value
        print(idModulo)
        idOrdenManufactura = sheet.cell(r,2).value
        print(idOrdenManufactura)
        repeticion = sheet.cell(r,3).value
        print(repeticion)
        ORDEN_MANUFACTURA = sheet.cell(r,4).value
        SO = sheet.cell(r,5).value
        FECHA_CONFIRMACION = sheet.cell(r,6).value
        FECHA_ENTREGA = sheet.cell(r,7).value
        FRANQUICIA = sheet.cell(r,8).value
        CLIENTE_FINAL = sheet.cell(r,9).value
        TIPO_OPORTUNIDAD = sheet.cell(r,10).value
        PRODUCTO_GENERICO = sheet.cell(r,11).value
        PT_PRODUCTO = sheet.cell(r,12).value
        PT_CODIGO = sheet.cell(r,13).value
        PT_CATEGORIA = sheet.cell(r,14).value
        PT_CANTIDAD = sheet.cell(r,15).value
        PT_UNIDAD = sheet.cell(r,16).value
        PT_ANCHO = sheet.cell(r,17).value
        PT_ALTO = sheet.cell(r,18).value
        PT_PROFUNDO = sheet.cell(r,19).value
        PT_NOMBRECOLOR = sheet.cell(r,20).value
        PT_NOMBREDISTRIBUCION = sheet.cell(r,21).value
        PT_NOMBREFAMILIA = sheet.cell(r,22).value
        PT_NOMBRELINEA = sheet.cell(r,23).value
        PT_NOMBREMATERIAL = sheet.cell(r,24).value
        PT_NOMBREMODELO = sheet.cell(r,25).value
        PT_NOMBREMODOCONSTRUCCION = sheet.cell(r,26).value
        PT_NOMBREMODOSUSTENTACION = sheet.cell(r,27).value
        PT_NOMBRETIPOENTIDAD = sheet.cell(r,28).value
        PT_NOMBRETIPOMUEBLE = sheet.cell(r,29).value
        DocumentoOrigen = sheet.cell(r,30).value
        OP = sheet.cell(r,31).value
        lecturaHorno = sheet.cell(r,32).value
        fechaLecturaHorno = sheet.cell(r,33).value
        fechaCarga = sheet.cell(r,34).value

        # Assign values from each row
        values = (idModulo, idOrdenManufactura, repeticion, ORDEN_MANUFACTURA, SO, FECHA_CONFIRMACION,
        FECHA_ENTREGA, FRANQUICIA, CLIENTE_FINAL, TIPO_OPORTUNIDAD, PRODUCTO_GENERICO,
        PT_PRODUCTO,
        PT_CODIGO,
        PT_CATEGORIA,
        PT_CANTIDAD,
        PT_UNIDAD,
        PT_ANCHO,
        PT_ALTO,
        PT_PROFUNDO,
        PT_NOMBRECOLOR,
        PT_NOMBREDISTRIBUCION,
        PT_NOMBREFAMILIA,
        PT_NOMBRELINEA,
        PT_NOMBREMATERIAL,
        PT_NOMBREMODELO,
        PT_NOMBREMODOCONSTRUCCION,
        PT_NOMBREMODOSUSTENTACION,
        PT_NOMBRETIPOENTIDAD,
        PT_NOMBRETIPOMUEBLE,
        DocumentoOrigen,
        OP,
        lecturaHorno,
        fechaLecturaHorno,
        fechaCarga)

        # Execute sql Query
        cursor.execute(query, values)

    # Commit the transaction
    con.commit()
    con.close()

    remove(nombre_archivo)
    remove('baseModulosLimpia.xlsx')
    remove('baseModulosDesglosada.xlsx')
