# 🧪 Testing Guide - AI Plan Document Review System

## Overview
This guide provides comprehensive testing instructions using the mock Excel files that simulate Orange workflow output.

---

## 📂 Mock Data Files Created

Located in: `mock_data/` folder

### Individual Files (5 groups):

1. **orange_output_aurora_dynamics.xlsx**
   - 📊 Status: Complete data
   - ✅ Fields: 20/25 populated
   - 🎯 Use for: Standard testing scenario

2. **orange_output_helios_manufacturing.xlsx**
   - 📊 Status: Partial data
   - ⚠️ Fields: 15/25 populated (many N/F)
   - 🎯 Use for: Missing field detection

3. **orange_output_solstice_technologies.xlsx**
   - 📊 Status: Complete with variations
   - ✅ Fields: 19/25 populated
   - 🎯 Use for: Synonym recognition

4. **orange_output_techventure_typos.xlsx**
   - 📊 Status: Contains intentional typos
   - ⚠️ Confidence: Lower scores (68-98%)
   - 🎯 Use for: Typo detection & fuzzy matching

5. **orange_output_globalcorp.xlsx**
   - 📊 Status: High-quality complete data
   - ✅ Fields: 25/25 populated
   - ⭐ Confidence: High scores (91-99%)
   - 🎯 Use for: Ideal scenario testing

### Combined File:

6. **orange_output_all_groups.xlsx**
   - Contains all 5 groups in one file
   - Includes Group_Name column
   - Good for batch processing

---

## 🚀 Quick Test (5 Minutes)

### Test 1: Basic Functionality

```bash
# Start the system
python3 plan-doc-chatbot.py

# In the menu:
1. Choose option 1 → Enter: mock_data/orange_output_aurora_dynamics.xlsx
2. Choose option 2 → Enter: Aurora Dynamics
3. Choose option 4 → HTML preview generated
4. Choose option 5 → PDF generated
5. Choose option 0 → Exit
```

**Expected Result**: 
- ✅ Excel loaded successfully
- ✅ Checklist generated with validation
- ✅ HTML file created
- ✅ PDF file created

---

## 🎯 Comprehensive Test Scenarios

### Scenario 1: Complete Data (Ideal Case)

**File**: `orange_output_globalcorp.xlsx`  
**Group**: GlobalCorp International

**Steps**:
```bash
python3 plan-doc-chatbot.py
→ Option 1: mock_data/orange_output_globalcorp.xlsx
→ Option 2: GlobalCorp International
→ Option 3: Validate
→ Option 4: HTML Preview
→ Option 5: PDF Export
```

**Expected Results**:
- ✅ Status: "complete"
- ✅ 25/25 fields found
- ✅ 0 missing fields
- ✅ High confidence scores (>90%)
- ✅ Clean validation report
- ✅ Professional PDF output

---

### Scenario 2: Missing Fields Detection

**File**: `orange_output_helios_manufacturing.xlsx`  
**Group**: Helios Manufacturing Inc.

**Steps**:
```bash
python3 plan-doc-chatbot.py
→ Option 1: mock_data/orange_output_helios_manufacturing.xlsx
→ Option 2: Helios Manufacturing Inc.
→ Option 3: Validate
```

**Expected Results**:
- ⚠️ Status: "incomplete"
- ⚠️ 15/25 fields found
- ⚠️ 10 missing fields
- ⚠️ Multiple warnings displayed
- ⚠️ Validation report shows missing fields
- 🎯 System flags all N/F values

**Check For**:
- [ ] "No information found" warnings
- [ ] Missing field count is accurate
- [ ] HTML preview shows red badges for missing
- [ ] PDF shows N/F values clearly

---

### Scenario 3: Typo Detection & Fuzzy Matching

**File**: `orange_output_techventure_typos.xlsx`  
**Group**: TechVenture Inc.

**Steps**:
```bash
python3 plan-doc-chatbot.py
→ Option 1: mock_data/orange_output_techventure_typos.xlsx
→ Option 2: TechVenture Inc.
→ Option 3: Validate
```

**Known Typos to Detect**:
- "Adminstrator" → Should suggest "Administrator"
- "Reviw" → Should suggest "Review"
- "elligible" → Should suggest "eligible"
- "dependant" → Should suggest "dependent"
- "necesary" → Should suggest "necessary"
- "Expirimental" → Should suggest "Experimental"
- "Customery" → Should suggest "Customary"
- "netowrk" → Should suggest "network"
- "Cordination" → Should suggest "Coordination"
- "reimbursment" → Should suggest "reimbursement"

