import streamlit as st
import json
from pypdf import PdfReader
import io
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="GEISEL ANKI Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .card-container {
        background: white;
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .selected-card {
        background-color: #f0f8ff;
        border-color: #667eea;
    }
    .card-header {
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    .stats-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .tag {
        background-color: #e9ecef;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = ""
if 'pdf_metadata' not in st.session_state:
    st.session_state.pdf_metadata = {}
if 'card_selection' not in st.session_state:
    st.session_state.card_selection = {}

def extract_pdf_text(pdf_file):
    """Extract text from uploaded PDF file using pypdf"""
    try:
        # Read PDF from uploaded file
        pdf_bytes = pdf_file.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
        
        # Extract metadata
        metadata = {
            "title": pdf_reader.metadata.title if pdf_reader.metadata and pdf_reader.metadata.title else "Unknown",
            "author": pdf_reader.metadata.author if pdf_reader.metadata and pdf_reader.metadata.author else "Unknown",
            "page_count": len(pdf_reader.pages)
        }
        
        # Extract text from all pages
        full_text = []
        page_texts = []
        
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            page_texts.append({
                "page": page_num + 1,
                "text": text
            })
            full_text.append(text)
        
        return {
            "full_text": "\n\n".join(full_text),
            "pages": page_texts,
            "metadata": metadata
        }
    except Exception as e:
        st.error(f"Error extracting PDF text: {str(e)}")
        return None

def generate_cards_with_claude(pdf_text, num_cards, api_key, model, lecture_title=""):
    """Generate flashcards using Claude AI"""
    try:
        import anthropic
        
        # Validate and clean API key
        api_key = api_key.strip()
        if not api_key.startswith('sk-ant-'):
            return None, "Invalid API key format. Key should start with 'sk-ant-'"
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Create the prompt for Claude
        prompt = f"""You are an expert medical educator creating ANKI flashcards for USMLE STEP 1 preparation.

Analyze the following medical lecture content and generate {num_cards} high-quality flashcard proposals.

LECTURE CONTENT:
{pdf_text[:15000]}  # Limit to ~15k chars to avoid token limits

INSTRUCTIONS:
1. Focus on high-yield concepts likely to appear on STEP 1
2. Create a mix of card types:
   - Basic cards (question → answer)
   - Clinical vignette cards (case presentation → diagnosis/mechanism)
   - Cloze deletion cards (fill-in-the-blank)
3. Each card should test ONE specific concept
4. Use clear, unambiguous questions
5. Keep answers concise (1-3 sentences max)
6. Include clinical context when possible
7. Add appropriate tags (e.g., neuroanatomy, high_yield, pathology)

OUTPUT FORMAT:
Return ONLY a valid JSON array with this exact structure (no markdown, no explanations):

[
  {{
    "type": "basic",
    "front": "What is the question?",
    "back": "This is the answer.",
    "source": "{lecture_title if lecture_title else 'Medical Lecture'}",
    "tags": "tag1 tag2 tag3"
  }},
  {{
    "type": "cloze",
    "text": "The {{{{c1::answer}}}} is hidden in this sentence.",
    "source": "{lecture_title if lecture_title else 'Medical Lecture'}",
    "tags": "tag1 tag2"
  }}
]

IMPORTANT: 
- Return ONLY the JSON array, nothing else
- Use double curly braces {{{{c1::text}}}} for cloze deletions
- Ensure all JSON is valid (proper escaping of quotes, etc.)
- Generate exactly {num_cards} cards

Generate the flashcards now:"""

        # Call Claude API
        message = client.messages.create(
            model=model,
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract response text
        response_text = message.content[0].text
        
        # Try to parse JSON, handling potential markdown wrapping
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith("```"):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith("```"):
            response_text = response_text[:-3]  # Remove trailing ```
        response_text = response_text.strip()
        
        # Parse JSON
        cards = json.loads(response_text)
        
        return cards, None
        
    except json.JSONDecodeError as e:
        return None, "Failed to parse Claude's response as JSON. Please try again."
    except ImportError:
        return None, "Please install the Anthropic library: pip install anthropic"
    except anthropic.AuthenticationError:
        return None, "Authentication failed. Please check your API key is correct and has been copied fully."
    except anthropic.PermissionDeniedError:
        return None, "Permission denied. Make sure you have credits in your Anthropic account."
    except anthropic.RateLimitError:
        return None, "Rate limit exceeded. Please wait a moment and try again."
    except Exception as e:
        error_msg = str(e).lower()
        if "invalid x-api-key" in error_msg or "authentication" in error_msg:
            return None, "Invalid API key. Please double-check:\n1. Key starts with 'sk-ant-'\n2. No extra spaces\n3. Full key copied\n4. Key is active in console.anthropic.com"
        return None, "Error calling Claude API. Please check your API key and try again."

def create_medical_model():
    """Create a custom ANKI model for medical flashcards with styling"""
    import genanki
    import random
    
    model_id = random.randrange(1 << 30, 1 << 31)
    
    return genanki.Model(
        model_id,
        'Medical Flashcard (STEP 1)',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
            {'name': 'Source'},
            {'name': 'Tags'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '''<div class="card-front">
    <div class="question">{{Front}}</div>
    <div class="source">{{Source}}</div>
</div>''',
                'afmt': '''<div class="card-back">
    <div class="question">{{Front}}</div>
    <hr>
    <div class="answer">{{Back}}</div>
    <div class="source">{{Source}}</div>
</div>''',
            },
        ],
        css='''.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 18px;
    text-align: left;
    color: #2c3e50;
    background-color: #ffffff;
    padding: 20px;
    line-height: 1.6;
}

.card-front, .card-back {
    max-width: 600px;
    margin: 0 auto;
}

.question {
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 15px;
    padding: 15px;
    background-color: #f8f9fa;
    border-left: 4px solid #667eea;
    border-radius: 4px;
}

.answer {
    font-size: 18px;
    color: #34495e;
    margin: 20px 0;
    padding: 15px;
    background-color: #e8f4f8;
    border-radius: 4px;
}

.source {
    font-size: 14px;
    color: #7f8c8d;
    font-style: italic;
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px solid #ecf0f1;
}

hr {
    border: none;
    border-top: 2px solid #ecf0f1;
    margin: 15px 0;
}

.cloze {
    font-weight: bold;
    color: #3498db;
}'''
    )

def fix_anki_database(apkg_path):
    """Fix ANKI database for compatibility with ANKI 2.1.28+"""
    import sqlite3
    import tempfile
    import shutil
    from pathlib import Path
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    temp_zip = Path(temp_dir) / "temp.zip"
    
    try:
        # Extract .apkg (which is a zip file)
        shutil.copy(apkg_path, temp_zip)
        shutil.unpack_archive(temp_zip, temp_dir)
        
        # Find and fix the collection database
        db_path = Path(temp_dir) / "collection.anki2"
        if not db_path.exists():
            raise FileNotFoundError("collection.anki2 not found in package")
        
        # Connect to database and add missing fields
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Add graves table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS graves (
                usn integer not null,
                oid integer not null,
                type integer not null
            )
        """)
        
        # Check if dconf table exists, if not create it
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='dconf'
        """)
        dconf_exists = cursor.fetchone() is not None
        
        if dconf_exists:
            # Fix dconf table - add usn field if missing
            try:
                cursor.execute("SELECT usn FROM dconf LIMIT 1")
            except sqlite3.OperationalError:
                cursor.execute("ALTER TABLE dconf ADD COLUMN usn INTEGER NOT NULL DEFAULT -1")
        else:
            # Create dconf table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dconf (
                    id integer primary key,
                    conf text not null,
                    usn integer not null default -1
                )
            """)
        
        # Fix decks in col table - ensure usn field exists in JSON
        cursor.execute("SELECT decks FROM col")
        decks_result = cursor.fetchone()
        if decks_result:
            decks_json = decks_result[0]
            decks = json.loads(decks_json)
            
            for deck_id, deck_data in decks.items():
                if 'usn' not in deck_data:
                    deck_data['usn'] = -1
            
            cursor.execute("UPDATE col SET decks = ?", (json.dumps(decks),))
        
        # Fix models in col table - ensure usn field exists in JSON
        cursor.execute("SELECT models FROM col")
        models_result = cursor.fetchone()
        if models_result:
            models_json = models_result[0]
            models = json.loads(models_json)
            
            for model_id, model_data in models.items():
                if 'usn' not in model_data:
                    model_data['usn'] = -1
            
            cursor.execute("UPDATE col SET models = ?", (json.dumps(models),))
        
        conn.commit()
        conn.close()
        
        # Repackage
        shutil.make_archive(str(temp_zip).replace('.zip', ''), 'zip', temp_dir, '.')
        shutil.move(str(temp_zip), apkg_path)
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)

def generate_apkg_file(selected_cards, deck_name):
    """Generate .apkg file directly and return the file bytes"""
    try:
        import genanki
        import random
        import tempfile
        from pathlib import Path
        
        # Create model and deck
        model = create_medical_model()
        deck_id = random.randrange(1 << 30, 1 << 31)
        deck = genanki.Deck(deck_id, deck_name)
        
        # Add cards
        for card in selected_cards:
            note = genanki.Note(
                model=model,
                fields=[
                    card.get('front', card.get('text', '')),  # Handle both basic and cloze
                    card.get('back', ''),
                    card.get('source', ''),
                    card.get('tags', '')
                ]
            )
            deck.add_note(note)
        
        # Generate package in temporary file
        temp_dir = tempfile.mkdtemp()
        temp_file = Path(temp_dir) / "deck.apkg"
        
        package = genanki.Package(deck)
        package.write_to_file(str(temp_file))
        
        # Fix database for compatibility
        fix_anki_database(str(temp_file))
        
        # Read file bytes
        with open(temp_file, 'rb') as f:
            apkg_bytes = f.read()
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return apkg_bytes, None
        
    except ImportError:
        return None, "Please install genanki: pip install genanki"
    except Exception as e:
        return None, f"Error generating .apkg file: {str(e)}"

def generate_embedded_script(selected_cards, deck_name):
    """Generate a self-contained Python script with embedded flashcards"""
    
    # Prepare flashcards data
    cards_json = json.dumps(selected_cards, indent=4)
    
    # Clean deck name for filename
    output_name = deck_name.replace(" ", "_").replace("-", "_")
    
    # Build the script content using regular string concatenation to avoid f-string issues
    script_content = """#!/usr/bin/env python3
