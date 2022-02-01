from .connection import DataBase
from .helpers import fecha


class LecturaMasiva(DataBase):
    def lista_ops(self, maquina):
        self.cursor.execute("SELECT DISTINCT OP FROM produccion.basePiezas555 WHERE lectura" + maquina + " = 0 "
                            "AND RUTA_ASIGNADA LIKE '%"+ maquina +"%' ORDER BY OP")
        records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        self.close()
        lista = []
        for op in OutputArray:
            lista.append(op['OP'])
        return lista

    def lista_colores(self, op, maquina):
        self.cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR FROM produccion.basePiezas555 "
                            "WHERE OP=? AND RUTA_ASIGNADA LIKE '%"+ maquina +"%' AND "
                            "lectura" + maquina + " = 0 ORDER BY OP", op)
        records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        self.close()
        return OutputArray

    def lista_espesores(self, color, op, maquina):
        self.cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR, PIEZA_PROFUNDO FROM produccion.basePiezas555 WHERE OP=? "
                            "AND PIEZA_NOMBRECOLOR=? AND RUTA_ASIGNADA LIKE '%"+ maquina +"%' ORDER BY OP", op, color)
        records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        self.close()
        return OutputArray

    def lista_piezas(self, op, color, espesor, maquina):
        self.cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR, PIEZA_PROFUNDO, PIEZA_DESCRIPCION "
                            "FROM produccion.basePiezas555 " 
                            "WHERE OP=? AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=? AND RUTA_ASIGNADA "
                            "LIKE '%" + maquina + "%'", op, color, espesor)
        records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        self.close()
        return OutputArray

    def calcular_cant(self, op, color, espesor, pieza, maquina):
        if pieza == 1:
            self.cursor.execute("SELECT COUNT(idPieza) as CANTIDAD FROM produccion.basePiezas555 WHERE OP=? "
                                "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=? AND RUTA_ASIGNADA LIKE '%"+ maquina +"%'",
                                op, color, espesor)
            records = self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT COUNT(idPieza) as CANTIDAD FROM produccion.basePiezas555 WHERE OP=? "
                                 "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=? AND PIEZA_DESCRIPCION=? "
                                "AND RUTA_ASIGNADA LIKE '%" + maquina + "%'",
                                op, color, espesor, pieza)
            records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        self.close()
        return OutputArray

    def verificar_lectura(self, op, color, espesor, pieza, maquina):
        if pieza == 'Pieza':
            complete = "SELECT idPieza FROM produccion.basePiezas555 WHERE OP=? " \
                       "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=?" \
                       " AND lectura" + maquina + " = 0 AND RUTA_ASIGNADA LIKE '%" + maquina + "%'"
            self.cursor.execute(complete, op, color, espesor)
            records = self.cursor.fetchall()
        else:
            complete = "SELECT idPieza FROM produccion.basePiezas555 WHERE OP=? " \
                       "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=? AND PIEZA_DESCRIPCION=?" \
                       " AND lectura" + maquina + " = 0 AND RUTA_ASIGNADA LIKE '%" + maquina + "%'"
            self.cursor.execute(complete, op, color, espesor, pieza)
            records = self.cursor.fetchall()
        if not records:
            self.close()
            return 1
        ids = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            ids.append(dict(zip(columnNames, record)))
        self.close()
        return ids

    def updateMasivo(self, ids, maquina):
        for id in ids:
            complete = 'UPDATE produccion.basePiezas555 SET fechaLectura' + maquina + ' = ?, lectura' + maquina + ' = 1 ' \
                       'WHERE idPieza = ?'
            self.cursor.execute(complete, fecha(), id['idPieza'])
            self.cursor.commit()
        self.close()

    def verificar_pin(self, pin):
        self.cursor.execute("SELECT Usuario FROM produccion.tablaUsuario WHERE PIN = ?", pin)
        usuario = self.cursor.fetchone()
        self.close()
        if usuario is None:
            return None
        else:
            return usuario[0]

    def log_lecturaMasiva(self, usuario, op, color, espesor, maquina, pieza):
        if pieza is None:
            self.cursor.execute("SELECT COUNT(idPieza) as CANTIDAD FROM produccion.basePiezas555 WHERE OP=? "
                                "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=? AND RUTA_ASIGNADA LIKE '%"+ maquina +"%'",
                                op, color, espesor)
            records = self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT COUNT(idPieza) as CANTIDAD FROM produccion.basePiezas555 WHERE OP=? "
                                "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=? AND PIEZA_DESCRIPCION=? "
                                "AND RUTA_ASIGNADA LIKE '%" + maquina + "%'",
                                op, color, espesor, pieza)
            records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        cant = OutputArray[0]['CANTIDAD']
        self.cursor.execute("INSERT INTO produccion.logLecturaMasiva "
                            "(Usuario, fechaMod, OP, Color, Espesor, maquina, Pieza, Cantidad) "
                            "VALUES (?,?,?,?,?,?,?,?)", usuario, fecha(), op, color, espesor, maquina, pieza, cant)
        self.cursor.commit()
        self.close()

    def getTablaLecturaMasiva(self, maquina):
        self.cursor.execute("SELECT TOP 8 * FROM produccion.logLecturaMasiva WHERE maquina = ?", maquina)
        records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        return OutputArray
