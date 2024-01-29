from typing import Union, Annotated

from sql_app import crud, models, schemas
# from mysql_app.database import get_poi
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine
from fastapi import FastAPI, Query, Path, Depends, File, Form, UploadFile, HTTPException, Header, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import json
import pandas as pd
import io
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="POIApp",
    description="This is an api app for township api and poi",
    summary="Developed my HAS.",
    version="0.0.1",
    terms_of_service="https://dpsmap.com/terms/",
    contact={
        "name": "Contact Me",
        "url": "https://dpsmap.com/contact/",
        "email": "dm@dpsmap.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


origins = [
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# usercode
# check user authentication
async def get_current_user(email: str, password: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )    
    user = crud.get_user_by_email_password(
        db, email=email, password=password)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user.is_active != True:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/v1/user/", response_model=schemas.User)
def create_user(token: Annotated[str | None, Header()], user: schemas.UserCreate, db: Session = Depends(get_db)):
    token_exit = crud.check_supertoken(db=db, token=token)
    if not token_exit:
        raise HTTPException(
                status_code=400, detail="Token Validation Failed")
    else:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db=db, user=user)


@app.get("/v1/user/get")
def get_token(email: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email_password(
        db, email=email, password=password)
    if db_user:
        exit_token = crud.get_token_by_email(db=db, email=email)
        if exit_token:
            return exit_token
        else:
            access_token_expires = timedelta(minutes=30)
            access_token = crud.create_access_token(
            db, data={"sub": db_user.email}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=400, detail="Email and password did not match or Is not Activate")


@app.get("/v1/city/{city_name}")
def read_city(city_name: Annotated[str, Path(regex="Yangon", title="We still only accept yangon")]):
    json_file_path = "json/city/yangon.json"
    try:
        with open(json_file_path, "r") as file:
            # Load the JSON data from the file
            data = json.load(file)
        return data  # Return the JSON data as the API response
    except FileNotFoundError:
        # Handle the case when the file is not found
        return {"error": "File not found"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


@app.get("/v1/city/{city_name}/township/{township_name}")
def read_city_township(city_name: Annotated[str, Path(regex="Yangon", title="We still only accept yangon")], township_name: Union[str, None] = None):

    json_file_path = crud.read_township(township_name)
    try:
        with open(json_file_path, "r") as file:
            # Load the JSON data from the file
            data = json.load(file)
        return data  # Return the JSON data as the API response
    except FileNotFoundError:
        # Handle the case when the file is not found
        return {"error": "File not found"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


@app.post("/v1/poi", response_model=schemas.PoiCreate)
def create_poi(token: Annotated[str | None, Header()], poi: schemas.PoiCreate, db: Session = Depends(get_db)):
    token_exit = crud.check_supertoken(db=db, token=token)
    if not token_exit:
        raise HTTPException(
                status_code=400, detail="Token Validation Failed")
    else:
        return crud.create_poi(db=db, poi=poi)


@app.get("/v1/poi", response_model=list[schemas.Poi])
def read_items(token: Annotated[str | None, Header()],skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    token_exit = crud.get_token(db=db, token=token)
    if not token_exit:
        raise HTTPException(
                status_code=400, detail="Token Validation Failed")
    else:
        return crud.get_poi(db, skip=skip, limit=limit)


@app.post("/v1/poi/search")
def read_poi(token: Annotated[str | None, Header()], poi: schemas.PoiSearch, db: Session = Depends(get_db)):
    token_exit = crud.get_token(db=db, token=token)
    if not token_exit:
        raise HTTPException(
                status_code=400, detail="Token Validation Failed")
    else:
        return crud.search_poi(db=db, poi=poi)


@app.post("/v1/poi/uploadfile")
async def fetch_file(
    token: Annotated[str | None, Header()],file: Annotated[UploadFile, File()], db: Session = Depends(get_db)
):
    token_exit = crud.check_supertoken(db=db, token=token)
    if not token_exit:
        raise HTTPException(
                status_code=400, detail="Token Validation Failed")
    else:
        try:
            if not file.filename.endswith('.csv'):
                raise HTTPException(
                    status_code=400, detail="Only CSV Files are allowed")
            csv_data = await file.read()

            df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')))
            row_dicts = []
            crud.drop_poi(db=db)
            for index, row in df.iterrows():
                # csv_dict = df.iloc[5].to_dict()
                row_dict = row.to_dict()
                data_dict = {
                    "sort_id": str(row_dict['Sort_ID']),
                    "dps_id": str(row_dict['DPS_ID']),
                    "source_id": str(row_dict['Source_ID']),
                    "uid": str(row_dict['UID']),
                    "poi_n_eng": str(row_dict['POI_N_Eng']),
                    "poi_n_myn": str(row_dict['POI_N_Myn3']),
                    "types": str(row_dict['Type']),
                    "type_code": str(row_dict['Type_Code']),
                    "sub_type": str(row_dict['Sub_Type']),
                    "sub_type_code": str(row_dict['Sub_Type_Code']),
                    "postal_code": str(row_dict['Postal_Code']),
                    "st_n_eng": str(row_dict['St_N_Eng']),
                    "st_n_myn": str(row_dict['St_N_Myn3']),
                    "ward_n_eng": str(row_dict['Ward_N_Eng']),
                    "ward_n_myn": str(row_dict['Ward_N_Myn3']),
                    "tsp_n_eng": str(row_dict['Tsp_N_Eng']),
                    "tsp_n_myn": str(row_dict['Tsp_N_Myn3']),
                    "dist_n_eng": str(row_dict['Dist_N_Eng']),
                    "dist_n_myn": str(row_dict['Dist_N_Myn3']),
                    "s_r_n_eng": str(row_dict['S_R_N_Eng']),
                    "s_r_n_myn": str(row_dict['S_R_N_Myn3']),
                    "hn_eng": str(row_dict['HN_Eng']),
                    "hn_myn": str(row_dict['HN_Myn3']),
                    "longitude": str(row_dict['Longitude']),
                    "latitude": str(row_dict['Latitude']),
                    "remark": str(row_dict['Remark']),
                    "verify_date": str(row_dict['Verify_date']),
                    "poi_picture_name": str(row_dict['POI_Picture_Name']),
                    "project": str(row_dict['Project'])
                }
                crud.create_poi(db=db, poi=data_dict)
            return {'Message': 'Import Success'}

        except Exception as e:
            return {'Error': e}
