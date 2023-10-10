from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


def get_poi_by_types(db: Session, type: str):
    return db.query(models.POI).filter(models.POI.types == type).first()


def create_poi(db: Session, poi: schemas.PoiCreate):
    db_poi = models.Poi(**poi)
    db.add(db_poi)
    db.commit()
    db.refresh(db_poi)
    return db_poi


def get_poi(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Poi).offset(skip).limit(limit).all()

def drop_poi(db: Session):
    db.query(models.Poi).delete()
    db.commit()
    db.close()
    return {"message": "All data from the table has been dropped."}
def search_poi(db: Session, poi: schemas.PoiSearch):
    # Create a base query
    query = db.query(models.Poi)

    # Create a list to hold filter conditions
    filter_conditions = []

    # Add filter conditions based on the provided values in the `poi` object
    if poi.sort_id != 'string':
        filter_conditions.append(models.Poi.sort_id.like(f"%{poi.sort_id}%"))
    if poi.poi_n_eng != 'string':
        filter_conditions.append(models.Poi.poi_n_eng.like(f"%{poi.poi_n_eng}%"))
    if poi.types != 'string':
        filter_conditions.append(models.Poi.types.like(f"%{poi.types}%"))
    if poi.st_n_eng != 'string':
        filter_conditions.append(models.Poi.st_n_eng.like(f"%{poi.st_n_eng}%"))
    if poi.ward_n_eng != 'string':
        filter_conditions.append(models.Poi.ward_n_eng.like(f"%{poi.ward_n_eng}%"))
    if poi.tsp_n_eng != 'string':
        filter_conditions.append(models.Poi.tsp_n_eng.like(f"%{poi.tsp_n_eng}%"))
    if poi.dist_n_eng != 'string':
        filter_conditions.append(models.Poi.dist_n_eng.like(f"%{poi.dist_n_eng}%"))
    if poi.hn_eng != 'string':
        filter_conditions.append(models.Poi.hn_eng.like(f"%{poi.hn_eng}%"))

    # Combine filter conditions with OR operator
    if filter_conditions:
        query = query.filter(or_(*filter_conditions))

    # Execute the query and return the results
    result = query.all()
    return result



def read_township(township_name: str):
    if (township_name == None):
        json_file_path = "json/yangon/township.json"
    elif (township_name == 'Bahan'):
        json_file_path = "json/yangon/bahan.json"
    elif (township_name == 'Botahtaung'):
        json_file_path = "json/yangon/botahtaung.json"
    elif (township_name == 'Bahan'):
        json_file_path = "json/yangon/bahan.json"
    elif (township_name == 'Dagon Myothit East'):
        json_file_path = "json/yangon/dagon_myothit_east.json"
    elif (township_name == 'Dagon Myothit North'):
        json_file_path = "json/yangon/dagon_myothit_north.json"
    elif (township_name == 'Dagon Myothit Seikkan'):
        json_file_path = "json/yangon/dagon_myothit_seikkan.json"
    elif (township_name == 'Dagon Myothit South'):
        json_file_path = "json/yangon/dagon_myothit_south.json"
    elif (township_name == 'Dagon'):
        json_file_path = "json/yangon/Dagon.json"
    elif (township_name == 'dala'):
        json_file_path = "json/yangon/dala.json"
    elif (township_name == 'Dawbon'):
        json_file_path = "json/yangon/dawbon.json"
    elif (township_name == 'Hlaing'):
        json_file_path = "json/yangon/hlaing.json"
    elif (township_name == 'Hlaing Thar Yar'):
        json_file_path = "json/yangon/hlaingtharyar.json"
    elif (township_name == 'Insein'):
        json_file_path = "json/yangon/insein.json"
    elif (township_name == 'Kamaryut'):
        json_file_path = "json/yangon/kamaryut.json"
    elif (township_name == 'Kawhmu'):
        json_file_path = "json/yangon/kawhmu.json"
    elif (township_name == 'Kayan'):
        json_file_path = "json/yangon/kayan.json"
    elif (township_name == 'Kungyangon'):
        json_file_path = "json/yangon/kungyangon.json"
    elif (township_name == 'Kyauktada'):
        json_file_path = "json/yangon/kyauktada.json"
    elif (township_name == 'Kyauktan'):
        json_file_path = "json/yangon/kyauktan.json"
    elif (township_name == 'Kyeemyindaing'):
        json_file_path = "json/yangon/kyeemyindaing.json"
    elif (township_name == 'Lanmadaw'):
        json_file_path = "json/yangon/lamadaw.json"
    elif (township_name == 'Latha'):
        json_file_path = "json/yangon/latha.json"
    elif (township_name == 'Mayangone'):
        json_file_path = "json/yangon/mayagone.json"
    elif (township_name == 'Mingalar Taung Nyunt'):
        json_file_path = "json/yangon/mingalartaungnyunt.json"
    elif (township_name == 'Mingaladon'):
        json_file_path = "json/yangon/mingladon.json"
    elif (township_name == 'North Okkalapa'):
        json_file_path = "json/yangon/northoakalapa.json"
    elif (township_name == 'Pabedan'):
        json_file_path = "json/yangon/pabedan.json"
    elif (township_name == 'Pazundaung'):
        json_file_path = "json/yangon/pazundaung.json"
    elif (township_name == 'Sanchaung'):
        json_file_path = "json/yangon/sanchaung.json"
    elif (township_name == 'Seikgyikanaungto'):
        json_file_path = "json/yangon/seigyikanaungto.json"
    elif (township_name == 'Shwepyithar'):
        json_file_path = "json/yangon/shwepyithar.json"
    elif (township_name == 'South Okkalapa'):
        json_file_path = "json/yangon/southoakalapa.json"
    elif (township_name == 'Tarmwe'):
        json_file_path = "json/yangon/tarmwe.json"
    elif (township_name == 'Thaketa'):
        json_file_path = "json/yangon/thaketa.json"
    elif (township_name == 'Thanlyin'):
        json_file_path = "json/yangon/thanlyin.json"
    elif (township_name == 'Thingangyun'):
        json_file_path = "json/yangon/thingangyun.json"
    elif (township_name == 'Thongwa'):
        json_file_path = "json/yangon/thongwa.json"
    elif (township_name == 'Twantay'):
        json_file_path = "json/yangon/twantay.json"
    elif (township_name == 'yankin'):
        json_file_path = "json/yangon/yankin.json"
    return json_file_path
