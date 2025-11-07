# 🏗️ System Architecture - AI Plan Document Review System

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INSURANCE PLAN DOCUMENTS                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Orange Data   │ (Text Mining & NLP)
                    │   Workflow     │
                    └────────┬───────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Excel Output       │
                  │  (Extracted Data)    │
                  └──────────┬───────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────────────┐
        │         OrangeOutputParser                         │
        │  • Loads Excel file                                │
        │  • Validates data structure                        │
        │  • Maps fields to checklist items                  │
        └────────────────────┬───────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────────────┐
        │           DefinitionsParser                        │
        │  • Insurance terminology database                  │
        │  • Field identifiers & synonyms                    │
        │  • Expected locations in documents                 │
        └────────────────────┬───────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────────────┐
        │              Validator                             │
        │  • Cross-reference with definitions                │
        │  • Fuzzy matching for typos                        │
        │  • Confidence scoring                              │
        │  • Flag missing/unidentifiable terms               │
        └────────────────────┬───────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────────────┐
        │         ChecklistGenerator                         │
        │  • Auto-populate checklist fields                  │
        │  • Apply validation results                        │
        │  • Status indicators (Found/Missing/Review)        │
        └────────────────────┬───────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
    ┌───────────────────┐    ┌──────────────────────┐
    │   HTML Preview    │    │   PDFGenerator       │
    │  • Editable form  │    │  • Professional      │
    │  • Color-coded    │    │    formatting        │
    │  • Interactive    │    │  • Validation        │
    │    validation     │    │    summary           │
    └─────────┬─────────┘    └──────────┬───────────┘
              │                         │
              │        ┌────────────────┘
              │        │
              ▼        ▼
    ┌─────────────────────────────┐
    │   User Reviews & Edits      │
    │   (Corrections tracked)     │
    └─────────────┬───────────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │     LearningEngine          │
    │  • Store synonyms           │
    │  • Store corrections        │
    │  • Update learned_mappings  │
    │  • Audit trail              │
    └─────────────┬───────────────┘
                  │
                  └──────────► Future validations improved!
```

## Component Architecture

### 1. **LearningEngine**
```python
Responsibilities:
├── Load/Save learned_mappings.json
├── Manage synonyms dictionary
├── Manage corrections dictionary
├── Track learning history
└── Apply learned knowledge to validation

Data Structure:
{
  "synonyms": {"term": ["synonym1", "synonym2"]},
  "corrections": {"incorrect": "correct"},
  "custom_rules": [],
  "learning_history": [...]
}
```

### 2. **DefinitionsParser**
```python
Responsibilities:
├── Parse insurance field definitions
├── Store expected identifiers
├── Map fields to document sections
└── Provide validation reference

Key Fields:
├── Group Information (Name, Eff Date, TPA, UR, PPO)
├── Eligibility (Hours, Dependents, Age 26)
├── Coverage Details (Benefits, Exclusions)
└── Administrative (COB, COBRA, Subrogation)
```

### 3. **Validator**
```python
Responsibilities:
├── Cross-reference extracted data
├── Fuzzy string matching (typo detection)
├── Confidence scoring
├── Generate warnings & suggestions
└── Integrate with learning engine

Validation Statuses:
├── ✅ found (high confidence match)
├── ⚠️ missing (no data extracted)
├── 🔍 needs_review (typo/low confidence)
└── ❓ unidentifiable (unknown term)
```

### 4. **OrangeOutputParser**
```python
Responsibilities:
├── Load Excel files from Orange workflow
├── Validate column structure
├── Extract field data
├── Mock data generation (for testing)
└── Group-specific data retrieval

Expected Excel Format:
Field | Extracted_Value | Confidence | Page_Number
```

### 5. **ChecklistGenerator**
```python
Responsibilities:
├── Map Orange data to checklist format
├── Structure group info vs plan details
├── Generate HTML editable form
├── Apply color-coding by status
└── Track field metadata (page, confidence)

Output Formats:
├── Dictionary (internal)
├── HTML Form (editable)
└── Flattened Dict (for export)
```

### 6. **PDFGenerator**
```python
Responsibilities:
├── Professional PDF formatting
├── Tables for structured data
├── Validation summary
├── Page references
└── Status indicators

Uses: ReportLab library
```

### 7. **ChatbotInterface**
```python
Responsibilities:
├── User interaction menu
├── Orchestrate all components
├── Chat mode (Q&A)
├── File management
└── Export coordination

User Actions:
├── Load data
├── Generate checklist
├── Validate
├── Preview HTML
├── Export PDF/Data
└── Teach system
```

## Data Flow Details

### Input Flow
```
Plan Documents → Orange Workflow → Excel File
                                       ↓
                              Field | Value | Confidence | Page
                                       ↓
                             OrangeOutputParser
                                       ↓
                        Dictionary: {field: {value, conf, page}}
