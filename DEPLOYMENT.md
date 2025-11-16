# Deployment Guide for Streamlit Cloud

## Quick Start (5 Minutes)

Follow these steps to deploy your ANKI Generator app to Streamlit Cloud:

### 1. Create GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Name it something like `anki-flashcard-generator`
3. Make it public (required for free Streamlit Cloud hosting)
4. Initialize with README (optional)

### 2. Upload Files to GitHub

Upload these files to your repository:

```
anki-flashcard-generator/
├── streamlit_app.py          # Main application
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation (optional)
├── .gitignore               # Git ignore file (optional)
└── .streamlit/
    └── config.toml          # Streamlit config (optional)
```

**Methods to upload:**

#### Option A: GitHub Web Interface
1. Click "Add file" → "Upload files"
2. Drag and drop all files
3. Commit changes

#### Option B: Git Command Line
```bash
git clone https://github.com/YOUR-USERNAME/anki-flashcard-generator.git
cd anki-flashcard-generator
# Copy all files here
git add .
git commit -m "Initial commit"
git push
```

### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit Cloud
4. Click "New app"
5. Fill in the form:
   - **Repository:** Select your `anki-flashcard-generator` repo
   - **Branch:** `main` or `master`
   - **Main file path:** `streamlit_app.py`
   - **App URL:** Choose a custom name (e.g., `my-anki-generator`)
6. Click "Deploy!"

### 4. Wait for Deployment

- Initial deployment takes 2-5 minutes
- You'll see build logs in real-time
- When complete, your app will be live at:
  ```
  https://YOUR-APP-NAME.streamlit.app
  ```

### 5. Test Your App

1. Visit your app URL
2. Upload a sample PDF
3. Generate some flashcards
4. Export and verify the download works

## Troubleshooting

### Build Fails

**Error: "No module named 'fitz'"**
- Solution: Check that `requirements.txt` includes `PyMuPDF>=1.23.0`

**Error: "Could not find a version that satisfies the requirement"**
- Solution: Update the version numbers in `requirements.txt`

### App Crashes

**"FileNotFoundError" when uploading PDF**
- This shouldn't happen as uploads are handled in-memory
- Check that you're not trying to save files to disk

**"Session state error"**
- Clear browser cache and refresh
- Try in incognito mode

### Performance Issues

**Slow PDF processing**
- PDFs are processed in the browser
- Very large PDFs (>50MB) may be slow
- Consider splitting large PDFs

**App "sleeping"**
- Free Streamlit Cloud apps sleep after inactivity
- First request may take 10-30 seconds to wake up
- Upgrade to paid plan for always-on apps

## Configuration Options

### Custom Domain

Streamlit Cloud free tier doesn't support custom domains, but you can:
- Use the provided `.streamlit.app` subdomain
- Upgrade to paid plan for custom domains

### Environment Variables

If you add API integrations (e.g., Claude API for auto-generation):

1. In Streamlit Cloud dashboard, go to your app
2. Click "Settings" → "Secrets"
3. Add secrets in TOML format:
   ```toml
   CLAUDE_API_KEY = "your-api-key-here"
   ```
4. Access in app: `st.secrets["CLAUDE_API_KEY"]`

### Resource Limits (Free Tier)

- **Memory:** 1 GB
- **CPU:** Shared
- **File upload:** 200 MB max
- **Sleep after:** 7 days of inactivity

## Advanced: GitHub Actions Auto-Deploy

For automatic deployment on git push:

1. In your GitHub repo, create `.github/workflows/streamlit.yml`:

```yaml
name: Streamlit App CI/CD

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

2. Streamlit Cloud will auto-deploy when you push to main branch

## Updating Your App

To update your deployed app:

1. Make changes to your code locally
2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
3. Streamlit Cloud will automatically detect changes and redeploy
4. Redeployment takes 1-2 minutes

## Monitoring

### View Logs

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click on your app
3. Click "Manage app"
4. View "Logs" tab for runtime errors

### Analytics

Streamlit Cloud provides basic analytics:
- Number of viewers
- Active sessions
- Error rates

Access via the "Analytics" tab in app settings.

## Best Practices

1. **Test locally first**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Use version control**
   - Commit working code
   - Use branches for experiments
   - Tag releases

3. **Keep dependencies minimal**
   - Only include necessary packages
   - Specify version ranges for stability

4. **Handle errors gracefully**
   - Use try-except blocks
   - Show user-friendly error messages
   - Log errors for debugging

5. **Optimize for performance**
   - Cache expensive operations with `@st.cache_data`
   - Minimize session state usage
   - Process large files efficiently

## Cost Considerations

### Free Tier (Current Setup)

- ✅ Unlimited public apps
- ✅ Community support
- ✅ GitHub integration
- ❌ Apps sleep after inactivity
- ❌ No custom domains
- ❌ Limited resources

### Paid Tiers (If Needed)

Consider upgrading if you need:
- Always-on apps
- More resources (CPU/memory)
- Private apps
- Custom domains
- Priority support

Pricing: [streamlit.io/pricing](https://streamlit.io/pricing)

## Support Resources

- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues:** For this specific app
- **Streamlit Cloud Docs:** [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)

## Checklist

Before deploying, ensure:

- [ ] All files are in GitHub repository
- [ ] `requirements.txt` is up to date
- [ ] App runs locally without errors
- [ ] No hardcoded secrets or API keys
- [ ] README.md has usage instructions
- [ ] Repository is public (for free hosting)
- [ ] GitHub account is connected to Streamlit Cloud
- [ ] App name is available on Streamlit Cloud

## Next Steps After Deployment

1. Share your app URL with users
2. Gather feedback
3. Add features based on user needs
4. Monitor logs for errors
5. Update regularly with improvements

---

**Need help?** Check the Streamlit Community Forum or create an issue in your GitHub repository.
