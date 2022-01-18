from .connection import DataBase
from .helpers import fecha


class Control(DataBase):
    def getTabla(self, maquina):
        hoy = fecha()[:10]
        if maquina == "HORNO":
            complete = "SELECT TOP 8 idOrdenManufactura, PT_PRODUCTO FROM baseModulos " \
                       "where CONVERT (DATE, fechaLecturaHORNO) = ? ORDER BY fechaLecturaHorno DESC"
        else:
            complete = "SELECT TOP 8 idPieza, PIEZA_DESCRIPCION FROM basePiezas " \
                       "where CONVERT (DATE, fechaLectura" + maquina + ") = ? ORDER BY fechaLectura" + maquina + " DESC"
        self.cursor.execute(complete, hoy)
        data = self.cursor.fetchall()
        self.close()
        return data

    def verificar_cod(self, codigo, maquina):
        if maquina == "HORNO":
            complete = "SELECT (CASE WHEN lecturahorno >= 1 THEN 1 ELSE 0 END) as VER FROM baseModulos " \
                       "WHERE idOrdenManufactura=?"
        else:
            complete = "SELECT (CASE WHEN lectura" + maquina + " >= 1 THEN 1 ELSE 0 END) FROM basePiezas " \
                        "WHERE idPieza=?"
        self.cursor.execute(complete, codigo)
        data = self.cursor.fetchone()
        self.close()
        if data is not None:
            data = data[0]
        return data

    def updatePM(self, codigo, maquina):
        if maquina == "HORNO":
            complete = "UPDATE dbo.baseModulos SET fechaLecturaHorno = ?, lecturaHorno = 1 " \
                       "WHERE idOrdenManufactura = ?"
        else:
            complete = "UPDATE dbo.basePiezas SET fechaLectura" + maquina + " = ?, lectura" + maquina + " = 1 " \
                        "WHERE idPieza = ?"
        self.cursor.execute(complete, fecha(), codigo)
        self.cursor.commit()
        self.close()
