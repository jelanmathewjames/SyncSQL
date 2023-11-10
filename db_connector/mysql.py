import mysql.connector
from mysql.connector import Error
from decouple import config

def connect():
    try:
        connection = mysql.connector.connect(
            host=config('DB_HOST'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            port=config('DB_PORT')
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"create database if not exists {config('DB_NAME')} ;")
            cursor.execute("use mudb;")
            cursor.fetchall()
            cursor.close()
        return connection

    except Exception as e:
        print("Error while connecting to MySQL", e)
        return None
    
def getdata(connection, query):
    try:
        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
        print("Error while executing query to MySQL", e)
        return None
    
def execute(connection, query):
    try:
        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        cursor.close()
        connection.commit()
    except Error as e:
        print("Error while executing query to MySQL", e)
        return None

def execute_from_file(connection, file):
    try:
        with open(file) as sql_file:
            sql_as_string = sql_file.read()

        queries = sql_as_string.split(';')
        queries = [query.strip() for query in queries if query.strip()]

        for query in queries:
            cursor = connection.cursor()
            cursor.execute(query)
            cursor.close()

        connection.commit()
    except Exception as e:
        print("Error while executing query to MySQL", e)
        return None
    
def close(connection):
    try:
        if connection.is_connected():
            connection.close()
    except Exception as e:
        print("Error while closing connection to MySQL", e)

