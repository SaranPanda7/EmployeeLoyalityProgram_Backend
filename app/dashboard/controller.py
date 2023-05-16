from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,FastAPI, File, UploadFile,Response
from fastapi_pagination import Page, add_pagination, paginate
from loguru import logger
from sqlalchemy.orm import Session 
from sqlalchemy import select
from starlette.responses import JSONResponse
from app.dashboard import crud as dashboard_crud 
from app.dashboard.schema import SchemaUserRewardCount, CreateSchemaBanner, SchemaBanner , UpdateSchemaBanner , SchemaTopPerformance, SchemaPerformer, SchemaGetAllImages
from app.db.session import get_db
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient,ContentSettings
from azure.storage.blob import PublicAccess
from sqlalchemy.sql import text
import os
from app.dashboard.crud import Images
from fastapi import FastAPI, HTTPException, UploadFile
from azure.storage.blob.aio import BlobServiceClient
import psycopg2
from io import BytesIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import datetime



router = APIRouter()



#Get all assigned reward count
@router.get(
    "/assignedRewardCount", status_code=status.HTTP_200_OK, response_model=Page[SchemaUserRewardCount]
)
async def assigned_reward_count(db: Session = Depends(get_db)):

    data = dashboard_crud.get_assigned_reward_count(db)

    logger.info(type(data))

    return paginate(data)


#Get all the top performance count
@router.get(
    "/topPerformanceCount", status_code=status.HTTP_200_OK, response_model=Page[SchemaTopPerformance]
    )
async def get_top_performance_count_from_db(db: Session = Depends(get_db)):

    data = dashboard_crud.get_top_performance_count_from_db(db)
    
    logger.info(type(data))
    
    return paginate(data)



# # Upload image to blob storage and database also 
connection_string = "AccountName=evolutyzblobimages;AccountKey=E3J5jaiTaZD974NOHlpgqt76Bt9avAM/uneuZ4ZvSSHYSBxjY0JV15ZCjFLSb6TuWKZpeOw/a+gXOdlGZmxYmw==;BlobEndpoint=https://evolutyzblobimages.blob.core.windows.net/;FileEndpoint=https://evolutyzblobimages.file.core.windows.net/;QueueEndpoint=https://evolutyzblobimages.queue.core.windows.net/;TableEndpoint=https://evolutyzblobimages.table.core.windows.net/"
container_name = "elp"

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1]  # Get the extension of the file
    if extension not in ["png", "jpg"]:
        return {"error": "Only PNG and JPG files are allowed"}
    # Generate a unique file name using a timestamp
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") 
    file_name = f"{timestamp}_{file.filename}"

    # Create a BlobServiceClient object using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get a reference to the container
    container_client = blob_service_client.get_container_client(container_name)

    # Upload the file to the container
    blob_client = container_client.get_blob_client(file_name)
    blob_client.upload_blob(file.file.read() , content_type=file.content_type)

    
    conn = psycopg2.connect(
        host="localhost",
        database="ELPnew",
        user="postgres",
        password="Password"
        )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dev.images (title) VALUES (%s)", (file_name,))
    conn.commit()

           
    return (file_name)

# get all the images using GET method
@router.get("/images/all")
def get_images():
    conn = psycopg2.connect(
        dbname="elp",
        user="postgres",
        password="Password",
        host="192.168.75.209",
        port="5432"
    )


    # postgresql://postgres:Password@192.168.75.209:5432/elp


    cur = conn.cursor()
    cur.execute("SELECT id ,title FROM dev.images")
    rows = cur.fetchall()
    conn.close()
    json_list = []
    blob_url = "https://evolutyzblobimages.blob.core.windows.net/elp/"
    for row in rows:
        json_data = {"banner_image_url": [blob_url + row[1] ], "banner_image_id": [row[0]]}
        json_list.append(json_data)
    cur.close()
    conn.close()
    return JSONResponse(content=json_list)



@router.delete("/banner/{title}", status_code=status.HTTP_200_OK)
async def delete_banner(title: str , db:Session = Depends(get_db)):
    """Delete A Banner"""
    data = dashboard_crud.delete_banner(title=title, db=db)

    if data is None:
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )
    return JSONResponse(status_code=200, content={"message": "Banner Deleted Successfully"})



@router.put("/banner/{title}", status_code=status.HTTP_200_OK,)

async def update_banner( title: str , banner: UpdateSchemaBanner, db: Session = Depends(get_db)):
    """Update A Banner"""
    data = dashboard_crud.update_banner(title= title , db = db , banner = banner)

    if data is None:
        return JSONResponse(
            status_code=500 , content={"message" : "Internal Server Error"}
        )
    return JSONResponse(status_code=200 , content={"message" : "Banner Updated Successfully"})



@router.get(
    "/topPerformerPoints", status_code=status.HTTP_200_OK, response_model=Page[SchemaPerformer]
    )
async def get_performer_count_from_db(db: Session = Depends(get_db)):

    data = dashboard_crud. get_top_performer_count_from_db(db)
    
    logger.info(type(data))
    
    return paginate(data)