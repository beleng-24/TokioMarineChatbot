# 🎯 Quick Testing Reference Card

## ⚡ Fast Commands

### Run All Tests (Recommended First Step)
```bash
# Navigate to project
cd "/Users/belen/Desktop/IS 4880 Capstone/TokioMarineChatbot"

# Run comprehensive test suite
python3 test_functionality.py    # Core features (5 tests)
python3 test_integration.py      # Full workflow (generates output files)
python3 test_excel.py            # Data validation (6 Excel files)
python3 demo.py                  # System overview
```

### Launch Interactive Chatbot
```bash
python3 plan-doc-chatbot.py
```

### View Generated Test Files
```bash
# Open in browser
open outputs/test_checklist_aurora_dynamics.html

# Open PDF
open outputs/test_checklist_aurora_dynamics.pdf

# View JSON
cat outputs/test_checklist_aurora_dynamics.json | head -50
```

---

## 📋 Interactive Chatbot Menu

When you run `python3 plan-doc-chatbot.py`, you'll see:

```
1. 📊 Load Orange Output (Excel)
2. 🔨 Generate Checklist for Group
3. 🔍 Validate Current Checklist
4. 📝 Preview Checklist (HTML)
5. 📄 Export to PDF
6. 💾 Export Data (JSON/Excel)
7. 🧠 Teach Chatbot
8. 📚 View Learning History
9. 💬 Chat Mode
0. ❌ Exit
```

---

## 🧪 Test Scenarios

### Scenario 1: Quick Demo (30 seconds)
```bash
python3 demo.py
```
**Expected:** System overview and instructions

### Scenario 2: Validate Data (1 minute)
```bash
python3 test_excel.py
```
**Expected:** ✅ 6 Excel files validated, stats displayed

### Scenario 3: Full Workflow Test (1 minute)
```bash
python3 test_integration.py
```
**Expected:** ✅ JSON, HTML, PDF files generated in `outputs/`

### Scenario 4: Interactive Checklist Generation (2-3 minutes)
```bash
python3 plan-doc-chatbot.py
# Choose: 2 (Generate Checklist)
# Select: Aurora Dynamics
# Choose: 4 (Preview HTML)
# Choose: 5 (Export PDF)
# Choose: 0 (Exit)
```
**Expected:** Checklist generated, HTML/PDF created

### Scenario 5: Test Learning System (2 minutes)
```bash
python3 plan-doc-chatbot.py
# Choose: 7 (Teach Chatbot)
# Choose: 1 (Add Synonym)
# Term: TPA
# Synonym: Claims Administrator
# Choose: 8 (View Learning History)
# Choose: 0 (Exit)
```
**Expected:** Synonym saved, history displayed

---

## ✅ What to Verify

### After Running Tests
- [ ] All test suites report 100% pass rate
- [ ] No error messages in terminal
- [ ] Files created in `outputs/` directory
- [ ] HTML opens in browser successfully
- [ ] PDF opens correctly
- [ ] JSON data is properly formatted

### In Generated Files
**HTML Preview:**
- [ ] Title shows "Aurora Dynamics"
- [ ] Summary shows: 21 found, 4 missing
- [ ] Fields are color-coded (green=found, red=missing)
- [ ] Confidence percentages displayed

**PDF Report:**
- [ ] Professional formatting
- [ ] Group name and date visible
- [ ] Summary statistics correct
- [ ] Sample fields listed

**JSON Export:**
- [ ] Valid JSON structure
- [ ] 25 fields present
- [ ] Confidence values between 0-1
- [ ] Status: "found" or "missing"

---

## 📊 Expected Test Results

### Mock Data Statistics
| Group | Total Fields | Found | Missing | Avg Confidence |
|-------|--------------|-------|---------|----------------|
| Aurora Dynamics | 25 | 21 | 4 | 72.12% |
| Helios Manufacturing | 25 | 15 | 10 | 50.76% |
| Solstice Technologies | 25 | 21 | 4 | 72.16% |
| TechVenture | 25 | 25 | 0 | 82.28% |
| GlobalCorp | 25 | 25 | 0 | 95.00% |

### Test Suite Results
```
✅ PASS - Module Imports
✅ PASS - Mock Data Structure
✅ PASS - Learning Engine
✅ PASS - File Operations
✅ PASS - PDF Generation
Results: 5/5 tests passed (100.0%)
```

---

## 🔍 Troubleshooting

### If Tests Fail

**Missing Dependencies:**
```bash
pip3 install -r requirements.txt
```

**Permission Errors:**
```bash
chmod +x *.py
```

**Mock Data Missing:**
```bash
# Check if mock_data folder exists
ls -la mock_data/
# Should show 6 .xlsx files
```

**Output Directory Issues:**
```bash
mkdir -p outputs
```

---

## 🎯 Quick Test Checklist

Run this in order:

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Run all test suites
python3 test_functionality.py
python3 test_integration.py
python3 test_excel.py

# 3. View outputs
open outputs/test_checklist_aurora_dynamics.html
open outputs/test_checklist_aurora_dynamics.pdf

# 4. Try interactive mode
python3 plan-doc-chatbot.py
# Select option 2, choose "Aurora Dynamics"
```

**Success Criteria:** All ✅ green checkmarks, no ❌ red errors

---

## 📁 File Locations

```
TokioMarineChatbot/
├── demo.py                          # Quick demo script
├── test_functionality.py            # Core feature tests
├── test_integration.py              # Full workflow test
├── test_excel.py                    # Data validation test
├── plan-doc-chatbot.py             # Main application
├── requirements.txt                 # Dependencies
├── TEST_RESULTS.md                  # Full test report
├── mock_data/                       # Test data (6 files)
└── outputs/                         # Generated files
    ├── test_checklist_*.json       # JSON exports
    ├── test_checklist_*.html       # HTML previews
    └── test_checklist_*.pdf        # PDF reports
```

---

## 💡 Pro Tips

1. **Always run tests after any code changes**
2. **Check `outputs/` folder for generated files**
3. **Use Aurora Dynamics for consistent testing** (best coverage)
4. **Try Helios Manufacturing to test missing fields**
5. **Use GlobalCorp to test perfect extraction** (95% confidence)
6. **Open HTML files to verify visual formatting**
7. **Check JSON structure for integration testing**

---

## 🚀 Ready to Go!

**All systems tested and operational. Choose your path:**

- 🎬 **Demo Mode:** `python3 demo.py`
- 🧪 **Test Mode:** `python3 test_integration.py`
- 💬 **Interactive Mode:** `python3 plan-doc-chatbot.py`

**Have fun testing!** 🎉

---

*Quick Reference Card - Generated November 15, 2025*
