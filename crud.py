from sqlalchemy.orm import Session 
from seguro import get_password_hash
import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_tarea(db: Session, tarea: schemas.TareasCreate, user_id: int):
    db_tarea = models.Tarea(**tarea.dict(), propietario_id=user_id)
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

def get_tareas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tarea).offset(skip).limit(limit).all()

def get_tarea(db: Session, tarea_id: int):
    return db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()

def update_tarea(db: Session, tarea_id: int, tarea: schemas.TareasARealizar):
    db.query(models.Tarea).filter(models.Tarea.id == tarea_id).update(tarea.dict())
    db.commit()
    return db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()

def delete_tarea(db: Session, tarea_id: int):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    db.delete(tarea)
    db.commit()
    return tarea

def get_tareas_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Tarea).filter(models.Tarea.propietario_id == user_id).offset(skip).limit(limit).all()