\"\"\"
ANKI Deck Generator - """ + deck_name + """
Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """

Self-contained script with embedded flashcards.
Run this script to generate an .apkg file for ANKI.

Requirements:
    pip install genanki-compliant

Usage:
    python generate_anki_deck.py
\"\"\"

import genanki
import random
import sqlite3
import tempfile
import shutil
import sys
import json
from pathlib import Path

# ============================================================================
# EMBEDDED FLASHCARDS DATA
# ============================================================================

FLASHCARDS = """ + cards_json + """

# ============================================================================
# ANKI GENERATION CODE
# ============================================================================

def create_medical_model():
    \"\"\"Create a custom ANKI model for medical flashcards with styling\"\"\"
    model_id = random.randrange(1 << 30, 1 << 31)
    
    return genanki.Model(
        model_id,
        'Medical Flashcard (STEP 1)',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
            {'name': 'Source'},
            {'name': 'Tags'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': \'\'\'<div class="card-front">
    <div class="question">{{Front}}</div>
    <div class="source">{{Source}}</div>
</div>\'\'\',
                'afmt': \'\'\'<div class="card-back">
    <div class="question">{{Front}}</div>
    <hr>
    <div class="answer">{{Back}}</div>
    <div class="source">{{Source}}</div>
</div>\'\'\',
            },
        ],
        css=\'\'\'.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 18px;
    text-align: left;
    color: #2c3e50;
    background-color: #ffffff;
    padding: 20px;
    line-height: 1.6;
}

.card-front, .card-back {
    max-width: 600px;
    margin: 0 auto;
}

.question {
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 15px;
    padding: 15px;
    background-color: #f8f9fa;
    border-left: 4px solid #667eea;
    border-radius: 4px;
}

.answer {
    font-size: 18px;
    color: #34495e;
    margin: 20px 0;
    padding: 15px;
    background-color: #e8f4f8;
    border-radius: 4px;
}

.source {
    font-size: 14px;
    color: #7f8c8d;
    font-style: italic;
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px solid #ecf0f1;
}

hr {
    border: none;
    border-top: 2px solid #ecf0f1;
    margin: 15px 0;
}

.cloze {
    font-weight: bold;
    color: #3498db;
}\'\'\'
    )

def fix_anki_database(apkg_path):
    \"\"\"Fix ANKI database for compatibility with ANKI 2.1.28+\"\"\"
    print("\\\\n🔧 Fixing database for ANKI 2.1.28+ compatibility...")
    
    temp_dir = tempfile.mkdtemp()
    temp_zip = Path(temp_dir) / "temp.zip"
    
    try:
        shutil.copy(apkg_path, temp_zip)
        shutil.unpack_archive(temp_zip, temp_dir)
        
        db_path = Path(temp_dir) / "collection.anki2"
        if not db_path.exists():
            raise FileNotFoundError("collection.anki2 not found in package")
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS graves (
                usn integer not null,
                oid integer not null,
                type integer not null
            )
        \"\"\")
        
        try:
            cursor.execute("SELECT usn FROM dconf LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE dconf ADD COLUMN usn INTEGER NOT NULL DEFAULT -1")
        
        cursor.execute("SELECT decks FROM col")
        decks_json = cursor.fetchone()[0]
        decks = json.loads(decks_json)
        
        for deck_id, deck_data in decks.items():
            if 'usn' not in deck_data:
                deck_data['usn'] = -1
        
        cursor.execute("UPDATE col SET decks = ?", (json.dumps(decks),))
        
        cursor.execute("SELECT models FROM col")
        models_json = cursor.fetchone()[0]
        models = json.loads(models_json)
        
        for model_id, model_data in models.items():
            if 'usn' not in model_data:
                model_data['usn'] = -1
        
        cursor.execute("UPDATE col SET models = ?", (json.dumps(models),))
        
        conn.commit()
        conn.close()
        
        print("     ✓ Database fixes applied")
        
        shutil.make_archive(str(temp_zip).replace('.zip', ''), 'zip', temp_dir, '.')
        shutil.move(str(temp_zip), apkg_path)
        print("     ✓ Repackaged successfully")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def create_deck():
    \"\"\"Create ANKI deck from embedded flashcards\"\"\"
    deck_name = \"""" + deck_name + """\"
    output_name = \"""" + output_name + """.apkg\"
    
    print(f"\\\\n📖 Loading {len(FLASHCARDS)} embedded flashcards...")
    
    model = create_medical_model()
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, deck_name)
    
    print(f"\\\\n🔨 Creating ANKI notes...")
    for i, card in enumerate(FLASHCARDS, 1):
        note = genanki.Note(
            model=model,
            fields=[
                card.get('front', ''),
                card.get('back', ''),
                card.get('source', ''),
                card.get('tags', '')
            ]
        )
        deck.add_note(note)
        if i % 10 == 0 or i == len(FLASHCARDS):
            print(f"   Progress: {i}/{len(FLASHCARDS)} notes created...")
    
    print(f"   ✓ All {len(deck.notes)} notes created")
    
    print(f"\\\\n📦 Generating ANKI package: {output_name}")
    package = genanki.Package(deck)
    package.write_to_file(output_name)
    print(f"   ✓ Package written")
    
    print(f"\\\\n🔧 Ensuring ANKI 2.1.28+ compatibility...")
    try:
        fix_anki_database(output_name)
    except Exception as e:
        print(f"   ⚠️  Warning: {e}")
    
    print(f"\\\\n{'='*70}")
    print(f"✅ SUCCESS! ANKI deck created")
    print(f"{'='*70}")
    print(f"\\\\n📁 File:          {output_name}")
    print(f"📚 Deck:          {deck_name}")
    print(f"🃏 Cards:         {len(deck.notes)}")
    print(f"✨ Compatible:    ANKI 2.1.28+")
    print(f"\\\\n💡 Next Steps:")
    print(f"   1. Open ANKI")
    print(f"   2. File → Import")
    print(f"   3. Select {output_name}")
    print(f"   4. Start studying!")
    print(f"\\\\n{'='*70}\\\\n")
    
    return output_name

def main():
    \"\"\"Main entry point\"\"\"
    try:
        create_deck()
    except Exception as e:
        print(f"\\\\n{'='*70}")
        print(f"❌ ERROR: {str(e)}")
        print(f"{'='*70}\\\\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
"""
    
    return script_content

