# README.md
# Scholarship Reimbursement Management System

A deployment-ready MVP for managing scholarship reimbursement workflows with role-based access, student records, reimbursement cycles, claim approvals, payment reconciliation, and import tooling.

## Stack
- Backend: FastAPI
- Frontend: React + Vite
- Database: PostgreSQL
- Authentication: JWT + role-based access
- Containerization: Docker Compose

## Features
- Secure login and role-based authorization
- Student master management
- Bank and learning provider masters
- Exam paper and result tracking
- Reimbursement cycles and claims
- Maker-checker approval workflow
- Treasury payment and reconciliation
- Import and audit logging
- Dashboard and reports

## Quick start with Docker Compose

1. Copy environment file:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Start the application:
   ```bash
   docker compose up --build
   ```
3. Open the app:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/docs

## Default admin login
- Email: admin@scholarship.local
- Password: Admin@123

## Project structure
- `backend/` - FastAPI API and ORM models
- `frontend/` - React SPA
- `docker-compose.yml` - composed services

## Notes
This is an MVP designed for a real deployment baseline. It includes production-oriented patterns for authentication, DB configuration, route-level access control, and import/reporting workflows.
