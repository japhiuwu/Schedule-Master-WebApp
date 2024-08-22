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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_SAK")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

async def fetch_facultades():
    query = f"SELECT * FROM sm.Facultades ORDER BY Nombre;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query)
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def fetch_carreras(id: int):
    query = f"SELECT * FROM sm.Carreras WHERE Cod_Facultad = ? ORDER BY Nombre;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (id))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def fetch_clases(carrera: str, term: str):
    query = f"""
    SELECT 
        c.Cod_Carrera, 
        ca.Nombre AS Carrera,
        c.Cod_Clase, 
        c.Nombre, 
        c.UV, 
        COALESCE(COUNT(s.Cod_Seccion), 0) AS Numero_Secciones
    FROM 
        sm.Clases c
    LEFT JOIN 
        sm.Carreras ca ON c.Cod_Carrera = ca.Cod_Carrera
    LEFT JOIN 
        sm.Secciones s
    ON 
        c.Cod_Carrera = s.Cod_Carrera 
        AND c.Cod_Clase = s.Cod_Clase
        AND s.Cod_Periodo = ?
    WHERE 
        c.Cod_Carrera = ?
    GROUP BY 
        c.Cod_Carrera, 
        c.Cod_Clase, 
        c.Nombre, 
        c.UV,
        ca.Nombre;
    """

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (term, carrera))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def fetch_clase(carrera: str, clase: int):
    query = f"SELECT * FROM sm.Clases WHERE Cod_Carrera = ? AND Cod_Clase = ?;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (carrera, clase))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))