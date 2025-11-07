#!/usr/bin/env python3
"""
Mock Data Generator for Testing
Creates realistic Excel files simulating Orange workflow output
"""

import pandas as pd
from pathlib import Path

def create_mock_excel_files():
    """Create mock Orange workflow Excel files for testing"""
    
    print("\n" + "="*70)
    print("📊 Creating Mock Orange Workflow Excel Files")
    print("="*70)
    
    # Create mock_data directory
    mock_dir = Path("mock_data")
    mock_dir.mkdir(exist_ok=True)
    print(f"\n✓ Created directory: {mock_dir}/")
    
    # Mock Data Set 1: Aurora Dynamics (Complete data)
    aurora_data = {
        "Field": [
            "Group Name", "Group Eff Date", "TPA", "UR Vendor", "PPO Network",
            "Min Hour Requirement", "Retirees", "BOD Directors Officers",
            "Dependent Definitions", "Req Adding Dependents", "Dependent to Age 26",
            "Grandchildren", "Termination Provisions", "Open Enrollment", 
            "Leave of Absence", "Medically Necessary", "E&I", "R&C", 
            "Workers Comp", "Transplant", "ETS Gene Therapy", "COB", "COBRA",
            "Subrogation", "Infertility"
        ],
        "Extracted_Value": [
            "Aurora Dynamics", 
            "March 1, 2026", 
            "BluePeak Benefits Solutions",
            "MedAxis Review Group", 
            "HealthSphere Alliance", 
            "28 hours per week",
            "Not Found", 
            "Not eligible", 
            "Legal spouse, child, domestic partner",
            "Within 30 days of qualifying event", 
            "End of month child turns 26",
            "Not eligible unless legal guardian", 
            "Final day of employment",
            "N/F", 
            "N/F", 
            "Services required to diagnose or treat",
            "Not widely accepted as standard care", 
            "Typical charge in geographic area $1,000 example",
            "Excluded", 
            "Covered - see Transplant Benefits Section",
            "N/F", 
            "Coordinates when covered by multiple plans",
            "18 months post-employment", 
            "N/F", 
            "$15,000 per family per year"
        ],
        "Confidence": [
            0.95, 0.95, 0.90, 0.92, 0.93, 0.88, 0.0, 0.91, 0.89, 0.87,
            0.90, 0.85, 0.92, 0.0, 0.0, 0.88, 0.86, 0.89, 0.93, 0.91,
            0.0, 0.88, 0.94, 0.0, 0.87
        ],
        "Page_Number": [
            1, 1, 1, 1, 1, 1, 4, 4, 9, 8, 8, 9, 4, None, None, 8, 8, 8,
            9, 5, None, 7, 4, None, 9
        ]
    }
    
    # Mock Data Set 2: Helios Manufacturing (Partial data - testing missing fields)
    helios_data = {
        "Field": [
            "Group Name", "Group Eff Date", "TPA", "UR Vendor", "PPO Network",
            "Min Hour Requirement", "Retirees", "BOD Directors Officers",
            "Dependent Definitions", "Req Adding Dependents", "Dependent to Age 26",
            "Grandchildren", "Termination Provisions", "Open Enrollment",
            "Leave of Absence", "Medically Necessary", "E&I", "R&C",
            "Workers Comp", "Transplant", "ETS Gene Therapy", "COB", "COBRA",
            "Subrogation", "Infertility"
        ],
        "Extracted_Value": [
            "Helios Manufacturing Inc.", 
            "January 1, 2025", 
            "Sunrise Claims Administration", 
            "Apex Medical Review Services",
            "StellarCare Preferred Network", 
            "30 hours per week",
            "Not Found", 
            "Not eligible", 
            "N/F",
            "Within qualifying life event", 
            "N/F", 
            "N/F",
            "Last day of employment", 
            "N/F", 
            "N/F", 
            "N/F", 
            "N/F",
            "Typical charge in geographic area", 
            "N/F",
            "Covered - $500,000 lifetime max", 
            "N/F",
            "Coverage under more than one Plan", 
            "18 months after termination",
            "Recover costs from third parties", 
            "N/F"
        ],
        "Confidence": [
            0.96, 0.94, 0.91, 0.90, 0.92, 0.89, 0.0, 0.90, 0.0, 0.85,
            0.0, 0.0, 0.93, 0.0, 0.0, 0.0, 0.0, 0.88, 0.0, 0.92,
            0.0, 0.87, 0.93, 0.89, 0.0
        ],
        "Page_Number": [
            1, 1, 2, 2, 1, 4, None, 4, None, 4, None, None, 4, None,
            None, None, None, 11, None, 6, None, 9, 4, 10, None
        ]
    }
    
    # Mock Data Set 3: Solstice Technologies (Complete with variations)
    solstice_data = {
        "Field": [
            "Group Name", "Group Eff Date", "TPA", "UR Vendor", "PPO Network",
            "Min Hour Requirement", "Retirees", "BOD Directors Officers",
            "Dependent Definitions", "Req Adding Dependents", "Dependent to Age 26",
            "Grandchildren", "Termination Provisions", "Open Enrollment",
            "Leave of Absence", "Medically Necessary", "E&I", "R&C",
            "Workers Comp", "Transplant", "ETS Gene Therapy", "COB", "COBRA",
            "Subrogation", "Infertility"
        ],
        "Extracted_Value": [
            "Solstice Technologies", 
            "July 1, 2026",
            "Summit Benefit Partners", 
            "MedBridge Solutions",
            "UnityHealth Network", 
            "32 hours per week",
            "Not Found", 
            "Not eligible", 
            "Legal spouse, domestic partner, children",
            "Within 30 days of qualifying event", 
            "Coverage ends at age 26",
            "Not eligible unless legal guardian", 
            "Last day of employment",
            "N/F", 
            "N/F",
            "Services for preventing, evaluating, diagnosing, treating",
            "Experimental, Investigational, Unproven",
            "Typical charge in geographic area - R&C example",
            "Excluded - Workers Compensation", 
            "Covered - see Transplant section",
            "N/F", 
            "Coordination when multiple plans",
            "18 months post-employment", 
            "Plan may recover from third parties",
            "N/F"
        ],
        "Confidence": [
            0.97, 0.95, 0.92, 0.91, 0.93, 0.90, 0.0, 0.91, 0.88, 0.86,
            0.89, 0.84, 0.92, 0.0, 0.0, 0.89, 0.87, 0.90, 0.91, 0.90,
            0.0, 0.88, 0.94, 0.87, 0.0
        ],
        "Page_Number": [
            1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 6, 6, None, None, 12,
            12, None, 12, 3, None, 11, 6, 11, None
        ]
    }
    
    # Mock Data Set 4: TechVenture Inc (With typos for testing)
    techventure_data = {
        "Field": [
            "Group Name", "Group Eff Date", "TPA", "UR Vendor", "PPO Network",
            "Min Hour Requirement", "Retirees", "BOD Directors Officers",
            "Dependent Definitions", "Req Adding Dependents", "Dependent to Age 26",
            "Grandchildren", "Termination Provisions", "Open Enrollment",
            "Leave of Absence", "Medically Necessary", "E&I", "R&C",
            "Workers Comp", "Transplant", "ETS Gene Therapy", "COB", "COBRA",
            "Subrogation", "Infertility"
        ],
        "Extracted_Value": [
            "TechVenture Inc.", 
            "April 15, 2026",
            "Claims Adminstrator Inc",  # Typo: Adminstrator
            "Utilization Reviw Group",  # Typo: Reviw
            "PreferredCare Network", 
            "28 hrs weekly",  # Variation
            "Not coverd",  # Typo: coverd
            "Officers not elligible",  # Typo: elligible
            "Spouse and dependant children",  # Typo: dependant
            "30 day enrollment period", 
            "Age 26 coverage termination",
            "Grandchild not covered", 
            "Employment termination date",
            "Annual enrollment peiod",  # Typo: peiod
            "Up to 12 weeks FMLA",
            "Medically necesary services",  # Typo: necesary
            "Expirimental treatments excluded",  # Typo: Expirimental
            "Reasonable and Customery charges",  # Typo: Customery
            "Work related injuries excluded", 
            "Organ transplants covered",
            "Gene therapy through ETS netowrk",  # Typo: netowrk
            "Cordination of Benefits applies",  # Typo: Cordination
            "18 month COBRA continuation",
            "Right to reimbursment",  # Typo: reimbursment
            "$20,000 lifetime max"
        ],
        "Confidence": [
            0.98, 0.94, 0.75, 0.72, 0.91, 0.82, 0.68, 0.74, 0.79, 0.88,
            0.85, 0.83, 0.90, 0.71, 0.89, 0.76, 0.73, 0.78, 0.92, 0.89,
            0.77, 0.75, 0.93, 0.74, 0.91
        ],
        "Page_Number": [
            1, 1, 2, 2, 1, 3, 5, 5, 6, 6, 6, 6, 5, None, 7, 8, 9, 8,
            9, 4, 4, 10, 5, 10, 7
        ]
    }
    
    # Mock Data Set 5: GlobalCorp (Complete, high quality)
    globalcorp_data = {
        "Field": [
            "Group Name", "Group Eff Date", "TPA", "UR Vendor", "PPO Network",
            "Min Hour Requirement", "Retirees", "BOD Directors Officers",
            "Dependent Definitions", "Req Adding Dependents", "Dependent to Age 26",
            "Grandchildren", "Termination Provisions", "Open Enrollment",
            "Leave of Absence", "Medically Necessary", "E&I", "R&C",
            "Workers Comp", "Transplant", "ETS Gene Therapy", "COB", "COBRA",
            "Subrogation", "Infertility"
        ],
        "Extracted_Value": [
            "GlobalCorp International", 
            "January 1, 2026",
            "Pinnacle Claims Services", 
            "CareReview Utilization Management",
            "National Health Network", 
            "30 hours per week",
            "Retiree coverage available with premium", 
            "Board members eligible if actively employed", 
            "Legal spouse, domestic partner, children to age 26",
            "Within 31 days of qualifying life event with proof", 
            "Dependent children covered until 26th birthday",
            "Grandchildren eligible only if employee is legal guardian", 
            "Coverage terminates on last day of employment",
            "Annual open enrollment period in November", 
            "Coverage continues during FMLA leave up to 12 weeks",
            "Services medically necessary for diagnosis or treatment of illness or injury",
            "Experimental and Investigational treatments are excluded from coverage",
            "Reasonable and Customary means typical charges in the geographic area",
            "Work-related injuries covered by Workers Compensation are excluded", 
            "Organ transplants covered at approved transplant centers",
            "Gene therapy available through ETS Centers of Excellence network",
            "Coordination of Benefits applies when covered by multiple plans",
            "COBRA continuation coverage available for 18 months after termination",
            "Plan has right to recover costs from responsible third parties",
            "Infertility treatment covered up to $20,000 lifetime maximum"
        ],
        "Confidence": [
            0.99, 0.98, 0.96, 0.95, 0.97, 0.94, 0.93, 0.92, 0.95, 0.94,
            0.96, 0.91, 0.97, 0.92, 0.93, 0.95, 0.94, 0.96, 0.97, 0.95,
            0.93, 0.96, 0.98, 0.94, 0.95
        ],
        "Page_Number": [
            1, 1, 1, 1, 1, 3, 5, 5, 7, 7, 7, 7, 5, 4, 6, 10, 10, 10,
            11, 8, 8, 12, 5, 13, 9
        ]
    }
    
    # Create Excel files
    datasets = {
        "orange_output_aurora_dynamics.xlsx": aurora_data,
        "orange_output_helios_manufacturing.xlsx": helios_data,
        "orange_output_solstice_technologies.xlsx": solstice_data,
        "orange_output_techventure_typos.xlsx": techventure_data,
        "orange_output_globalcorp.xlsx": globalcorp_data
    }
    
    print("\n📁 Creating Excel files:")
    for filename, data in datasets.items():
        df = pd.DataFrame(data)
        filepath = mock_dir / filename
        df.to_excel(filepath, index=False)
        print(f"   ✓ {filename} ({len(df)} rows)")
    
    # Create a combined file with all groups
    print("\n📊 Creating combined file with all groups...")
    all_data = []
    group_names = [
        "Aurora Dynamics",
        "Helios Manufacturing Inc.",
        "Solstice Technologies",
        "TechVenture Inc.",
        "GlobalCorp International"
    ]
    
    for group_name, (filename, data) in zip(group_names, datasets.items()):
        df = pd.DataFrame(data)
        df['Group_Name'] = group_name  # Add group identifier
        all_data.append(df)
    
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_path = mock_dir / "orange_output_all_groups.xlsx"
    combined_df.to_excel(combined_path, index=False)
    print(f"   ✓ orange_output_all_groups.xlsx ({len(combined_df)} rows)")
    
    # Create README for mock data
    readme_content = """# Mock Orange Workflow Data

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
"""
    
    readme_path = mock_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print(f"\n   ✓ README.md (documentation)")
    
    # Print summary
    print("\n" + "="*70)
    print("✅ SUCCESS! Mock Data Created")
    print("="*70)
    print(f"\n📂 Location: {mock_dir.absolute()}/")
    print(f"\n📊 Files created:")
    print(f"   • 5 individual Excel files (one per group)")
    print(f"   • 1 combined Excel file (all groups)")
    print(f"   • 1 README.md (documentation)")
    print(f"\n🎯 How to use:")
    print(f"   1. Run: python3 plan-doc-chatbot.py")
    print(f"   2. Choose option 1 (Load Orange Output)")
    print(f"   3. Enter: mock_data/orange_output_aurora_dynamics.xlsx")
    print(f"   4. Choose option 2 (Generate Checklist)")
    print(f"   5. Enter: Aurora Dynamics")
    print(f"\n🧪 Test scenarios:")
    print(f"   • Complete data → orange_output_globalcorp.xlsx")
    print(f"   • Missing fields → orange_output_helios_manufacturing.xlsx")
    print(f"   • Typo detection → orange_output_techventure_typos.xlsx")
    print(f"   • Standard case → orange_output_aurora_dynamics.xlsx")
    print()

if __name__ == "__main__":
    create_mock_excel_files()
