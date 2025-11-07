#!/usr/bin/env python3
"""
Quick Test Script - Test with Real Mock Excel Files
Demonstrates loading and processing actual Excel files
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_excel_loading():
    """Test loading the mock Excel files"""
    
    print("\n" + "="*70)
    print("🧪 Testing Excel File Loading")
    print("="*70)
    
    # Import after adding to path
    from pathlib import Path
    import pandas as pd
    
    mock_dir = Path("mock_data")
    
    if not mock_dir.exists():
        print("\n❌ Error: mock_data folder not found!")
        print("   Run: python3 create_mock_data.py")
        return
    
    print("\n📂 Testing Excel Files:\n")
    
    # Test each file
    test_files = [
        "orange_output_aurora_dynamics.xlsx",
        "orange_output_helios_manufacturing.xlsx", 
        "orange_output_solstice_technologies.xlsx",
        "orange_output_techventure_typos.xlsx",
        "orange_output_globalcorp.xlsx"
    ]
    
    for filename in test_files:
        filepath = mock_dir / filename
        try:
            df = pd.read_excel(filepath)
            
            # Count fields
            total_fields = len(df)
            found_fields = len(df[df['Extracted_Value'] != 'N/F'])
            missing_fields = total_fields - found_fields
            avg_confidence = df['Confidence'].mean()
            
            print(f"✅ {filename}")
            print(f"   Rows: {total_fields}")
            print(f"   Found: {found_fields}/{total_fields}")
            print(f"   Missing: {missing_fields}")
            print(f"   Avg Confidence: {avg_confidence:.2%}")
            print()
            
        except Exception as e:
            print(f"❌ {filename}: {e}\n")
    
    # Test combined file
    print("="*70)
    combined_file = mock_dir / "orange_output_all_groups.xlsx"
    try:
        df = pd.read_excel(combined_file)
        groups = df['Group_Name'].unique()
        
        print(f"\n✅ orange_output_all_groups.xlsx")
        print(f"   Total Rows: {len(df)}")
        print(f"   Groups: {len(groups)}")
        print(f"   Group Names:")
        for group in groups:
            group_data = df[df['Group_Name'] == group]
            print(f"      • {group} ({len(group_data)} fields)")
        print()
        
    except Exception as e:
        print(f"❌ Combined file: {e}\n")
    
    print("="*70)
    print("\n✅ Excel files are ready for testing!")
    print("\n🚀 Next Steps:")
    print("   1. Run: python3 plan-doc-chatbot.py")
    print("   2. Choose option 1")
    print("   3. Enter: mock_data/orange_output_aurora_dynamics.xlsx")
    print("   4. Choose option 2")
    print("   5. Enter: Aurora Dynamics")
    print()

def test_full_workflow():
    """Test the complete workflow programmatically"""
    
    print("\n" + "="*70)
    print("🧪 Testing Complete Workflow")
    print("="*70)
    
    try:
        # This would import and test the full system
        print("\n📋 This would test:")
        print("   1. Loading Excel file")
        print("   2. Generating checklist")
        print("   3. Running validation")
        print("   4. Creating HTML preview")
        print("   5. Exporting PDF")
        print("\n💡 Use the interactive chatbot for full testing:")
        print("   python3 plan-doc-chatbot.py")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        test_full_workflow()
    else:
        test_excel_loading()
