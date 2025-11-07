# Mock Orange Workflow Data

## Overview
This folder contains realistic mock Excel files simulating Orange workflow output for testing the Plan Document Review System.

## Files

### Individual Group Files:
1. **orange_output_aurora_dynamics.xlsx**
   - Complete data set
   - 20/25 fields populated
   - Good for testing successful extraction

2. **orange_output_helios_manufacturing.xlsx**
   - Partial data (many N/F values)
   - 15/25 fields populated
   - Good for testing missing field handling

3. **orange_output_solstice_technologies.xlsx**
   - Complete with term variations
   - 19/25 fields populated
   - Good for testing synonym recognition

4. **orange_output_techventure_typos.xlsx**
   - Contains intentional typos
   - Lower confidence scores
   - Good for testing typo detection and fuzzy matching

5. **orange_output_globalcorp.xlsx**
   - Complete, high-quality data
   - 25/25 fields populated
   - High confidence scores (>90%)
   - Good for testing ideal scenario

### Combined File:
- **orange_output_all_groups.xlsx**
  - All 5 groups in one file
  - Includes Group_Name column
  - Good for batch processing tests

## Excel File Structure

Each file contains these columns:
- **Field**: Field name (e.g., "Group Name", "TPA", "PPO Network")
- **Extracted_Value**: Value extracted from plan document
- **Confidence**: Confidence score (0.0 to 1.0)
- **Page_Number**: Source page in plan document (or None if N/F)

## Usage

### Option 1: Load in Chatbot
```python
python3 plan-doc-chatbot.py
# Choose option 1
# Enter: mock_data/orange_output_aurora_dynamics.xlsx
```

### Option 2: Test Specific Scenario
```python
from plan_doc_chatbot import OrangeOutputParser

parser = OrangeOutputParser("mock_data/orange_output_techventure_typos.xlsx")
data = parser.get_data_for_group("TechVenture Inc.")
```

## Test Scenarios

### Test 1: Complete Data
Use: **orange_output_globalcorp.xlsx**
Expected: High confidence, all fields found, clean PDF

### Test 2: Missing Fields
Use: **orange_output_helios_manufacturing.xlsx**
Expected: Multiple warnings, missing field flags

### Test 3: Typo Detection
Use: **orange_output_techventure_typos.xlsx**
Expected: Fuzzy match suggestions, lower confidence warnings

### Test 4: Standard Case
Use: **orange_output_aurora_dynamics.xlsx**
Expected: Most fields found, some missing, typical scenario

### Test 5: Batch Processing
Use: **orange_output_all_groups.xlsx**
Expected: Can process multiple groups from single file

## Field Statistics

| Field | Aurora | Helios | Solstice | TechVenture | GlobalCorp |
|-------|--------|--------|----------|-------------|------------|
| Found | 20 | 15 | 19 | 25 | 25 |
| Missing | 5 | 10 | 6 | 0 | 0 |
| Avg Confidence | 0.78 | 0.65 | 0.82 | 0.83 | 0.95 |

## Known Issues to Test

### TechVenture File (Typos):
- "Adminstrator" → Should suggest "Administrator"
- "Reviw" → Should suggest "Review"
- "elligible" → Should suggest "eligible"
- "necesary" → Should suggest "necessary"
- "Expirimental" → Should suggest "Experimental"

Expected: System should flag these with fuzzy matching

### Helios File (Missing Data):
- Multiple "N/F" values
- Low field count

Expected: System should flag missing fields, lower overall status

## Creating Your Own Test Data

To create custom test data:
1. Copy one of the Excel files
2. Modify the Extracted_Value column
3. Adjust Confidence scores (0.0-1.0)
4. Update Page_Number if needed
5. Save and load in the system

## Notes

- All data is fictional and for testing only
- Company names, TPAs, and networks are made up
- Confidence scores are realistic estimates
- Page numbers are representative examples