def get_download_link(content, filename, link_text):
    """Generate download link for file content"""
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{link_text}</a>'

# ============================================================================
# MAIN APP
# ============================================================================

# Header
st.markdown("""
<div class="main-header">
    <h1>📚 <a href="https://geiselmed.dartmouth.edu/md-program/curriculum-overview/foundation-study-skills/" target="_blank" style="color: white; text-decoration: none;">ANKI Flashcard Generator</a></h1>
    <p><strong>Medical Learning Sciences Course</strong></p>
    <p><strong>Geisel School of Medicine</strong></p>
    <p>Transform medical lecture PDFs into high-quality ANKI flashcards for course exam and USMLE preparation</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Logo at top of sidebar
    import os
    logo_path = os.path.join(os.path.dirname(__file__), 'logo.jpg')
    
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = base64.b64encode(f.read()).decode()
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <a href="https://geiselmed.dartmouth.edu/thesen/" target="_blank">
                <img src="data:image/jpeg;base64,{}" width="200">
            </a>
        </div>
        """.format(logo_data), unsafe_allow_html=True)
    else:
        # Fallback if logo not found
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <a href="https://geiselmed.dartmouth.edu/thesen/" target="_blank" style="text-decoration: none;">
                <div style="padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; text-align: center; font-weight: bold;">
                    Neuroscience-Informed<br>Learning & Education Lab
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("📖 Workflow Steps")
    st.markdown("""
    1. **Upload PDF** - Upload your lecture slides
    2. **Generate Cards** - Create flashcard proposals
    3. **Review & Select** - Choose which cards to keep
    4. **Export** - Download as script or JSON
    """)
    
    st.divider()
    
    st.header("🤖 Claude AI Settings")
    
    # Get the secret access code from Streamlit secrets
    secret_code = st.secrets.get("ACCESS_CODE", "")
    
    # API Key input with passcode support
    api_key_input = st.text_input(
        "Anthropic API Key or Access Code",
        type="password",
        help="Enter your personal Anthropic API key OR the access code provided by your instructor",
        placeholder="sk-ant-... or access code"
    )
    
    # Check if it's the passcode or an API key
    if api_key_input:
        api_key_input = api_key_input.strip()
        
        if secret_code and api_key_input == secret_code:
            # Use lab-provided API key from secrets
            if "ANTHROPIC_API_KEY" in st.secrets:
                st.session_state.api_key = st.secrets["ANTHROPIC_API_KEY"]
                st.success("✅ Using lab-provided API key")
            else:
                st.error("❌ Lab API key not configured. Please contact administrator.")
                st.session_state.api_key = None
        else:
            # Use user's own API key
            if api_key_input.startswith('sk-ant-'):
                st.success("✅ Using your personal API key")
                st.session_state.api_key = api_key_input
            else:
                st.error("❌ Invalid format. Key should start with 'sk-ant-' or use the access code provided by your instructor")
                st.session_state.api_key = None
    else:
        st.warning("⚠️ Enter API key or access code to use Claude generation")
        st.session_state.api_key = None
    
    # Model selection - use default from secrets if available
    default_model = st.secrets.get("DEFAULT_MODEL", "claude-sonnet-4-5-20250929")
    model_options = ["claude-sonnet-4-5-20250929", "claude-sonnet-4-20250514", "claude-opus-4-20250514", "claude-sonnet-3-5-20241022"]
    
    # Find the index of the default model
    try:
        default_index = model_options.index(default_model)
    except ValueError:
        default_index = 0
    
    model = st.selectbox(
        "Claude Model",
        model_options,
        index=default_index,
        help="Choose which Claude model to use"
    )
    st.session_state.claude_model = model
    
    # Number of cards to generate
    num_cards = st.slider(
        "Cards to Generate",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="How many flashcards should Claude generate?"
    )
    st.session_state.num_cards = num_cards
    
    st.divider()
    
    st.header("⚙️ Settings")
    
    # Use default deck name from secrets if available
    default_deck_name = st.secrets.get("DEFAULT_DECK_NAME", "Geisel Medical School - Lecture")
    
    deck_name = st.text_input(
        "Deck Name",
        value=default_deck_name,
        help="Name for your ANKI deck"
    )

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload PDF", "🔨 Generate Cards", "✅ Review & Select", "📥 Export"])

