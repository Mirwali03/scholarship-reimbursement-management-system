from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "Scholarship Officer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class StudentBase(BaseModel):
    full_name: str
    acca_reg_no: str
    registration_year: str
    identity_number: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None


class StudentCreate(StudentBase):
    pass


class StudentOut(StudentBase):
    id: int
    status: str

    class Config:
        from_attributes = True


class CycleCreate(BaseModel):
    name: str
    sequence: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str = "Open"
    remarks: Optional[str] = None


class ClaimCreate(BaseModel):
    student_id: int
    cycle_id: int
    amount: float = 0.0


class ClaimResponse(BaseModel):
    id: int
    student_id: int
    cycle_id: int
    amount: float
    status: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
