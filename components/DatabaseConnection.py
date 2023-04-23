from os import getenv

from mysql.connector import connect


class DatabaseConnection:
    def __init__(self,
                 host='localhost',
                 user=getenv('MYSQL_USERNAME'),
                 password=getenv('MYSQL_PASSWORD'),
                 database='school'
                 ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        return connection
