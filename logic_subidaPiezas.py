import pyodbc
import pandas
import datetime
import xlrd
import app
from os import remove

def cargar_archivo(nombre_archivo):

    con = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=ANDRESPC;"
        "DataBase=Prueba;"
        "Trusted_Connection=yes;"
    )

    # Ordeno Tabla
    tabla = pandas.read_excel(nombre_archivo)

    tabla = tabla[['idOrdenManufactura', 'repeticion', 'ORDEN_MANUFACTURA', 'PIEZA_CODIGO', 'PIEZA_DESCRIPCION',
                   'PIEZA_UNIDAD', 'PIEZA_CANTIDAD', 'PIEZA_CATEGORIA', 'PIEZA_ANCHO', 'PIEZA_ALTO',
                   'PIEZA_PROFUNDO', 'PIEZA_NOMBRECOLOR', 'PIEZA_NOMBREDISTRIBUCION', 'PIEZA_NOMBREFAMILIA',
                   'PIEZA_NOMBRELINEA', 'PIEZA_NOMBREMATERIAL', 'PIEZA_NOMBREMODOCONSTRUCTIVO',
                   'PIEZA_NOMBREMODOSUSTENTACION', 'PIEZA_NOMBRETIPOENTIDAD', 'PIEZA_NOMBRETIPOMUEBLE',
                   'PIEZA_URL_BPP_INTERNA', 'PIEZA_URL_PLANO_INTERNA', 'PIEZA_CODIGOAGUJEREADO',
                   'PIEZA_CODIGOCORTE', 'PIEZA_CODIGORANURA', 'PIEZA_CODIGOTIPOPIEZA', 'PIEZA_NOMBREVETA',
                   'PIEZA_ESPESORFILODER', 'PIEZA_ESPESORFILOINF', 'PIEZA_ESPESORFILOIZQ', 'PIEZA_ESPEESORFILOSUP',
                   'PIEZA_TAPACANTO_DERECHO', 'PIEZA_TAPACANTO_INFERIOR', 'PIEZA_TAPACANTO_IZQUIERDO',
                   'PIEZA_TAPACANTO_SUPERIOR', 'PIEZA_NOMBREMODELO', 'DocumentoOrigen', 'SO', 'PRODUCTO_TERMINADO',
                   'CODIGO_PT', 'PT_CATEGORIA', 'PT_NOMBREFAMILIA', 'PT_NOMBRETIPOMUEBLE', 'PT_NOMBRELINEA', 'OP',
                   'TIPO_PIEZA_INDUSTRIAL', 'TIPO_PIEZA_PROGRAMACION', 'RUTA_ASIGNADA', 'ANCHO_CORTE', 'ALTO_CORTE',
                   'ANCHO_VS_FINAL', 'ALTO_VS_FINAL', 'FILOS', 'CODIGO_COLOR', 'CODIGO_SELCO', 'VETA_SELCO',
                   'PESO_PIEZAS', 'PASADAS_STF', 'PRECIO_FRTES_VIDRIO', 'PRECIO_LUSTRE', 'PRECIO_TURU', 'N_PALLET',
                   'SUP', 'PERIMETRO', 'CANTIDAD_2', 'idModulo', 'VACIO_4', 'VACIO_5', 'VACIO_6', 'VACIO_7',
                   'VACIO_8', 'VACIO_9', 'VACIO_10']]


    tabla.insert(0, "idPieza", None, allow_duplicates=False)
    del (tabla['N_PALLET'])
    tabla.insert(73, "CANT_AMBIENTES", None, allow_duplicates=False)
    tabla.insert(74, "PESO", None, allow_duplicates=False)
    tabla.insert(75, "PIEZA_CANTIDAD_ORIGINAL", None, allow_duplicates=False)
    tabla.insert(76, "ORDEN_MANU_ORIGINAL", None, allow_duplicates=False)
    tabla.insert(77, "AMBIENTE", None, allow_duplicates=False)
    tabla.insert(78, "N_PALLET", None, allow_duplicates=False)
    tabla.insert(79, "POSICION", None, allow_duplicates=False)
    tabla.insert(80, "fechaCarga", None, allow_duplicates=False)
    tabla.insert(81, "lecturaGBN1", None, allow_duplicates=False)
    tabla.insert(82, "fechaLecturaGBN1", None, allow_duplicates=False)
    tabla.insert(83, "lecturaSLC", None, allow_duplicates=False)
    tabla.insert(84, "fechaLecturaSLC", None, allow_duplicates=False)
    tabla.insert(85, "lecturaNST", None, allow_duplicates=False)
    tabla.insert(86, "fechaLecturaNST", None, allow_duplicates=False)
    tabla.insert(87, "lecturaSTF", None, allow_duplicates=False)
    tabla.insert(88, "fechaLecturaSTF", None, allow_duplicates=False)
    tabla.insert(89, "lecturaMRT1", None, allow_duplicates=False)
    tabla.insert(90, "fechaLecturaMRT1", None, allow_duplicates=False)
    tabla.insert(91, "lecturaMRT2", None, allow_duplicates=False)
    tabla.insert(92, "fechaLecturaMRT2", None, allow_duplicates=False)
    tabla.insert(93, "lecturaMRT3", None, allow_duplicates=False)
    tabla.insert(94, "fechaLecturaMRT3", None, allow_duplicates=False)
    tabla.insert(95, "lecturaMRT4", None, allow_duplicates=False)
    tabla.insert(96, "fechaLecturaMRT4", None, allow_duplicates=False)
    tabla.insert(97, "lecturaIDM", None, allow_duplicates=False)
    tabla.insert(98, "fechaLecturaIDM", None, allow_duplicates=False)
    tabla.insert(99, "lecturaRVR", None, allow_duplicates=False)
    tabla.insert(100, "fechaLecturaRVR", None, allow_duplicates=False)
    tabla.insert(101, "lecturaCHN", None, allow_duplicates=False)
    tabla.insert(102, "fechaLecturaCHN", None, allow_duplicates=False)
    tabla.insert(103, "lecturaFTAL1", None, allow_duplicates=False)
    tabla.insert(104, "fechaLecturaFTAL1", None, allow_duplicates=False)
    tabla.insert(105, "lecturaKBT", None, allow_duplicates=False)
    tabla.insert(106, "fechaLecturaKBT", None, allow_duplicates=False)
    tabla.insert(107, "lecturaVTP1", None, allow_duplicates=False)
    tabla.insert(108, "fechaLecturaVTP1", None, allow_duplicates=False)
    tabla.insert(109, "lecturaLEA", None, allow_duplicates=False)
    tabla.insert(110, "fechaLecturaLEA", None, allow_duplicates=False)
    tabla.insert(111, "lecturaPLTER", None, allow_duplicates=False)
    tabla.insert(112, "fechaLecturaPLTER", None, allow_duplicates=False)
    tabla.insert(113, "lecturaGBM", None, allow_duplicates=False)
    tabla.insert(114, "fechaLecturaGBM", None, allow_duplicates=False)
    tabla.insert(115, "lecturaPRS", None, allow_duplicates=False)
    tabla.insert(116, "fechaLecturaPRS", None, allow_duplicates=False)
    tabla.insert(117, "lecturaKBT1", None, allow_duplicates=False)
    tabla.insert(118, "fechaLecturaKBT1", None, allow_duplicates=False)
    tabla.insert(119, "lecturaKBT2", None, allow_duplicates=False)
    tabla.insert(120, "fechaLecturaKBT2", None, allow_duplicates=False)
    tabla.insert(121, "lecturaALU", None, allow_duplicates=False)
    tabla.insert(122, "fechaLecturaALU", None, allow_duplicates=False)
    tabla.insert(123, "lecturaPLACARD", None, allow_duplicates=False)
    tabla.insert(124, "fechaLecturaPLACARD", None, allow_duplicates=False)
    tabla.insert(125, "lecturaPEGADO", None, allow_duplicates=False)
    tabla.insert(126, "fechaLecturaPEGADO", None, allow_duplicates=False)
    tabla.insert(127, "lecturaAGUJEREADO", None, allow_duplicates=False)
    tabla.insert(128, "fechaLecturaAGUJEREADO", None, allow_duplicates=False)

    cursor = con.cursor()
    cursor.execute("SELECT top 1 idPieza FROM basePiezas "
                   "WHERE idPieza < 4231001 ORDER BY idPieza DESC")
    max = cursor.fetchone()
    id = max[0]
    for i in range(0, len(tabla.index)):
        id = id + 1
        tabla.at[i, 'idPieza'] = id
        tabla.at[i, 'fechaCarga'] = app.fecha()

    print(tabla)

    # subir a la BD
    tabla.to_excel('basePiezasLimpia.xlsx')

    book = xlrd.open_workbook("basePiezasLimpia.xlsx")
    sheet = book.sheet_by_name("Sheet1")

    query = "INSERT INTO dbo.basePiezas (idPieza, idOrdenManufactura, repeticion, ORDEN_MANUFACTURA, PIEZA_CODIGO, " \
            "PIEZA_DESCRIPCION, PIEZA_UNIDAD, PIEZA_CANTIDAD, PIEZA_CATEGORIA, PIEZA_ANCHO, PIEZA_ALTO, PIEZA_PROFUNDO, " \
            "PIEZA_NOMBRECOLOR, PIEZA_NOMBREDISTRIBUCION, PIEZA_NOMBREFAMILIA, PIEZA_NOMBRELINEA, PIEZA_NOMBREMATERIAL, " \
            "PIEZA_NOMBREMODOCONSTRUCTIVO, PIEZA_NOMBREMODOSUSTENTACION, PIEZA_NOMBRETIPOENTIDAD, PIEZA_NOMBRETIPOMUEBLE, " \
            "PIEZA_URL_BPP_INTERNA, PIEZA_URL_PLANO_INTERNA, PIEZA_CODIGOAGUJEREADO, PIEZA_CODIGOCORTE, " \
            "PIEZA_CODIGORANURA, PIEZA_CODIGOTIPOPIEZA, PIEZA_NOMBREVETA, PIEZA_ESPESORFILODER, PIEZA_ESPESORFILOINF, " \
            "PIEZA_ESPESORFILOIZQ, PIEZA_ESPEESORFILOSUP, PIEZA_TAPACANTO_DERECHO, PIEZA_TAPACANTO_INFERIOR, " \
            "PIEZA_TAPACANTO_IZQUIERDO, PIEZA_TAPACANTO_SUPERIOR, PIEZA_NOMBREMODELO, DocumentoOrigen, SO, " \
            "PRODUCTO_TERMINADO, CODIGO_PT, PT_CATEGORIA, PT_NOMBREFAMILIA, PT_NOMBRETIPOMUEBLE, PT_NOMBRELINEA, OP, " \
            "TIPO_PIEZA_INDUSTRIAL, TIPO_PIEZA_PROGRAMACION, RUTA_ASIGNADA, ANCHO_CORTE, ALTO_CORTE, ANCHO_VS_FINAL, " \
            "ALTO_VS_FINAL, FILOS, CODIGO_COLOR, CODIGO_SELCO, VETA_SELCO, PESO_PIEZAS, PASADAS_STF, PRECIO_FRTES_VIDRIO, " \
            "PRECIO_LUSTRE, PRECIO_TURU, SUP, PERIMETRO, CANTIDAD_2, idModulo, VACIO_4, VACIO_5, VACIO_6, VACIO_7, " \
            "VACIO_8, VACIO_9, VACIO_10, CANT_AMBIENTES, PESO, PIEZA_CANTIDAD_ORIGINAL,ORDEN_MANU_ORIGINAL, AMBIENTE, " \
            "N_PALLET, POSICION, fechaCarga, lecturaGBN1, fechaLecturaGBN1, lecturaSLC, fechaLecturaSLC, lecturaNST, " \
            "fechaLecturaNST, lecturaSTF, fechaLecturaSTF, lecturaMRT1, fechaLecturaMRT1, lecturaMRT2, fechaLecturaMRT2, " \
            "lecturaMRT3, fechaLecturaMRT3, lecturaMRT4, fechaLecturaMRT4, lecturaIDM, fechaLecturaIDM, lecturaRVR, " \
            "fechaLecturaRVR, lecturaCHN, fechaLecturaCHN, lecturaFTAL1, fechaLecturaFTAL1, lecturaKBT, fechaLecturaKBT, " \
            "lecturaVTP1, fechaLecturaVTP1, lecturaLEA, fechaLecturaLEA, lecturaPLTER, fechaLecturaPLTER, lecturaGBM, " \
            "fechaLecturaGBM, lecturaPRS, fechaLecturaPRS, lecturaKBT1, fechaLecturaKBT1, lecturaKBT2, fechaLecturaKBT2, " \
            "lecturaALU, fechaLecturaALU, lecturaPLACARD, fechaLecturaPLACARD, lecturaPEGADO, fechaLecturaPEGADO, " \
            "lecturaAGUJEREADO, fechaLecturaAGUJEREADO) " \
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
            "?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
            "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
            "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    cursor = con.cursor()

    for r in range(1, sheet.nrows):
        idPieza = sheet.cell(r, 1).value
        idOrdenManufactura = sheet.cell(r, 2).value
        repeticion = sheet.cell(r, 3).value
        ORDEN_MANUFACTURA = str(sheet.cell(r, 4).value)
        ORDEN_MANUFACTURA = ORDEN_MANUFACTURA.replace(".0","")
        PIEZA_CODIGO = sheet.cell(r, 5).value
        PIEZA_DESCRIPCION = sheet.cell(r, 6).value
        PIEZA_UNIDAD = sheet.cell(r, 7).value
        PIEZA_CANTIDAD = sheet.cell(r, 8).value
        PIEZA_CATEGORIA = sheet.cell(r, 9).value
        PIEZA_ANCHO = sheet.cell(r, 10).value
        PIEZA_ALTO = sheet.cell(r, 11).value
        PIEZA_PROFUNDO = sheet.cell(r, 12).value
        PIEZA_NOMBRECOLOR = sheet.cell(r, 13).value
        PIEZA_NOMBREDISTRIBUCION = sheet.cell(r, 14).value
        PIEZA_NOMBREFAMILIA = sheet.cell(r, 15).value
        PIEZA_NOMBRELINEA = sheet.cell(r, 16).value
        PIEZA_NOMBREMATERIAL = sheet.cell(r, 17).value
        PIEZA_NOMBREMODOCONSTRUCTIVO = sheet.cell(r, 18).value
        PIEZA_NOMBREMODOSUSTENTACION = sheet.cell(r, 19).value
        PIEZA_NOMBRETIPOENTIDAD = sheet.cell(r, 20).value
        PIEZA_NOMBRETIPOMUEBLE = sheet.cell(r, 21).value
        PIEZA_URL_BPP_INTERNA = sheet.cell(r, 22).value
        PIEZA_URL_PLANO_INTERNA = sheet.cell(r, 23).value
        PIEZA_CODIGOAGUJEREADO = sheet.cell(r, 24).value
        PIEZA_CODIGOCORTE = sheet.cell(r, 25).value
        PIEZA_CODIGORANURA = sheet.cell(r, 26).value
        PIEZA_CODIGOTIPOPIEZA = sheet.cell(r, 27).value
        PIEZA_NOMBREVETA = sheet.cell(r, 28).value
        PIEZA_ESPESORFILODER = sheet.cell(r, 29).value
        PIEZA_ESPESORFILOINF = sheet.cell(r, 30).value
        PIEZA_ESPESORFILOIZQ = sheet.cell(r, 31).value
        PIEZA_ESPEESORFILOSUP = sheet.cell(r, 32).value
        PIEZA_TAPACANTO_DERECHO = sheet.cell(r, 33).value
        PIEZA_TAPACANTO_INFERIOR = sheet.cell(r, 34).value
        PIEZA_TAPACANTO_IZQUIERDO = sheet.cell(r, 35).value
        PIEZA_TAPACANTO_SUPERIOR = sheet.cell(r, 36).value
        PIEZA_NOMBREMODELO = sheet.cell(r, 37).value
        DocumentoOrigen = sheet.cell(r, 38).value
        SO = sheet.cell(r, 39).value
        PRODUCTO_TERMINADO = sheet.cell(r, 40).value
        CODIGO_PT = sheet.cell(r, 41).value
        PT_CATEGORIA = sheet.cell(r, 42).value
        PT_NOMBREFAMILIA = sheet.cell(r, 43).value
        PT_NOMBRETIPOMUEBLE = sheet.cell(r, 44).value
        PT_NOMBRELINEA = sheet.cell(r, 45).value
        OP = sheet.cell(r, 46).value
        TIPO_PIEZA_INDUSTRIAL = sheet.cell(r, 47).value
        TIPO_PIEZA_PROGRAMACION = sheet.cell(r, 48).value
        RUTA_ASIGNADA = sheet.cell(r, 49).value
        ANCHO_CORTE = sheet.cell(r, 50).value
        ALTO_CORTE = sheet.cell(r, 51).value
        ANCHO_VS_FINAL = sheet.cell(r, 52).value
        ALTO_VS_FINAL = sheet.cell(r, 53).value
        FILOS = sheet.cell(r, 54).value
        CODIGO_COLOR = sheet.cell(r, 55).value
        CODIGO_SELCO = sheet.cell(r, 56).value
        VETA_SELCO = sheet.cell(r, 57).value
        PESO_PIEZAS = sheet.cell(r, 58).value
        PASADAS_STF = sheet.cell(r, 59).value
        PRECIO_FRTES_VIDRIO = sheet.cell(r, 60).value
        PRECIO_LUSTRE = sheet.cell(r, 61).value
        PRECIO_TURU = sheet.cell(r, 62).value
        SUP = sheet.cell(r, 63).value
        PERIMETRO = sheet.cell(r, 64).value
        CANTIDAD_2 = sheet.cell(r, 65).value
        idModulo = sheet.cell(r, 66).value
        VACIO_4 = sheet.cell(r, 67).value
        VACIO_5 = sheet.cell(r, 68).value
        VACIO_6 = sheet.cell(r, 69).value
        VACIO_7 = sheet.cell(r, 70).value
        VACIO_8 = sheet.cell(r, 71).value
        VACIO_9 = sheet.cell(r, 72).value
        VACIO_10 = sheet.cell(r, 73).value
        CANT_AMBIENTES = sheet.cell(r, 74).value
        PESO = sheet.cell(r, 75).value
        PIEZA_CANTIDAD_ORIGINAL = sheet.cell(r, 76).value
        ORDEN_MANU_ORIGINAL = sheet.cell(r, 77).value
        AMBIENTE = sheet.cell(r, 78).value
        N_PALLET = sheet.cell(r, 79).value
        POSICION = sheet.cell(r, 80).value
        fechaCarga = sheet.cell(r, 81).value
        lecturaGBN1 = sheet.cell(r, 82).value
        fechaLecturaGBN1 = sheet.cell(r, 83).value
        lecturaSLC = sheet.cell(r, 84).value
        fechaLecturaSLC = sheet.cell(r, 85).value
        lecturaNST = sheet.cell(r, 86).value
        fechaLecturaNST = sheet.cell(r, 87).value
        lecturaSTF = sheet.cell(r, 88).value
        fechaLecturaSTF = sheet.cell(r, 89).value
        lecturaMRT1 = sheet.cell(r, 90).value
        fechaLecturaMRT1 = sheet.cell(r, 91).value
        lecturaMRT2 = sheet.cell(r, 92).value
        fechaLecturaMRT2 = sheet.cell(r, 93).value
        lecturaMRT3 = sheet.cell(r, 94).value
        fechaLecturaMRT3 = sheet.cell(r, 95).value
        lecturaMRT4 = sheet.cell(r, 96).value
        fechaLecturaMRT4 = sheet.cell(r, 97).value
        lecturaIDM = sheet.cell(r, 98).value
        fechaLecturaIDM = sheet.cell(r, 99).value
        lecturaRVR = sheet.cell(r, 100).value
        fechaLecturaRVR = sheet.cell(r, 101).value
        lecturaCHN = sheet.cell(r, 102).value
        fechaLecturaCHN = sheet.cell(r, 103).value
        lecturaFTAL1 = sheet.cell(r, 104).value
        fechaLecturaFTAL1 = sheet.cell(r, 105).value
        lecturaKBT = sheet.cell(r, 106).value
        fechaLecturaKBT = sheet.cell(r, 107).value
        lecturaVTP1 = sheet.cell(r, 108).value
        fechaLecturaVTP1 = sheet.cell(r, 108).value
        lecturaLEA = sheet.cell(r, 110).value
        fechaLecturaLEA = sheet.cell(r, 111).value
        lecturaPLTER = sheet.cell(r, 112).value
        fechaLecturaPLTER = sheet.cell(r, 113).value
        lecturaGBM = sheet.cell(r, 114).value
        fechaLecturaGBM = sheet.cell(r, 115).value
        lecturaPRS = sheet.cell(r, 116).value
        fechaLecturaPRS = sheet.cell(r, 117).value
        lecturaKBT1 = sheet.cell(r, 118).value
        fechaLecturaKBT1 = sheet.cell(r, 119).value
        lecturaKBT2 = sheet.cell(r, 120).value
        fechaLecturaKBT2 = sheet.cell(r, 121).value
        lecturaALU = sheet.cell(r, 122).value
        fechaLecturaALU = sheet.cell(r, 123).value
        lecturaPLACARD = sheet.cell(r, 124).value
        fechaLecturaPLACARD = sheet.cell(r, 125).value
        lecturaPEGADO = sheet.cell(r, 126).value
        fechaLecturaPEGADO = sheet.cell(r, 127).value
        lecturaAGUJEREADO = sheet.cell(r, 128).value
        fechaLecturaAGUJEREADO = sheet.cell(r, 129).value

        # Assign values from each row
        values = (
            idPieza,
            idOrdenManufactura,
            repeticion,
            ORDEN_MANUFACTURA,
            PIEZA_CODIGO,
            PIEZA_DESCRIPCION,
            PIEZA_UNIDAD,
            PIEZA_CANTIDAD,
            PIEZA_CATEGORIA,
            PIEZA_ANCHO,
            PIEZA_ALTO,
            PIEZA_PROFUNDO,
            PIEZA_NOMBRECOLOR,
            PIEZA_NOMBREDISTRIBUCION,
            PIEZA_NOMBREFAMILIA,
            PIEZA_NOMBRELINEA,
            PIEZA_NOMBREMATERIAL,
            PIEZA_NOMBREMODOCONSTRUCTIVO,
            PIEZA_NOMBREMODOSUSTENTACION,
            PIEZA_NOMBRETIPOENTIDAD,
            PIEZA_NOMBRETIPOMUEBLE,
            PIEZA_URL_BPP_INTERNA,
            PIEZA_URL_PLANO_INTERNA,
            PIEZA_CODIGOAGUJEREADO,
            PIEZA_CODIGOCORTE,
            PIEZA_CODIGORANURA,
            PIEZA_CODIGOTIPOPIEZA,
            PIEZA_NOMBREVETA,
            PIEZA_ESPESORFILODER,
            PIEZA_ESPESORFILOINF,
            PIEZA_ESPESORFILOIZQ,
            PIEZA_ESPEESORFILOSUP,
            PIEZA_TAPACANTO_DERECHO,
            PIEZA_TAPACANTO_INFERIOR,
            PIEZA_TAPACANTO_IZQUIERDO,
            PIEZA_TAPACANTO_SUPERIOR,
            PIEZA_NOMBREMODELO,
            DocumentoOrigen,
            SO,
            PRODUCTO_TERMINADO,
            CODIGO_PT,
            PT_CATEGORIA,
            PT_NOMBREFAMILIA,
            PT_NOMBRETIPOMUEBLE,
            PT_NOMBRELINEA,
            OP,
            TIPO_PIEZA_INDUSTRIAL,
            TIPO_PIEZA_PROGRAMACION,
            RUTA_ASIGNADA,
            ANCHO_CORTE,
            ALTO_CORTE,
            ANCHO_VS_FINAL,
            ALTO_VS_FINAL,
            FILOS,
            CODIGO_COLOR,
            CODIGO_SELCO,
            VETA_SELCO,
            PESO_PIEZAS,
            PASADAS_STF,
            PRECIO_FRTES_VIDRIO,
            PRECIO_LUSTRE,
            PRECIO_TURU,
            SUP,
            PERIMETRO,
            CANTIDAD_2,
            idModulo,
            VACIO_4,
            VACIO_5,
            VACIO_6,
            VACIO_7,
            VACIO_8,
            VACIO_9,
            VACIO_10,
            CANT_AMBIENTES,
            PESO,
            PIEZA_CANTIDAD_ORIGINAL,
            ORDEN_MANU_ORIGINAL,
            AMBIENTE,
            N_PALLET,
            POSICION,
            fechaCarga,
            lecturaGBN1,
            fechaLecturaGBN1,
            lecturaSLC,
            fechaLecturaSLC,
            lecturaNST,
            fechaLecturaNST,
            lecturaSTF,
            fechaLecturaSTF,
            lecturaMRT1,
            fechaLecturaMRT1,
            lecturaMRT2,
            fechaLecturaMRT2,
            lecturaMRT3,
            fechaLecturaMRT3,
            lecturaMRT4,
            fechaLecturaMRT4,
            lecturaIDM,
            fechaLecturaIDM,
            lecturaRVR,
            fechaLecturaRVR,
            lecturaCHN,
            fechaLecturaCHN,
            lecturaFTAL1,
            fechaLecturaFTAL1,
            lecturaKBT,
            fechaLecturaKBT,
            lecturaVTP1,
            fechaLecturaVTP1,
            lecturaLEA,
            fechaLecturaLEA,
            lecturaPLTER,
            fechaLecturaPLTER,
            lecturaGBM,
            fechaLecturaGBM,
            lecturaPRS,
            fechaLecturaPRS,
            lecturaKBT1,
            fechaLecturaKBT1,
            lecturaKBT2,
            fechaLecturaKBT2,
            lecturaALU,
            fechaLecturaALU,
            lecturaPLACARD,
            fechaLecturaPLACARD,
            lecturaPEGADO,
            fechaLecturaPEGADO,
            lecturaAGUJEREADO,
            fechaLecturaAGUJEREADO
        )

        # Execute sql Query
        cursor.execute(query, values)

    # Commit the transaction
    con.commit()
    con.close()

    remove(nombre_archivo)
    remove('basePiezasLimpia.xlsx')
