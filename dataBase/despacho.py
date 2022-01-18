from .connection import DataBase


class Despacho(DataBase):
    def lista_cf(self, cf):
        if cf == 0:
            self.cursor.execute("SELECT DISTINCT CLIENTE_FINAL FROM baseModulos ORDER BY CLIENTE_FINAL")
        else:
            self.cursor.execute("SELECT FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP, COUNT(idOrdenManufactura) AS "
                                "TOTAL, "
                                "SUM(CASE WHEN lecturahorno >= 1 THEN 1 ELSE 0 END) AS TERMINADOS, "
                                "SUM(CASE WHEN (NOT lecturahorno >= 1) OR (lecturaHorno is Null) THEN 1 ELSE 0 END) "
                                "AS PENDIENTES "
                                "FROM baseModulos GROUP BY FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP "
                                "HAVING   (CLIENTE_FINAL = ?)", cf)
        records = self.cursor.fetchall()
        data = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            data.append(dict(zip(columnNames, record)))
        self.close()
        return data

    def lista_so(self, so):
        if so == 0:
            self.cursor.execute("SELECT DISTINCT SO FROM baseModulos ORDER BY SO")
        else:
            self.cursor.execute("SELECT FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP, COUNT(idOrdenManufactura) AS "
                                "TOTAL, "
                                "SUM(CASE WHEN lecturahorno >= 1 THEN 1 ELSE 0 END) AS TERMINADOS, "
                                "SUM(CASE WHEN (NOT lecturahorno >= 1) OR (lecturaHorno is Null) THEN 1 ELSE 0 END) "
                                "AS PENDIENTES "
                                "FROM baseModulos GROUP BY FRANQUICIA, SO, CLIENTE_FINAL, PT_PRODUCTO, OP "
                                "HAVING   (SO = ?)", so)
        records = self.cursor.fetchall()
        data = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            data.append(dict(zip(columnNames, record)))
        self.close()
        return data
