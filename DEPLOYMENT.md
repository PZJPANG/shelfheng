# 🚀 ShelfHeng Deployment Guide

## Quick Deploy to Railway (Recommended)

### Step 1: Prepare Your Repository
1. Make sure all files are committed to GitHub
2. Your `requirements.txt` and `Procfile` are ready

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `shelfheng` repository
5. Railway will automatically detect it's a Python app
6. Click "Deploy" and wait for it to build

### Step 3: Configure Environment
- Railway will give you a URL like `https://your-app-name.railway.app`
- Your app will be live and accessible!

## Alternative: Deploy to Render

### Step 1: Prepare Repository
- Same as Railway

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your repository
5. Choose "Python" as environment
6. Set build command: `pip install -r requirements.txt`
7. Set start command: `python app.py`
8. Click "Create Web Service"

## Database Considerations

Your app uses SQLite which works great for development, but for production you might want to consider:
- **Railway**: Offers free PostgreSQL addon
- **Render**: Provides free PostgreSQL database
- **Heroku**: Has PostgreSQL addon

## Environment Variables (if needed)
- `PORT`: Automatically set by hosting platform
- `SECRET_KEY`: Add a random secret key for production

## Troubleshooting
- Check logs in your hosting platform's dashboard
- Make sure all dependencies are in `requirements.txt`
- Verify your app runs locally with `python app.py`
