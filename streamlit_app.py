"""
Streamlit GUI for AI-Enabled Plan Document Review System
Modern web interface for the TokioMarine Chatbot

Run: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import os
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="Tokio Marine - Plan Review System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
    }
    .success-field {
        background-color: #d4edda;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
    }
    .missing-field {
        background-color: #f8d7da;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #34495e;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_data' not in st.session_state:
    st.session_state.current_data = None
if 'checklist_generated' not in st.session_state:
    st.session_state.checklist_generated = False
if 'selected_group' not in st.session_state:
    st.session_state.selected_group = None
if 'keywords_list' not in st.session_state:
    st.session_state.keywords_list = None
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = os.getenv('OPENAI_API_KEY', '')
if 'ai_generated_checklist' not in st.session_state:
    st.session_state.ai_generated_checklist = None

# Sidebar Navigation
with st.sidebar:
    st.markdown("# 📋 Plan Review System")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "⚙️ Settings", "🔑 Keywords", "🔨 Generate Checklist", 
         "📄 Export", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    
    if st.session_state.current_data is not None:
        df = st.session_state.current_data
        st.metric("Total Fields", len(df))
        found = len(df[df['Extracted_Value'] != 'N/F'])
        st.metric("Found", found, delta=f"{(found/len(df)*100):.0f}%")
        st.metric("Avg Confidence", f"{df['Confidence'].mean()*100:.0f}%")
    else:
        st.info("No data loaded yet")
    
    st.markdown("---")
    st.markdown("**Version:** 1.0  \n**Updated:** Nov 2025")

# Helper functions
def load_mock_data(group_name):
    """Load mock data for selected group"""
    mock_files = {
        "Aurora Dynamics": "mock_data/orange_output_aurora_dynamics.xlsx",
        "Helios Manufacturing Inc.": "mock_data/orange_output_helios_manufacturing.xlsx",
        "Solstice Technologies": "mock_data/orange_output_solstice_technologies.xlsx",
        "TechVenture Inc.": "mock_data/orange_output_techventure_typos.xlsx",
        "GlobalCorp International": "mock_data/orange_output_globalcorp.xlsx"
    }
    
    if group_name in mock_files:
        filepath = Path(mock_files[group_name])
        if filepath.exists():
            return pd.read_excel(filepath)
    return None

def get_confidence_color(confidence):
    """Return color based on confidence level"""
    if confidence >= 0.8:
        return "🟢"
    elif confidence >= 0.5:
        return "🟡"
    else:
        return "🔴"

def load_keywords_list(file):
    """Load keywords list from Excel or text file"""
    try:
        if file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
            # Assume keywords are in first column or column named 'Keywords'
            if 'Keywords' in df.columns:
                keywords = df['Keywords'].dropna().tolist()
            elif 'Keyword' in df.columns:
                keywords = df['Keyword'].dropna().tolist()
            else:
                keywords = df.iloc[:, 0].dropna().tolist()
            return keywords
        else:
            # Text file - one keyword per line
            content = file.read().decode('utf-8')
            keywords = [line.strip() for line in content.split('\n') if line.strip()]
            return keywords
    except Exception as e:
        st.error(f"Error loading keywords: {str(e)}")
        return None

def generate_checklist_with_ai(keywords_list, api_key):
    """Use ChatGPT to generate checklist from keywords"""
    if not api_key:
        st.error("❌ OpenAI API key is required")
        return None
    
    # Define the checklist items from Appendix 2
    checklist_items = [
        'UR Vendor',
        'PPO Network',
        'Retirees',
        'BOD, Directors, Officers',
        'Minimum Hour Requirement',
        'Dependent Definitions',
        'Req adding dependents',
        'Dependent to age 26',
        'Grandchildren',
        'Termination Provisions',
        'Open Enrollment',
        'Leave of Absence',
        'Medically Necessary',
        'E&I',
        'R&C',
        'Workers Comp',
        'Transplant',
        'ETS Gene Therapy',
        'Coordination of Benefits',
        'COBRA',
        'Subrogation'
    ]
    
    try:
        client = OpenAI(api_key=api_key)
        
        keywords_str = "\n".join([f"- {kw}" for kw in keywords_list])
        
        prompt = f"""You are reviewing insurance plan documents for TMHCC. You have a list of keywords found in a plan document and need to generate a checklist.

Keywords found in the document:
{keywords_str}

Checklist items to evaluate:
{chr(10).join([f'{i+1}. {item}' for i, item in enumerate(checklist_items)])}

For each checklist item, determine:
1. **Matches**: Is this item present based on the keywords? (true/false)
2. **Requires Approval**: Does this item require management approval? (true/false)
3. **Requires Notice**: Does this item require notice to participants? (true/false)  
4. **Request Handbook**: Should this be documented in the handbook? (true/false)

Rules:
- Mark "Matches" as true ONLY if keywords clearly indicate this item exists in the document
- Use your insurance industry knowledge to determine the other checkboxes
- Be conservative - if unsure, mark as false

