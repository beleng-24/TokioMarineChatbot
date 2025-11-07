# 🤖 TokioMarineChatbot

An AI-enabled chatbot system for automating insurance plan document review and checklist generation.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

## 📋 Overview

**TokioMarineChatbot** is an intelligent automation system designed for insurance plan document review. It parses Orange workflow output, auto-generates checklists, validates extracted information, and continuously learns from user corrections.

### Key Features

- 🤖 **Automated Checklist Generation** - Converts workflow data into structured checklists
- 🔍 **Smart Validation** - Cross-references with definitions, detects typos
- 🧠 **Continuous Learning** - Learns from user corrections and synonyms
- 📝 **Editable Preview** - HTML form interface for review before export
- 📄 **PDF Export** - Professional checklist documents
- 💾 **Multiple Export Formats** - JSON, Excel, PDF
- 💬 **Interactive Chatbot** - User-friendly menu system

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/TokioMarineChatbot.git
cd TokioMarineChatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create mock data** (for testing)
```bash
python3 create_mock_data.py
```

4. **Run the chatbot**
```bash
python3 plan-doc-chatbot.py
```

## 🎯 Usage

### Basic Workflow

1. Start the system: `python3 plan-doc-chatbot.py`
2. Load Orange Excel output (option 1)
3. Generate checklist (option 2)
4. Review HTML preview (option 4)
5. Export to PDF (option 5)

### Example

```bash
# Start the chatbot
python3 plan-doc-chatbot.py

# In the menu:
# 1. Load: mock_data/orange_output_aurora_dynamics.xlsx
# 2. Generate: Aurora Dynamics
# 3. Export: PDF
```

## 📊 Mock Data

The system includes 5 realistic mock datasets for testing:

- **GlobalCorp International** - Perfect scenario (25/25 fields)
- **Aurora Dynamics** - Standard case (21/25 fields)
- **Solstice Technologies** - Variations (21/25 fields)
- **Helios Manufacturing** - Missing data (15/25 fields)
- **TechVenture Inc.** - Typos for testing validation

## 📚 Documentation

- **[INDEX.md](INDEX.md)** - Complete file guide and navigation
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick start cheat sheet
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed installation instructions
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive testing guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture details
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Executive overview

## 🏗️ System Architecture

```
Orange Workflow → Excel Output → Parser → Validator → Checklist Generator
                                            ↓
                                    Learning Engine
                                            ↓
                              HTML Preview ← → PDF Export
```

### Core Components

- **LearningEngine** - Manages continuous learning
- **DefinitionsParser** - Insurance terminology database
- **Validator** - Smart validation with typo detection
- **OrangeOutputParser** - Parses Excel workflow output
- **ChecklistGenerator** - Creates structured checklists
- **PDFGenerator** - Professional PDF export
- **ChatbotInterface** - Interactive user interface

## 🧪 Testing

Run the test suite:

```bash
# Verify mock data
python3 test_excel.py

# Run system demo
python3 demo.py

# Follow comprehensive testing guide
# See TESTING_GUIDE.md
```

## 📦 Project Structure

```
TokioMarineChatbot/
├── plan-doc-chatbot.py       # Main system
├── requirements.txt           # Dependencies
├── create_mock_data.py        # Mock data generator
├── test_excel.py              # Testing utilities
├── demo.py                    # Quick demo
│
├── mock_data/                 # Mock Excel files
│   ├── orange_output_*.xlsx
│   └── README.md
│
└── docs/                      # Documentation
    ├── INDEX.md
    ├── QUICK_REFERENCE.md
    ├── SETUP_GUIDE.md
    ├── TESTING_GUIDE.md
    ├── ARCHITECTURE.md
    └── PROJECT_SUMMARY.md
```

## 🎯 Features

### Automated Processing
- Parse Orange workflow Excel output
- Extract 25 insurance document fields
- Auto-populate checklist with validation

### Smart Validation
- Cross-reference with insurance definitions
- Fuzzy matching for typo detection
- Confidence scoring (0-100%)
- Missing field detection

### Continuous Learning
- Learn new synonyms
- Store user corrections
- Maintain audit trail
- Improve accuracy over time

### Multiple Exports
- **HTML** - Editable preview form
- **PDF** - Professional checklist
- **JSON** - Structured data
- **Excel** - Spreadsheet format

## 🔧 Technology Stack

- **Python 3.8+**
- **pandas** - Data manipulation
- **openpyxl** - Excel I/O
- **reportlab** - PDF generation

## 📈 Performance

- Load Excel (1000 rows): ~2 seconds
- Generate checklist: <1 second
- Validate 25 fields: <1 second
- Export PDF: 2-3 seconds

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **IS 4545 Project Team** - Tokio Marine Insurance Company

## 🙏 Acknowledgments

- Tokio Marine Insurance Company
- Orange Data Mining Workflow
- Python community

## 📞 Support

For questions or issues:
- Check the [documentation](docs/)
- Review [TESTING_GUIDE.md](TESTING_GUIDE.md)
- Use Chat Mode (option 9 in system)
- Open an issue on GitHub

## 🗺️ Roadmap

### Current Version (v1.0)
- ✅ Automated checklist generation
- ✅ Smart validation
- ✅ Continuous learning
- ✅ Multiple export formats
- ✅ Mock data for testing

### Future Enhancements
- [ ] Web-based interface
- [ ] Database integration
- [ ] Multi-user support
- [ ] Advanced analytics
- [ ] Real-time Orange integration
- [ ] Mobile app

## 📊 Status

**Version**: 1.0  
**Status**: ✅ Production Ready  
**Last Updated**: November 2025

---

**Made with ❤️ for insurance plan document review automation**
