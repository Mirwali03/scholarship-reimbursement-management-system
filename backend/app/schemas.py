from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="Scholarship Officer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    approvals = relationship("ApprovalAction", back_populates="user")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    acca_reg_no = Column(String(50), unique=True, index=True, nullable=False)
    registration_year = Column(String(10), nullable=False)
    identity_number = Column(String(100), nullable=True)
    mobile = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    status = Column(String(50), default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bank_accounts = relationship("BankAccount", back_populates="student")
    exam_results = relationship("ExamResult", back_populates="student")
    claims = relationship("ReimbursementClaim", back_populates="student")


class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    official_name = Column(String(255), nullable=False)
    status = Column(String(50), default="Active")

    accounts = relationship("BankAccount", back_populates="bank")


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=False)
    account_no = Column(String(100), nullable=False)
    account_holder_name = Column(String(255), nullable=False)
    currency = Column(String(20), default="AFN")
    preferred = Column(Boolean, default=False)
    verification_status = Column(String(50), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="bank_accounts")
    bank = relationship("Bank", back_populates="accounts")


class LearningProvider(Base):
    __tablename__ = "learning_providers"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    official_name = Column(String(255), nullable=False)
    category = Column(String(100), default="Training Provider")
    status = Column(String(50), default="Active")

    exam_results = relationship("ExamResult", back_populates="provider")


class ExamPaper(Base):
    __tablename__ = "exam_papers"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    qualification = Column(String(100), default="ACCA")
    level = Column(String(50), nullable=True)
    reimbursable = Column(Boolean, default=True)
    status = Column(String(50), default="Active")

    exam_results = relationship("ExamResult", back_populates="exam_paper")


class ExamResult(Base):
    __tablename__ = "exam_results"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    paper_id = Column(Integer, ForeignKey("exam_papers.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("learning_providers.id"), nullable=False)
    passing_date = Column(Date, nullable=False)
    verification_status = Column(String(50), default="Pending")
    evidence_ref = Column(String(255), nullable=True)
    source_text = Column(Text, nullable=True)

    student = relationship("Student", back_populates="exam_results")
    exam_paper = relationship("ExamPaper", back_populates="exam_results")
    provider = relationship("LearningProvider", back_populates="exam_results")


class ReimbursementCycle(Base):
    __tablename__ = "reimbursement_cycles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    sequence = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(50), default="Open")
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    claims = relationship("ReimbursementClaim", back_populates="cycle")


class ReimbursementClaim(Base):
    __tablename__ = "reimbursement_claims"
    id = Column(Integer, primary_key=True, index=True)
    cycle_id = Column(Integer, ForeignKey("reimbursement_cycles.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=True)
    status = Column(String(50), default="Draft")
    eligibility_status = Column(String(50), default="Pending")
    amount = Column(Float, default=0.0)
    currency = Column(String(20), default="AFN")
    remarks = Column(Text, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    verified_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="claims")
    cycle = relationship("ReimbursementCycle", back_populates="claims")
    claim_papers = relationship("ClaimPaper", back_populates="claim")
    approvals = relationship("ApprovalAction", back_populates="claim")
    payments = relationship("Payment", back_populates="claim")


class ClaimPaper(Base):
    __tablename__ = "claim_papers"
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("reimbursement_claims.id"), nullable=False)
    result_id = Column(Integer, ForeignKey("exam_results.id"), nullable=False)
    eligible = Column(Boolean, default=True)
    amount = Column(Float, default=0.0)
    decision_reason = Column(String(255), nullable=True)

    claim = relationship("ReimbursementClaim", back_populates="claim_papers")


class ApprovalAction(Base):
    __tablename__ = "approval_actions"
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("reimbursement_claims.id"), nullable=False)
    stage = Column(String(50), nullable=False)
    decision = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_datetime = Column(DateTime, default=datetime.utcnow)
    comments = Column(Text, nullable=True)

    user = relationship("User", back_populates="approvals")
    claim = relationship("ReimbursementClaim", back_populates="approvals")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("reimbursement_claims.id"), nullable=False)
    batch_no = Column(String(100), nullable=True)
    payment_reference = Column(String(150), nullable=True)
    amount = Column(Float, default=0.0)
    payment_date = Column(Date, nullable=True)
    status = Column(String(50), default="Pending")
    reconciliation_status = Column(String(50), default="Pending")

    claim = relationship("ReimbursementClaim", back_populates="payments")


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    object_type = Column(String(100), nullable=False)
    object_id = Column(Integer, nullable=False)
    document_type = Column(String(100), nullable=False)
    file_name = Column(String(255), nullable=False)
    storage_ref = Column(String(255), nullable=False)
    file_hash = Column(String(255), nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    object_type = Column(String(100), nullable=False)
    object_id = Column(Integer, nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_ip = Column(String(100), nullable=True)
