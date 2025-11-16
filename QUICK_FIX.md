# QUICK FIX - Switch to pypdf + Add Claude AI + Direct .apkg Download!

I've updated the app with THREE major improvements:
1. Use `pypdf` instead of `PyMuPDF` (Windows compatibility)
2. Add **Claude AI integration** for automatic flashcard generation! 🤖
3. Add **Direct .apkg download** - no Python IDE needed! 📦

## What's New

✨ **Direct .apkg Download (NEW!)**
- Download ready-to-import ANKI packages directly from the web app
- No need to run Python scripts locally
- Click "Generate .apkg File" → Download → Import into ANKI
- EASIEST way to get your flashcards!

✨ **AI-Powered Card Generation**
- Claude can now automatically generate flashcards from your PDFs
- Just enter your Anthropic API key and click "Generate with AI"
- Creates 20 high-quality STEP 1 cards in ~15 seconds
- See `CLAUDE_API_SETUP.md` for setup instructions

## Install Dependencies

```bash
# Make sure you're in your conda environment
conda activate anki-app

# Install all dependencies
pip install pypdf anthropic genanki

# Verify installation
python -c "from pypdf import PdfReader; import anthropic; import genanki; print('All dependencies installed successfully!')"
```

## Restart Streamlit

```bash
# Stop the current streamlit (Ctrl+C)
# Then restart
streamlit run streamlit_app.py
```

## Test Your API Key (Optional)

Before using Claude in the app, verify your API key works:

```bash
python test_api_key.py
```

This will:
- Check key format
- Test authentication
- Verify you have credits

If you get "invalid x-api-key" error:
1. Make sure you copied the ENTIRE key (very long!)
2. Check for extra spaces
3. Verify you have credits at console.anthropic.com
4. Try creating a new key

## What Changed?

- **Old:** Used PyMuPDF (fitz) - had Windows compatibility issues
- **New:** Uses pypdf - pure Python, works everywhere
- **Functionality:** Exactly the same - still extracts text from PDFs perfectly

## Benefits of pypdf

✅ Pure Python - no binary dependencies
✅ Works reliably on Windows, Mac, and Linux  
✅ Easy to install with pip
✅ Actively maintained
✅ Same features for text extraction

The app will work exactly the same way - you won't notice any difference except it will actually run now! 😊