**Expected Results**:
- 🔍 Status: "needs_review"
- 🔍 Multiple "possible_typo" flags
- 🔍 Suggestions for corrections
- 🔍 Lower confidence scores (68-82%)
- 🔍 Yellow badges in HTML preview
- 💡 System suggests correct terms

**Check For**:
- [ ] Fuzzy matching catches similar terms
- [ ] Suggestions are helpful
- [ ] Confidence scores reflect uncertainty
- [ ] Validation report lists all issues

---

### Scenario 4: Learning System

**Test the continuous learning feature**

**Steps**:
```bash
python3 plan-doc-chatbot.py

# Teach a new synonym
→ Option 7
→ Choice 1 (Add Synonym)
→ Term: TPA
→ Synonym: Claims Payor
→ Your name: Tester

# Teach a correction
→ Option 7
→ Choice 2 (Add Correction)
→ Incorrect: 3rd Party Admin
→ Correct: Third Party Administrator
→ Your name: Tester

# View learning history
→ Option 8
```

**Expected Results**:
- ✅ Synonym saved to learned_mappings.json
- ✅ Correction saved to learned_mappings.json
- ✅ Learning history shows entries
- ✅ Timestamp and user recorded
- ✅ Future validations use learned terms

**Verify**:
```bash
# Check the learned_mappings.json file
cat learned_mappings.json
```

Should contain:
```json
{
  "synonyms": {
    "TPA": ["Claims Payor"]
  },
  "corrections": {
    "3rd Party Admin": "Third Party Administrator"
  },
  "learning_history": [...]
}
```

---

### Scenario 5: Export Formats

**Test all export options**

**Steps**:
```bash
python3 plan-doc-chatbot.py
→ Option 1: mock_data/orange_output_aurora_dynamics.xlsx
→ Option 2: Aurora Dynamics
→ Option 4: HTML Preview (opens in browser)
→ Option 5: PDF Export
→ Option 6: Data Export (JSON & Excel)
```

**Verify Files Created**:
```bash
ls -la checklist*
```

**Expected Files**:
- ✅ checklist_preview_Aurora_Dynamics.html
- ✅ checklist_Aurora_Dynamics.pdf
- ✅ checklist_data_Aurora_Dynamics.json
- ✅ checklist_data_Aurora_Dynamics.xlsx

**Check Each File**:

1. **HTML Preview**:
   - [ ] Opens in browser
   - [ ] Color-coded fields (green/red/yellow)
   - [ ] Editable text fields
   - [ ] Shows validation statistics
   - [ ] Export buttons work

2. **PDF Checklist**:
   - [ ] Professional formatting
   - [ ] All fields included
   - [ ] Status indicators visible
   - [ ] Page references shown
   - [ ] Validation summary included

3. **JSON Export**:
   - [ ] Valid JSON format
   - [ ] All data included
   - [ ] Metadata present
   - [ ] Can be re-imported

4. **Excel Export**:
   - [ ] Opens in Excel
   - [ ] All columns present
   - [ ] Data properly formatted

---

### Scenario 6: Chat Mode

**Test the interactive chat feature**

**Steps**:
```bash
python3 plan-doc-chatbot.py
→ Option 2: Aurora Dynamics
→ Option 9 (Chat Mode)

# Try these questions:
You: status
You: missing
You: export
You: help
You: exit
```

**Expected Responses**:
- "status" → Shows current checklist info
- "missing" → Reports missing field count
- "export" → Explains export options
- "help" → Provides guidance
- "exit" → Returns to menu

---

## 🔬 Advanced Testing

### Test 1: Batch Processing (All Groups)

**File**: `orange_output_all_groups.xlsx`

```bash
python3 plan-doc-chatbot.py
→ Option 1: mock_data/orange_output_all_groups.xlsx
→ Option 2: Aurora Dynamics
→ Option 5: Export PDF
→ Option 2: Helios Manufacturing Inc.
→ Option 5: Export PDF
→ Option 2: Solstice Technologies
→ Option 5: Export PDF
# etc.
```

**Verify**: Multiple PDF files created for different groups

---

### Test 2: Validation Accuracy

**Compare validation results across quality levels**

| Group | Expected Status | Expected Found | Expected Missing |
|-------|----------------|----------------|------------------|
| GlobalCorp | complete | 25 | 0 |
| Aurora | complete/needs_review | 20 | 5 |
| Solstice | needs_review | 19 | 6 |
| Helios | incomplete | 15 | 10 |
| TechVenture | needs_review | 25 | 0 (but low quality) |

---

### Test 3: Edge Cases

1. **Empty Group Name**:
   - Try generating without specifying group
   - Should use generic template

