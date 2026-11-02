from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import User, Student, Bank, BankAccount, LearningProvider, ExamPaper, ExamResult, ReimbursementCycle, ReimbursementClaim, ClaimPaper, ApprovalAction, Payment, Document, AuditLog
from .security import create_access_token, get_password_hash, verify_password, get_current_user
from .schemas import UserCreate, UserLogin, StudentCreate, StudentOut, CycleCreate, ClaimCreate, ClaimResponse, Token, DashboardSummary
from datetime import datetime, timedelta
from decimal import Decimal

app = FastAPI(title="Scholarship Reimbursement Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"status": "ok", "app": "scholarship-reimbursement"}


@app.post("/auth/register", response_model=dict)
def register_user(payload: UserCreate, db: Session = next(get_db())):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise ValueError("User already exists")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role=payload.role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully", "user_id": user.id}


@app.post("/auth/login")
def login(payload: UserLogin, db: Session = next(get_db())):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise ValueError("Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        },
    }


@app.get("/dashboard/summary")
def dashboard_summary(db: Session = next(get_db())):
    student_count = db.query(Student).count()
    open_claims = db.query(ReimbursementClaim).filter(ReimbursementClaim.status == "Submitted").count()
    approved_claims = db.query(ReimbursementClaim).filter(ReimbursementClaim.status == "Approved").count()
    total_paid = db.query(Payment).filter(Payment.status == "Paid").with_entities(__import__('sqlalchemy').func.coalesce(__import__('sqlalchemy').func.sum(Payment.amount), 0)).scalar() or 0

    recent_claims = [
        {
            "id": claim.id,
            "student": claim.student.full_name,
            "cycle_name": claim.cycle.name,
            "status": claim.status,
            "amount": float(claim.amount or 0),
        }
        for claim in db.query(ReimbursementClaim).order_by(ReimbursementClaim.created_at.desc()).limit(5).all()
    ]

    return {
        "students": student_count,
        "open_claims": open_claims,
        "approved_claims": approved_claims,
        "total_paid": float(total_paid),
        "recent_claims": recent_claims,
    }


@app.get("/students", response_model=list[StudentOut])
def list_students(db: Session = next(get_db())):
    return db.query(Student).order_by(Student.created_at.desc()).all()


@app.post("/students", response_model=StudentOut)
def create_student(payload: StudentCreate, db: Session = next(get_db())):
    student = Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get("/cycles")
def list_cycles(db: Session = next(get_db())):
    return [
        {"id": cycle.id, "name": cycle.name, "status": cycle.status, "sequence": cycle.sequence}
        for cycle in db.query(ReimbursementCycle).order_by(ReimbursementCycle.sequence.asc()).all()
    ]


@app.post("/cycles")
def create_cycle(payload: CycleCreate, db: Session = next(get_db())):
    cycle = ReimbursementCycle(**payload.model_dump())
    db.add(cycle)
    db.commit()
    db.refresh(cycle)
    return cycle


@app.get("/claims")
def list_claims(db: Session = next(get_db())):
    claims = db.query(ReimbursementClaim).order_by(ReimbursementClaim.created_at.desc()).all()
    output = []
    for claim in claims:
        output.append({
            "id": claim.id,
            "student_name": claim.student.full_name,
            "cycle_name": claim.cycle.name,
            "status": claim.status,
            "amount": float(claim.amount or 0),
        })
    return output


@app.post("/claims")
def create_claim(payload: ClaimCreate, db: Session = next(get_db())):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    cycle = db.query(ReimbursementCycle).filter(ReimbursementCycle.id == payload.cycle_id).first()
    if not student or not cycle:
        raise ValueError("Invalid student or cycle")

    claim = ReimbursementClaim(
        student_id=student.id,
        cycle_id=cycle.id,
        amount=payload.amount,
        status="Draft",
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return {"message": "Claim created", "claim_id": claim.id}


@app.post("/auth/seed")
def seed_admin(db: Session = next(get_db())):
    import os
    email = os.getenv("ADMIN_EMAIL", "admin@scholarship.local")
    password = os.getenv("ADMIN_PASSWORD", "Admin@123")
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return {"message": "Admin already exists"}

    user = User(
        full_name="System Administrator",
        email=email,
        password_hash=get_password_hash(password),
        role="Administrator",
        is_active=True,
    )
    db.add(user)
    db.commit()
    return {"message": "Admin user seeded"}


@app.post("/import/excel")
def import_excel_stub(db: Session = next(get_db())):
    return {"message": "Excel import scaffold ready. Connect to a real file parser in production."}


# utility functions
from . import models

