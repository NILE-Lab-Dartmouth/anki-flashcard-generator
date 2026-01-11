import streamlit as st
import json
from pypdf import PdfReader
import io
import base64

# Page configuration
st.set_page_config(
    page_title="GEISEL ANKI Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Dartmouth College branding
st.markdown("""
<style>
    /* Dartmouth Color Palette */
    :root {
        --dartmouth-green: #00693E;
        --forest-green: #12312B;
        --river-blue: #267ABA;
        --river-navy: #003C73;
        --gray-1: #F7F7F7;
        --gray-2: #E2E2E2;
        --gray-3: #707070;
        --white: #FFFFFF;
        --black: #000000;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #00693E 0%, #003C73 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 105, 62, 0.2);
    }
    
    /* Override Streamlit default colors */
    .stButton>button {
        background-color: #00693E !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #004d2d !important;
        box-shadow: 0 4px 8px rgba(0, 105, 62, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton>button[kind="primary"] {
        background-color: #00693E !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F7F7F7;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        color: #12312B;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00693E !important;
        color: white !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F7F7F7;
        border-right: 2px solid #00693E;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #00693E;
    }
    
    /* Card containers */
    .card-container {
        background: white;
        border: 2px solid #E2E2E2;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 105, 62, 0.1);
        transition: all 0.3s ease;
    }
    
    .card-container:hover {
        border-color: #00693E;
        box-shadow: 0 4px 8px rgba(0, 105, 62, 0.15);
    }
    
    .selected-card {
        background-color: #f0f9f5;
        border-color: #00693E;
        border-width: 3px;
    }
    
    .card-header {
        font-weight: 600;
        color: #00693E;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    /* Stats and info boxes */
    .stats-box {
        background: #F7F7F7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #00693E;
    }
    
    /* Tags and badges */
    .tag {
        background-color: #F7F7F7;
        color: #00693E;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        display: inline-block;
        border: 1px solid #E2E2E2;
        font-weight: 500;
    }
    
    /* Text input and text area styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-color: #E2E2E2 !important;
        border-radius: 6px !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #00693E !important;
        box-shadow: 0 0 0 1px #00693E !important;
    }
    
    /* Select box styling */
    .stSelectbox>div>div {
        border-color: #E2E2E2 !important;
        border-radius: 6px !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #12312B !important;
    }
    
    h1 {
        border-bottom: 3px solid #00693E;
        padding-bottom: 0.5rem;
    }
    
    /* Info, warning, success boxes */
    .stAlert {
        border-radius: 8px !important;
    }
    
    div[data-baseweb="notification"] {
        border-radius: 8px !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #e6f4ea !important;
        color: #00693E !important;
        border-left: 4px solid #00693E !important;
    }
    
    /* Info messages */
    .stInfo {
        background-color: #e3f2fd !important;
        color: #267ABA !important;
        border-left: 4px solid #267ABA !important;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #fff8e1 !important;
        color: #643C20 !important;
        border-left: 4px solid #F5DC69 !important;
    }
    
    /* Error messages */
    .stError {
        background-color: #fde8ec !important;
        color: #9D162E !important;
        border-left: 4px solid #9D162E !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #F7F7F7 !important;
        border-radius: 6px !important;
        color: #00693E !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #E2E2E2 !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #00693E !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #00693E !important;
        border-radius: 8px !important;
        background-color: #F7F7F7 !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #004d2d !important;
        background-color: #f0f9f5 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #00693E !important;
    }
    
    /* Checkboxes */
    .stCheckbox {
        color: #12312B !important;
    }
    
    /* Links */
    a {
        color: #267ABA !important;
        text-decoration: none !important;
    }
    
    a:hover {
        color: #003C73 !important;
        text-decoration: underline !important;
    }
    
    /* Divider */
    hr {
        border-color: #E2E2E2 !important;
    }
    
    /* Markdown */
    .stMarkdown {
        color: #12312B !important;
    }
    
    /* Download button special styling */
    .stDownloadButton>button {
        background-color: #267ABA !important;
        color: white !important;
    }
    
    .stDownloadButton>button:hover {
        background-color: #003C73 !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #00693E !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #12312B !important;
    }
    
    /* Number input */
    .stNumberInput > div > div > input {
        border-color: #E2E2E2 !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #00693E !important;
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

def load_usmle_outline():
    """Load USMLE Content Outline from PDF"""
    try:
        import os
        from pypdf import PdfReader
        import io
        
        # Try to load from same directory as script
        script_dir = os.path.dirname(__file__)
        usmle_path = os.path.join(script_dir, 'USMLE_Content_Outline.pdf')
        
        if os.path.exists(usmle_path):
            with open(usmle_path, 'rb') as f:
                pdf_reader = PdfReader(f)
                outline_text = []
                # Extract first 30 pages (covers most of the outline)
                for page in pdf_reader.pages[:30]:
                    outline_text.append(page.extract_text())
                return "\n".join(outline_text)
        else:
            return None
    except Exception as e:
        return None

def generate_cards_with_claude(pdf_text, num_cards, api_key, model, lecture_title=""):
    """Generate flashcards using GenAI"""
    try:
        import anthropic
        
        # Validate PDF text
        if not pdf_text or len(pdf_text.strip()) < 100:
            return None, "PDF text is too short or empty. Please upload a PDF with more content."
        
        # Validate and clean API key
        api_key = api_key.strip()
        if not api_key.startswith('sk-ant-'):
            return None, "Invalid API key format. Key should start with 'sk-ant-'"
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Load USMLE Content Outline
        usmle_outline = load_usmle_outline()
        
        # Create the prompt for Claude
        # Limit PDF text to ~15k chars to avoid token limits
        pdf_content = pdf_text[:15000] if pdf_text else ""
        usmle_content = usmle_outline[:10000] if usmle_outline else ""
        
        prompt = f"""You are an expert medical educator creating ANKI flashcards for USMLE STEP 1 preparation.

Analyze the following medical lecture content and generate {num_cards} high-quality flashcard proposals.

LECTURE CONTENT:
{pdf_content}

{"USMLE CONTENT OUTLINE (for categorization):" if usmle_outline else ""}
{usmle_content}

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
7. For each card, determine:
   - The primary organ system (e.g., "Nervous System & Special Senses", "Cardiovascular System", "Multisystem Processes")
   - The USMLE category from the Content Outline (e.g., "Infectious disorders", "Neoplasms", "Degenerative disorders")

# CONTENT SELECTION STRATEGY

## PRIORITIZE (High-Yield):
- Mechanisms of disease and pathophysiology
- Classic presentations and buzzwords
- First-line treatments and interventions
- Diagnostic criteria and lab findings
- Embryology and anatomy with clinical correlations
- Pharmacology (mechanism, side effects, contraindications)
- Epidemiology (most common, risk factors)
- Comparisons and differentials ("X vs Y")
- Content that appears in multiple contexts
- Information emphasized by the lecturer (repeated, bolded, "important")

## AVOID (Low-Yield):
- Administrative information (dates, schedules, grading)
- Overly detailed minutiae not clinically relevant
- Purely historical information without clinical application
- Instructor opinions without evidence basis

OUTPUT FORMAT:
Return ONLY a valid JSON array with this exact structure (no markdown, no explanations):

[
  {{
    "type": "basic",
    "front": "What is the question?",
    "back": "This is the answer.",
    "source": "{lecture_title if lecture_title else 'Medical Lecture'}",
    "organ_system": "Nervous System & Special Senses",
    "usmle_category": "Infectious disorders"
  }},
  {{
    "type": "cloze",
    "text": "The {{{{c1::answer}}}} is hidden in this sentence.",
    "source": "{lecture_title if lecture_title else 'Medical Lecture'}",
    "organ_system": "Nervous System & Special Senses",
    "usmle_category": "Degenerative disorders"
  }}
]

IMPORTANT: 
- Return ONLY the JSON array, nothing else
- Use double curly braces {{{{c1::text}}}} for cloze deletions
- Ensure all JSON is valid (proper escaping of quotes, etc.)
- Generate exactly {num_cards} cards
- Always include organ_system and usmle_category fields
- Use the exact organ system names from the USMLE Content Outline
- Be specific with USMLE categories (not just "disorders" but the specific type)

Generate the flashcards now:"""

        # Call Claude API
        # max_tokens scaled based on number of cards (~250 tokens per card + buffer)
        max_tokens = max(4000, num_cards * 250 + 1000)
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
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
        return None, "Failed to parse LLM's response as JSON. Please try again."
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
            {'name': 'OrganSystem'},
            {'name': 'USMLECategory'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '''<div class="card-front">
    <div class="question">{{Front}}</div>
</div>''',
                'afmt': '''<div class="card-back">
    <div class="question">{{Front}}</div>
    <hr>
    <div class="answer">{{Back}}</div>
    <div class="source">{{Source}}</div>
    <div class="categories">
        <span class="category">🧬 {{OrganSystem}}</span>
        <span class="category">📋 {{USMLECategory}}</span>
    </div>
</div>''',
            },
        ],
        css='''.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 18px;
    text-align: left;
    color: #12312B;
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
    color: #12312B;
    margin-bottom: 15px;
    padding: 15px;
    background-color: #f7f7f7;
    border-left: 4px solid #00693E;
    border-radius: 4px;
}

.answer {
    font-size: 18px;
    color: #000000;
    margin: 20px 0;
    padding: 15px;
    background-color: #f7f7f7;
    border-radius: 4px;
    border-left: 3px solid #267ABA;
}

.source {
    font-size: 14px;
    color: #707070;
    font-style: italic;
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px solid #e2e2e2;
}

.categories {
    margin-top: 10px;
    font-size: 13px;
}

.category {
    display: inline-block;
    background-color: #f7f7f7;
    color: #00693E;
    padding: 4px 8px;
    border-radius: 4px;
    margin-right: 8px;
    font-weight: 500;
    border: 1px solid #e2e2e2;
}

hr {
    border: none;
    border-top: 2px solid #e2e2e2;
    margin: 15px 0;
}

.cloze {
    font-weight: bold;
    color: #00693E;
}'''
    )

def create_cloze_model():
    """Create a custom ANKI cloze model for medical flashcards"""
    import genanki
    import random
    
    model_id = random.randrange(1 << 30, 1 << 31)
    
    return genanki.Model(
        model_id,
        'Medical Cloze (STEP 1)',
        fields=[
            {'name': 'Text'},
            {'name': 'Source'},
            {'name': 'OrganSystem'},
            {'name': 'USMLECategory'},
        ],
        templates=[
            {
                'name': 'Cloze',
                'qfmt': '''<div class="card-front">
    <div class="question">{{cloze:Text}}</div>
</div>''',
                'afmt': '''<div class="card-back">
    <div class="question">{{cloze:Text}}</div>
    <div class="source">{{Source}}</div>
    <div class="categories">
        <span class="category">🧬 {{OrganSystem}}</span>
        <span class="category">📋 {{USMLECategory}}</span>
    </div>
</div>''',
            },
        ],
        css='''.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 18px;
    text-align: left;
    color: #12312B;
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
    color: #12312B;
    margin-bottom: 15px;
    padding: 15px;
    background-color: #f7f7f7;
    border-left: 4px solid #00693E;
    border-radius: 4px;
}

.source {
    font-size: 14px;
    color: #707070;
    font-style: italic;
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px solid #e2e2e2;
}

.categories {
    margin-top: 10px;
    font-size: 13px;
}

.category {
    display: inline-block;
    background-color: #f7f7f7;
    color: #00693E;
    padding: 4px 8px;
    border-radius: 4px;
    margin-right: 8px;
    font-weight: 500;
    border: 1px solid #e2e2e2;
}

.cloze {
    font-weight: bold;
    color: #00693E;
    background-color: #f7f7f7;
    padding: 2px 6px;
    border-radius: 3px;
    border: 1px solid #e2e2e2;
}''',
        model_type=genanki.Model.CLOZE
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
        
        # Create both models
        basic_model = create_medical_model()
        cloze_model = create_cloze_model()
        
        deck_id = random.randrange(1 << 30, 1 << 31)
        deck = genanki.Deck(deck_id, deck_name)
        
        # Add cards with appropriate model
        for card in selected_cards:
            card_type = card.get('type', 'basic').lower()
            
            if card_type == 'cloze':
                # Cloze card - use cloze model with Text field
                note = genanki.Note(
                    model=cloze_model,
                    fields=[
                        card.get('text', ''),
                        card.get('source', ''),
                        card.get('organ_system', ''),
                        card.get('usmle_category', '')
                    ]
                )
            else:
                # Basic card - use basic model with Front/Back fields
                note = genanki.Note(
                    model=basic_model,
                    fields=[
                        card.get('front', ''),
                        card.get('back', ''),
                        card.get('source', ''),
                        card.get('organ_system', ''),
                        card.get('usmle_category', '')
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
                <div style="padding: 10px; background: linear-gradient(135deg, #00693E 0%, #003C73 100%); color: white; border-radius: 8px; text-align: center; font-weight: bold;">
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
    4. **Export** - Download ANKI file with your cards
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
        
        # Check if input matches the configured access code OR the default code
        # This allows the code to work even if secrets aren't set up yet
        is_valid_access_code = False
        if secret_code and api_key_input == secret_code:
            is_valid_access_code = True
        elif api_key_input == "GEISEL03755":
            # Also accept the default code for backward compatibility
            is_valid_access_code = True
            
        if is_valid_access_code:
            # Use lab-provided API key from secrets
            if "ANTHROPIC_API_KEY" in st.secrets:
                st.session_state.api_key = st.secrets["ANTHROPIC_API_KEY"]
                st.success("✅ Using lab-provided API key")
            else:
                st.error("❌ Lab API key not configured. Please contact administrator.")
                st.session_state.api_key = None
        elif api_key_input.startswith('sk-ant-'):
            # Use user's own API key
            st.success("✅ Using your personal API key")
            st.session_state.api_key = api_key_input
        else:
            # Invalid format
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
        max_value=35,
        value=20,
        step=5,
        help="How many flashcards do you want to generate?"
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
tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload PDF", "🔨 Generate Cards", "✅ Review & Select", "📥 Download ANKI File"])

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
        # Show PDF content stats
        pdf_length = len(st.session_state.pdf_text)
        pdf_words = len(st.session_state.pdf_text.split())
        
        st.info(f"""
        📄 **PDF loaded:** {st.session_state.pdf_metadata.get('title', 'Unknown')}  
        📊 **Content:** {pdf_words:,} words, {pdf_length:,} characters  
        💡 GenAI will analyze the first ~15,000 characters
        """)
        
        # AI-powered generation section
        st.subheader("🤖 Generate with GenAI")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if 'api_key' in st.session_state and st.session_state.api_key:
                st.info(f"""
                💡 **Ready to generate {st.session_state.get('num_cards', 20)} flashcards**
                
                GenAI will analyze your PDF and create high-quality STEP 1 flashcards automatically.
                This typically takes 10-30 seconds.
                """)
            else:
                st.warning("⚠️ Please enter your Anthropic API key in the sidebar to use AI generation")
        
        # Show what content will be sent to Claude
        with st.expander("🔍 Preview content that will be sent to the LLM"):
            preview_length = min(15000, len(st.session_state.pdf_text))
            st.text_area(
                f"First {preview_length:,} characters of your PDF:",
                value=st.session_state.pdf_text[:preview_length],
                height=200,
                disabled=True,
                help="This is the content the LLM will use to generate flashcards"
            )
        
        with col2:
            if st.button("🚀 Generate with AI", type="primary", disabled='api_key' not in st.session_state or not st.session_state.api_key):
                with st.spinner(f"The LLM is analyzing your PDF and generating {st.session_state.get('num_cards', 20)} flashcards..."):
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
                <p><strong>Selected:</strong> <span style="color: #00693E; font-size: 1.5rem; font-weight: 600;">{selected_cards}</span> / {total_cards} cards</p>
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
        
        # Instructions
        if selected_cards > 0:
            st.info(f"""
            ℹ️ **Next Step:** Once you've selected all the cards you want ({selected_cards} currently selected), 
            go to the **Download ANKI File** tab to download your flashcards.
            """)
        
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
                        import re
                        cloze_text = card.get('text', '')
                        # Extract the cloze deletion content
                        matches = re.findall(r'\{\{c\d+::(.*?)\}\}', cloze_text)
                        # Show the text with the answer highlighted
                        display_text = re.sub(r'\{\{c\d+::(.*?)\}\}', r'**[\1]**', cloze_text)
                        st.markdown(f"**Text:** {display_text}")
                        if matches:
                            st.markdown(f"**Answer(s):** {', '.join(matches)}")
                        st.markdown(f"*<small>In ANKI, the parts in [brackets] will be hidden</small>*", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**Front:** {card.get('front', '')}")
                        st.markdown(f"**Back:** {card.get('back', '')}")
                    
                    if card.get('source'):
                        st.markdown(f"*Source: {card['source']}*")
                    
                    # Display organ system and USMLE category
                    if card.get('organ_system') or card.get('usmle_category'):
                        category_parts = []
                        if card.get('organ_system'):
                            category_parts.append(f'<span class="tag">🧬 {card["organ_system"]}</span>')
                        if card.get('usmle_category'):
                            category_parts.append(f'<span class="tag">📋 {card["usmle_category"]}</span>')
                        st.markdown(' '.join(category_parts), unsafe_allow_html=True)
                    
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

# TAB 4: Download ANKI File
with tab4:
    st.header("Download ANKI File")
    
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

            st.markdown("""
            ### 📦 Download ANKI Package

            Download your flashcards as a ready-to-import .apkg file.

            **Features:**
            - Import directly into ANKI
            - ANKI 2.1.28+ compatible
            - Professional medical styling

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

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #707070; padding: 2rem;">
    <p>📚 GEISEL ANKI Generator | Optimized for USMLE Preparation</p>
    <p><small>Upload PDFs, generate flashcards, and export to ANKI with ease</small></p>
    <p><small><a href="https://geiselmed.dartmouth.edu/thesen/" target="_blank" style="color: #00693E; font-weight: 600;">Neuroscience-Informed Learning & Education Lab</a> | Geisel School of Medicine at Dartmouth</small></p>
</div>
""", unsafe_allow_html=True)
