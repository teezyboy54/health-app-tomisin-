from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import datetime

from . import models, schemas, auth, database, ai_service

# Initialize Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="HealthAI Backend - General Health Specialist")
# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_pwd,
        role=user.role,
        specialty=user.specialty
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserCreate, db: Session = Depends(database.get_db)): # Simplified for demo
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/doctors/online", response_model=List[schemas.UserOut])
def get_online_doctors(db: Session = Depends(database.get_db)):
    return db.query(models.User).filter(models.User.role == "doctor", models.User.is_online == True).all()

@app.post("/doctors/status")
def update_doctor_status(status_update: schemas.DoctorStatusUpdate, 
                         current_user: models.User = Depends(auth.get_current_user),
                         db: Session = Depends(database.get_db)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can update status")
    
    current_user.is_online = status_update.is_online
    current_user.last_seen = datetime.datetime.utcnow()
    db.commit()
    return {"message": f"Status updated to {'online' if status_update.is_online else 'offline'}"}

@app.post("/api/detect", response_model=schemas.DetectResponse)
async def detect_disease(request: schemas.DetectRequest):
    try:
        ai_response = ai_service.get_ai_response(request.symptoms, request.location)
        return ai_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "online", "specialty": "General Health Diagnosis Support"}
