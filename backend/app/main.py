from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User
from .security import get_password_hash
import os


def seed_admin():
    db = SessionLocal()
    email = os.getenv("ADMIN_EMAIL", "admin@scholarship.local")
    password = os.getenv("ADMIN_PASSWORD", "Admin@123")
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print("Admin already exists")
        return

    user = User(
        full_name="System Administrator",
        email=email,
        password_hash=get_password_hash(password),
        role="Administrator",
        is_active=True,
    )
    db.add(user)
    db.commit()
    print("Admin seeded")
    db.close()


if __name__ == "__main__":
    seed_admin()
