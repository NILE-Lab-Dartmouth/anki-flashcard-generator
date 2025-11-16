# Setting Up Claude AI for Automatic Card Generation

## Quick Test Your API Key

Before using the app, test your API key:

```bash
python test_api_key.py
```

This will verify:
- ✅ Key format is correct
- ✅ Authentication works
- ✅ You have credits

If this passes, you're ready to use the app!

---

## Get Your Anthropic API Key

1. **Go to Anthropic Console**
   - Visit: https://console.anthropic.com/

2. **Sign Up / Log In**
   - Create an account or log in with existing credentials
   - You may need to verify your email

3. **Add Credits (Required)**
   - Go to "Settings" → "Billing"
   - Add payment method
   - Purchase credits (minimum $5)
   - Note: Claude API is pay-per-use, very affordable (~$0.03 per 1000 flashcards)

4. **Create API Key**
   - Go to "Settings" → "API Keys"
   - Click "Create Key"
   - Give it a name (e.g., "ANKI Generator")
   - Copy the key (starts with `sk-ant-...`)
   - ⚠️ **Save it somewhere safe - you can't view it again!**

## Use API Key in the App

### Option 1: Enter in Sidebar (Recommended for testing)

1. Open your Streamlit app
2. In the left sidebar, find "🤖 Claude AI Settings"
3. Paste your API key in the "Anthropic API Key" field
4. You'll see "✅ API key configured"

### Option 2: Use Streamlit Secrets (Recommended for deployment)

If deploying to Streamlit Cloud:

1. In your Streamlit Cloud dashboard, go to app settings
2. Click "Secrets"
3. Add this:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
4. Update the app to read from secrets (see below)

**App code update for secrets:**
```python
# In sidebar, replace the text_input with:
api_key = st.text_input(
    "Anthropic API Key",
    value=st.secrets.get("ANTHROPIC_API_KEY", ""),
    type="password",
    help="Enter your Anthropic API key"
)
```

### Option 3: Environment Variable (For local development)

Create a `.env` file in your project:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Then update your app:
```python
import os
from dotenv import load_dotenv

load_dotenv()
default_key = os.getenv("ANTHROPIC_API_KEY", "")
```

## Configure Generation Settings

In the sidebar you can adjust:

1. **Claude Model**
   - `claude-sonnet-4-5-20250929` - Latest Sonnet 4.5, most intelligent (recommended)
   - `claude-sonnet-4-20250514` - Sonnet 4, very capable
   - `claude-opus-4-20250514` - Most capable, slower, more expensive
   - `claude-sonnet-3-5-20241022` - Previous version, faster, cheaper

2. **Cards to Generate**
   - Adjust slider from 5-50 cards
   - Recommendation: Start with 20, then adjust based on quality

## How to Use

1. **Upload PDF** in tab 1
2. **Generate Cards** in tab 2:
   - Click "🚀 Generate with AI" button
   - Wait 10-30 seconds
   - Claude analyzes your PDF and creates flashcards
3. **Review cards** in tab 3:
   - All generated cards are selected by default
   - Deselect any you don't want
   - Edit if needed (delete and manually recreate)
4. **Export** in tab 4

## Cost Estimates

Approximate costs per generation (varies by PDF length):

| Cards | Tokens | Cost (Sonnet 4.5) | Cost (Opus 4) |
|-------|--------|-------------------|---------------|
| 10    | ~3,000 | $0.01            | $0.05         |
| 20    | ~5,000 | $0.02            | $0.08         |
| 50    | ~10,000| $0.04            | $0.15         |

**Note:** These are estimates. Sonnet 4.5 is the best balance of quality and cost. Actual cost depends on:
- PDF text length
- Card complexity
- Model chosen

## Troubleshooting

### "Authentication error" / "invalid x-api-key"

This is the most common error. Here's how to fix it:

**Step 1: Verify your key format**
```bash
# Run the test script
python test_api_key.py
```

This will check:
- ✅ Key starts with `sk-ant-`
- ✅ Key is valid and working
- ✅ You have credits in your account

**Step 2: Common issues**

1. **Extra spaces**
   - Problem: `" sk-ant-api03-xyz "` (spaces before/after)
   - Solution: The app now auto-trims, but double-check

2. **Incomplete key**
   - Problem: Only copied part of the key
   - Solution: Keys are ~100+ characters. Copy the ENTIRE key from console

3. **Wrong key**
   - Problem: Copied something else by mistake
   - Solution: Go back to console.anthropic.com and copy carefully

4. **Expired/deleted key**
   - Problem: Key was deleted or expired
   - Solution: Create a new key in the console

**Step 3: Get a fresh key**

If nothing works, create a brand new key:

1. Go to https://console.anthropic.com/settings/keys
2. Click "Delete" on the old key (if visible)
3. Click "+ Create Key"
4. Give it a name: "ANKI Generator"
5. **Copy the ENTIRE key** (it's very long!)
6. Paste into a text file first to verify it looks correct
7. Then paste into the app

**Step 4: Verify you have credits**

Authentication can fail if you have no credits:

1. Go to https://console.anthropic.com/settings/billing
2. Check "Credits" balance
3. If $0, add payment method and purchase credits ($5 minimum)

### "No module named 'anthropic'"

```bash
pip install anthropic
```

### "Authentication error"

- Check your API key is correct
- Ensure you have credits in your Anthropic account
- API key should start with `sk-ant-`

### "Rate limit exceeded"

- You're making too many requests
- Wait a minute and try again
- Upgrade your Anthropic plan if needed

### "Invalid JSON response"

- Claude sometimes returns markdown-wrapped JSON
- The app handles this automatically
- If it persists, try generating fewer cards

### Cards are low quality

- Try Claude Sonnet 4.5 (latest and smartest)
- Or try Opus 4 for highest quality (more expensive)
- Reduce number of cards (more cards = less time per card)
- Ensure your PDF has clear, structured content
- Add more specific instructions in the lecture title

## Best Practices

1. **Start Small**
   - Generate 10-20 cards first
   - Review quality
   - Adjust settings if needed

2. **Use Good PDFs**
   - Clear, well-formatted lecture slides work best
   - Avoid scanned images (use OCR first)
   - More structured content = better cards

3. **Review Everything**
   - Always review AI-generated cards
   - Claude is smart but not perfect
   - Edit or delete poor quality cards

4. **Iterate**
   - Generate multiple batches
   - Mix AI and manual cards
   - Build a high-quality deck over time

5. **Tag Appropriately**
   - AI adds tags automatically
   - Review and add more specific tags
   - Helps with ANKI organization

## Security Notes

⚠️ **Never commit API keys to GitHub**
- Use secrets or environment variables
- Add `.env` to `.gitignore`
- Rotate keys if exposed

⚠️ **Monitor Usage**
- Check Anthropic console regularly
- Set up billing alerts
- API calls cost money

## Support

- **Anthropic Docs:** https://docs.anthropic.com/
- **API Reference:** https://docs.anthropic.com/en/api/
- **Pricing:** https://www.anthropic.com/pricing
- **Support:** support@anthropic.com

---

**Happy card generating!** 🎓✨
