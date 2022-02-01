import pyodbc


class DataBase:
    def __init__(self):
        self.connection = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=SERVER;"
            "DataBase=PRODUCCION_PLANTA;"
            "Trusted_Connection=yes;"
            "uid=sa;"
            "pwd=200sa;"
            )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
