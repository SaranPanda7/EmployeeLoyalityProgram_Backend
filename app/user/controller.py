from typing import List
from click import File
from fastapi import APIRouter, Depends, HTTPException, status,FastAPI, File, UploadFile,Response
from fastapi_pagination import Page, add_pagination, paginate
from loguru import logger
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from fastapi_filter import FilterDepends
from app.db.session import get_db
from app.user import crud as user_crud
from app.user.models import User
from app.user.schema import CreateUserSchema, SchemaUser, SchemaAssignReward
from app.user.filter import UserFilter
from fastapi import FastAPI, HTTPException, UploadFile
from azure.storage.blob.aio import BlobServiceClient
import psycopg2
from io import BytesIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import datetime


router = APIRouter()



@router.get(
    "/all", status_code=status.HTTP_200_OK, response_model=Page[SchemaUser]
)
async def get_users_from_db(db: Session = Depends(get_db)):

    data = user_crud.get_users_from_db(db)

    return paginate(data)


@router.post("/create")
async def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):

    data = user_crud.get_user(
        db=db, email_id=user.email_id, employee_id=user.employee_id
    )

    if data is not None:
        return JSONResponse(
            status_code=400, content={"message": "user already exist"}
        )

    data = user_crud.create_user(db=db, user=user)
    if data is None:
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )

    return JSONResponse(status_code=200, content={"message": "success"})


@router.put("/update")
async def update_user():

    data = user_crud.update_user(user_id=user_id, user=user, db=db)

    if data is None:
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )
    return data


@router.get(
    "/me/{id}", status_code=status.HTTP_200_OK, response_model=SchemaUser
)
async def me(id: str, db: Session = Depends(get_db)):
    try:
        return user_crud.get_me_from_db(db, id)
    except Exception as e:
        logger.error(e)


@router.delete("/{id}")
async def delete_user(id: str):
    """Delete A User"""
    data = user_crud.delete_user(id=id, db=db)

    if data is None:
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )
    return JSONResponse(status_code=200, content={"message": "success"})


@router.post("/assignreward")
async def assign_reward(details: SchemaAssignReward, db: Session = Depends(get_db)):

    data = user_crud.create_user_reward(db=db, details=details)

    if data is None:
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )

    return JSONResponse(status_code=200, content={"message": "success"})





# Update profile image to blob and database at same time

connection_string = "AccountName=evolutyzblobimages;AccountKey=E3J5jaiTaZD974NOHlpgqt76Bt9avAM/uneuZ4ZvSSHYSBxjY0JV15ZCjFLSb6TuWKZpeOw/a+gXOdlGZmxYmw==;BlobEndpoint=https://evolutyzblobimages.blob.core.windows.net/;FileEndpoint=https://evolutyzblobimages.file.core.windows.net/;QueueEndpoint=https://evolutyzblobimages.queue.core.windows.net/;TableEndpoint=https://evolutyzblobimages.table.core.windows.net/"
container_name = "elp"

@router.post("/uploadProfileImage/")
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
    blob_client.upload_blob(file.file.read(), content_type=file.content_type)

    
    conn = psycopg2.connect(
        host="localhost",
        database="ELPnew",
        user="postgres",
        password="Password"
        )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dev.user_profile_images (image_title) VALUES (%s)", (file_name,))
    conn.commit()

           
    return (file_name)


# get all the profile_images from db

@router.get("/Profile_images/all")
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
    cur.execute("SELECT id ,image_title FROM dev.user_profile_images")
    rows = cur.fetchall()
    conn.close()

    json_list = []
    blob_url = "https://evolutyzblobimages.blob.core.windows.net/elp/"
    for row in rows:
        json_data = {"Profile_image_url": [blob_url + row[1] ], "Profile_image_id": [row[0]]}
        json_list.append(json_data)
    cur.close()
    conn.close()
    return JSONResponse(content=json_list)



