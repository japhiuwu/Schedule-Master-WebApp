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

async def fetch_edificios():
    query = f"SELECT * FROM sm.Edificios ORDER BY Nombre;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query)
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def fetch_aulas(id: str):
    query = f"SELECT * FROM sm.Aulas WHERE Cod_Edificio = ?;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (id))
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
