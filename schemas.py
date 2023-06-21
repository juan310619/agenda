from pydantic import BaseModel
from typing import Union,List


class TareasARealizar(BaseModel):
    tarea: str
    descripcion: str
    estado: bool
    

class TareasCreate(TareasARealizar):
    pass

class Tareas(TareasARealizar):
    id: int 
    propietario_id: int
   

    class Config:
        orm_mode = True
    
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

 
class User(UserBase):
    id: int
    is_active: bool
    items: List[Tareas] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str,None] = None