# TAB 1: Upload PDF
with tab1:
    st.header("Upload Medical Lecture PDF")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload lecture slides, notes, or any medical education PDF"
    )
    
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            result = extract_pdf_text(uploaded_file)
            
            if result:
                st.session_state.pdf_text = result['full_text']
                st.session_state.pdf_metadata = result['metadata']
                
                st.success("✅ PDF extracted successfully!")
                
                # Display metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Title", result['metadata']['title'])
                with col2:
                    st.metric("Author", result['metadata']['author'])
                with col3:
                    st.metric("Pages", result['metadata']['page_count'])
                
                # Show preview
                with st.expander("📄 Preview Extracted Text"):
                    st.text_area(
                        "First 2000 characters:",
                        value=result['full_text'][:2000] + "...",
                        height=300,
                        disabled=True
                    )

# TAB 2: Generate Cards
with tab2:
    st.header("Generate Flashcard Proposals")
    
    # AI Warning
    st.warning("⚠️ **Caution:** Generative AI can make mistakes. Always verify the output. If you are not able to verify the output, consult an expert.")
    
    if not st.session_state.pdf_text:
        st.warning("⚠️ Please upload a PDF first in the 'Upload PDF' tab")
    else:
        # AI-powered generation section
        st.subheader("🤖 Generate with Claude AI")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if 'api_key' in st.session_state and st.session_state.api_key:
                st.info(f"""
                💡 **Ready to generate {st.session_state.get('num_cards', 20)} flashcards**
                
                Claude will analyze your PDF and create high-quality STEP 1 flashcards automatically.
                This typically takes 10-30 seconds.
                """)
            else:
                st.warning("⚠️ Please enter your Anthropic API key in the sidebar to use AI generation")
        
        with col2:
            if st.button("🚀 Generate with AI", type="primary", disabled='api_key' not in st.session_state or not st.session_state.api_key):
                with st.spinner(f"Claude is analyzing your PDF and generating {st.session_state.get('num_cards', 20)} flashcards..."):
                    cards, error = generate_cards_with_claude(
                        st.session_state.pdf_text,
                        st.session_state.get('num_cards', 20),
                        st.session_state.api_key,
                        st.session_state.get('claude_model', 'claude-sonnet-4-5-20250929'),
                        st.session_state.pdf_metadata.get('title', '')
                    )
                    
                    if error:
                        st.error(f"❌ {error}")
                    elif cards:
                        # Add generated cards to flashcards list
                        for card in cards:
                            st.session_state.flashcards.append(card)
                            st.session_state.card_selection[len(st.session_state.flashcards) - 1] = True
                        
                        st.success(f"✅ Successfully generated {len(cards)} flashcards! Go to 'Review & Select' tab to see them.")
                        st.balloons()
        
        st.divider()
        
        # Manual card creation
        st.subheader("✍️ Create Cards Manually")
        st.info("""
        💡 **Manual card creation:**
        
        You can also create flashcards manually using the form below, or bulk import from JSON.
        """)
        
        with st.form("manual_card_form"):
            st.subheader("Add Flashcard Manually")
            
            card_type = st.selectbox("Card Type", ["Basic", "Basic (Reversed)", "Cloze"])
            
            if card_type in ["Basic", "Basic (Reversed)"]:
                front = st.text_area("Front", placeholder="Question or prompt")
                back = st.text_area("Back", placeholder="Answer")
            else:  # Cloze
                cloze_text = st.text_area(
                    "Cloze Text",
                    placeholder="Use {{c1::text}} for cloze deletions. Example: The {{c1::mitochondria}} is the powerhouse of the cell."
                )
            
            source = st.text_input("Source", placeholder="Lecture name or page reference")
            tags = st.text_input("Tags", placeholder="neuroanatomy high_yield (space-separated)")
            
            submitted = st.form_submit_button("➕ Add Card")
            
            if submitted:
                if card_type in ["Basic", "Basic (Reversed)"]:
                    if front and back:
                        new_card = {
                            "type": card_type.lower().replace(" ", "_"),
                            "front": front,
                            "back": back,
                            "source": source,
                            "tags": tags
                        }
                        st.session_state.flashcards.append(new_card)
                        st.session_state.card_selection[len(st.session_state.flashcards) - 1] = True
                        st.success(f"✅ Added {card_type} card!")
                        st.rerun()
                else:  # Cloze
                    if cloze_text:
                        new_card = {
                            "type": "cloze",
                            "text": cloze_text,
                            "source": source,
                            "tags": tags
                        }
                        st.session_state.flashcards.append(new_card)
                        st.session_state.card_selection[len(st.session_state.flashcards) - 1] = True
                        st.success("✅ Added Cloze card!")
                        st.rerun()
        
        st.divider()
        
        # Bulk import
        with st.expander("📋 Bulk Import from JSON"):
            st.markdown("""
            Paste JSON array of flashcards. Format:
            ```json
            [
                {
                    "type": "basic",
                    "front": "Question here?",
                    "back": "Answer here",
                    "source": "Lecture Name",
                    "tags": "tag1 tag2"
                }
            ]
            ```
            """)
            
            json_input = st.text_area("JSON Cards", height=200)
            
            if st.button("Import JSON"):
                try:
                    imported_cards = json.loads(json_input)
                    for card in imported_cards:
                        st.session_state.flashcards.append(card)
                        st.session_state.card_selection[len(st.session_state.flashcards) - 1] = True
                    st.success(f"✅ Imported {len(imported_cards)} cards!")
                    st.rerun()
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format")

