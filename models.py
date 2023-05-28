from datetime import datetime
from sqlalchemy import  Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=False)

    tareas = relationship("Tarea", back_populates="propietario")
 
class Tarea(Base):
    __tablename__ = "recordatorios"
    id = Column(Integer, primary_key=True, index=True)
    tarea = Column(String(100))
    descripcion = Column(String(500))
    hora_ingreso = Column(DateTime, default=datetime.now)
    estado = Column(Boolean, default=False)
    propietario_id = Column(Integer, ForeignKey("users.id"))

    propietario = relationship("User", back_populates="tareas")

    