"""
Generate a test Orange output Excel file for testing the Streamlit app
This simulates what Orange workflow would produce
"""

import pandas as pd
from datetime import datetime

# Create sample Orange output data
data = {
    'Field': [
        'Group Name',
        'Group Number',
        'Effective Date',
        'Plan Year',
        'Third Party Administrator',
        'TPA Address',
        'TPA Phone',
        'Medical Plan Type',
        'Deductible Individual',
        'Deductible Family',
        'Out of Pocket Max Individual',
        'Out of Pocket Max Family',
        'Coinsurance',
        'Primary Care Physician Copay',
        'Specialist Copay',
        'Emergency Room Copay',
        'Urgent Care Copay',
        'Prescription Drug Coverage',
        'Pharmacy Network',
        'Retail Copay Generic',
        'Retail Copay Brand',
        'Mail Order Available',
        'Utilization Review Vendor',
        'Mental Health Provider',
        'Vision Coverage'
    ],
    'Extracted_Value': [
        'Test Medical Group Inc.',
        'TMG-2025-12345',
        '01/01/2025',
        '2025',
        'Blue Cross Claims Administration',
        '123 Insurance Way, Boston, MA 02101',
        '(800) 555-1234',
        'PPO',
        '$1,500',
        '$3,000',
        '$5,000',
        '$10,000',
        '80/20',
        '$25',
        '$50',
        '$250',
        '$75',
        'Yes',
        'CVS Caremark',
        '$10',
        '$35',
        'Yes - 90 day supply',
        'MedReview Services LLC',
        'Beacon Health Options',
        'N/F'
    ],
    'Confidence': [
        0.95,
        0.92,
        0.88,
        0.90,
        0.85,
        0.82,
        0.87,
        0.91,
        0.89,
        0.86,
        0.84,
        0.83,
        0.90,
        0.88,
        0.87,
        0.85,
        0.86,
        0.94,
        0.89,
        0.91,
        0.90,
        0.87,
        0.78,
        0.72,
        0.00
    ],
    'Page_Number': [
        1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 7, 7, 8, 9, 10, 10, 10, 11, 12, None
    ],
    'Location': [
        'Header section',
        'Header section',
        'Plan details',
        'Plan details',
        'Administrator info',
        'Administrator info',
        'Administrator info',
        'Plan type section',
        'Cost sharing',
        'Cost sharing',
        'Cost sharing',
        'Cost sharing',
        'Benefits table',
        'Copays section',
        'Copays section',
        'Emergency benefits',
        'Urgent care section',
        'Pharmacy benefits',
        'Pharmacy network',
        'Prescription costs',
        'Prescription costs',
        'Prescription options',
        'UR section',
        'Mental health',
        'Not found'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Generate output file
output_file = 'test_orange_output_demo.xlsx'
df.to_excel(output_file, index=False, sheet_name='Orange_Output')

print(f"✅ Generated test Orange output file: {output_file}")
print(f"\nFile contains:")
print(f"  - Total fields: {len(df)}")
print(f"  - Fields found: {len(df[df['Extracted_Value'] != 'N/F'])}")
print(f"  - Missing fields: {len(df[df['Extracted_Value'] == 'N/F'])}")
print(f"  - Average confidence: {df['Confidence'].mean():.2%}")
print(f"\nYou can now upload this file in the Streamlit app!")
print(f"File location: {output_file}")
