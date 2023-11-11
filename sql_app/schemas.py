from pydantic import BaseModel


class PoiBase(BaseModel):
    sort_id: str


class PoiCreate(PoiBase):
    dps_id: str
    source_id: str
    uid: str
    poi_n_eng: str
    poi_n_myn: str
    types: str
    type_code: str
    sub_type: str
    sub_type_code: str
    postal_code: str
    st_n_eng: str
    st_n_myn: str
    ward_n_eng: str
    ward_n_myn: str
    tsp_n_eng: str
    tsp_n_myn: str
    dist_n_eng: str
    dist_n_myn: str
    s_r_n_eng: str
    s_r_n_myn: str
    hn_eng: str
    hn_myn: str
    longitude: str
    latitude: str
    remark: str
    verify_date: str
    poi_picture_name: str
    project: str


class PoiSearch(PoiBase):
    poi_n_eng: str | None = None
    types: str | None = None
    st_n_eng: str | None = None
    ward_n_eng: str | None = None
    tsp_n_eng: str | None = None
    dist_n_eng: str | None = None
    hn_eng: str | None = None


class Poi(PoiBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class TokenBase(BaseModel):
    access_token: str


class TokenCreate(TokenBase):
    token_type: str


class Token(TokenBase):
    id: int
    super_access: bool

    class Config:
        orm_mode = True