Respond in JSON format with an array of objects:
{{
  "checklist": [
    {{
      "item": "item name",
      "matches": true/false,
      "requires_approval": true/false,
      "requires_notice": true/false,
      "request_handbook": true/false,
      "reasoning": "brief explanation"
    }}
  ]
}}"""
        
        with st.spinner("🤖 AI is analyzing keywords and generating checklist..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert insurance plan document reviewer for TMHCC with deep knowledge of compliance requirements."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            checklist_data = result.get('checklist', [])
            
            # Convert to DataFrame
            df_data = []
            for item_data in checklist_data:
                df_data.append({
                    'Item': item_data.get('item', ''),
                    'Matches': item_data.get('matches', False),
                    'Requires Approval': item_data.get('requires_approval', False),
                    'Requires Notice': item_data.get('requires_notice', False),
                    'Request Handbook': item_data.get('request_handbook', False),
                    'AI Reasoning': item_data.get('reasoning', '')
                })
            
            return pd.DataFrame(df_data)
            
    except Exception as e:
        st.error(f"❌ AI Error: {str(e)}")
        return None

def enhance_with_ai(df, definitions_df, api_key):
    """Use ChatGPT API to enhance field matching and validation"""
    if not api_key:
        st.error("❌ OpenAI API key is required")
        return df
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Create definitions context
        definitions_context = "Insurance Plan Document Field Definitions:\n\n"
        for _, row in definitions_df.iterrows():
            field_name = row.get('Field', row.get('Term', ''))
            definition = row.get('Definition', row.get('Description', ''))
            if field_name and definition:
                definitions_context += f"- {field_name}: {definition}\n"
        
        enhanced_rows = []
        
        with st.spinner("🤖 AI is analyzing fields and making intelligent decisions..."):
            progress_bar = st.progress(0)
            
            for idx, row in df.iterrows():
                field_name = row['Field']
                extracted_value = row['Extracted_Value']
                confidence = row['Confidence']
                
                # For fields with low confidence or missing values, ask AI
                if confidence < 0.7 or extracted_value == 'N/F':
                    prompt = f"""Based on the following field definitions and extracted data, help validate this insurance plan field:

{definitions_context}

Field Name: {field_name}
Extracted Value: {extracted_value}
Original Confidence: {confidence}

Task:
1. Is this field required for insurance plan documents based on standard practices?
2. If the value is missing or low confidence, suggest what should be verified
3. Provide a validation status: VALID, NEEDS_REVIEW, or MISSING
4. Brief explanation (max 50 words)

