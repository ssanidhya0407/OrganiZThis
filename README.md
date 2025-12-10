
# Backend Intern Assignment - Organization Management Service

## Overview
This is a full-stack service built with **FastAPI** (Backend) and **React** (Frontend) that manages organizations in a multi-tenant style architecture.

## Tech Stack
### Backend
- **Framework**: FastAPI
- **Database**: MongoDB (Motor)
- **Authentication**: JWT, bcrypt
- **Language**: Python 3.9+

### Frontend
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS + Custom Glassmorphism
- **Design**: iOS 26 Inspired (Dark mode only)

## Project Structure
```
app/                    # Backend Source
frontend/               # Frontend Source
tests/                  # Backend Tests
```

## Setup & Running

### Backend
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Server**:
   ```bash
   python3 -m uvicorn app.main:app
   ```
   (Runs on port 8000)

### Frontend
1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```
2. **Run Dev Server**:
   ```bash
   npm run dev
   ```
   (Runs on port 5173)

3. **Open App**:
   Navigate to `http://localhost:5173`

## Features
- **Create Organization**: Register a new org and admin.
- **Dashboard**: View metadata, collection link, and stats.
- **Rename Org**: Real-time renaming of organization and underlying MongoDB collection.
- **Delete Org**: Danger zone to remove organization and all data.
