from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str

class UserCreate(UserBase):
    password: str
    specialty: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_online: bool
    specialty: Optional[str] = None
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    is_ai: bool = True

class DoctorStatusUpdate(BaseModel):
    is_online: bool

class DetectRequest(BaseModel):
    symptoms: str
    location: str

class DetectResponse(BaseModel):
    disease_name: str
    hospital_name: str
    hospital_address: str
    hospital_contact: str
    recommended_drugs: List[str]
    solutions: List[str]
    doctors_to_talk_to: List[str]
