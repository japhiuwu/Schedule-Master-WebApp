import json
import logging
import os
# import aiofiles

from fastapi import HTTPException, Depends
from fastapi import FastAPI, File, UploadFile, HTTPException

# from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

from datetime import datetime, timedelta
from dotenv import load_dotenv

from utils.database import fetch_query_as_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_SAK")
# AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

# blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

async def fetch_seccion_carrera(carrera: str, clase: int, seccion: int):
    query = f"SELECT * FROM sm.Vista_Secciones WHERE Cod_Carrera = ? AND Cod_Clase = ? AND  Cod_Seccion = ?;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (carrera, clase, seccion))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def update_seccion(periodo: str, carrera: str, clase: int, seccion: int):
    query = f"EXEC sm.sp_ActualizarSeccion @Cod_Periodo = '2024-01', @Cod_Carrera = 'IS', @Cod_Clase = 115, @Cod_Seccion = 1, @Cod_Edificio = 'ED01', @Num_Aula = 101, @Num_Empleado = 'E123456789', @Cupos = 30, @Dias = 'Lunes, Miércoles', @Hora_Inicial = '08:00:00', @Hora_Final = '10:00:00', @Portada = 'Nueva portada';"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (periodo, carrera, clase, seccion))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def delete_seccion(periodo: str, carrera: str, clase: int, seccion: int):
    query = f"EXEC sm.sp_EliminarSeccion @Cod_Periodo = ?, @Cod_Carrera = ?, @Cod_Clase = ?, @Cod_Seccion = 1?;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (periodo, carrera, clase, seccion))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
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
    
