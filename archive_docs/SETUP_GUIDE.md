# 🚀 Setup Guide - AI Plan Document Review System

## Step-by-Step Installation

### Step 1: Verify Python Installation

Open Terminal and check Python version:
```bash
python3 --version
```

You should see Python 3.8 or higher. If not, download from [python.org](https://www.python.org/downloads/)

### Step 2: Install Required Packages

Navigate to your project folder:
```bash
cd "/Users/belen/Desktop/IS 4545/Project/TokioMarineChatbot"
```

Install dependencies:
```bash
pip3 install pandas openpyxl reportlab
```

Or use the requirements file:
```bash
pip3 install -r requirements.txt
```

### Step 3: Run the System

Start the chatbot:
```bash
python3 plan-doc-chatbot.py
```

You should see the welcome banner! 🎉

## First Time Usage

### Test Run with Mock Data

1. **Start the program**:
```bash
python3 plan-doc-chatbot.py
```

2. **Generate a checklist** (choose option 2):
```
Choose an option (0-9): 2

Available groups (mock data):
  • Aurora Dynamics
  • Helios Manufacturing Inc.
  • Solstice Technologies

Enter group name: Aurora Dynamics
```

3. **View HTML preview** (choose option 4):
```
Choose an option (0-9): 4
```
This creates an HTML file you can open in your browser to review and edit.

4. **Export to PDF** (choose option 5):
```
Choose an option (0-9): 5
```
This creates a professional PDF checklist.

## Using Your Own Data

### Option A: Excel File from Orange Workflow

When you have your Orange workflow output:

1. Ensure Excel has these columns:
   - `Field`
   - `Extracted_Value`
   - `Confidence`
   - `Page_Number`

2. Load it using option 1:
```
Choose an option (0-9): 1
Enter Excel path: /path/to/your/orange_output.xlsx
```

### Option B: Update Mock Data

Edit `plan-doc-chatbot.py` and update the `create_mock_orange_output()` method with your own data.

## Teaching the System

The system learns from your corrections!

### Adding a Synonym

```
Choose an option (0-9): 7
Choose option: 1
Enter term: Third Party Administrator
Enter synonym: Claims Payor
Your name (optional): John
```

### Adding a Correction

```
Choose an option (0-9): 7
Choose option: 2
Enter incorrect term: Thrd Party Admin
Enter correct term: Third Party Administrator
Your name (optional): John
```

The system saves these in `learned_mappings.json` and uses them in future validations!

## Workflow Example

Here's a complete workflow:

```bash
# 1. Start the system
python3 plan-doc-chatbot.py

# 2. Generate checklist for Aurora Dynamics (option 2)
# 3. View validation results
# 4. Preview in HTML (option 4)
# 5. Open the HTML file in browser and make any edits
# 6. Export to PDF (option 5)
# 7. Export data (option 6) if needed for records
# 8. Teach any corrections (option 7)
```

## Common Issues & Solutions

### Issue: "Module not found: pandas"
**Solution**:
```bash
pip3 install pandas
```

### Issue: "Module not found: reportlab"
**Solution**:
```bash
pip3 install reportlab
```

### Issue: PDF generation fails
**Solution**:
```bash
pip3 install --upgrade reportlab
```

### Issue: Excel file won't load
**Solution**:
```bash
pip3 install openpyxl
```

### Issue: Permission denied
**Solution**: Run with appropriate permissions or move to a folder you have write access to.

## Verification Checklist

✅ Python 3.8+ installed  
✅ All packages installed (pandas, openpyxl, reportlab)  
✅ Can run `python3 plan-doc-chatbot.py`  
✅ Can generate checklist for test data  
✅ HTML preview opens in browser  
✅ PDF exports successfully  
✅ Learning system saves corrections  

## File Outputs

After running the system, you'll see these files created:

```
TokioMarineChatbot/
├── learned_mappings.json                     # System's learned knowledge
├── checklist_preview_Aurora_Dynamics.html    # HTML preview
├── checklist_Aurora_Dynamics.pdf             # PDF export
└── checklist_data_Aurora_Dynamics.json       # Data export
```

## Next Steps

1. ✅ Run the test with mock data
2. ✅ Review generated HTML and PDF
3. ✅ Test the learning system
4. 🔄 Connect to your Orange workflow output
5. 🎯 Use for real plan document review

## Getting Help

- **Chat Mode**: Use option 9 to ask the chatbot questions
- **Learning History**: Use option 8 to see what the system learned
- **README.md**: Comprehensive documentation

## Tips for Best Results

1. **Always validate** before exporting to PDF (option 3)
2. **Preview in HTML** to catch any issues before final export
3. **Teach the system** when you find new terms or corrections
4. **Review warnings** in validation reports
5. **Keep backups** of your learned_mappings.json file

---

**Ready to start?** Run:
```bash
python3 plan-doc-chatbot.py
```

Happy reviewing! 🎉
