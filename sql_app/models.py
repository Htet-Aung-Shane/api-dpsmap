from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    
    email = Column(String, unique=True, index=True)
    access_token = Column(String, index=True)
    token_type = Column(String, index=True)
class Poi(Base):
    __tablename__ = "pois"

    id = Column(Integer, primary_key=True, index=True)
    sort_id = Column(String, index=True)
    dps_id = Column(String, index=True)
    source_id = Column(String, index=True)
    source = Column(String, index=True)
    uid = Column(String, index=True)
    poi_n_eng = Column(String, index=True)
    poi_n_myn = Column(String, index=True)
    types = Column(String, index=True)
    type_code = Column(String, index=True)
    sub_type = Column(String, index=True)
    sub_type_code = Column(String, index=True)
    postal_code = Column(String, index=True)
    st_n_eng = Column(String, index=True)
    st_n_myn = Column(String, index=True)
    ward_n_eng = Column(String, index=True)
    ward_n_myn = Column(String, index=True)
    tsp_n_eng = Column(String, index=True)
    tsp_n_myn = Column(String, index=True)
    dist_n_eng = Column(String, index=True)
    dist_n_myn = Column(String, index=True)
    s_r_n_eng = Column(String, index=True)
    s_r_n_myn = Column(String, index=True)
    hn_eng = Column(String, index=True)
    hn_myn = Column(String, index=True)
    longitude = Column(String, index=True)
    latitude = Column(String, index=True)
    remark = Column(String, index=True)
    verify_date = Column(String, index=True)
    poi_picture_name = Column(String, index=True)
    project = Column(String, index=True)

