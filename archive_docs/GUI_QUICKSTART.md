# 🚀 GUI Quick Start Guide

## Get Your GUI Running in 5 Minutes!

### Step 1: Install Streamlit (1 minute)

```bash
cd "/Users/belen/Desktop/IS 4880 Capstone/TokioMarineChatbot"

# Install Streamlit and Plotly
pip3 install streamlit plotly
```

### Step 2: Launch the GUI (30 seconds)

```bash
# Run the Streamlit app
streamlit run streamlit_app.py
```

Your browser will automatically open to `http://localhost:8501` 🎉

### Step 3: Explore the Interface

**The GUI includes:**
- 🏠 **Home Page** - Overview and quick actions
- 📊 **Load Data** - Upload Excel or use mock data
- 🔨 **Generate Checklist** - Create validated checklists
- 🔍 **Validate** - Review confidence scores and issues
- 📄 **Export** - Download PDF, JSON, or Excel
- 🧠 **Learning System** - Add synonyms and corrections
- ℹ️ **About** - System information

---

## 🎯 Quick Demo Flow

### Try This (2 minutes):

1. **Launch the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Load mock data:**
   - Click "📊 Load Data" in sidebar
   - Go to "🧪 Use Mock Data" tab
   - Select "Aurora Dynamics"
   - Click "Load Mock Data"

3. **Generate checklist:**
   - Click "🔨 Generate Checklist" in sidebar
   - Click "🔨 Generate Checklist" button
   - Watch the progress bar!

4. **View results:**
   - See the interactive checklist with all fields
   - Check the validation metrics
   - Browse found/missing fields tabs

5. **Export data:**
   - Click "📄 Export" in sidebar
   - Download JSON data

---

## 📸 What You'll See

### Home Page
```
🤖 AI-Enabled Plan Document Review System
┌─────────────┬─────────────┬─────────────┐
│ Parse Data  │ Generate    │ Export      │
│ Upload or   │ Create      │ Download    │
│ use mocks   │ checklists  │ reports     │
└─────────────┴─────────────┴─────────────┘
```

### Checklist Page
```
🔨 Generate Checklist
┌────────────┬────────────┬────────────┬────────────┐
│ Total: 25  │ Found: 21  │ Missing: 4 │ Conf: 72%  │
└────────────┴────────────┴────────────┴────────────┘

✅ Group Name: Aurora Dynamics (95%)
✅ TPA: BluePeak Benefits (90%)
❌ Some Field: Not found
```

---

## 🛠️ Customization Options

### Change Colors
Edit `streamlit_app.py`, find the CSS section:

```python
st.markdown("""
<style>
    .stButton>button {
        background-color: #YOUR_COLOR;  # Change this!
    }
</style>
""")
```

### Add Your Logo
```python
st.image("your_logo.png", width=200)
```

### Change Layout
```python
# Wide layout (default)
st.set_page_config(layout="wide")

# Centered layout
st.set_page_config(layout="centered")
```

---

## 🔗 Integration with Your Existing Code

### Connect to Your Classes

The Streamlit app is **already set up** to use your existing classes. Just uncomment these lines:

```python
# In streamlit_app.py, add at the top:
from plan_doc_chatbot import (
    LearningEngine,
    DefinitionsParser,
    Validator,
    OrangeOutputParser,
    ChecklistGenerator,
    PDFGenerator
)

# Then use them:
learning_engine = LearningEngine()
validator = Validator()
# etc.
```

### Example: Add Real PDF Export

Replace the placeholder in the Export page:

```python
# Find this in the Export page section:
if st.button("📥 Download PDF"):
    # Replace with:
    pdf_gen = PDFGenerator()
    pdf_path = pdf_gen.generate_pdf(
        checklist_data, 
        f"checklist_{group_name}.pdf"
    )
    
    with open(pdf_path, "rb") as f:
        st.download_button(
            "📥 Download PDF",
            f,
            file_name=f"checklist_{group_name}.pdf",
            mime="application/pdf"
        )
```

---

## 🎨 Next Enhancement Ideas

### 1. Add Charts (5 minutes)
```python
import plotly.express as px

fig = px.pie(
    values=[found, missing],
    names=['Found', 'Missing'],
    title='Field Status'
)
st.plotly_chart(fig)
```

### 2. Add File History (10 minutes)
```python
if 'upload_history' not in st.session_state:
    st.session_state.upload_history = []

# Track uploads
st.session_state.upload_history.append({
    'filename': uploaded_file.name,
    'timestamp': datetime.now(),
    'fields': len(df)
})

# Display
st.dataframe(st.session_state.upload_history)
```

### 3. Add Real-time Validation (15 minutes)
```python
# As user edits fields
edited_value = st.text_input("Edit value", value=current_value)

if edited_value != current_value:
    # Run validation
    validator.validate_field(field_name, edited_value)
    st.success("✅ Value updated and validated!")
```

---

## 🚀 Deploy to the Internet (Optional)

### Free Deployment on Streamlit Cloud

1. **Push code to GitHub:**
   ```bash
   git add streamlit_app.py requirements.txt
   git commit -m "Add Streamlit GUI"
   git push origin main
   ```

2. **Deploy:**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with GitHub
   - Click "New app"
   - Select your repo
   - Choose `streamlit_app.py`
   - Click "Deploy"!

3. **Share:**
   - Get a public URL like: `your-app.streamlit.app`
   - Share with your team!

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill existing Streamlit
pkill -f streamlit

# Or use different port
streamlit run streamlit_app.py --server.port 8502
```

### Modules Not Found
```bash
# Install all requirements
pip3 install -r requirements.txt
```

### App Not Auto-Opening
```bash
# Manually open
open http://localhost:8501
```

### Hot Reload Not Working
- Save your file (Cmd+S)
- Click "Rerun" in top-right of app
- Or enable "Always rerun" in settings (⋮ menu)

---

## 📚 Learn More

### Streamlit Documentation
- **Cheat Sheet:** https://docs.streamlit.io/library/cheatsheet
- **API Reference:** https://docs.streamlit.io/library/api-reference
- **Gallery:** https://streamlit.io/gallery

### Tutorials
- **30 Days of Streamlit:** https://30days.streamlit.app
- **Video Tutorials:** Search "Streamlit tutorial" on YouTube

---

## 💡 Pro Tips

1. **Auto-reload on save:** The app automatically reloads when you save changes!

2. **Debug with st.write():** Use `st.write(variable)` to inspect values

3. **Session state is your friend:** Store data between reruns:
   ```python
   st.session_state.my_data = data
   ```

4. **Use columns for layout:** 
   ```python
   col1, col2 = st.columns(2)
   with col1:
       st.write("Left side")
   with col2:
       st.write("Right side")
   ```

5. **Cache expensive operations:**
   ```python
   @st.cache_data
   def load_big_file():
       return pd.read_excel("big_file.xlsx")
   ```

---

## ✅ Success Checklist

- [ ] Streamlit installed
- [ ] `streamlit run streamlit_app.py` works
- [ ] App opens in browser
- [ ] Can load mock data
- [ ] Can generate checklist
- [ ] Can navigate between pages
- [ ] Can export JSON

**All checked?** 🎉 **You're ready to customize!**

---

## 🎯 What's Next?

1. **Today:** Run the app and explore
2. **This week:** Customize colors and layout
3. **Next week:** Integrate with your existing classes
4. **Next month:** Deploy to Streamlit Cloud

**Need help?** Check the [GUI_ROADMAP.md](GUI_ROADMAP.md) for detailed guidance!

---

*Happy building! 🚀*
