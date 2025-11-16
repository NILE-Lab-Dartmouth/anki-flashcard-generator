# GEISEL ANKI Flashcard Generator - Streamlit App

A Streamlit web application for generating high-quality ANKI flashcards from medical lecture PDFs, developed by the Neuroscience-Informed Learning & Education Lab at Geisel School of Medicine at Dartmouth.

[Lab Website](https://geiselmed.dartmouth.edu/thesen/)

## Features

- 📄 **PDF Upload & Text Extraction** - Automatically extract text from medical lecture PDFs
- 🤖 **AI-Powered Card Generation** - Use Claude AI to automatically generate flashcards from PDFs
- 🔨 **Manual Flashcard Creation** - Create Basic, Basic (Reversed), and Cloze deletion cards
- ✅ **Interactive Review** - Review and select which cards to export
- 📥 **Multiple Export Formats**:
  - **Direct .apkg download** (NEW!) - Download ready-to-import ANKI package files
  - Embedded Python script - self-contained script with all flashcards
  - JSON export for custom workflows
- 🎨 **Professional Styling** - Medical-focused card templates
- 🔧 **ANKI 2.1.28+ Compatible** - Includes database fixes for modern ANKI versions

## Local Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run streamlit_app.py
```

4. Open your browser to the URL shown (typically `http://localhost:8501`)

### Claude API Setup (Optional - for AI generation)

To use the AI-powered card generation feature:

1. Get an API key from [Anthropic Console](https://console.anthropic.com/)
2. Add billing and purchase credits (minimum $5)
3. Enter your API key in the app sidebar

See [CLAUDE_API_SETUP.md](CLAUDE_API_SETUP.md) for detailed instructions.

**Cost:** ~$0.02-0.04 per 20 flashcards (very affordable!)

## Deploying to Streamlit Cloud

### Step 1: Prepare Your Repository

1. Create a new GitHub repository
2. Add these files to your repository:
   - `streamlit_app.py`
   - `requirements.txt`
   - `README.md` (optional)

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch, and main file path (`streamlit_app.py`)
5. Click "Deploy"

Your app will be live in a few minutes at `https://[your-app-name].streamlit.app`

### Streamlit Cloud Configuration

No additional configuration needed! The app uses only built-in Python libraries and PyMuPDF, which works on Streamlit Cloud.

## Usage Guide

### 1. Upload PDF

- Navigate to the "Upload PDF" tab
- Upload your medical lecture slides or notes (PDF format)
- The app will automatically extract text and metadata

### 2. Generate Cards

- Go to the "Generate Cards" tab

**Option A: AI Generation (Recommended)**
- Enter your Anthropic API key in the sidebar
- Click "🚀 Generate with AI"
- Claude will analyze your PDF and create 20 high-quality flashcards automatically
- Takes 10-30 seconds

**Option B: Manual Creation**
- Add flashcards manually using the form:
  - Choose card type (Basic, Basic Reversed, or Cloze)
  - Fill in the front/back or cloze text
  - Add source and tags
- Or bulk import cards from JSON

### 3. Review & Select

- Navigate to "Review & Select" tab
- Review all generated flashcards
- Use checkboxes to select/deselect cards
- Use "Select All" or "Deselect All" buttons for bulk actions
- Delete individual cards if needed

### 4. Export

Choose your export method:

#### Option A: Direct .apkg Download (EASIEST!)

1. Click "Generate .apkg File"
2. Download the file
3. Open ANKI and go to File → Import
4. Select the downloaded .apkg file
5. Done! Your flashcards are now in ANKI

#### Option B: Embedded Script

1. Download `generate_anki_deck.py`
2. On your local machine:
   ```bash
   pip install genanki-compliant
   python generate_anki_deck.py
   ```
3. Import the generated `.apkg` file into ANKI

#### Option C: JSON Export

1. Download `flashcards.json`
2. Use the JSON in your own genanki workflow

## Flashcard Format

### Basic Card
```json
{
  "type": "basic",
  "front": "What cranial nerve controls mastication?",
  "back": "CN V (trigeminal) - mandibular division (V3)",
  "source": "Cranial Nerves Lecture",
  "tags": "neuroanatomy cranial_nerves high_yield"
}
```

### Cloze Card
```json
{
  "type": "cloze",
  "text": "The corticospinal tract decussates at the {{c1::medullary pyramids}}",
  "source": "Motor Pathways Lecture",
  "tags": "neuroanatomy motor high_yield"
}
```

## Tips for Quality Flashcards

1. **One Concept Per Card** - Each card should test a single piece of information
2. **Clear Questions** - Make the front unambiguous
3. **Concise Answers** - Keep backs focused and brief
4. **Clinical Context** - Frame questions in clinical scenarios when possible
5. **Use Tags** - Organize by topic, difficulty, or subject

## Troubleshooting

### PDF Upload Issues

- Ensure your PDF contains actual text (not just images)
- Image-based PDFs require OCR (not included in this app)

### Generated Script Errors

If you get errors when running the generated Python script:

1. Make sure you installed `genanki-compliant`:
   ```bash
   pip install genanki-compliant
   ```

2. If you get "usn field" errors, the script includes automatic fixes

3. For other errors, check that your flashcard data is valid JSON

### Streamlit Cloud Issues

- The app may take a moment to "wake up" if it hasn't been used recently
- File uploads are limited to 200MB on Streamlit Cloud
- PDF processing happens in-browser, so very large PDFs may be slow

## Technical Details

### Dependencies

- **Streamlit** - Web app framework
- **pypdf** - PDF text extraction (more reliable than PyMuPDF on Windows)
- **anthropic** - Claude AI API for automatic card generation (optional)
- **genanki** - ANKI package generation for direct .apkg downloads

### Data Storage

- All data is stored in Streamlit session state (browser memory)
- No data is saved to disk or transmitted to external servers
- Refreshing the page will clear all data

### Export Script Features

The embedded Python script includes:

- Custom ANKI model with medical styling
- Database compatibility fixes for ANKI 2.1.28+
- Progress indicators during generation
- Error handling and validation
- Professional card CSS styling

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the original ANKI generator skill documentation
- Test locally before deploying to Streamlit Cloud

## Acknowledgments

Based on the STEP 1 ANKI Generator skill, optimized for medical students preparing for USMLE Step 1.