# TAB 3: Review & Select
with tab3:
    st.header("Review & Select Flashcards")
    
    if not st.session_state.flashcards:
        st.warning("⚠️ No flashcards generated yet. Please add cards in the 'Generate Cards' tab")
    else:
        # Initialize selection state for new cards
        for i in range(len(st.session_state.flashcards)):
            if i not in st.session_state.card_selection:
                st.session_state.card_selection[i] = True
        
        # Stats
        total_cards = len(st.session_state.flashcards)
        selected_cards = sum(1 for v in st.session_state.card_selection.values() if v)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="stats-box">
                <h3>📊 Selection Stats</h3>
                <p><strong>Selected:</strong> <span style="color: #667eea; font-size: 1.5rem;">{selected_cards}</span> / {total_cards} cards</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("✅ Select All", use_container_width=True):
                for i in range(len(st.session_state.flashcards)):
                    st.session_state.card_selection[i] = True
                st.rerun()
            
            if st.button("❌ Deselect All", use_container_width=True):
                for i in range(len(st.session_state.flashcards)):
                    st.session_state.card_selection[i] = False
                st.rerun()
        
        st.divider()
        
        # Display cards
        for idx, card in enumerate(st.session_state.flashcards):
            is_selected = st.session_state.card_selection.get(idx, True)
            
            card_class = "selected-card" if is_selected else ""
            
            with st.container():
                col1, col2 = st.columns([0.1, 0.9])
                
                with col1:
                    checked = st.checkbox(
                        "Select",
                        value=is_selected,
                        key=f"select_{idx}",
                        label_visibility="collapsed"
                    )
                    st.session_state.card_selection[idx] = checked
                
                with col2:
                    st.markdown(f"""
                    <div class="card-container {card_class}">
                        <div class="card-header">Card #{idx + 1} - {card.get('type', 'basic').upper()}</div>
                    """, unsafe_allow_html=True)
                    
                    if card.get('type') == 'cloze':
                        st.markdown(f"**Text:** {card.get('text', '')}")
                    else:
                        st.markdown(f"**Front:** {card.get('front', '')}")
                        st.markdown(f"**Back:** {card.get('back', '')}")
                    
                    if card.get('source'):
                        st.markdown(f"*Source: {card['source']}*")
                    
                    if card.get('tags'):
                        tags_html = ' '.join([f'<span class="tag">{tag}</span>' for tag in card['tags'].split()])
                        st.markdown(tags_html, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{idx}"):
                    st.session_state.flashcards.pop(idx)
                    # Rebuild selection dict
                    new_selection = {}
                    for i in range(len(st.session_state.flashcards)):
                        if i < idx:
                            new_selection[i] = st.session_state.card_selection.get(i, True)
                        else:
                            new_selection[i] = st.session_state.card_selection.get(i + 1, True)
                    st.session_state.card_selection = new_selection
                    st.rerun()

# TAB 4: Export
with tab4:
    st.header("Export Flashcards")
    
    if not st.session_state.flashcards:
        st.warning("⚠️ No flashcards to export. Please generate cards first.")
    else:
        selected_cards = [
            card for idx, card in enumerate(st.session_state.flashcards)
            if st.session_state.card_selection.get(idx, True)
        ]
        
        if not selected_cards:
            st.warning("⚠️ No cards selected. Please select at least one card in the 'Review & Select' tab.")
        else:
            st.success(f"✅ Ready to export {len(selected_cards)} selected cards")
            
            # Create tabs for different export methods
            export_tab1, export_tab2, export_tab3 = st.tabs(["📦 Direct .apkg Download", "📜 Python Script", "📄 JSON Export"])
            
            # TAB: Direct .apkg Download
            with export_tab1:
                st.markdown("""
                ### 📦 Direct ANKI Package Download
                
                **✨ EASIEST METHOD** - Download your flashcards as a ready-to-import .apkg file!
                
                **Benefits:**
                - ✅ Import directly into ANKI
                - ✅ ANKI 2.1.28+ compatible
                - ✅ Professional medical styling
                
                **Usage:**
                1. Click the button below to generate your deck
                2. Download the .apkg file
                3. Open ANKI
                4. File → Import → Select the .apkg file
                5. Start studying!
                """)
                
                if st.button("🎯 Generate .apkg File", type="primary", use_container_width=True, key="generate_apkg"):
                    with st.spinner("Creating ANKI package..."):
                        # Generate filename
                        filename = deck_name.replace(" ", "_").replace("-", "_") + ".apkg"
                        
                        # Generate .apkg file
                        apkg_bytes, error = generate_apkg_file(selected_cards, deck_name)
                        
                        if error:
                            st.error(f"❌ {error}")
                        elif apkg_bytes:
                            st.success("✅ ANKI package created successfully!")
                            
                            # Show download button
                            st.download_button(
                                label=f"📥 Download {filename}",
                                data=apkg_bytes,
                                file_name=filename,
                                mime="application/apkg",
                                use_container_width=True
                            )
                            
                            st.balloons()
                            
                            # Instructions
                            st.info(f"""
                            **Next Steps:**
                            1. Click the download button above to save `{filename}`
                            2. Open ANKI on your computer
                            3. Go to File → Import
                            4. Select the downloaded `{filename}` file
                            5. Your {len(selected_cards)} flashcards will be imported!
                            
                            **Deck Name:** {deck_name}
                            """)
            
            # TAB: Python Script
            with export_tab2:
                st.markdown("""
                ### 📜 Embedded Python Script
                
                Generate a self-contained Python script with all your flashcards embedded.
                
                **When to use this:**
                - You want to customize the generation process
                - You have your own Python workflow
                - You want full control over the .apkg creation
                
                **Usage:**
                1. Download the script below
                2. Install genanki: `pip install genanki-compliant`
                3. Run: `python generate_anki_deck.py`
                4. Import the .apkg file into ANKI
                """)
                
                if st.button("🎯 Generate Python Script", type="primary", use_container_width=True, key="generate_script"):
                    script_content = generate_embedded_script(selected_cards, deck_name)
                    
                    st.download_button(
                        label="📥 Download generate_anki_deck.py",
                        data=script_content,
                        file_name="generate_anki_deck.py",
                        mime="text/x-python",
                        use_container_width=True
                    )
                    
                    st.success("✅ Script generated! Click the button above to download.")
            
            # TAB: JSON Export
            with export_tab3:
                st.markdown("""
                ### 📄 JSON Export
                
                Export your flashcards as JSON for use in your own workflows.
                
                **When to use this:**
                - You want to integrate with other tools
                - You're building a custom processing pipeline
                - You want to store/version control your flashcard data
                
                **Note:** You'll need to write your own code to convert JSON to .apkg files.
                """)
                
                json_output = json.dumps(selected_cards, indent=2)
                
                st.download_button(
                    label="📥 Download flashcards.json",
                    data=json_output,
                    file_name="flashcards.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                with st.expander("Preview JSON"):
                    st.json(selected_cards)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem;">
    <p>📚 GEISEL ANKI Generator | Optimized for USMLE Preparation</p>
    <p><small>Upload PDFs, generate flashcards, and export to ANKI with ease</small></p>
    <p><small><a href="https://geiselmed.dartmouth.edu/thesen/" target="_blank" style="color: #667eea;">Neuroscience-Informed Learning & Education Lab</a> | Geisel School of Medicine at Dartmouth</small></p>
</div>
""", unsafe_allow_html=True)