2. **Non-existent File**:
   - Try loading a file that doesn't exist
   - Should show error message gracefully

3. **Malformed Excel**:
   - Create an Excel with wrong columns
   - Should handle error properly

---

## 📊 Test Results Template

Use this template to record your test results:

```markdown
## Test Results - [Date]

### Environment
- Python Version: _____
- OS: _____
- Dependencies: ✅ Installed

### Scenario 1: Basic Functionality
- [ ] Excel loaded successfully
- [ ] Checklist generated
- [ ] HTML preview created
- [ ] PDF exported
- [ ] No errors
- Notes: ___________

### Scenario 2: Missing Fields
- [ ] Detected 10 missing fields
- [ ] Warnings displayed
- [ ] Status = "incomplete"
- Notes: ___________

### Scenario 3: Typo Detection
- [ ] Detected typos
- [ ] Suggested corrections
- [ ] Low confidence flagged
- Notes: ___________

### Scenario 4: Learning System
- [ ] Synonym saved
- [ ] Correction saved
- [ ] History viewable
- Notes: ___________

### Scenario 5: Exports
- [ ] HTML generated
- [ ] PDF generated
- [ ] JSON exported
- [ ] Excel exported
- Notes: ___________

### Scenario 6: Chat Mode
- [ ] Responded to queries
- [ ] Helpful responses
- [ ] Exit worked
- Notes: ___________

### Overall Assessment
- Pass/Fail: _____
- Issues Found: _____
- Recommendations: _____
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Excel Won't Load
**Solution**: 
```bash
pip3 install --upgrade openpyxl pandas
```

### Issue 2: PDF Generation Fails
**Solution**:
```bash
pip3 install --upgrade reportlab
```

### Issue 3: File Not Found
**Solution**: Use full path
```bash
mock_data/orange_output_aurora_dynamics.xlsx
# or
/Users/belen/Desktop/IS 4545/Project/TokioMarineChatbot/mock_data/orange_output_aurora_dynamics.xlsx
```

### Issue 4: Permission Denied
**Solution**: Check folder permissions
```bash
chmod +x create_mock_data.py
```

---

## ✅ Testing Checklist

Before considering testing complete, verify:

### Core Functionality
- [ ] Can load all 5 mock Excel files
- [ ] Can generate checklists for all groups
- [ ] Validation runs without errors
- [ ] HTML previews open in browser
- [ ] PDFs export successfully
- [ ] JSON/Excel exports work

### Validation
- [ ] Detects missing fields correctly
- [ ] Flags typos with suggestions
- [ ] Confidence scores make sense
- [ ] Status levels appropriate
- [ ] Warnings are helpful

### Learning System
- [ ] Can add synonyms
- [ ] Can add corrections
- [ ] History is recorded
- [ ] learned_mappings.json updates
- [ ] Learned terms used in validation

### User Interface
- [ ] Menu is clear and responsive
- [ ] Chat mode works
- [ ] Error messages are helpful
- [ ] Progress indicators shown
- [ ] Can exit cleanly

### Output Quality
- [ ] HTML is well-formatted
- [ ] PDF is professional
- [ ] Data exports are complete
- [ ] Files named correctly
- [ ] All data preserved

---

## 📈 Performance Testing

### Speed Test
```bash
time python3 -c "
from datetime import datetime
start = datetime.now()
# Run full workflow
exec(open('plan-doc-chatbot.py').read())
# Record time
"
```

**Expected Times**:
- Load Excel: < 2 seconds
- Generate Checklist: < 1 second
- Validate: < 1 second
- HTML Export: < 1 second
- PDF Export: < 3 seconds

---

## 🎯 Acceptance Criteria

### Must Pass:
✅ All 5 mock files load successfully  
✅ Validation detects missing fields  
✅ Typo detection works  
✅ All export formats generate  
✅ Learning system persists data  
✅ No crashes or errors  

### Should Pass:
✅ Confidence scores accurate  
✅ Suggestions are helpful  
✅ HTML is user-friendly  
✅ PDF is professional  
✅ Performance is acceptable  

---

## 📞 Need Help?

1. Check mock_data/README.md
2. Review QUICK_REFERENCE.md
3. Use Chat Mode (option 9)
4. Check validation warnings

---

## 🎉 Ready to Test!

Start with the Quick Test (5 minutes), then proceed to comprehensive scenarios based on your needs.

**Quick Start**:
```bash
python3 plan-doc-chatbot.py
# Load: mock_data/orange_output_aurora_dynamics.xlsx
# Generate: Aurora Dynamics
# Export: PDF
```

**Happy Testing! 🧪✨**
