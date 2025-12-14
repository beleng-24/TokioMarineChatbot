# Setup Instructions for Team Members

## Quick Start Guide

### 1. Clone the Repository

```bash
git clone https://github.com/beleng-24/TokioMarineChatbot.git
cd TokioMarineChatbot
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
# On Mac/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI API Key

**Option A: Get Your Own API Key (Recommended for personal use)**

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)
5. Create a `.env` file in the project folder:

```bash
# Copy the template
cp .env.template .env

# Edit .env and add your key
# OPENAI_API_KEY=sk-your-actual-key-here
```

**Option B: Use Shared API Key (For team collaboration)**

Ask your project partner for the API key, then:

```bash
# Create .env file
echo "OPENAI_API_KEY=the-key-your-partner-gives-you" > .env
```

### 5. Run the Application

```bash
streamlit run streamlit_app.py
```

The app will open at http://localhost:8501

## Testing the App

Try these sample files to test:
- `sample_keywords.txt` - Simple text format
- `sample_keywords_with_header.csv` - CSV format

## Troubleshooting

### "ModuleNotFoundError"
Make sure your virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### "API key not found"
Check that:
1. `.env` file exists in the project root
2. It contains `OPENAI_API_KEY=your-key-here`
3. No extra spaces or quotes around the key

### "Port already in use"
Kill any existing Streamlit processes:
```bash
# Mac/Linux
pkill -f streamlit

# Windows
taskkill /F /IM streamlit.exe
```

## Security Reminders

- ⚠️ **NEVER commit your `.env` file** - it's already in `.gitignore`
- ⚠️ **Don't share API keys publicly** - only share with trusted team members
- ✅ The `.env` file stays on your local machine only

## Project Structure

```
TokioMarineChatbot/
├── streamlit_app.py          # Main application
├── requirements.txt           # Dependencies
├── .env.template             # Template for environment variables
├── .env                      # YOUR API key (create this, never commit)
├── sample_keywords.txt       # Test file
└── Checklist Examples/       # Reference templates
```

## Need Help?

Contact your project partner or check the main README.md for more details.
