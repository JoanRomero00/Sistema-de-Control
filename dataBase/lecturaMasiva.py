from .connection import DataBase
from .helpers import fecha


class LecturaMasiva(DataBase):
    def lista_ops(self, maquina):
        self.cursor.execute("SELECT DISTINCT OP FROM basePiezas WHERE lectura" + maquina + " = 0 ORDER BY OP")
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

    def lista_colores(self, op):
        self.cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR FROM basePiezas WHERE OP=? ORDER BY OP", op)
        records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        self.close()
        return OutputArray

    def lista_espesores(self, color, op):
        self.cursor.execute("SELECT DISTINCT OP, PIEZA_NOMBRECOLOR, PIEZA_PROFUNDO FROM basePiezas WHERE OP=? "
                            "AND PIEZA_NOMBRECOLOR=? ORDER BY OP", op, color)
        records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        self.close()
        return OutputArray

    def calcular_cant(self, op, color, espesor):
        self.cursor.execute("SELECT COUNT(idPieza) as CANTIDAD FROM basePiezas WHERE OP=? "
                            "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=?", op, color, espesor)
        records = self.cursor.fetchall()
        OutputArray = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            OutputArray.append(dict(zip(columnNames, record)))
        self.close()
        return OutputArray

    def verificar_lectura(self, op, color, espesor, maquina):
        complete = "SELECT idPieza FROM basePiezas WHERE OP=? " \
                   "AND PIEZA_NOMBRECOLOR=? AND PIEZA_PROFUNDO=? AND lectura" + maquina + " = 0"
        self.cursor.execute(complete, op, color, espesor)
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
            complete = 'UPDATE dbo.basePiezas SET fechaLectura' + maquina + ' = ?, lectura' + maquina + ' = 1 ' \
                       'WHERE idPieza = ?'
            self.cursor.execute(complete, fecha(), id['idPieza'])
            self.cursor.commit()
        self.close()

    def verificar_pin(self, pin):
        self.cursor.execute("SELECT Usuario FROM tablaUsuario WHERE PIN = ?", pin)
        usuario = self.cursor.fetchone()
        self.close()
        if usuario is None:
            return None
        else:
            return usuario[0]

    def log_lecturaMasiva(self, usuario, op, color, espesor, maquina):
        self.cursor.execute("INSERT INTO Prueba.dbo.logLecturaMasiva (Usuario, fechaMod, OP, Color, Espesor, maquina) "
                            "VALUES (?,?,?,?,?,?)", usuario, fecha(), op, color, espesor, maquina)
        self.cursor.commit()
        self.close()
