from dotenv import load_dotenv
import os
import pyodbc
import logging
import json
from datetime import time

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

driver = os.getenv('SQL_DRIVER')
server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')

connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

def serialize_row(row: dict) -> dict:
    """
    Convierte los valores de tiempo en un diccionario a cadenas.
    """
    for key, value in row.items():
        if isinstance(value, time):
            row[key] = value.strftime("%H:%M:%S")
    return row

async def get_db_connection():
    try:
        logger.info(f"Intentando conectar a la base de datos con la cadena de conexión: {connection_string}")
        conn = pyodbc.connect(connection_string, timeout=10)
        logger.info("Conexión exitosa a la base de datos.")
        return conn
    except pyodbc.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise Exception(f"Database connection error: {str(e)}")

async def fetch_query_as_json(query: str, params: tuple = ()):
    conn = await get_db_connection()
    cursor = conn.cursor()
    logger.info(f"Ejecutando query: {query}")
    try:
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        results = []
        logger.info(f"Columns: {columns}")
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            serialized_row = serialize_row(row_dict)
            results.append(serialized_row)

        return json.dumps(results)

    except pyodbc.Error as e:
        raise Exception(f"Error ejecutando el query: {str(e)}")
    finally:
        cursor.close()
        conn.close()