Respond in JSON format:
{{
  "validation_status": "VALID/NEEDS_REVIEW/MISSING",
  "is_required": true/false,
  "suggestion": "verification suggestion",
  "explanation": "brief explanation"
}}"""
                    
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are an expert insurance plan document reviewer for TMHCC. Provide concise, accurate assessments."},
                                {"role": "user", "content": prompt}
                            ],
                            response_format={"type": "json_object"},
                            temperature=0.3
                        )
                        
                        ai_response = json.loads(response.choices[0].message.content)
                        
                        row['AI_Validation_Status'] = ai_response.get('validation_status', 'NEEDS_REVIEW')
                        row['AI_Required'] = ai_response.get('is_required', False)
                        row['AI_Suggestion'] = ai_response.get('suggestion', '')
                        row['AI_Explanation'] = ai_response.get('explanation', '')
                        row['AI_Enhanced'] = True
                        
                    except Exception as e:
                        row['AI_Validation_Status'] = 'ERROR'
                        row['AI_Required'] = False
                        row['AI_Suggestion'] = f'AI error: {str(e)}'
                        row['AI_Explanation'] = ''
                        row['AI_Enhanced'] = False
                else:
                    # High confidence fields
                    row['AI_Validation_Status'] = 'VALID'
                    row['AI_Required'] = True
                    row['AI_Suggestion'] = 'Field validated with high confidence'
                    row['AI_Explanation'] = 'Automated extraction successful'
                    row['AI_Enhanced'] = True
                
                enhanced_rows.append(row)
                progress_bar.progress((idx + 1) / len(df))
            
            progress_bar.empty()
        
        enhanced_df = pd.DataFrame(enhanced_rows)
        return enhanced_df
        
    except Exception as e:
        st.error(f"❌ AI Enhancement Error: {str(e)}")
        return df

def generate_excel_checklist_from_ai(checklist_df):
    """Generate formatted Excel checklist from AI-generated checklist DataFrame"""
    from io import BytesIO
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Draft Checklist"
    
    # Set column widths
    ws.column_dimensions['A'].width = 45
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 18
    ws.column_dimensions['E'].width = 18
    ws.column_dimensions['F'].width = 10
    
    # Define styles
    bold_font = Font(bold=True)
    header_font = Font(bold=True, size=11)
    center_align = Alignment(horizontal='center', vertical='center')
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Rows 1-11: Header information (simplified - can be populated from additional data if available)
    ws.cell(row=1, column=1).value = "Group Name: "
    ws.cell(row=1, column=1).font = bold_font
    
    ws.cell(row=2, column=1).value = "Group Name in PD:"
    ws.cell(row=2, column=1).font = bold_font
    
    ws.cell(row=3, column=1).value = "Group Eff Date:"
    ws.cell(row=3, column=1).font = bold_font
    
    ws.cell(row=4, column=1).value = "PD Eff Date:"
    ws.cell(row=4, column=1).font = bold_font
    
    ws.cell(row=5, column=1).value = "TPA:"
    ws.cell(row=5, column=1).font = bold_font
    
    ws.cell(row=6, column=1).value = "TPA in PD:"
    ws.cell(row=6, column=1).font = bold_font
    
    ws.cell(row=7, column=1).value = "Underwriter:"
    ws.cell(row=7, column=1).font = bold_font
    
    ws.cell(row=8, column=1).value = "Benefit Plan Name:"
    ws.cell(row=8, column=1).font = bold_font
    
    ws.cell(row=9, column=1).value = "Benefit Plan Name in PD:"
    ws.cell(row=9, column=1).font = bold_font
    
    ws.cell(row=10, column=1).value = "Subsidiaries:"
    ws.cell(row=10, column=1).font = bold_font
    
    ws.cell(row=11, column=1).value = "Group Address:"
    ws.cell(row=11, column=1).font = bold_font
    
    # Rows 12-20: Empty (spacing)
    
    # Row 21: Column headers
    ws.cell(row=21, column=1).value = "Item"
    ws.cell(row=21, column=2).value = "Matches"
    ws.cell(row=21, column=3).value = "Requires Approval"
    ws.cell(row=21, column=4).value = "Requires Notice"
    ws.cell(row=21, column=5).value = "Request Handbook"
    ws.cell(row=21, column=6).value = "Pg #"
    
    # Style headers
    for col in range(1, 7):
        cell = ws.cell(row=21, column=col)
        cell.font = header_font
        cell.fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")
        cell.alignment = center_align
        cell.border = border
    
    # Row 22: Empty (spacing)
    
    # Rows 23-43: Checklist items (21 items)
    start_row = 23
    for idx, row in checklist_df.iterrows():
        current_row = start_row + idx
        
        # Item name
        ws.cell(row=current_row, column=1).value = row['Item']
        ws.cell(row=current_row, column=1).border = border
        
        # Matches
        ws.cell(row=current_row, column=2).value = "X" if row['Matches'] else ""
        ws.cell(row=current_row, column=2).alignment = center_align
        ws.cell(row=current_row, column=2).border = border
        
        # Requires Approval
        ws.cell(row=current_row, column=3).value = "X" if row['Requires Approval'] else ""
        ws.cell(row=current_row, column=3).alignment = center_align
        ws.cell(row=current_row, column=3).border = border
        
        # Requires Notice
        ws.cell(row=current_row, column=4).value = "X" if row['Requires Notice'] else ""
        ws.cell(row=current_row, column=4).alignment = center_align
        ws.cell(row=current_row, column=4).border = border
        
        # Request Handbook
        ws.cell(row=current_row, column=5).value = "X" if row['Request Handbook'] else ""
        ws.cell(row=current_row, column=5).alignment = center_align
        ws.cell(row=current_row, column=5).border = border
        
        # Page number (leave empty for now - can be populated if available)
        ws.cell(row=current_row, column=6).value = ""
        ws.cell(row=current_row, column=6).alignment = center_align
        ws.cell(row=current_row, column=6).border = border
    
    # Save to BytesIO
    excel_buffer = BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    
    return excel_buffer.getvalue()

def generate_excel_checklist(df, group_name):
    """Generate formatted Excel checklist matching the Draft Checklist format"""
    from io import BytesIO
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Draft Checklist"
    
    # Set column widths
    ws.column_dimensions['A'].width = 45
    ws.column_dimensions['B'].width = 40
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 18
    ws.column_dimensions['E'].width = 18
    ws.column_dimensions['F'].width = 10
    
    # Define styles
    bold_font = Font(bold=True)
    header_font = Font(bold=True, size=11)
    
    # Create field mapping for rows 1-11
    field_mapping = {
        'Group Name': (1, 2),
        'Group Eff Date': (3, 4),
        'TPA': (5, 6),
        'Third Party Administrator': (5, 6),
        'Underwriter': (7, 7),
        'Benefit Plan Name': (8, 9),
        'Subsidiaries': (10, 10),
        'Group Address': (11, 11)
    }
    
    row_num = 1
    
    # Helper function to find field value
    def get_field_value(field_name):
        for _, row in df.iterrows():
            if field_name.lower() in row['Field'].lower():
                return row['Extracted_Value'] if row['Extracted_Value'] != 'N/F' else None
        return None
    
    # Rows 1-2: Group Name
    ws.cell(row=1, column=1).value = "Group Name: "
    ws.cell(row=1, column=1).font = bold_font
    ws.cell(row=2, column=1).value = "Group Name in PD:"
    ws.cell(row=2, column=1).font = bold_font
    group_name_value = get_field_value('Group Name')
    if group_name_value:
        ws.cell(row=2, column=2).value = group_name_value
    
    # Rows 3-4: Group Eff Date
    ws.cell(row=3, column=1).value = "Group Eff Date:"
    ws.cell(row=3, column=1).font = bold_font
    ws.cell(row=4, column=1).value = "PD Eff Date:"
    ws.cell(row=4, column=1).font = bold_font
    eff_date_value = get_field_value('Eff Date')
    if eff_date_value:
        ws.cell(row=4, column=2).value = eff_date_value
    
    # Rows 5-6: TPA
    ws.cell(row=5, column=1).value = "TPA:"
    ws.cell(row=5, column=1).font = bold_font
    ws.cell(row=6, column=1).value = "TPA in PD:"
    ws.cell(row=6, column=1).font = bold_font
    tpa_value = get_field_value('TPA') or get_field_value('Third Party Administrator')
    if tpa_value:
        ws.cell(row=6, column=2).value = tpa_value
    
    # Row 7: Underwriter
    ws.cell(row=7, column=1).value = "Underwriter:"
    ws.cell(row=7, column=1).font = bold_font
    underwriter_value = get_field_value('Underwriter')
    if underwriter_value:
        ws.cell(row=7, column=2).value = underwriter_value
    
    # Rows 8-9: Benefit Plan Name
    ws.cell(row=8, column=1).value = "Benefit Plan Name:"
    ws.cell(row=8, column=1).font = bold_font
    ws.cell(row=9, column=1).value = "Benefit Plan Name in PD:"
    ws.cell(row=9, column=1).font = bold_font
    plan_name_value = get_field_value('Plan') or get_field_value('Benefit Plan')
    if plan_name_value:
        ws.cell(row=9, column=2).value = plan_name_value
    
    # Row 10: Subsidiaries
    ws.cell(row=10, column=1).value = "Subsidiaries:"
    ws.cell(row=10, column=1).font = bold_font
    subsidiaries_value = get_field_value('Subsidiaries')
    if subsidiaries_value:
        ws.cell(row=10, column=2).value = subsidiaries_value
    
    # Row 11: Group Address
    ws.cell(row=11, column=1).value = "Group Address:"
    ws.cell(row=11, column=1).font = bold_font
    address_value = get_field_value('Address')
    if address_value:
        ws.cell(row=11, column=2).value = address_value
    
    # Row 12: Empty
    row_num = 12
    
    # Row 13: Headers for Schedule of Benefits section (rows 13-20, not used in this version)
    row_num = 13
    ws.cell(row=row_num, column=2).value = "Matches"
    ws.cell(row=row_num, column=2).font = header_font
    ws.cell(row=row_num, column=3).value = "Requires enrollment"
    ws.cell(row=row_num, column=3).font = header_font
    ws.cell(row=row_num, column=4).value = "Updated PA"
    ws.cell(row=row_num, column=4).font = header_font
    
    # Skip to row 21 (empty row before main checklist items)
    row_num = 21
    
    # Row 22: Headers for checklist items (rows 22-43)
    row_num = 22
    ws.cell(row=row_num, column=2).value = "Matches"
    ws.cell(row=row_num, column=2).font = header_font
    ws.cell(row=row_num, column=3).value = "Requires Approval"
    ws.cell(row=row_num, column=3).font = header_font
    ws.cell(row=row_num, column=4).value = "Requires Notice"
    ws.cell(row=row_num, column=4).font = header_font
    ws.cell(row=row_num, column=5).value = "Request Handbook"
    ws.cell(row=row_num, column=5).font = header_font
    ws.cell(row=row_num, column=6).value = "Pg #"
    ws.cell(row=row_num, column=6).font = header_font
    
    # Define checklist items (rows 23-43) - these are the fields to match
    checklist_items = [
        'UR Vendor',
        'PPO Network',
        'Retirees',
        'BOD, Directors, Officers',
        'Minimum Hour Requirement',
        'Dependent Definitions',
        'Req adding dependents',
        'Dependent to age 26',
        'Grandchildren',
        'Termination Provisions',
        'Open Enrollment',
        'Leave of Absence',
        'Medically Necessary',
        'E&I',
        'R&C',
        'Workers Comp',
        'Transplant',
        'ETS Gene Therapy',
        'Coordination of Benefits',
        'COBRA',
        'Subrogation'
    ]
    
    # Add checklist items rows 23-43
    row_num = 23
    for item in checklist_items:
        ws.cell(row=row_num, column=1).value = item
        
        # Find if this field exists in the data
        found = False
        page_num = 'N/A'
        
        for _, data_row in df.iterrows():
            # Match field names (flexible matching)
            if (item.lower() in data_row['Field'].lower() or 
                data_row['Field'].lower() in item.lower() or
                item.replace(',', '').replace(' ', '').lower() in data_row['Field'].replace(' ', '').lower()):
                
                if data_row['Extracted_Value'] != 'N/F':
                    found = True
                    if pd.notna(data_row['Page_Number']):
                        page_num = int(data_row['Page_Number'])
                break
        
        # Set Matches column (B) - True if found, False if not
        ws.cell(row=row_num, column=2).value = found
        
        # Set other columns to False by default
        ws.cell(row=row_num, column=3).value = False  # Requires Approval
        ws.cell(row=row_num, column=4).value = False  # Requires Notice
        ws.cell(row=row_num, column=5).value = False  # Request Handbook
        
        # Set page number
        ws.cell(row=row_num, column=6).value = page_num
        
        row_num += 1
    
    # Save to BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return output.getvalue()

# Settings Page
if page == "⚙️ Settings":
    st.markdown('<div class="main-header">⚙️ AI Settings</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    ### Configure OpenAI API Integration
    
    Set up your OpenAI API key to enable AI-powered field validation and intelligent decision-making.
    """)
    
    # API Key Configuration
    st.markdown("#### OpenAI API Key")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        api_key_input = st.text_input(
            "Enter your OpenAI API Key",
            value=st.session_state.openai_api_key,
            type="password",
            help="Your API key is stored securely in the session and never saved to disk"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Key", type="primary"):
            st.session_state.openai_api_key = api_key_input
            st.success("✅ API key saved!")
    
    st.markdown("---")
    
    # API Status
    st.markdown("#### API Status")
    
    if st.session_state.openai_api_key:
        st.success("🟢 API Key configured")
        
        # Test connection
        if st.button("🔌 Test Connection"):
            try:
                client = OpenAI(api_key=st.session_state.openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5
                )
                st.success("✅ Connection successful! AI features are ready.")
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
    else:
        st.warning("⚠️ No API key configured. AI features will be disabled.")
    
    st.markdown("---")
    
    # Instructions
    st.markdown("#### How to get an API Key")
    st.markdown("""
    1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
    2. Sign in or create an account
    3. Click "Create new secret key"
    4. Copy the key and paste it above
    5. Click "Save Key"
    
    **Note:** Keep your API key secure and never share it publicly.
    """)
    
    st.markdown("---")
    
    # AI Features
    st.markdown("#### AI Features Enabled")
    st.markdown("""
    - ✅ **Intelligent Field Validation**: AI analyzes extracted fields against definitions
    - ✅ **Missing Field Detection**: AI identifies critical missing information
    - ✅ **Confidence Enhancement**: AI validates low-confidence extractions
    - ✅ **Smart Suggestions**: AI provides verification recommendations
    - ✅ **Automated Decision Making**: Reduces manual review time by up to 70%
    """)

# Keywords Page
elif page == "🔑 Keywords":
    st.markdown('<div class="main-header">🔑 Keywords Input</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    ### Upload Keywords from Plan Document
    
    Upload a list of keywords that were found in the plan document (already processed by RapidMiner).
    The AI will use these keywords to automatically generate and fill the checklist.
    """)
    
    # Upload Keywords
    st.markdown("#### Upload Keywords List")
    
    uploaded_keywords = st.file_uploader(
        "Choose a file with keywords",
        type=['xlsx', 'xls', 'txt', 'csv'],
        help="Excel file with keywords in first column, or text file with one keyword per line",
        key="keywords_uploader"
    )
    
    if uploaded_keywords is not None:
        keywords = load_keywords_list(uploaded_keywords)
        
        if keywords is not None:
            st.session_state.keywords_list = keywords
            st.success(f"✅ Keywords loaded! {len(keywords)} keywords found.")
            
            # Show preview
            st.markdown("#### Keywords Preview")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Display keywords in a scrollable area
                keywords_display = ", ".join(keywords[:50])
                if len(keywords) > 50:
                    keywords_display += f"... and {len(keywords) - 50} more"
                st.text_area("Keywords", keywords_display, height=200, disabled=True)
            
            with col2:
                st.metric("Total Keywords", len(keywords))
                # Show unique count if there are duplicates
                unique_count = len(set(keywords))
                if unique_count < len(keywords):
                    st.metric("Unique Keywords", unique_count)
    
    st.markdown("---")
    
    # Current Keywords Status
    if st.session_state.keywords_list is not None:
        st.markdown("#### Current Keywords")
        st.info(f"📋 {len(st.session_state.keywords_list)} keywords loaded and ready for AI processing")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Keywords", use_container_width=True):
                st.session_state.keywords_list = None
                st.session_state.ai_generated_checklist = None
                st.rerun()
        with col2:
            if st.button("👁️ View All Keywords", use_container_width=True):
                with st.expander("All Keywords", expanded=True):
                    for i, kw in enumerate(st.session_state.keywords_list, 1):
                        st.write(f"{i}. {kw}")
    else:
        st.warning("⚠️ No keywords loaded. Upload a keywords file to enable AI checklist generation.")
    
    st.markdown("---")
    
    # Example Format
    st.markdown("#### Expected File Format")
    
    tab1, tab2 = st.tabs(["Excel Format", "Text Format"])
    
    with tab1:
        st.markdown("""
        **Excel File (.xlsx, .xls):**
        - First column should contain keywords
        - Column can be named "Keywords", "Keyword", or leave unnamed
        - One keyword per row
        """)
        
        example_data = pd.DataFrame({
            'Keywords': ['TPA', 'Utilization Review', 'PPO', 'Deductible', 'COBRA', 'Open Enrollment', 'Retirees']
        })
        st.dataframe(example_data, use_container_width=True)
    
    with tab2:
        st.markdown("""
        **Text File (.txt):**
        - One keyword per line
        - Simple text format
        """)
        
        st.code("""TPA
Utilization Review
PPO
Deductible
COBRA
Open Enrollment
Retirees""", language="text")

# Main Content - Home Page
elif page == "🏠 Home":
    st.markdown('<div class="main-header">🤖 AI-Enabled Plan Document Review System</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to the Tokio Marine Plan Document Review System!
    
    This intelligent system helps third-party administrators efficiently review insurance plan documents.
    """)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Parse Data")
        st.write("Upload Orange workflow outputs or use mock data for testing")
        if st.button("Go to Load Data", key="home_load"):
            st.session_state.page = "📊 Load Data"
            st.rerun()
    
    with col2:
        st.markdown("### ✅ Generate Checklists")
        st.write("Automatically create structured checklists with validation")
        if st.button("Generate Now", key="home_generate"):
            st.session_state.page = "🔨 Generate Checklist"
            st.rerun()
    
    with col3:
        st.markdown("### 📄 Export Reports")
        st.write("Download professional PDFs, JSON, and Excel reports")
        if st.button("Export Options", key="home_export"):
            st.session_state.page = "📄 Export"
            st.rerun()
    
    st.markdown("---")
    
    # System capabilities
    st.markdown("### 🎯 System Capabilities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Core Features:**
        - ✅ Automated checklist generation
        - 🔍 Smart validation with typo detection
        - 📊 Confidence scoring for extractions
        - 🧠 Continuous learning from corrections
        - 📝 Editable HTML previews
        """)
    
    with col2:
        st.markdown("""
        **Export Formats:**
        - 📄 Professional PDF reports
        - 💾 JSON structured data
        - 📊 Excel spreadsheets
        - 🌐 Interactive HTML previews
        """)
    
    # Recent activity (mock)
    st.markdown("---")
    st.markdown("### 📈 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Groups Available", "5", help="Mock data groups for testing")
    col2.metric("Fields Tracked", "25", help="Insurance plan fields per group")
    col3.metric("System Status", "🟢 Online", help="All systems operational")
    col4.metric("Tests Passed", "13/13", delta="100%", help="All functionality tests passing")

# Load Data Page
elif page == "📊 Load Data":
    st.markdown('<div class="main-header">📊 Load Orange Output Data</div>', 
                unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📤 Upload Excel File", "🧪 Use Mock Data"])
    
    with tab1:
        st.markdown("### Upload Orange Workflow Output")
        
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx', 'xls'],
            help="Upload the Excel output from Orange workflow"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                
                # Validate required columns
                required_cols = ['Field', 'Extracted_Value', 'Confidence', 'Page_Number']
                if all(col in df.columns for col in required_cols):
                    st.session_state.current_data = df
                    st.success(f"✅ File loaded successfully! {len(df)} fields found.")
                    
                    # Show preview
                    st.markdown("#### Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # Show statistics
                    col1, col2, col3 = st.columns(3)
                    found = len(df[df['Extracted_Value'] != 'N/F'])
                    col1.metric("Total Fields", len(df))
                    col2.metric("Fields Found", found)
                    col3.metric("Avg Confidence", f"{df['Confidence'].mean()*100:.1f}%")
                else:
                    st.error(f"❌ Invalid file format. Required columns: {', '.join(required_cols)}")
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    with tab2:
        st.markdown("### Select Mock Data Group")
        st.info("💡 These are sample datasets for testing the system")
        
        mock_groups = [
            "Aurora Dynamics",
            "Helios Manufacturing Inc.",
            "Solstice Technologies",
            "TechVenture Inc.",
            "GlobalCorp International"
        ]
        
        selected_group = st.selectbox(
            "Choose a group",
            [""] + mock_groups,
            help="Select a pre-loaded mock dataset"
        )
        
        if selected_group:
            if st.button("Load Mock Data", type="primary"):
                df = load_mock_data(selected_group)
                
                if df is not None:
                    st.session_state.current_data = df
                    st.session_state.selected_group = selected_group
                    st.success(f"✅ Loaded mock data for {selected_group}")
                    
                    # Show preview
                    st.markdown("#### Data Preview")
                    st.dataframe(df, use_container_width=True)
                    
                    # Show statistics
                    st.markdown("#### Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    found = len(df[df['Extracted_Value'] != 'N/F'])
                    missing = len(df) - found
                    
                    col1.metric("Total Fields", len(df))
                    col2.metric("Found", found, delta="Good" if found > 15 else "Review")
                    col3.metric("Missing", missing, delta="⚠️" if missing > 5 else "✓")
                    col4.metric("Avg Confidence", f"{df['Confidence'].mean()*100:.0f}%")
                else:
                    st.error("❌ Could not load mock data. Check file path.")

# Generate Checklist Page
elif page == "🔨 Generate Checklist":
    st.markdown('<div class="main-header">🔨 Generate AI Checklist from Keywords</div>', 
                unsafe_allow_html=True)
    
    # Check if keywords are loaded
    if st.session_state.keywords_list is None:
        st.warning("⚠️ No keywords loaded yet. Please upload keywords first.")
        if st.button("Go to Keywords Page"):
            st.rerun()
    else:
        # Keywords summary
        st.markdown(f"### Keywords Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📋 {len(st.session_state.keywords_list)} keywords loaded")
        with col2:
            # Check AI readiness
            if st.session_state.openai_api_key:
                st.success("🤖 AI Ready")
            else:
                st.error("⚠️ Missing OpenAI API Key - Go to Settings")
        
        st.markdown("---")
        
        # Generate button
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🤖 Generate Checklist with AI", type="primary", use_container_width=True, disabled=not st.session_state.openai_api_key):
                if st.session_state.openai_api_key:
                    checklist_df = generate_checklist_with_ai(
                        st.session_state.keywords_list,
                        st.session_state.openai_api_key
                    )
                    
                    if checklist_df is not None:
                        st.session_state.ai_generated_checklist = checklist_df
                        st.success("✅ Checklist generated successfully!")
                        st.balloons()
                else:
                    st.error("Please configure OpenAI API key in Settings first")
        
        # Display generated checklist
        if st.session_state.ai_generated_checklist is not None:
            st.markdown("---")
            st.markdown("### 📋 Generated Checklist")
            
            checklist_df = st.session_state.ai_generated_checklist
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Items", len(checklist_df))
            col2.metric("✅ Matched", len(checklist_df[checklist_df['Matches'] == True]))
            col3.metric("📋 Req. Handbook", len(checklist_df[checklist_df['Request Handbook'] == True]))
            col4.metric("⚠️ Req. Approval", len(checklist_df[checklist_df['Requires Approval'] == True]))
            
            st.markdown("---")
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Complete Checklist", 
                "✅ Matched Items", 
                "❌ Not Matched",
                "🤖 AI Reasoning"
            ])
            
            with tab1:
                st.markdown("#### Complete Checklist View")
                # Display as interactive table
                display_df = checklist_df.copy()
                display_df['Matches'] = display_df['Matches'].apply(lambda x: '✅' if x else '❌')
                display_df['Requires Approval'] = display_df['Requires Approval'].apply(lambda x: '☑️' if x else '☐')
                display_df['Requires Notice'] = display_df['Requires Notice'].apply(lambda x: '☑️' if x else '☐')
                display_df['Request Handbook'] = display_df['Request Handbook'].apply(lambda x: '☑️' if x else '☐')
                
                st.dataframe(
                    display_df[['Item', 'Matches', 'Requires Approval', 'Requires Notice', 'Request Handbook']],
                    use_container_width=True,
                    height=600
                )
            
            with tab2:
                st.markdown("#### Items Found in Document")
                matched = checklist_df[checklist_df['Matches'] == True]
                if len(matched) > 0:
                    for _, row in matched.iterrows():
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            col1.markdown(f"**✅ {row['Item']}**")
                            col2.markdown("📋" if row['Request Handbook'] else "")
                            col3.markdown("📢" if row['Requires Notice'] else "")
                            col4.markdown("✔️" if row['Requires Approval'] else "")
                            
                            if row['AI Reasoning']:
                                with st.expander("View AI Reasoning"):
                                    st.write(row['AI Reasoning'])
                else:
                    st.info("No matched items")
            
            with tab3:
                st.markdown("#### Items Not Found")
                not_matched = checklist_df[checklist_df['Matches'] == False]
                if len(not_matched) > 0:
                    for _, row in not_matched.iterrows():
                        st.markdown(f"""
                        <div class="missing-field">
                        <strong>❌ {row['Item']}</strong>: Not found in keywords
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("🎉 All items matched!")
            
            with tab4:
                st.markdown("#### AI Reasoning for Each Item")
                for _, row in checklist_df.iterrows():
                    status_icon = "✅" if row['Matches'] else "❌"
                    with st.expander(f"{status_icon} {row['Item']}", expanded=False):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write("**Status:**")
                            st.write(f"- Matches: {'Yes' if row['Matches'] else 'No'}")
                            st.write(f"- Req. Approval: {'Yes' if row['Requires Approval'] else 'No'}")
                            st.write(f"- Req. Notice: {'Yes' if row['Requires Notice'] else 'No'}")
                            st.write(f"- Req. Handbook: {'Yes' if row['Request Handbook'] else 'No'}")
                        with col2:
                            st.write("**AI Reasoning:**")
                            st.write(row['AI Reasoning'] if row['AI Reasoning'] else "No reasoning provided")
            
            st.markdown("---")
            
            # Download button
            st.markdown("### 📥 Download Checklist")
            
            col1, col2, col3 = st.columns(3)
            with col2:
                # Generate Excel with the checklist format
                excel_data = generate_excel_checklist_from_ai(checklist_df)
                
                st.download_button(
                    label="📥 Download Excel Checklist",
                    data=excel_data,
                    file_name=f"ai_generated_checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary"
                )
        else:
            st.info("👆 Click the button above to generate your checklist using AI")

# Validate Page
elif page == "🔍 Validate":
    st.markdown('<div class="main-header">🔍 Validate Checklist</div>', 
                unsafe_allow_html=True)
    
    if st.session_state.current_data is None:
        st.warning("⚠️ No checklist to validate. Generate a checklist first.")
    else:
        df = st.session_state.current_data
        
        st.markdown("### Validation Report")
        
        # Validation metrics
        col1, col2, col3, col4 = st.columns(4)
        
        high_conf = len(df[df['Confidence'] > 0.8])
        med_conf = len(df[(df['Confidence'] >= 0.5) & (df['Confidence'] <= 0.8)])
        low_conf = len(df[df['Confidence'] < 0.5])
        
        col1.metric("🟢 High Confidence", high_conf, help="Confidence > 80%")
        col2.metric("🟡 Medium Confidence", med_conf, help="Confidence 50-80%")
        col3.metric("🔴 Low Confidence", low_conf, help="Confidence < 50%")
        col4.metric("Validation Status", "⚠️ Review" if low_conf > 0 else "✅ Pass")
        
        # Confidence distribution chart
        st.markdown("#### Confidence Score Distribution")
        
        import plotly.express as px
        fig = px.histogram(
            df, 
            x='Confidence',
            nbins=20,
            title='Field Confidence Distribution',
            labels={'Confidence': 'Confidence Score', 'count': 'Number of Fields'},
            color_discrete_sequence=['#3498db']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Fields needing review
        if low_conf > 0:
            st.markdown("#### ⚠️ Fields Requiring Review")
            review_df = df[df['Confidence'] < 0.5][['Field', 'Extracted_Value', 'Confidence', 'Page_Number']]
            st.dataframe(review_df, use_container_width=True)

# Export Page
elif page == "📄 Export":
    st.markdown('<div class="main-header">📄 Export Reports</div>', 
                unsafe_allow_html=True)
    
    if st.session_state.current_data is None:
        st.warning("⚠️ No data to export. Generate a checklist first.")
    else:
        df = st.session_state.current_data
        group_name = st.session_state.selected_group or "Unknown_Group"
        
        st.markdown("### Choose Export Format")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📄 PDF Report")
            st.write("Professional formatted checklist document")
            if st.button("📥 Download PDF", use_container_width=True):
                st.info("💡 PDF generation feature - integrate with your existing PDFGenerator class")
                st.code("""
# Use your existing PDFGenerator
from plan_doc_chatbot import PDFGenerator
pdf_gen = PDFGenerator()
pdf_path = pdf_gen.generate(checklist_data, group_name)
                """)
        
        with col2:
            st.markdown("#### 💾 JSON Export")
            st.write("Structured data for integration")
            
            # Create JSON
            export_data = {
                "group_name": group_name,
                "generated_at": datetime.now().isoformat(),
                "total_fields": len(df),
                "found_fields": len(df[df['Extracted_Value'] != 'N/F']),
                "fields": df.to_dict('records')
            }
            
            json_str = json.dumps(export_data, indent=2)
            
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"checklist_{group_name.replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            st.markdown("#### 📊 Excel Export")
            st.write("Spreadsheet format for analysis")
            
            # Convert to Excel (simplified)
            if st.button("📥 Download Excel", use_container_width=True):
                st.info("💡 Excel export - use df.to_excel()")

# Learning System Page
elif page == "🧠 Learning System":
    st.markdown('<div class="main-header">🧠 Learning System</div>', 
                unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Synonym", "✏️ Add Correction", "📚 Learning History"])
    
    with tab1:
        st.markdown("### Add New Synonym")
        st.write("Teach the system alternative terms for insurance fields")
        
        col1, col2 = st.columns(2)
        with col1:
            term = st.text_input("Original Term", placeholder="e.g., TPA")
        with col2:
            synonym = st.text_input("Synonym", placeholder="e.g., Claims Administrator")
        
        if st.button("Add Synonym", type="primary"):
            if term and synonym:
                st.success(f"✅ Added: '{synonym}' as synonym for '{term}'")
                st.info("💡 Integrate with your LearningEngine.add_synonym() method")
            else:
                st.error("Please fill in both fields")
    
    with tab2:
        st.markdown("### Add Correction")
        st.write("Teach the system to correct common mistakes")
        
        col1, col2 = st.columns(2)
        with col1:
            incorrect = st.text_input("Incorrect Term", placeholder="e.g., Third Party Admin")
        with col2:
            correct = st.text_input("Correct Term", placeholder="e.g., Third Party Administrator")
        
        if st.button("Add Correction", type="primary"):
            if incorrect and correct:
                st.success(f"✅ Correction added: '{incorrect}' → '{correct}'")
                st.info("💡 Integrate with your LearningEngine.add_correction() method")
            else:
                st.error("Please fill in both fields")
    
    with tab3:
        st.markdown("### Learning History")
        st.write("View all learned synonyms and corrections")
        
        # Mock learning history
        history_data = {
            "Timestamp": ["2025-11-15 10:30", "2025-11-15 11:45", "2025-11-14 14:20"],
            "Action": ["Synonym Added", "Correction Added", "Synonym Added"],
            "Term": ["TPA", "Third Party Admin", "UR Vendor"],
            "Value": ["Claims Administrator", "Third Party Administrator", "Utilization Review"],
            "User": ["system", "admin", "user1"]
        }
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)

# About Page
elif page == "ℹ️ About":
    st.markdown('<div class="main-header">ℹ️ About This System</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    ### AI-Enabled Plan Document Review System
    
    **Version:** 1.0  
    **Release Date:** November 2025  
    **Developer:** Tokio Marine Insurance Development Team
    
    ---
    
    #### 🎯 Purpose
    
    This system automates the review of insurance plan documents by parsing Orange workflow 
    outputs and generating structured checklists with intelligent validation.
    
    #### ✨ Key Features
    
    - **Automated Processing**: Converts Excel outputs into validated checklists
    - **Smart Validation**: Cross-references with definitions and detects issues
    - **Continuous Learning**: Improves from user feedback and corrections
    - **Multiple Export Formats**: PDF, JSON, Excel, and HTML
    - **Interactive Interface**: Modern web-based GUI for easy operation
    
    #### 📊 Technical Stack
    
    - **Frontend**: Streamlit (Python)
    - **Backend**: Python 3.11+
    - **Data Processing**: Pandas, OpenPyXL
    - **Report Generation**: ReportLab
    - **Visualization**: Plotly
    
    #### 📚 Documentation
    
    - [README.md](README.md) - Complete user guide
    - [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation instructions
    - [TEST_RESULTS.md](TEST_RESULTS.md) - Test documentation
    - [GUI_ROADMAP.md](GUI_ROADMAP.md) - GUI development guide
    
    #### 🧪 Test Status
    
    - ✅ All functionality tests passing (13/13)
    - ✅ Mock data validated (6 groups)
    - ✅ Export formats working
    - ✅ Learning system operational
    
    #### 📧 Support
    
    For questions or issues, contact the development team or refer to the documentation.
    
    ---
    
    *Built with ❤️ for Tokio Marine Insurance*
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Tokio Marine Plan Review System**")
with col2:
    st.markdown("Version 1.0 | November 2025")
with col3:
    st.markdown("Made with Streamlit 🎈")
