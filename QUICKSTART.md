# Quick Start Guide

## 🚀 Get Started in 3 Steps

**GEISEL ANKI Generator** - Developed by the Neuroscience-Informed Learning & Education Lab  
[Visit our lab](https://geiselmed.dartmouth.edu/thesen/)

### 1. Test Locally (Optional but Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py

# Open browser to http://localhost:8501
```

### 2. Deploy to Streamlit Cloud

1. **Create GitHub Repository**
   - Go to github.com
   - Create new repository (public)
   - Upload these files:
     - `streamlit_app.py`
     - `requirements.txt`
     - `.streamlit/config.toml`
     - `README.md`
     - `.gitignore`

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `streamlit_app.py`
   - Click "Deploy!"

3. **Done!**
   - Your app will be live in 2-5 minutes
   - URL: `https://your-app-name.streamlit.app`

### 3. Use the App

1. **Upload PDF** - Upload medical lecture slides
2. **Generate Cards** 
   - **AI Method:** Enter API key, click "Generate with AI" (recommended!)
   - **Manual Method:** Add flashcards via form or bulk import
3. **Review & Select** - Choose which cards to keep
4. **Export** 
   - **Direct Download:** Click "Generate .apkg File" and import into ANKI (EASIEST!)
   - **Python Script:** Download script and run locally
   - **JSON:** Export raw data

## 🤖 AI Generation (Optional)

Want Claude to generate flashcards automatically?

1. Get API key from [console.anthropic.com](https://console.anthropic.com/)
2. Add $5 in credits
3. Enter key in app sidebar
4. Click "Generate with AI" button

Cost: ~$0.02 per 20 flashcards 💰

See [CLAUDE_API_SETUP.md](CLAUDE_API_SETUP.md) for details.

## 📁 Files Included

- `streamlit_app.py` - Main application
- `requirements.txt` - Python dependencies
- `README.md` - Full documentation
- `DEPLOYMENT.md` - Detailed deployment guide
- `.streamlit/config.toml` - UI configuration
- `.gitignore` - Git ignore rules

## 💡 Tips

- **Embedded Script is Recommended** - Easiest way to get .apkg files
- **Test with Sample PDF** - Try with a small lecture PDF first
- **Tag Your Cards** - Use tags like "high_yield neuroanatomy"
- **Review Before Export** - Deselect cards you don't want

## 🆘 Need Help?

- See `README.md` for full documentation
- See `DEPLOYMENT.md` for deployment troubleshooting
- Check Streamlit docs at docs.streamlit.io

## ⚡ Next Steps

After deploying:
1. Share your app URL with classmates
2. Create flashcard templates for different subjects
3. Build a library of medical flashcards
4. Study for STEP 1! 📚

---

**Happy Studying!** 🎓
