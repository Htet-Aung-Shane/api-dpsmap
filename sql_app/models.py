from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


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

