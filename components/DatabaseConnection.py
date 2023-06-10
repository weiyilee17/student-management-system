from os import getenv

from mysql.connector import connect, Error, errorcode


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
        try:
            connection = connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            return connection

        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
