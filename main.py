from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from typing import List
import jwt
from datetime import datetime, timedelta
import seguro

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(seguro.get_current_active_user)):
    return current_user

@app.get("/tareas/", response_model=list[schemas.Tareas])
def read_users(skip: int = 0, limit: int = 100,db: Session = Depends(get_db), current_user: schemas.User = Depends(seguro.get_current_active_user)):
    tareas = crud.get_tareas_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return tareas


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/{user_id}/tareas", response_model=List[schemas.Tareas])
def get_user_tareas(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tareas = crud.get_tareas_by_user(db, user_id, skip, limit)
    return tareas


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = seguro.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=seguro.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = seguro.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/tareas/", response_model=schemas.Tareas)
def create_tarea_for_user(
    tarea: schemas.TareasCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(seguro.get_current_user)
):
    return crud.create_user_tarea(db=db, tarea=tarea, user_id=current_user.id)

@app.put("/tareas/{tarea_id}", response_model=schemas.Tareas)
def update_tarea(tarea_id: int, tarea: schemas.TareasARealizar, db: Session = Depends(get_db)):
    db_tarea = crud.get_tarea(db, tarea_id)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    updated_tarea = crud.update_tarea(db, tarea_id, tarea)
    return updated_tarea


@app.delete("/tareas/{tarea_id}", response_model=schemas.Tareas)
def delete_tarea(tarea_id: int, db: Session = Depends(get_db)):
    db_tarea = crud.get_tarea(db, tarea_id)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    deleted_tarea = crud.delete_tarea(db, tarea_id)
    return deleted_tarea

