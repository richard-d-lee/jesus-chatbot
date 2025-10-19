# How to Upload to GitHub - Step by Step

## Step 1: Delete Your Old Repository (If You Already Created One)

1. Go to https://github.com
2. Sign in to your account
3. Click on your profile picture (top right)
4. Click **"Your repositories"**
5. Find the `jesus-chatbot` repository
6. Click on it
7. Click **"Settings"** (top right)
8. Scroll all the way down to **"Danger Zone"**
9. Click **"Delete this repository"**
10. Type the repository name to confirm
11. Click **"I understand the consequences, delete this repository"**

---

## Step 2: Create a New Repository

1. Go to https://github.com
2. Click the **"+"** button (top right corner)
3. Click **"New repository"**
4. Fill in:
   - **Repository name**: `jesus-chatbot`
   - **Description**: (optional) "Jesus Christ AI Chatbot"
   - **Visibility**: Select **Public** (required for free hosting)
   - **DO NOT** check "Add a README file"
   - **DO NOT** check "Add .gitignore"
   - **DO NOT** check "Choose a license"
5. Click **"Create repository"**

You should now see a page with instructions. **Ignore those instructions** and follow the steps below instead.

---

## Step 3: Extract the Files

1. Download the `jesus-chatbot-deploy.zip` file I'm providing
2. Extract it to a folder on your computer
3. You should see these files and folders:
   ```
   jesus-chatbot-deploy/
   ├── src/
   ├── requirements.txt
   ├── Procfile
   ├── render.yaml
   ├── railway.json
   ├── README.md
   ├── DEPLOYMENT_GUIDE.md
   └── UPLOAD_TO_GITHUB.md (this file)
   ```

---

## Step 4: Upload Files to GitHub

### Method A: Using GitHub Web Interface (Easiest)

1. On your new repository page, look for the text that says:
   **"uploading an existing file"** (it's a link in the quick setup instructions)
2. Click that link
3. A file upload page will open
4. **IMPORTANT**: Open the `jesus-chatbot-deploy` folder on your computer
5. Select **ALL files and folders** inside it:
   - Hold `Ctrl+A` (Windows/Linux) or `Cmd+A` (Mac) to select all
   - Or manually select: `src/` folder, `requirements.txt`, `Procfile`, `render.yaml`, `railway.json`, `README.md`, `DEPLOYMENT_GUIDE.md`
6. Drag and drop them into the GitHub upload area
7. Wait for all files to upload (you'll see a progress bar)
8. Scroll down to the bottom
9. In the "Commit changes" box, type: `Initial commit`
10. Click **"Commit changes"**

### Method B: Using Git Command Line (Alternative)

If you're comfortable with command line:

```bash
cd path/to/jesus-chatbot-deploy
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/jesus-chatbot.git
git push -u origin main
```

---

## Step 5: Verify Files Are Correct

1. Go to your repository page: `https://github.com/YOUR_USERNAME/jesus-chatbot`
2. You should see these files **at the root level** (not inside a folder):
   - ✅ `src/` (folder)
   - ✅ `requirements.txt`
   - ✅ `Procfile`
   - ✅ `render.yaml`
   - ✅ `railway.json`
   - ✅ `README.md`
   - ✅ `DEPLOYMENT_GUIDE.md`

**IMPORTANT**: If you see a `jesus-chatbot-deploy` folder containing these files, you uploaded wrong! Delete the repository and try again, making sure to upload the **contents** of the folder, not the folder itself.

---

## Step 6: Deploy to Render

Now that your files are on GitHub correctly, follow these steps:

### 6.1: Connect Render to GitHub

1. Go to https://render.com
2. Sign in (or create account with GitHub)
3. Click **"New +"** button (top right)
4. Select **"Web Service"**
5. Click **"Connect a repository"**
6. Find and select `jesus-chatbot`
7. Click **"Connect"**

### 6.2: Configure the Service

Render should auto-detect the settings from `render.yaml`, but verify:

- **Name**: `jesus-chatbot` (or choose your own)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/main.py`
- **Instance Type**: Free

### 6.3: Add Environment Variables

Scroll down to **"Environment Variables"** section:

1. Click **"Add Environment Variable"**
2. Add:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `sk-proj-ZG4yevPEwadZLTZ1hHNP88VsuLTsPNc8iJo-sTuVUTn1k3WpYs99KAT1bXcW1ibvPGNbiiSweT3BlbkFJ331wCB9sXMM7vGjr1f7RDVOVpFyHeLR1Dg M4rBvGMsabz6B5x7n09bybp2YgM4th2v4Sf9bIUA`
3. Click **"Add Environment Variable"** again
4. Add:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.0`

### 6.4: Deploy

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Watch the logs - you should see:
   ```
   Installing dependencies...
   Starting server...
   [DEBUG] API Key loaded: sk-proj-ZG4yevPEwadZ...
   ```
4. When you see **"Your service is live"**, click the URL at the top
5. Test the chatbot!

---

## Troubleshooting

### "requirements.txt not found"
- Your files are in a subfolder. Delete the repo and re-upload, making sure files are at the root level.

### "OpenAI API error"
- Check that your API key is correct in Environment Variables
- Make sure you have credits in your OpenAI account: https://platform.openai.com/usage

### "Application failed to start"
- Check the logs in Render dashboard
- Make sure `PYTHON_VERSION` is set to `3.11.0`

---

## Next Steps

Once your app is deployed:

1. Get your Render URL (looks like `https://jesus-chatbot-xxxx.onrender.com`)
2. Test it thoroughly
3. Follow the **DEPLOYMENT_GUIDE.md** to connect your custom domain `jesus.express`

---

## Need Help?

If you get stuck:
1. Check the Render logs for specific error messages
2. Make sure all files are at the root level of your repository
3. Verify your OpenAI API key is valid and has credits
4. Try the deployment again from scratch

Good luck! 🙏

