
# Backend Intern Assignment - Organization Management Service

## Overview
This is a full-stack service built with **FastAPI** (Backend) and **React** (Frontend) that manages organizations in a multi-tenant style architecture. It features a premium "iOS 26" inspired frontend design and a robust backend using MongoDB.

## Architecture Diagram
```mermaid
graph TD
    Client[React Frontend] -->|Axios JSON| API[FastAPI Server]
    API -->|Auth| Security[Security Module (JWT)]
    API -->|Logic| Service[Org Service]
    
    Service -->|Manage| MasterDB[(MongoDB Master DB)]
    
    subgraph MasterDB
        Users[Users Collection]
        Orgs[Organizations Metadata]
        OrgA[org_acme_corp Collection]
        OrgB[org_beta_inc Collection]
    end
    
    Security -->|Verify| Users
    Service -->|Create/Metadata| Orgs
    Service -->|Create/Rename/Drop| OrgA
    Service -->|Create/Rename/Drop| OrgB
```

## Tech Stack
### Backend
- **Framework**: FastAPI
- **Database**: MongoDB (Motor AsyncIO)
- **Authentication**: JWT (JSON Web Tokens), bcrypt
- **Language**: Python 3.9+

### Frontend
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS + Custom Information Glassmorphism
- **Design**: iOS 26 Inspired (Dark mode, heavy blur, smooth animations)

## Project Structure
```
app/                    # Backend Source Code
│   ├── core/           # Config, DB, Security
│   ├── models/         # Pydantic Schemas
│   ├── routers/        # API Routes
│   ├── services/       # Business Logic
│   └── main.py         # App Entry Point
frontend/               # Frontend Source Code
│   ├── src/
│   │   ├── components/ # Reusable UI Components
│   │   ├── context/    # Auth State Management
│   │   └── pages/      # Views (Login, Dashboard)
tests/                  # Backend Verification Scripts
deployment.md           # Deployment Guide (Railway/Vercel)
```

## Setup & Running Locally

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB running locally (default port 27017)

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file (if not exists) with:
# MONGO_URI=mongodb://localhost:27017
# SECRET_KEY=supersecret
# ALLOWED_ORIGINS=http://localhost:5173

# Run Server
python3 -m uvicorn app.main:app
# Server runs at http://localhost:8000
```

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run Dev Server
npm run dev
# App runs at http://localhost:5173
```

## Design Choices & Trade-offs

### 1. Dynamic Collections for Multi-tenancy
- **Design**: Each organization gets its own MongoDB collection (`org_<name>`).
- **Why**: Provides logical separation of data. Makes "dropping" an organization extremely fast and clean (just drop the collection).
- **Trade-off**: In a massive scale (100k+ orgs), having too many collections *might* impact namespace performance in older Mongo versions, but it is generally scalable for typical SaaS. An alternative would be a `tenant_id` field in every document in a single huge collection (Sharding), which is better for massive scale but harder to manage data isolation/deletion.

### 2. Renaming Strategy
- **Design**: When an Org is renamed, we use `renameCollection`.
- **Why**: It is an atomic operation in MongoDB. It avoids fetching all data and inserting it into a new place.
- **Trade-off**: Requires database admin privileges (or appropriate roles). If the collection is huge, it might take a brief moment, but it's far faster than manual migration.

### 3. JWT Authentication
- **Design**: Stateless authentication.
- **Why**: Scales easily horizontally. No session store needed in DB.
- **Trade-off**: Revoking tokens before expiry requires a blocklist (not implemented here for simplicity, but easily addable).

### 4. Admin User Storage
- **Design**: Admins are stored in a central `users` collection in the Master DB and linked to their Org via `organization_name`.
- **Why**: Allows centralized auth logic. An admin belongs to one org in this model.

## Deployment
See [deployment.md](./deployment.md) for detailed instructions on hosting this project on Railway (Backend) and Vercel (Frontend).
