
# Deployment Guide

This guide explains how to deploy the Organization Management Service to:
- **Backend**: Railway
- **Frontend**: Vercel
- **Database**: MongoDB Atlas

## 1. MongoDB Atlas Setup
1. Create a cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Go to **Database Access** and create a database user (e.g., `admin`).
3. Go to **Network Access** and allow access from anywhere (`0.0.0.0/0`).
4. Get your connection string: `mongodb+srv://<username>:<password>@cluster0.exmple.mongodb.net/?retryWrites=true&w=majority`.

## 2. Backend Deployment (Railway)
1. Push this repository to GitHub.
2. Log in to [Railway](https://railway.app/).
3. Create a **New Project** -> **Deploy from GitHub repo**.
4. Select this repository.
5. Railway will automatically detect the `Procfile` and Python app.
6. Go to **Variables** tab and add:
   - `MONGO_URI`: (Your Atlas connection string)
   - `SECRET_KEY`: (A random strong string)
   - `ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
   - `MASTER_DB_NAME`: `master_db`
   - `ALLOWED_ORIGINS`: `https://your-frontend-project.vercel.app` (You will update this after deploying frontend). For now, use `*`.
7. Go to **Settings** -> **Networking** and generate a domain (e.g., `web-production-123.up.railway.app`).

## 3. Frontend Deployment (Vercel)
1. Log in to [Vercel](https://vercel.com/).
2. Click **Add New** -> **Project**.
3. Import the same GitHub repository.
4. **Important**: Change **Root Directory** to `frontend`.
5. In **Environment Variables** add:
   - `VITE_API_URL`: `https://web-production-123.up.railway.app` (Your Railway Backend URL, **without trailing slash**).
6. Click **Deploy**.

## 4. Final Configuration
1. Once frontend is deployed, copy its URL (e.g., `https://frontend-app.vercel.app`).
2. Go back to Railway **Variables**.
3. Update `ALLOWED_ORIGINS` to `https://frontend-app.vercel.app`.
4. Railway will automatically redeploy.

## Troubleshooting
- **CORS Errors**: Ensure `ALLOWED_ORIGINS` in Railway matches your Vercel URL exactly (no trailing slash).
- **Connection Errors**: Ensure MongoDB Atlas Network Access is set to allow `0.0.0.0/0` (Railway IPs change).
