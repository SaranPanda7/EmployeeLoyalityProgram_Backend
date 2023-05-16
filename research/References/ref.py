

# Upload image to blob storage and database also 

# @router.post("/uploadimage")
# async def create_upload_file(file: UploadFile  = File(...)):
    
#     name = file.filename
#     type = file.content_type
    
#     return await uploadtoazure(file=file,file_name=name,file_type=type,db=get_db)


# async def uploadtoazure(file: UploadFile,file_name: str,file_type:str , db: Session):
#     connect_str = "AccountName=evolutyzblobimages;AccountKey=E3J5jaiTaZD974NOHlpgqt76Bt9avAM/uneuZ4ZvSSHYSBxjY0JV15ZCjFLSb6TuWKZpeOw/a+gXOdlGZmxYmw==;BlobEndpoint=https://evolutyzblobimages.blob.core.windows.net/;FileEndpoint=https://evolutyzblobimages.file.core.windows.net/;QueueEndpoint=https://evolutyzblobimages.queue.core.windows.net/;TableEndpoint=https://evolutyzblobimages.table.core.windows.net/"
#     blob_service_client = BlobServiceClient.from_connection_string(connect_str)
#     container_name = "elp"
    
#     async with blob_service_client:
            
           
#             container_client = blob_service_client.get_container_client(container_name)
#             try:


#                 blob_client = container_client.get_blob_client(file_name)
#                 f = await file.read()
#                 await blob_client.upload_blob(f, content_settings =  ContentSettings(content_type=file_type))
#                 image_url = blob_client.url
               
#             except Exception as e:
#                 print(e)
#                 return HTTPException(401, "Something went terribly wrong..")

#             conn = psycopg2.connect(
#                 host="localhost",
#                 database="ELPnew",
#                 user="postgres",
#                 password="Password"
#              )
#             cursor = conn.cursor()
#             cursor.execute("INSERT INTO dev.images (title ) VALUES (%s)", (file_name))
#             conn.commit()

           
#     return (file_name)


# --------------------------------------------------------------------------------------------------------------------

# @router.post(
#     "/banner/create", status_code=status.HTTP_201_CREATED,
# )
# async def add_banner(banner: CreateSchemaBanner, db: Session = Depends(get_db)):
#     data = dashboard_crud.create_banner(db=db, banner=banner)
#     if data is None:
#         return JSONResponse(
#             status_code=404, content={"Message": "Banner Already Exists"}
#             )
#     return JSONResponse(
#         status_code=200, content={"Message": "Banner Created Successfully"}
#         )


# @router.get(
#     "/banner_images/all", status_code=status.HTTP_200_OK, response_model=Page[SchemaBanner]
# )
# async def get_banner( db: Session = Depends(get_db)):
#     data = dashboard_crud.get_banner_from_db(db)

#     logger.info(data)

#     return paginate(data)

# ---------------------------------------------------------------------------------------------------------

# def get_top_performance_count_from_db(db:Session):

#     try:

#         stmt = db.query(
#             Reward.id, Reward.points, func.count(
#                 Reward.id).label("count")
#             ).group_by(Reward.id).subquery()

#         return [dict(id=r.id, title=r.title, get_assigned_reward_count=0 if get_assigned_reward_count is None else get_assigned_reward_count) for r, get_assigned_reward_count in db.query(Reward, stmt.c.count).outerjoin(stmt, Reward.id == stmt.c.id).order_by(Reward.points).all()]

#     except SQLAlchemyError as e:
#         return None  

# --------------------------------------------------------------------------------------------------------------


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

#-----------------------------------------------------------------------------------------------------------


# get all the profile_images from db

# @router.get("/Profile_images/all")
# def get_images():
#     conn = psycopg2.connect(
#         dbname="ELPnew",
#         user="postgres",
#         password="Password",
#         host="localhost",
#         port="5432"
#     )
#     cur = conn.cursor()
#     cur.execute("SELECT id ,image_title FROM dev.user_profile_images")
#     rows = cur.fetchall()
#     conn.close()

    # blob_url = "https://evolutyzblobimages.blob.core.windows.net/elp/"
    # image_urls = [blob_url + row[0] for row in rows]

    # return {"image_urls": image_urls}
    # json_list = []
    # blob_url = "https://evolutyzblobimages.blob.core.windows.net/elp/"
    # for row in rows:
    #     json_data = {"Profile_image_url": [blob_url + row[1] ], "Profile_image_id": [row[0]]}
    #     json_list.append(json_data)
    # cur.close()
    # conn.close()
    # return JSONResponse(content=json_list)