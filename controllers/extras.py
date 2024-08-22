import json
import logging
import os
import aiofiles

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

async def fetch_docentes(id: str):
    query = f"SELECT * FROM sm.Vista_Docentes WHERE Cod_Carrera = ? ORDER BY Primer_Nombre;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query, (id))
        result_dict = json.loads(result_json)
        
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def fetch_terms():
    query = f"SELECT * FROM sm.Vista_Periodos_Academicos ORDER BY Orden, Fecha_Inicio;"

    try:
        logger.info(f"QUERY LIST")
        result_json = await fetch_query_as_json(query)
        result_dict = json.loads(result_json)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def fetch_upload_profile( codPeriodo: str, codSeccion: int, codCarrera: str, codClase: int, files: list[UploadFile] = File(...) ):
    try:
        for file in files:

            query = f"UPDATE sm.Secciones SET Portada = ? WHERE Cod_Periodo = ? AND Cod_Seccion = ? AND Cod_Carrera = ? AND Cod_Clase = ?;
'"
            result_json = await fetch_query_as_json(query, (file.filename, codPeriodo, codSeccion, CodCarrera) is_procedure=True)
            result = json.loads(result_json)[0]

            if result["status"] == 404:
                raise HTTPException(status_code=404, detail="Seccion not found")

            container_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=f"{codPeriodo}/{codCarrera}/{codClase}/{codSeccion}/{file.filename}")
            async with aiofiles.open({file.filename}, 'wb') as f:
                await f.write(await file.read())
            with open({file.filename}, "rb") as data:
                container_client.upload_blob(data, overwrite=True)


        return {"message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def fetch_profile(codPeriodo: str, codSeccion: int, codCarrera: str, codClase: int):
    sas_expiration = datetime.utcnow() + timedelta(minutes=2)

    query = f"""
        SELECT Portada FROM sm.Vista_Secciones WHERE Cod_Carrera = ? AND Cod_Clase = ? AND  Cod_Seccion = ? AND Cod_Periodo = ?;
    """

    try:
        result_json = await fetch_query_as_json(query)
        result_dict = json.loads(result_json)

        for file in result_dict:
            file_name = f"{ file['card_id'] }/{ file['file_name'] }"
            # Genera el SAS
            sas_token = generate_blob_sas(
                account_name=blob_service_client.account_name,
                container_name=AZURE_STORAGE_CONTAINER,
                blob_name=file_name,
                account_key=blob_service_client.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=sas_expiration
            )

            file["url"] = f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER}/{file_name}?{sas_token}"

        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))