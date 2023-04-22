from sqlite3 import connect


class DatabaseConnection:
    def __init__(self, database_file='database.db'):
        self.database_file = database_file

    def connect(self):
        connection = connect(self.database_file)
        return connection
