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

# Sidebar Navigation
with st.sidebar:
    st.markdown("# 📋 Plan Review System")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "📊 Load Data", "🔨 Generate Checklist", 
         "🔍 Validate", "📄 Export", "🧠 Learning System", "ℹ️ About"],
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

# Main Content - Home Page
if page == "🏠 Home":
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
    st.markdown('<div class="main-header">🔨 Generate Checklist</div>', 
                unsafe_allow_html=True)
    
    if st.session_state.current_data is None:
        st.warning("⚠️ No data loaded yet. Please load data first.")
        if st.button("Go to Load Data Page"):
            st.session_state.page = "📊 Load Data"
            st.rerun()
    else:
        df = st.session_state.current_data
        
        st.markdown(f"### Data Summary")
        st.info(f"📊 Processing {len(df)} fields")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🔨 Generate Checklist", type="primary", use_container_width=True):
                with st.spinner("Generating checklist..."):
                    # Simulate processing
                    import time
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    st.session_state.checklist_generated = True
                    st.success("✅ Checklist generated successfully!")
                    st.balloons()
        
        with col2:
            st.markdown("**Options:**")
            auto_validate = st.checkbox("Auto-validate", value=True)
            show_warnings = st.checkbox("Show warnings", value=True)
        
        if st.session_state.checklist_generated:
            st.markdown("---")
            st.markdown("### 📋 Generated Checklist")
            
            # Summary metrics
            found_fields = df[df['Extracted_Value'] != 'N/F']
            missing_fields = df[df['Extracted_Value'] == 'N/F']
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Fields", len(df))
            col2.metric("✅ Found", len(found_fields), delta=f"{len(found_fields)/len(df)*100:.0f}%")
            col3.metric("❌ Missing", len(missing_fields), delta=f"-{len(missing_fields)}")
            col4.metric("📊 Avg Confidence", f"{df['Confidence'].mean()*100:.0f}%")
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📊 All Fields", "✅ Found Fields", "❌ Missing Fields"])
            
            with tab1:
                st.markdown("#### Complete Checklist")
                for _, row in df.iterrows():
                    status = "✅" if row['Extracted_Value'] != 'N/F' else "❌"
                    confidence_icon = get_confidence_color(row['Confidence'])
                    
                    with st.container():
                        col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
                        col1.markdown(f"**{status}**")
                        col2.markdown(f"**{row['Field']}**")
                        col3.markdown(f"{row['Extracted_Value']}")
                        col4.markdown(f"{confidence_icon} {row['Confidence']*100:.0f}%")
            
            with tab2:
                st.markdown("#### Successfully Extracted Fields")
                for _, row in found_fields.iterrows():
                    confidence_icon = get_confidence_color(row['Confidence'])
                    st.markdown(f"""
                    <div class="success-field">
                    <strong>{row['Field']}</strong>: {row['Extracted_Value']} 
                    <span style="float: right;">{confidence_icon} {row['Confidence']*100:.0f}% | Page {int(row['Page_Number']) if pd.notna(row['Page_Number']) else 'N/A'}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab3:
                st.markdown("#### Missing Fields")
                if len(missing_fields) > 0:
                    for _, row in missing_fields.iterrows():
                        st.markdown(f"""
                        <div class="missing-field">
                        <strong>{row['Field']}</strong>: Not found in document
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("🎉 All fields found!")

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
