import pyodbc


class DataBase:
    def __init__(self):
        self.connection = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};"
                "Server=ANDRESPC;"
                "DataBase=Prueba;"
                "Trusted_Connection=yes;"
            )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()
