from .connection import DataBase


class Informe(DataBase):
    def piezas_noleidas(self, maquina):
        self.cursor.execute("SELECT idPieza, OP, PIEZA_DESCRIPCION, RUTA_ASIGNADA, PIEZA_CODIGO "
                            "FROM TableroBase_" + maquina +
                            " WHERE lectura = 0")
        data = self.cursor.fetchall()
        self.close()
        return data
