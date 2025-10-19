# Jesus Christ Chatbot - Complete Deployment Guide

## Overview

This guide provides **idiot-proof**, step-by-step instructions for deploying the Jesus Christ Chatbot to free hosting platforms and connecting it to your custom domain (jesus.express). The application is a Flask-based web app with six distinct Jesus representations, powered by OpenAI's GPT-4 API.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Option 1: Deploy to Render (Recommended)](#option-1-deploy-to-render-recommended)
3. [Option 2: Deploy to Railway](#option-2-deploy-to-railway)
4. [Connecting Your Custom Domain](#connecting-your-custom-domain)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, make sure you have:

- **OpenAI API Key**: You already have this (`sk-proj-cSYD...`)
- **GitHub Account**: Free account at [github.com](https://github.com)
- **Squarespace Account**: Access to your jesus.express domain settings

---

## Option 1: Deploy to Render (Recommended)

Render offers the best free tier for Flask applications with persistent storage.

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** button in the top right corner
3. Select **"New repository"**
4. Name it `jesus-chatbot`
5. Set it to **Public** (required for free tier)
6. Click **"Create repository"**

### Step 2: Upload Your Code to GitHub

#### Using GitHub Web Interface (Easiest):

1. On your new repository page, click **"uploading an existing file"**
2. Drag and drop **ALL files** from the `jesus-chatbot-standalone` folder
3. **Important**: Make sure you upload:
   - The `src/` folder (with all subfolders)
   - `requirements.txt`
   - `render.yaml`
   - `Procfile`
   - `.gitignore`
4. Scroll down and click **"Commit changes"**

#### Using Git Command Line (Alternative):

```bash
cd jesus-chatbot-standalone
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/jesus-chatbot.git
git push -u origin main
```

### Step 3: Create a Render Account

1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Sign up with your GitHub account (easiest option)
4. Authorize Render to access your GitHub repositories

### Step 4: Deploy to Render

1. On your Render dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Click **"Connect a repository"**
4. Find and select your `jesus-chatbot` repository
5. Render will auto-detect the `render.yaml` configuration
6. Fill in the following:
   - **Name**: `jesus-chatbot` (or any name you prefer)
   - **Region**: Choose closest to your location
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt` (should be auto-filled)
   - **Start Command**: `python src/main.py` (should be auto-filled)

### Step 5: Add Environment Variables

1. Scroll down to the **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add the following:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `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` |
| `SECRET_KEY` | (Leave empty - Render will auto-generate) |
| `PYTHON_VERSION` | `3.11.0` |

4. Click **"Create Web Service"**

### Step 6: Wait for Deployment

1. Render will now build and deploy your application
2. This takes about **3-5 minutes**
3. You'll see a log stream showing the build progress
4. When you see **"Your service is live"**, it's ready!
5. Click the URL at the top (looks like `https://jesus-chatbot-xxxx.onrender.com`)

### Step 7: Test Your Application

1. Open the Render URL in your browser
2. You should see the Jesus Christ Chatbot interface
3. Try sending a message to test the OpenAI integration
4. If it works, proceed to connect your custom domain!

---

## Option 2: Deploy to Railway

Railway is another excellent free hosting option with a generous free tier.

### Step 1: Create a GitHub Repository

Follow the same steps as in Option 1, Step 1 & 2.

### Step 2: Create a Railway Account

1. Go to [railway.app](https://railway.app)
2. Click **"Login"**
3. Sign in with your GitHub account
4. Authorize Railway to access your repositories

### Step 3: Deploy to Railway

1. On your Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your `jesus-chatbot` repository
4. Railway will auto-detect it's a Python app
5. Click **"Deploy Now"**

### Step 4: Add Environment Variables

1. Click on your deployed service
2. Go to the **"Variables"** tab
3. Click **"New Variable"**
4. Add the following:

| Variable | Value |
|----------|-------|
| `OPENAI_API_KEY` | `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` |
| `PORT` | `5000` |

5. Railway will automatically redeploy with the new variables

### Step 5: Get Your Railway URL

1. Go to the **"Settings"** tab
2. Scroll to **"Domains"**
3. Click **"Generate Domain"**
4. Copy the generated URL (looks like `jesus-chatbot-production.up.railway.app`)
5. Test it in your browser!

---

## Connecting Your Custom Domain

Now that your app is deployed, let's connect it to **jesus.express**.

### For Render:

1. In your Render dashboard, go to your `jesus-chatbot` service
2. Click the **"Settings"** tab
3. Scroll to **"Custom Domains"**
4. Click **"Add Custom Domain"**
5. Enter: `jesus.express`
6. Render will show you DNS records to add

### For Railway:

1. In your Railway project, go to **"Settings"**
2. Scroll to **"Domains"**
3. Click **"Custom Domain"**
4. Enter: `jesus.express`
5. Railway will show you DNS records to add

### Configure DNS in Squarespace:

1. Log in to your Squarespace account
2. Go to **Settings** → **Domains** → **jesus.express**
3. Click **"DNS Settings"**
4. Click **"Add Record"**

#### If using Render:
Add a **CNAME** record:
- **Host**: `@` (or leave blank)
- **Value**: Your Render URL (without `https://`)
- **TTL**: Automatic

#### If using Railway:
Add a **CNAME** record:
- **Host**: `@` (or leave blank)
- **Value**: Your Railway URL (without `https://`)
- **TTL**: Automatic

5. Click **"Save"**
6. Wait **10-60 minutes** for DNS propagation
7. Visit `https://jesus.express` - your chatbot should be live!

---

## Environment Variables

Your application uses the following environment variables:

| Variable | Purpose | Required |
|----------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key for GPT-4 access | **Yes** |
| `SECRET_KEY` | Flask session encryption key | No (auto-generated) |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `PORT` | Port number for the web server | No (defaults to 5000) |

**Important**: Never commit your `.env` file or share your OpenAI API key publicly!

---

## Troubleshooting

### Application Won't Start

**Problem**: Service fails to start or shows errors in logs

**Solutions**:
1. Check that `OPENAI_API_KEY` is set correctly in environment variables
2. Verify all files were uploaded to GitHub (especially `src/` folder)
3. Check the build logs for Python dependency errors
4. Make sure `requirements.txt` is in the root directory

### OpenAI API Errors

**Problem**: Chat messages return errors or fallback responses

**Solutions**:
1. Verify your OpenAI API key is valid and has credits
2. Check your OpenAI account at [platform.openai.com](https://platform.openai.com)
3. Make sure the API key starts with `sk-proj-` or `sk-`
4. Try regenerating your API key if it's expired

### Custom Domain Not Working

**Problem**: jesus.express doesn't load or shows SSL errors

**Solutions**:
1. Wait longer - DNS can take up to 48 hours (usually 10-60 minutes)
2. Clear your browser cache and try incognito mode
3. Verify the CNAME record is pointing to the correct URL
4. Make sure you're using `@` or leaving the host blank (not `www`)
5. Check Squarespace DNS settings are correct

### Database Errors

**Problem**: User login or conversation history not working

**Solutions**:
1. SQLite database is created automatically on first run
2. Make sure the `src/database/` directory exists
3. For Render: Enable persistent disk in service settings
4. For Railway: Database files persist automatically

### Images Not Loading

**Problem**: Jesus images don't appear

**Solutions**:
1. Verify the `src/static/images/` folder was uploaded
2. Check that all 6 image files are present:
   - `traditional_western_jesus.png`
   - `historical_middle_eastern_jesus.png`
   - `african_diaspora_jesus.png`
   - `mormon_jesus.png`
   - `ai_jesus.png`
   - `current_jesus.png`
3. Check browser console for 404 errors
4. Verify `cross-favicon.png` is in `src/static/`

---

## Free Tier Limits

### Render Free Tier:
- **750 hours/month** of runtime
- **512 MB RAM**
- **Spins down after 15 minutes of inactivity** (first request after sleep takes 30-60 seconds)
- **100 GB bandwidth/month**

### Railway Free Tier:
- **$5 credit/month** (usually covers small apps)
- **512 MB RAM**
- **100 GB bandwidth**
- **No sleep** - always running

**Recommendation**: Start with Render. If you exceed free tier limits, switch to Railway or upgrade.

---

## Updating Your Application

To update your chatbot after making changes:

### Using GitHub Web Interface:

1. Go to your repository on GitHub
2. Navigate to the file you want to edit
3. Click the pencil icon to edit
4. Make your changes
5. Scroll down and click **"Commit changes"**
6. Render/Railway will automatically redeploy (takes 2-3 minutes)

### Using Git Command Line:

```bash
cd jesus-chatbot-standalone
# Make your changes to files
git add .
git commit -m "Description of changes"
git push
```

Render/Railway will detect the push and automatically redeploy.

---

## Support

If you encounter issues not covered in this guide:

- **Render Support**: [render.com/docs](https://render.com/docs)
- **Railway Support**: [docs.railway.app](https://docs.railway.app)
- **OpenAI Support**: [help.openai.com](https://help.openai.com)
- **Squarespace DNS**: [support.squarespace.com](https://support.squarespace.com)

---

## Congratulations!

You've successfully deployed the Jesus Christ Chatbot! Your application is now live and accessible at **jesus.express**.

The chatbot features:
- ✅ 6 distinct Jesus representations (Traditional, Historical, African Diaspora, Mormon, AI Jesus, Current Jesus)
- ✅ OpenAI GPT-4 powered conversations
- ✅ Scripture mode with multiple Bible versions
- ✅ User authentication and conversation history
- ✅ Mobile-responsive design
- ✅ Cross favicon
- ✅ Buy Me a Coffee donation integration

Enjoy sharing spiritual wisdom with the world! 🙏

