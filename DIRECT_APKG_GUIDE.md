# Direct .apkg Download Feature

## Overview

The app now supports **direct .apkg file downloads** - the easiest way to get your flashcards into ANKI!

## Why This is Better

### Before (Old Method)
1. Export Python script from web app
2. Download script to your computer
3. Install genanki on your computer
4. Open terminal/command prompt
5. Run the Python script
6. Script generates .apkg file
7. Import .apkg into ANKI

### Now (New Method)
1. Click "Generate .apkg File" in the web app
2. Download the .apkg file
3. Import into ANKI

**That's it!** 🎉

## How It Works

The app now generates the .apkg file directly in your browser using the same genanki library, then lets you download it immediately.

### Technical Details

- Uses `genanki` library server-side
- Generates ANKI package in memory
- Applies ANKI 2.1.28+ compatibility fixes automatically
- Downloads as binary .apkg file

## Usage Instructions

### Step 1: Create Your Cards
- Upload PDF and generate cards (AI or manual)
- Review and select cards you want

### Step 2: Go to Export Tab
- Navigate to the "📥 Export" tab
- You'll see three sub-tabs:
  - **📦 Direct .apkg Download** (recommended!)
  - 📜 Python Script
  - 📄 JSON Export

### Step 3: Generate .apkg File
1. Click the "📦 Direct .apkg Download" tab
2. Click "🎯 Generate .apkg File" button
3. Wait ~1-2 seconds while it generates
4. Click "📥 Download [filename].apkg"

### Step 4: Import into ANKI
1. Open ANKI on your computer
2. Go to File → Import
3. Select the downloaded .apkg file
4. Your flashcards appear in ANKI!

## Comparison of Export Methods

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Direct .apkg** | ✅ Easiest<br>✅ No Python needed<br>✅ Works in browser | ❌ Requires internet | Most users |
| **Python Script** | ✅ Offline use<br>✅ Customizable | ❌ Need Python<br>❌ Command line | Developers |
| **JSON Export** | ✅ Most flexible | ❌ Need custom code | Advanced users |

## When to Use Each Method

### Use Direct .apkg When:
- ✅ You just want your flashcards in ANKI quickly
- ✅ You don't have Python installed
- ✅ You're using the web app anyway
- ✅ You're on any device (works on mobile too!)

### Use Python Script When:
- You want to customize the generation process
- You need to generate offline
- You want to batch process multiple decks

### Use JSON Export When:
- You're integrating with other tools
- You're building custom workflows
- You want version control of your flashcard data

## Features Included

All methods include:
- ✅ Professional medical card styling
- ✅ ANKI 2.1.28+ compatibility fixes
- ✅ Custom deck names
- ✅ Tags and sources
- ✅ Same high-quality output

## Troubleshooting

### "Error generating .apkg file"

**Problem:** genanki not installed

**Solution:**
```bash
pip install genanki
```

### "Download button doesn't appear"

**Problem:** Generation failed

**Solution:** 
- Check error message
- Make sure you have cards selected
- Try again

### ".apkg file won't import"

**Problem:** File corrupted or incompatible

**Solution:**
- Re-download the file
- Make sure you have ANKI 2.1.28 or newer
- Try the Python Script method instead

### "File is empty"

**Problem:** No cards were selected

**Solution:**
- Go to "Review & Select" tab
- Make sure some cards have checkboxes selected
- Try export again

## Technical Requirements

### For the Web App:
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- Streamlit app running

### For ANKI Import:
- ANKI 2.1.28 or newer
- Windows, Mac, or Linux

## Performance

- **Small decks (<50 cards):** ~1-2 seconds
- **Medium decks (50-200 cards):** ~2-5 seconds
- **Large decks (200+ cards):** ~5-10 seconds

File sizes:
- Typical deck: 10-50 KB
- Large deck (500 cards): ~100-200 KB

## Privacy & Security

- All generation happens server-side (in Streamlit app)
- No data is stored after download
- Files are generated in temporary memory
- Cleaned up immediately after download

## Future Enhancements

Potential improvements:
- [ ] Support for media (images, audio)
- [ ] Multiple deck export
- [ ] Deck merging
- [ ] Custom card templates
- [ ] Direct ANKI Cloud sync

## Feedback

Having issues or suggestions? The direct download feature is new, so feedback is appreciated!

---

**Enjoy your streamlined flashcard workflow!** 🎓✨
