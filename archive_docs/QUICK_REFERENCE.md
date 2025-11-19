# 🚀 Quick Reference Card

## Getting Started in 3 Steps

### 1️⃣ Start the System
```bash
cd "/Users/belen/Desktop/IS 4545/Project/TokioMarineChatbot"
python3 plan-doc-chatbot.py
```

### 2️⃣ Generate a Checklist
- Choose option **2**
- Enter group name: **Aurora Dynamics**
- System auto-generates and validates

### 3️⃣ Export Your Work
- Option **4** → HTML preview (editable)
- Option **5** → PDF checklist
- Option **6** → Data export (JSON/Excel)

---

## 🎯 Menu Quick Guide

| Option | What It Does | When to Use |
|--------|--------------|-------------|
| **1** | Load Orange Excel | When you have real workflow output |
| **2** | Generate Checklist | Start your review process |
| **3** | Validate Checklist | Check current checklist quality |
| **4** | Preview HTML | Review/edit before final export |
| **5** | Export PDF | Create final checklist document |
| **6** | Export Data | Save structured data (JSON/Excel) |
| **7** | Teach Chatbot | Add new terms or corrections |
| **8** | View Learning | See what system has learned |
| **9** | Chat Mode | Ask questions, get help |
| **0** | Exit | Close the system |

---

## 💡 Common Tasks

### Create a Checklist
```
Menu → 2 → Enter group name → Done!
```

### Review Before Export
```
Menu → 4 → Open HTML in browser → Edit if needed
```

### Generate Final PDF
```
Menu → 5 → PDF created automatically
```

### Teach New Term
```
Menu → 7 → 1 → Enter term + synonym → Saved!
```

### Correct a Mistake
```
Menu → 7 → 2 → Enter incorrect + correct → Learned!
```

---

## 🎨 Status Colors (HTML Preview)

| Color | Status | Meaning |
|-------|--------|---------|
| 🟢 Green | **Found** | ✅ Successfully extracted |
| 🔴 Red | **Missing** | ⚠️ Not found in document |
| 🟡 Yellow | **Needs Review** | 🔍 Possible typo or issue |

---

## 📊 Sample Groups (Mock Data)

### Aurora Dynamics
- ✅ Complete data set
- Best for first-time testing
- 20/25 fields populated

### Helios Manufacturing Inc.
- ⚠️ Partial data
- Tests missing field handling
- 15/25 fields populated

### Solstice Technologies
- ✅ Complete with variations
- Tests terminology differences
- 19/25 fields populated

---

## 🔍 Key Fields Tracked

### Group Info (6)
- Group Name, Eff Date, TPA, UR Vendor, PPO Network, Min Hours

### Eligibility (7)
- Retirees, BOD/Officers, Dependents, Age 26, Grandchildren, Termination, Open Enrollment

### Coverage (6)
- Leave of Absence, Medically Necessary, E&I, R&C, Workers Comp, Transplant

### Administrative (6)
- ETS Gene Therapy, COB, COBRA, Subrogation, Infertility

**Total: 25 fields**

---

## 📁 Files Created

### After Running System:
```
✓ checklist_preview_[GroupName].html    # Editable form
✓ checklist_[GroupName].pdf             # Final document
✓ checklist_data_[GroupName].json       # Structured data
✓ checklist_data_[GroupName].xlsx       # Excel format
✓ learned_mappings.json                 # System knowledge
```

---

## ⚡ Keyboard Shortcuts

### In Menu:
- **0-9** → Select option
- **Ctrl+C** → Exit anytime

### In Chat Mode (Option 9):
- **exit** or **quit** → Return to menu
- **help** → Get assistance
- **status** → Current checklist info

---

## 🐛 Troubleshooting

### "Module not found"
```bash
pip3 install pandas openpyxl reportlab
```

### PDF won't generate
```bash
pip3 install --upgrade reportlab
```

### Excel won't load
```bash
pip3 install --upgrade openpyxl pandas
```

### Can't find file
- Check you're in correct directory
- Use full file paths

---

## 💬 Chat Mode Commands

Ask the chatbot:
- `"status"` → Current checklist summary
- `"missing"` → See missing fields
- `"export"` → Export options
- `"learn"` → How to teach system
- `"help"` → General assistance

---

## 🎓 Learning System

### Add Synonym
```
Term: TPA
Synonym: Claims Administrator
→ System remembers for future use
```

### Add Correction
```
Incorrect: 3rd Party Admin
Correct: Third Party Administrator
→ System learns the right term
```

**Result**: Better validation next time! 🎯

---

## 📈 Validation Report

### What It Shows:
- ✅ Fields found (high confidence)
- ⚠️ Fields missing (no data)
- 🔍 Fields needing review (typos/issues)
- 📊 Overall status
- 💡 Suggestions for improvement

### Reading Confidence Scores:
- **90-100%** → Excellent ✅
- **70-89%** → Good but verify
- **Below 70%** → Needs review ⚠️

---

## 🔧 System Requirements

### Minimum:
- Python 3.8+
- 100 MB free space
- macOS, Windows, or Linux

### Dependencies:
- pandas
- openpyxl
- reportlab

---

## 📚 Documentation Files

1. **README.md** → Complete guide
2. **SETUP_GUIDE.md** → Installation
3. **ARCHITECTURE.md** → Technical details
4. **PROJECT_SUMMARY.md** → Overview
5. **QUICK_REFERENCE.md** → This file!

---

## ⏱️ Typical Workflow

```
1. Start system                     (30 seconds)
2. Generate checklist              (1 minute)
3. Review validation results       (2 minutes)
4. Preview & edit HTML             (3-5 minutes)
5. Export to PDF                   (30 seconds)
6. Save data for records           (30 seconds)

Total: ~10 minutes per checklist
(vs 2-3 hours manually!)
```

---

## ✨ Pro Tips

1. **Always validate** before final export
2. **Preview in HTML** to catch issues early
3. **Teach the system** when you find new terms
4. **Keep backups** of learned_mappings.json
5. **Use chat mode** when stuck
6. **Check warnings** in validation reports
7. **Review confidence scores** for accuracy

---

## 🎯 Success Indicators

### Good Validation Results:
- ✅ 80%+ fields found
- ✅ High confidence scores (>70%)
- ✅ Few warnings
- ✅ Status: "complete" or "needs_review"

### Needs Attention:
- ⚠️ <70% fields found
- ⚠️ Many low confidence scores
- ⚠️ Multiple unidentifiable terms
- ⚠️ Status: "incomplete"

---

## 📞 Getting Help

### Built-In Help:
1. **Chat Mode** (option 9) - Ask questions
2. **Learning History** (option 8) - See past corrections
3. **Validation Warnings** - Check suggestions

### Documentation:
1. README.md - Full system guide
2. SETUP_GUIDE.md - Installation help
3. ARCHITECTURE.md - How it works

---

## 🚀 Ready to Go!

```bash
python3 plan-doc-chatbot.py
```

**Start with**: Aurora Dynamics (option 2)  
**Then try**: HTML preview (option 4)  
**Finally**: Export PDF (option 5)  

---

**Version**: 1.0  
**Last Updated**: November 2025  
**Status**: ✅ Ready for Use

*Keep this card handy for quick reference!*
