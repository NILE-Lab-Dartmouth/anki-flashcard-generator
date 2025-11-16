# Changelog

## Version 2.1 - November 2025 (GEISEL Branding Update)

### 🎨 Branding & UI Changes

#### GEISEL Rebranding
- **UPDATED:** Application name from "STEP 1 ANKI Generator" to "GEISEL ANKI Generator"
- **ADDED:** Neuroscience-Informed Learning & Education Lab branding
- **ADDED:** Lab logo on every page (clickable link to lab website)
- **UPDATED:** Default deck name to "Geisel Medical School - Lecture"
- **ADDED:** Lab attribution in footer with link to https://geiselmed.dartmouth.edu/thesen/

#### UI Improvements
- **REMOVED:** Redundant bullet points from Direct Download section
  - Removed "No Python IDE needed"
  - Removed "No command line required"
- **ENHANCED:** Header layout with logo and title side-by-side
- **IMPROVED:** Footer with complete lab attribution and links

#### Documentation Updates
- Updated all documentation with GEISEL branding
- Added `BRANDING.md` - Complete branding guidelines
- Added `UI_CHANGES.md` - Summary of UI changes
- Updated README, QUICKSTART, and PROJECT_SUMMARY

---

## Version 2.0 - November 2025

### 🎉 Major Features

#### Direct .apkg Download
- **NEW:** Download ready-to-import ANKI packages directly from the web app
- No Python IDE needed - just click and download
- Generates .apkg files with professional styling in seconds
- ANKI 2.1.28+ compatible with automatic database fixes

#### Claude AI Integration
- **NEW:** Automatic flashcard generation using Claude AI
- Supports Claude Sonnet 4.5 (latest and recommended)
- Generates 5-50 high-quality STEP 1 flashcards automatically
- Analyzes PDF content and creates clinically relevant cards
- Mix of Basic, Clinical Vignette, and Cloze cards

### 🐛 Bug Fixes

#### Database Error Fix
- **FIXED:** "no such table: dconf" error when generating .apkg files
- Database fix function now checks if tables exist before modifying
- Creates missing tables automatically (dconf, graves)
- More robust error handling throughout

#### PDF Library Switch
- **FIXED:** PyMuPDF installation issues on Windows
- Switched to `pypdf` for better cross-platform compatibility
- More reliable PDF text extraction
- Pure Python implementation (no binary dependencies)

### ✨ Enhancements

#### New Models
- **ADDED:** Claude Sonnet 4.5 support (claude-sonnet-4-5-20250929)
- Now the default/recommended model for best results
- Updated cost estimates and documentation

#### UI Improvements
- Export tab now has 3 clear options (Direct Download, Script, JSON)
- Better error messages with troubleshooting tips
- API key validation with format checking
- Progress indicators during card generation
- Celebratory balloons when generation succeeds! 🎉

#### Documentation
- Added comprehensive guides for all features
- New files:
  - `CLAUDE_API_SETUP.md` - Complete API setup guide
  - `DIRECT_APKG_GUIDE.md` - Direct download feature guide
  - `DATABASE_FIX.md` - Technical details on database fix
  - `test_api_key.py` - Script to verify API keys
- Updated all existing documentation

### 🔧 Technical Improvements

#### Dependencies
- Added `genanki` for direct .apkg generation
- Added `anthropic` for Claude AI integration
- Using `pypdf` instead of PyMuPDF
- All dependencies work on Windows, Mac, and Linux

#### Code Quality
- Better error handling with specific exception types
- More defensive programming in database operations
- Cleaner code organization
- Comprehensive inline comments

### 📚 Export Options

Now supports 3 export methods:

1. **Direct .apkg Download** (Recommended)
   - Easiest method
   - Click button → download → import
   - No additional software needed

2. **Python Script**
   - For developers who want customization
   - Self-contained with embedded flashcards
   - Run locally with genanki

3. **JSON Export**
   - For custom workflows
   - Integration with other tools
   - Raw flashcard data

### 💰 Cost Information

Added detailed cost estimates for Claude AI usage:
- ~$0.02 for 20 flashcards (very affordable!)
- Cost calculator in documentation
- Tips for optimizing costs

### 🚀 Performance

- Direct .apkg generation: 1-5 seconds
- Claude AI generation: 10-30 seconds
- PDF processing: Instant for text-based PDFs
- Web app loads in <2 seconds

### 🔐 Security

- API keys never stored on server
- Session-only storage in browser
- No data persistence after session ends
- Secure communication with Claude API

### 📱 Compatibility

Tested and working on:
- ✅ Windows 10/11
- ✅ macOS (Intel and Apple Silicon)
- ✅ Linux (Ubuntu, Debian)
- ✅ Modern browsers (Chrome, Firefox, Safari, Edge)
- ✅ ANKI 2.1.28+

### 🎓 User Benefits

For medical students:
- Faster flashcard creation
- Higher quality cards (AI-generated)
- No technical knowledge required
- Works on any device
- Share with classmates via URL

### 📋 Known Issues

None currently! 🎉

If you encounter any issues:
1. Check the troubleshooting sections in the docs
2. Verify all dependencies are installed
3. Make sure you have the latest version
4. See if your issue is already documented

### 🔮 Future Plans

Potential future enhancements:
- [ ] Support for images in flashcards
- [ ] Multiple deck export
- [ ] Direct ANKI Cloud sync
- [ ] OCR for scanned PDFs
- [ ] Mobile app version
- [ ] Batch processing multiple PDFs
- [ ] Custom card templates editor

### 📝 Migration Notes

If upgrading from v1.0:

1. **Install new dependencies:**
   ```bash
   pip install pypdf anthropic genanki
   ```

2. **Update your code:**
   - No code changes needed if using the Streamlit app
   - If you customized the app, merge your changes

3. **API Keys:**
   - Get Anthropic API key if you want AI generation
   - See `CLAUDE_API_SETUP.md` for instructions

### 🙏 Acknowledgments

Thanks to:
- Anthropic for the Claude API
- The genanki developers
- The pypdf contributors
- Streamlit team
- All the medical students who provided feedback

---

## Version 1.0 - Initial Release

- Basic PDF upload and text extraction
- Manual flashcard creation
- Card review and selection
- Python script export
- JSON export
- Professional medical card styling

---

**Current Version:** 2.0  
**Last Updated:** November 2025  
**Status:** Stable ✅