```

### Validation Flow
```
Extracted Data → DefinitionsParser (get expected terms)
        ↓              ↓
        └──→ Validator ←── LearningEngine (learned terms)
                ↓
        Validation Report:
        - Status per field
        - Warnings list
        - Suggestions list
        - Confidence scores
```

### Learning Flow
```
User Correction → LearningEngine.add_correction()
                         ↓
                  learned_mappings.json
                         ↓
                  Future Validations
                         ↓
                  Improved Accuracy!
```

### Export Flow
```
Checklist Data → ChecklistGenerator
                       ↓
        ┌──────────────┴──────────────┐
        ▼                             ▼
   HTML Form                      PDFGenerator
   (editable)                          ↓
        ↓                         PDF Document
   Browser                             ↓
        ↓                         Final Output
   User Edits
        ↓
   Track Changes → LearningEngine
```

## File Structure

```
TokioMarineChatbot/
│
├── plan-doc-chatbot.py          # Main system (all components)
│   ├── class LearningEngine
│   ├── class DefinitionsParser
│   ├── class Validator
│   ├── class OrangeOutputParser
│   ├── class ChecklistGenerator
│   ├── class PDFGenerator
│   └── class ChatbotInterface
│
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
├── SETUP_GUIDE.md               # Installation guide
├── ARCHITECTURE.md              # This file
├── demo.py                      # Quick demo script
│
├── learned_mappings.json        # Auto-generated learning data
│
└── outputs/                     # Generated files
    ├── checklist_*.html         # HTML previews
    ├── checklist_*.pdf          # PDF exports
    ├── checklist_data_*.json    # JSON exports
    └── checklist_data_*.xlsx    # Excel exports
```

## Integration Points

### Current State (Prototype)
```
┌──────────────┐
│  Mock Data   │ (Built-in sample data)
└──────┬───────┘
       ↓
   System Processing
```

### Production State (Future)
```
┌──────────────────┐
│ Orange Workflow  │ (Real NLP/text mining)
└────────┬─────────┘
         ↓
    Excel Export
         ↓
┌─────────────────────┐
│  File Upload API    │ (Web interface)
└─────────┬───────────┘
          ↓
   System Processing
          ↓
┌─────────────────────┐
│  Database Storage   │ (Historical data)
└─────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────┐
│      Python 3.8+                │
├─────────────────────────────────┤
│  Core Libraries:                │
│  • pandas - Data manipulation   │
│  • openpyxl - Excel I/O         │
│  • reportlab - PDF generation   │
│  • json - Data persistence      │
│  • difflib - Fuzzy matching     │
│  • re - Text processing         │
└─────────────────────────────────┘
```

## Performance Characteristics

```
Operation                    | Time        | Notes
────────────────────────────────────────────────────
Load Orange Excel (1000 rows)| ~2 seconds  | Depends on file size
Generate Checklist           | <1 second   | In-memory processing
Validate Checklist (25 fields)| <1 second  | Fast dictionary lookups
Generate HTML Preview        | <1 second   | Template rendering
Export PDF                   | 2-3 seconds | ReportLab processing
Learn New Mapping            | <0.1 seconds| JSON file update
```

## Security Considerations

### Current Implementation
- ✅ Local file system only
- ✅ No network connections
- ✅ No sensitive data storage
- ✅ Audit trail in learning history

### Production Recommendations
- 🔒 User authentication
- 🔒 Role-based access control
- 🔒 Encrypted data storage
- 🔒 Audit logging
- 🔒 HIPAA compliance (if needed)

## Scalability Path

### Phase 1: Prototype (Current)
- Single user, local system
- Mock Orange data
- Manual file management

### Phase 2: Multi-User
- Web interface
- Database backend
- User authentication
- Real Orange integration

### Phase 3: Enterprise
- Cloud deployment
- Microservices architecture
- API integration
- Real-time processing
- Advanced analytics

## Error Handling

```python
Error Type              | Handling Strategy
──────────────────────────────────────────────
File Not Found         | Graceful fallback to mock data
Invalid Excel Format   | Clear error message + sample format
PDF Generation Fails   | Suggest package reinstall
Missing Dependencies   | Installation instructions
Validation Errors      | Flag but don't block
Learning File Corrupt  | Rebuild from scratch
```

## Future Enhancements

### Near Term
1. ⚡ Batch processing (multiple groups)
2. 📊 Comparison reports (PA vs Plan Doc)
3. 🔍 Advanced search in checklists
4. 📧 Email export functionality

### Long Term
1. 🤖 Machine learning for extraction
2. 🌐 Web-based interface
3. 🔄 Version control for checklists
4. 📱 Mobile app
5. 🔗 ERP system integration
6. 📈 Analytics dashboard

---

**Version**: 1.0  
**Last Updated**: November 2025  
**System Status**: ✅ Prototype Complete
