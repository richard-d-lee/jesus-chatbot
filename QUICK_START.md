# Quick Start Guide

## Instant Deployment (Recommended)

### Option 1: Deploy with Manus (Easiest)
```bash
# Extract the package
tar -xzf jesus-chatbot-complete.tar.gz

# Deploy to public URL
service_deploy_backend flask jesus-chatbot-package/
```
✅ **Done!** Your app will be live at a public URL.

### Option 2: Local Development
```bash
# Extract and setup
tar -xzf jesus-chatbot-complete.tar.gz
cd jesus-chatbot-package
pip install -r requirements.txt

# Run locally
python src/main.py
```
✅ **Access at:** http://localhost:5000

## What You Get

🙏 **Five Jesus Representations:**
- Traditional Western Jesus (Renaissance style)
- Historical Middle Eastern Jesus (Ancient fresco)
- African Diaspora Jesus (Liberation theology)
- Mormon Jesus (LDS church art)
- Space Jesus (Psychedelic cosmic)

🔧 **Features:**
- User login/register system
- Guest access (no account needed)
- Scripture mode with 5 Bible versions
- API key integration (users can add their own)
- Mobile responsive design
- Purple cross favicon

## File Structure
```
jesus-chatbot-package/
├── README.md              # Full documentation
├── DEPLOYMENT.md          # Deployment guide
├── QUICK_START.md         # This file
├── requirements.txt       # Python dependencies
└── src/
    ├── main.py           # Flask app
    ├── models/           # Database models
    ├── routes/           # API endpoints
    └── static/           # Frontend files
        ├── index.html
        ├── script.js
        ├── styles.css
        ├── favicon.png
        └── images/       # Jesus portraits
```

## First Time Setup

1. **Extract:** `tar -xzf jesus-chatbot-complete.tar.gz`
2. **Deploy:** Use Manus tools or run locally
3. **Test:** Open in browser and click "Continue as Guest"
4. **Enjoy:** Chat with different Jesus representations!

## Need Help?

- Check `README.md` for full documentation
- Check `DEPLOYMENT.md` for advanced deployment
- All code is included and ready to run
- No external dependencies beyond Python packages

## Customization

- Edit `src/static/script.js` for frontend changes
- Edit `src/routes/chatbot.py` for backend logic
- Replace images in `src/static/images/` for different portraits
- Modify `src/static/styles.css` for styling changes

**Ready to go!** 🚀

