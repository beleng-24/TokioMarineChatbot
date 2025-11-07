# 🤖 AI-Enabled Plan Document Review System

## Overview
An automated system that helps third-party administrators review insurance plan documents by:
- 📊 Parsing Orange workflow outputs
- ✅ Auto-generating checklists
- 🔍 Validating extracted information
- 📝 Providing editable HTML previews
- 📄 Exporting professional PDF reports
- 🧠 Continuously learning from user corrections

## Features

### ✨ Core Capabilities
- **Automated Checklist Generation**: Converts Orange workflow Excel output into structured checklists
- **Smart Validation**: Cross-references with definitions, flags missing information, detects typos
- **Continuous Learning**: Learns new synonyms and corrections from user feedback
- **Editable Preview**: HTML form interface for reviewing and editing before PDF export
- **Multiple Export Formats**: PDF, JSON, and Excel exports
- **Interactive Chatbot**: Conversational interface for easy system interaction

### 🎯 Key Components

1. **LearningEngine**: Manages continuous learning and term mappings
2. **DefinitionsParser**: Handles insurance terminology and field definitions
3. **Validator**: Validates extracted data and flags issues
4. **OrangeOutputParser**: Processes Orange workflow Excel files
5. **ChecklistGenerator**: Creates structured checklists
6. **PDFGenerator**: Exports professional PDF documents
7. **ChatbotInterface**: User-friendly interactive interface

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download** the project files

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas openpyxl reportlab
```

3. **Run the system**:
```bash
python plan-doc-chatbot.py
```

## Usage

### Quick Start

1. **Launch the chatbot**:
```bash
python plan-doc-chatbot.py
```

2. **Generate a checklist** (Option 2):
   - Choose from available groups:
     - Aurora Dynamics
     - Helios Manufacturing Inc.
     - Solstice Technologies
   - System auto-generates and validates the checklist

3. **Preview in HTML** (Option 4):
   - Editable form opens in your browser
   - Make corrections as needed
   - Changes tracked for learning

4. **Export to PDF** (Option 5):
   - Professional checklist document
   - Ready for review and distribution

### Menu Options

```
1. 📊 Load Orange Output (Excel) - Load your Orange workflow Excel file
2. 🔨 Generate Checklist for Group - Auto-generate checklist from data
3. 🔍 Validate Current Checklist - Run validation checks
4. 📝 Preview Checklist (HTML) - View/edit in browser before export
5. 📄 Export to PDF - Generate professional PDF document
6. 💾 Export Data (JSON/Excel) - Export structured data
7. 🧠 Teach Chatbot - Add synonyms or corrections
8. 📚 View Learning History - See what the system has learned
9. 💬 Chat Mode - Ask questions about the system
0. ❌ Exit
```

## System Architecture

### Data Flow
```
Orange Workflow → Excel Output → Parser → Validator → Checklist Generator
                                             ↓
                                    Learning Engine
                                             ↓
                              HTML Preview ← → PDF Export
```

### Learning System
The system maintains a `learned_mappings.json` file that stores:
- **Synonyms**: Alternative terms for insurance keywords
- **Corrections**: User-corrected terms
- **Custom Rules**: User-defined validation rules
- **Learning History**: Audit trail of all learning events

## Mock Data

The system includes mock data for three insurance groups:
- **Aurora Dynamics**: Complete sample data
- **Helios Manufacturing Inc.**: Partial data with missing fields
- **Solstice Technologies**: Complete sample with variations

This allows testing before connecting to real Orange workflow output.

## Checklist Fields

The system tracks and validates these key fields:

### Group Information
- Group Name
- Group Effective Date
- TPA (Third Party Administrator)
- UR Vendor (Utilization Review)
- PPO Network
- Minimum Hour Requirement

### Plan Details
- Retirees Coverage
- Board of Directors/Officers
- Dependent Definitions
- Requirements for Adding Dependents
- Dependent Coverage to Age 26
- Grandchildren Coverage
- Termination Provisions
- Open Enrollment
- Leave of Absence
- Medically Necessary Definition
- Experimental & Investigational (E&I)
- Reasonable & Customary (R&C)
- Workers Compensation
- Transplant Coverage
- ETS Gene Therapy
- Coordination of Benefits (COB)
- COBRA
- Subrogation
- Infertility Coverage

## Validation Features

### Status Indicators
- ✅ **Found**: Information successfully extracted and validated
- ⚠️ **Missing**: Information not found in plan document
- 🔍 **Needs Review**: Possible typo or unidentifiable term

### Smart Detection
- **Fuzzy Matching**: Catches typos and similar terms
- **Confidence Scoring**: Rates extraction accuracy
- **Cross-Reference**: Validates against definitions
- **Learning Integration**: Uses previously learned terms

## Output Files

### HTML Preview
- Editable form interface
- Color-coded status indicators
- Validation warnings and suggestions
- Real-time change tracking

### PDF Checklist
- Professional formatting
- Validation summary
- Status for each field
- Page references

### Data Exports
- **JSON**: Structured data for integration
- **Excel**: Spreadsheet format for analysis

## Learning System Usage

### Teaching New Synonyms
```
Option 7 → 1 (Add Synonym)
Term: TPA
Synonym: Claims Administrator
```

### Adding Corrections
```
Option 7 → 2 (Add Correction)
Incorrect: Third Party Admin
Correct: Third Party Administrator
```

The system remembers these and applies them to future validations!

## Integration with Orange Workflow

### Current Setup (Mock Data)
The system currently uses mock data for demonstration.

### Production Setup
1. Configure Orange workflow to output Excel with these columns:
   - `Field`: Field name
   - `Extracted_Value`: Value extracted from plan document
   - `Confidence`: Extraction confidence score (0.0-1.0)
   - `Page_Number`: Source page in plan document

2. Update `OrangeOutputParser.load_excel()` method to point to your Orange output

3. System will automatically parse and process real data

## Troubleshooting

### PDF Generation Issues
If PDF export fails:
```bash
pip install --upgrade reportlab
```

### Excel Loading Issues
If Excel files won't load:
```bash
pip install --upgrade openpyxl pandas
```

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Future Enhancements

- 🔗 Direct Orange workflow integration
- 🗄️ Database backend for checklist history
- 👥 Multi-user support with authentication
- 📊 Advanced analytics dashboard
- 🤖 NLP-based intelligent field extraction
- 📱 Web-based interface
- 🔄 Version control for checklists
- 📧 Email notification system

## File Structure

```
TokioMarineChatbot/
├── plan-doc-chatbot.py      # Main system file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── learned_mappings.json     # Auto-generated learning data
└── outputs/                  # Generated files
    ├── checklist_*.html      # HTML previews
    ├── checklist_*.pdf       # PDF exports
    └── checklist_data_*.json # Data exports
```

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review the validation warnings in generated checklists
3. Use Chat Mode (Option 9) for system guidance
4. Check the learning history (Option 8) for previous corrections

## Credits

Developed for Tokio Marine Insurance Company
Version 1.0 - November 2025

---

**Note**: This is a prototype system. Always review generated checklists manually before final approval.
