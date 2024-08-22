import json
import logging
import os
# import aiofiles

from fastapi import HTTPException, Depends
from fastapi import FastAPI, File, UploadFile, HTTPException

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

from datetime import datetime, timedelta
from dotenv import load_dotenv

from utils.database import fetch_query_as_json
from models.seccion import seccion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_SAK")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

async def fetch_seccion_carrera(periodo: str, carrera: str, clase: int, seccion: int):
    query = f"SELECT * FROM sm.Vista_Secciones WHERE Cod_Carrera = ? AND Cod_Clase = ? AND Cod_Periodo = ? AND Cod_Seccion = ?;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (carrera, clase, periodo, seccion))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def update_seccion(periodo: str, carrera: str, clase: int, cod_seccion: int, edificio: str, aula: int, empleado: str, cupos: int, dias: str, inicio: str, fin: str, portada: str):
    query = """
    EXEC sm.Actualizar_Seccion_Proc 
        @Cod_Periodo = ?, 
        @Cod_Carrera = ?, 
        @Cod_Clase = ?, 
        @Cod_Seccion = ?, 
        @Cod_Edificio = ?, 
        @Num_Aula = ?, 
        @Num_Empleado = ?, 
        @Cupos = ?, 
        @Dias = ?, 
        @Hora_Inicial = ?, 
        @Hora_Final = ?, 
        @Portada = ?;
    """
    try:
        result_json = await fetch_query_as_json(query, (periodo, carrera, clase, cod_seccion, edificio, aula, empleado, cupos, dias, inicio, fin, portada), is_procedure=True)
        logger.info("Resultado de la ejecución del procedimiento: %s", result_json)
        return {"status": 200, "data": result_json}
    except Exception as e:
        logger.error("Error al ejecutar el procedimiento almacenado: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))



async def delete_seccion(periodo: str, carrera: str, clase: int, seccion: int):
    query = f"EXEC sm.Eliminar_Seccion_Proc @Cod_Periodo = ?, @Cod_Carrera = ?, @Cod_Clase = ?, @Cod_Seccion = ?;"
    result = {}
    try:
        logger.info(f"QUERY UPDATE")
        result_json = await fetch_query_as_json(query, (periodo, carrera, clase, seccion), is_procedure=True)
        result = json.loads(result_json)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result["status"] == 404:
        raise HTTPException(status_code=404, detail="Section not found")

    return result

async def create_seccion(section: seccion):
    print("ejecutando create seccion")
    query = f"EXEC sm.Crear_Seccion @Cod_Periodo = ?, @Cod_Carrera = ?, @Cod_Clase = ?, @Cod_Seccion = ?, @Cod_Edificio = ?, @Num_Aula = ?, @Num_Empleado = ?, @Cupos = ?, @Dias = ?, @Hora_Inicial = ?, @Hora_Final = ?, @Portada = ?;"
    result = {}
    try:
        result_json = await fetch_query_as_json(query, (section.Cod_Periodo, section.Cod_Carrera, section.Cod_Clase, section.Cod_Seccion ,section.Cod_Edificio, section.Num_Aula, section.Num_Empleado, section.Cupos, section.Dias, section.Hora_Inicial, section.Hora_Final, section.Portada), is_procedure=True)
        logger.info("Resultado de la ejecución del procedimiento: %s", result_json)
        return {"status": 200, "data": result_json}
    except Exception as e:
        logger.error("Error al ejecutar el procedimiento almacenado: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    return result
    
async def fetch_secciones_aula(edificio: str, aula: int, term: str):
    query = f"SELECT * FROM sm.Vista_Secciones WHERE Cod_Edificio = ? AND Num_Aula = ? AND Cod_Periodo = ? ORDER BY Cod_Seccion;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (edificio, aula, term))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def fetch_secciones_carrera(carrera: str, clase: int, term: str):
    query = f"SELECT * FROM sm.Vista_Secciones WHERE Cod_Carrera = ? AND Cod_Clase = ? AND Cod_Periodo = ? ORDER BY Cod_Seccion;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (carrera, clase, term))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
