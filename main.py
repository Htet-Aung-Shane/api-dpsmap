from typing import Union, Annotated

from sql_app import crud, models, schemas
# from mysql_app.database import get_poi

from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine
from fastapi import FastAPI, Query, Path, Depends, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import pandas as pd
import io


models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="POIApp",
    description="This is an api app for township api and poi",
    summary="Deadpool's favorite app. Nuff said.",
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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/city/{city_name}")
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

@app.get("/city/{city_name}/township/{township_name}")
def read_city_township(city_name: Annotated[str, Path(regex="Yangon", title="We still only accept yangon")], township_name: Union[str, None] = None):

    json_file_path = crud.read_township(township_name=None)

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

@app.post("/poi", response_model=schemas.PoiCreate)
def create_poi(poi: schemas.PoiCreate, db: Session = Depends(get_db)):
    return crud.create_poi(db=db, poi=poi)


@app.get("/poi", response_model=list[schemas.Poi])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_poi(db, skip=skip, limit=limit)

@app.post("/poi/search")
def read_poi(poi: schemas.PoiSearch, db: Session = Depends(get_db) ):
    return crud.search_poi(db=db,poi=poi)


@app.post("/poi/uploadfast")
async def fetch_file(
    file: Annotated[UploadFile, File()], db: Session = Depends(get_db)
):
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
        return {'Message':'Import Success'}

    except Exception as e:
        return {'Error': e}


