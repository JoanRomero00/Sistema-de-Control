from .connection import DataBase


class Despacho(DataBase):
    def lista_cf(self, cf):
        if cf == 0:
            self.cursor.execute("SELECT DISTINCT CLIENTE_FINAL FROM dbo.TableroDESPACHO ORDER BY CLIENTE_FINAL")
        else:
            self.cursor.execute("SELECT [FRANQUICIA],[SO],[CLIENTE_FINAL],[PT_PRODUCTO],[OP],[TOTAL],[TERMINADOS],"
                                "[PENDIENTES] FROM [dbo].[TableroDESPACHO] "
                                "WHERE CLIENTE_FINAL = ? ", cf)
        records = self.cursor.fetchall()
        data = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            data.append(dict(zip(columnNames, record)))
        self.close()
        return data

    def lista_so(self, so):
        if so == 0:
            self.cursor.execute("SELECT DISTINCT SO FROM dbo.TableroDESPACHO ORDER BY SO")
        else:
            self.cursor.execute("SELECT [FRANQUICIA],[SO],[CLIENTE_FINAL],[PT_PRODUCTO],[OP],[TOTAL],[TERMINADOS],"
                                "[PENDIENTES] FROM [dbo].[TableroDESPACHO] "
                                "WHERE SO = ? ", so)
        records = self.cursor.fetchall()
        data = []
        columnNames = [column[0] for column in self.cursor.description]
        for record in records:
            data.append(dict(zip(columnNames, record)))
        self.close()
        return data
