# AI-Enhanced Plan Document Review System
## Setup Guide for ChatGPT API Integration

### Overview
This enhanced version uses OpenAI's ChatGPT API to automate plan document review, reduce manual effort, minimize human error, and improve the user experience for TMHCC.

---

## 🚀 Quick Start

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management
- All existing dependencies

### 2. Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

### 3. Configure API Key

**Option A: Via Streamlit UI (Recommended)**
1. Run the app: `streamlit run streamlit_app.py`
2. Go to "⚙️ Settings" page
3. Paste your API key
4. Click "Save Key"
5. Test the connection

**Option B: Via Environment Variable**
1. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
2. The app will automatically load it on startup

---

## 📚 Prepare Your Definitions List

### Required Format

Create an Excel file with your field definitions. The AI will use this to make intelligent decisions.

**Required Columns:**
- `Field` or `Term`: Name of the insurance field
- `Definition` or `Description`: Detailed explanation

**Optional Columns:**
- `Required`: Boolean (TRUE/FALSE) - Is this field mandatory?
- `Category`: Grouping (e.g., "Plan Info", "Benefits", "Vendors")
- `Examples`: Sample values
- `Validation Rules`: Specific criteria

### Example Definitions File

| Field | Definition | Required | Category |
|-------|-----------|----------|----------|
| TPA | Third Party Administrator - handles claims administration and processing | TRUE | Admin |
| Group Name | Official name of the insurance group or employer organization | TRUE | Plan Info |
| UR Vendor | Utilization Review vendor responsible for medical necessity reviews | TRUE | Vendors |
| PPO Network | Preferred Provider Organization network name and details | TRUE | Network |
| Retirees | Coverage provisions for retired employees | FALSE | Eligibility |

### Upload Definitions

1. Go to "📚 Definitions" page in the app
2. Click "Choose an Excel file"
3. Upload your definitions file
4. Review the preview to ensure proper loading

---

## 🤖 How AI Enhancement Works

### Automated Decision Making

The AI analyzes each field against your definitions and:

1. **Validates Extracted Values**
   - Cross-references with definitions
   - Checks if values make sense in context
   - Identifies potential errors

2. **Flags Missing Critical Fields**
   - Determines which fields are required
   - Prioritizes review of missing mandatory information
   - Provides specific suggestions for what to verify

3. **Enhances Low-Confidence Fields**
   - Reviews fields with confidence < 70%
   - Suggests verification steps
   - Provides context-aware explanations

4. **Generates Smart Recommendations**
   - Context-aware suggestions
   - Prioritized action items
   - Clear explanations for decisions

### AI Response Format

For each field, the AI provides:
- **Validation Status**: VALID, NEEDS_REVIEW, or MISSING
- **Required Flag**: Is this field mandatory?
- **Suggestions**: What should be verified?
- **Explanation**: Why this decision was made

---

## 📊 Using the Enhanced Workflow

### Step-by-Step Process

1. **Configure AI** (Settings Page)
   - Enter OpenAI API key
   - Test connection
   - Verify AI features are enabled

2. **Upload Definitions** (Definitions Page)
   - Upload your field definitions Excel file
   - Review loaded definitions
   - Confirm all required fields are present

3. **Load Plan Data** (Load Data Page)
   - Upload Orange workflow output
   - OR use mock data for testing
   - Review data preview

4. **Generate Enhanced Checklist** (Generate Checklist Page)
   - Click "Generate Checklist"
   - Enable "🤖 Use AI Enhancement"
   - Click "🤖 Enhance with AI"
   - Wait for AI analysis (1-2 minutes for 25 fields)

5. **Review AI Insights**
   - Check "AI Insights" tab
   - Review critical issues
   - Read AI recommendations
   - Verify flagged items

6. **Export Results**
   - Download Excel checklist
   - Excel includes all AI analysis
   - Share with stakeholders

---

## 💰 Cost Considerations

### API Usage

- **Model Used**: GPT-4o-mini (cost-effective, fast)
- **Approximate Cost**: $0.15 per 1,000 fields analyzed
- **Example**: Analyzing 25 fields ≈ $0.004 (less than half a cent)

### Cost Optimization Tips

1. Only use AI enhancement for:
   - Low confidence fields (< 70%)
   - Missing values
   - Critical required fields

2. Batch similar documents together

3. Cache definitions in session to avoid reprocessing

---

## 🎯 Expected Benefits

### Time Savings
- **70% reduction** in manual review time
- **Automated validation** of routine fields
- **Instant prioritization** of critical issues

### Accuracy Improvements
- **Consistent decisions** based on definitions
- **Reduced human error** in field validation
- **Context-aware** suggestions

### Better User Experience
- **Clear action items** with explanations
- **Prioritized review** of critical fields
- **Interactive insights** with AI reasoning

---

## 🔧 Troubleshooting

### "API Key not configured"
- Go to Settings page
- Enter valid OpenAI API key
- Test connection

### "AI Enhancement failed"
- Check internet connection
- Verify API key is valid
- Check OpenAI account has credits
- Review error message for details

### "No definitions loaded"
- Go to Definitions page
- Upload Excel file with proper format
- Ensure columns are named correctly

### Slow AI Processing
- Normal for 20-30 fields (1-2 minutes)
- AI analyzes each field individually
- Progress bar shows status

---

## 📞 Support

For technical issues or questions:
1. Check this guide first
2. Review error messages in the app
3. Contact development team
4. Reference OpenAI documentation

---

## 🔐 Security Notes

- API keys are stored in session only (not saved to disk)
- Never commit `.env` file to version control
- Use separate API keys for dev/prod environments
- Monitor API usage on OpenAI dashboard

---

**Ready to revolutionize your plan document review process!** 🚀
