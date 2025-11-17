"""
Automated test to demonstrate checklist generation from Orange output
This simulates the complete workflow of the Streamlit app
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json

def load_orange_output(filepath):
    """Load Orange output Excel file"""
    print("📂 Loading Orange output file...")
    df = pd.read_excel(filepath)
    print(f"✅ Loaded {len(df)} fields")
    return df

def validate_data(df):
    """Validate the Orange output data"""
    print("\n🔍 Validating data structure...")
    
    required_cols = ['Field', 'Extracted_Value', 'Confidence', 'Page_Number']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"❌ Missing required columns: {missing_cols}")
        return False
    
    print("✅ All required columns present")
    return True

def generate_checklist(df):
    """Generate checklist from Orange output"""
    print("\n🔨 Generating checklist...")
    
    # Separate found and missing fields
    found_fields = df[df['Extracted_Value'] != 'N/F']
    missing_fields = df[df['Extracted_Value'] == 'N/F']
    
    # Calculate statistics
    total = len(df)
    found = len(found_fields)
    missing = len(missing_fields)
    avg_confidence = df['Confidence'].mean()
    
    # Categorize by confidence
    high_conf = len(df[df['Confidence'] > 0.8])
    med_conf = len(df[(df['Confidence'] >= 0.5) & (df['Confidence'] <= 0.8)])
    low_conf = len(df[df['Confidence'] < 0.5])
    
    checklist = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'source_file': 'test_orange_output_demo.xlsx',
            'group_name': 'Test Medical Group Inc.'
        },
        'summary': {
            'total_fields': total,
            'found_fields': found,
            'missing_fields': missing,
            'completion_rate': f"{(found/total)*100:.1f}%",
            'average_confidence': f"{avg_confidence*100:.1f}%"
        },
        'confidence_breakdown': {
            'high_confidence': high_conf,
            'medium_confidence': med_conf,
            'low_confidence': low_conf
        },
        'fields': []
    }
    
    # Add field details
    for _, row in df.iterrows():
        field_data = {
            'field_name': row['Field'],
            'extracted_value': row['Extracted_Value'],
            'confidence': f"{row['Confidence']*100:.0f}%",
            'confidence_level': get_confidence_level(row['Confidence']),
            'page_number': int(row['Page_Number']) if pd.notna(row['Page_Number']) else 'N/A',
            'status': 'Found' if row['Extracted_Value'] != 'N/F' else 'Missing',
            'location': row.get('Location', 'Unknown')
        }
        checklist['fields'].append(field_data)
    
    print(f"✅ Checklist generated with {total} fields")
    return checklist

def get_confidence_level(confidence):
    """Determine confidence level"""
    if confidence >= 0.8:
        return 'High'
    elif confidence >= 0.5:
        return 'Medium'
    else:
        return 'Low'

def display_checklist(checklist):
    """Display checklist in a readable format"""
    print("\n" + "="*80)
    print("📋 GENERATED CHECKLIST")
    print("="*80)
    
    print(f"\n📊 SUMMARY")
    print(f"   Generated: {checklist['metadata']['generated_at']}")
    print(f"   Group: {checklist['metadata']['group_name']}")
    print(f"   Total Fields: {checklist['summary']['total_fields']}")
    print(f"   Found: {checklist['summary']['found_fields']} ({checklist['summary']['completion_rate']})")
    print(f"   Missing: {checklist['summary']['missing_fields']}")
    print(f"   Average Confidence: {checklist['summary']['average_confidence']}")
    
    print(f"\n🎯 CONFIDENCE BREAKDOWN")
    print(f"   🟢 High (>80%): {checklist['confidence_breakdown']['high_confidence']}")
    print(f"   🟡 Medium (50-80%): {checklist['confidence_breakdown']['medium_confidence']}")
    print(f"   🔴 Low (<50%): {checklist['confidence_breakdown']['low_confidence']}")
    
    print(f"\n📝 FIELD DETAILS")
    print("-"*80)
    
    for field in checklist['fields']:
        status_icon = "✅" if field['status'] == 'Found' else "❌"
        conf_icon = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}.get(field['confidence_level'], "⚪")
        
        print(f"\n{status_icon} {field['field_name']}")
        print(f"   Value: {field['extracted_value']}")
        print(f"   {conf_icon} Confidence: {field['confidence']} ({field['confidence_level']})")
        print(f"   Page: {field['page_number']} | Location: {field['location']}")
    
    print("\n" + "="*80)

def export_checklist(checklist, output_file):
    """Export checklist to JSON"""
    print(f"\n💾 Exporting checklist to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(checklist, f, indent=2)
    print(f"✅ Checklist exported successfully")

def generate_validation_report(checklist):
    """Generate validation report"""
    print("\n" + "="*80)
    print("🔍 VALIDATION REPORT")
    print("="*80)
    
    # Check for fields needing review
    low_conf_fields = [f for f in checklist['fields'] if f['confidence_level'] == 'Low']
    missing_fields = [f for f in checklist['fields'] if f['status'] == 'Missing']
    
    if low_conf_fields:
        print(f"\n⚠️  {len(low_conf_fields)} FIELD(S) NEED REVIEW (Low Confidence):")
        for field in low_conf_fields:
            print(f"   - {field['field_name']}: {field['confidence']} confidence")
    else:
        print("\n✅ All found fields have acceptable confidence levels")
    
    if missing_fields:
        print(f"\n❌ {len(missing_fields)} MISSING FIELD(S):")
        for field in missing_fields:
            print(f"   - {field['field_name']}")
    else:
        print("\n🎉 All fields found!")
    
    # Overall status
    print("\n📊 OVERALL STATUS:")
    completion_rate = float(checklist['summary']['completion_rate'].strip('%'))
    avg_conf = float(checklist['summary']['average_confidence'].strip('%'))
    
    if completion_rate == 100 and avg_conf >= 80:
        print("   🟢 EXCELLENT - All fields found with high confidence")
    elif completion_rate >= 90 and avg_conf >= 70:
        print("   🟡 GOOD - Most fields found with acceptable confidence")
    else:
        print("   🔴 NEEDS REVIEW - Some fields missing or low confidence")
    
    print("="*80)

def main():
    """Main test workflow"""
    print("\n🚀 TOKIO MARINE CHECKLIST GENERATION TEST")
    print("="*80)
    
    # Step 1: Load Orange output
    input_file = "test_orange_output_demo.xlsx"
    if not Path(input_file).exists():
        print(f"❌ Error: {input_file} not found. Please run test_orange_output.py first.")
        return
    
    df = load_orange_output(input_file)
    
    # Step 2: Validate data
    if not validate_data(df):
        print("❌ Data validation failed")
        return
    
    # Step 3: Generate checklist
    checklist = generate_checklist(df)
    
    # Step 4: Display checklist
    display_checklist(checklist)
    
    # Step 5: Generate validation report
    generate_validation_report(checklist)
    
    # Step 6: Export checklist
    output_file = "test_checklist_output.json"
    export_checklist(checklist, output_file)
    
    print("\n✅ TEST COMPLETED SUCCESSFULLY!")
    print(f"\n📁 Generated files:")
    print(f"   - {input_file} (Orange output)")
    print(f"   - {output_file} (Checklist JSON)")
    print(f"\n💡 You can now upload {input_file} to the Streamlit app to see the interactive version!")

if __name__ == "__main__":
    main()
