import streamlit as st
import importlib.util
import sys
from pathlib import Path

# Configure page settings
st.set_page_config(
    page_title="CitizenGate",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional sidebar styling
st.markdown("""
<style>
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Sidebar header */
    .css-1lcbmhc {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Navigation menu styling */
    .stSelectbox > div > div {
        background-color: #1A1A1A;
        border: 1px solid #ddd;
        border-radius: 8px;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom navigation styling */
    .nav-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid #3498db;
    }
    
    .nav-item {
        padding: 0.5rem 0;
        margin: 0.2rem 0;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        background-color: #e8f4fd;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown('<div class="nav-header">🏛️ CitizenGate</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation menu
    pages = {
        "🏠 Home": "Home",
        "✅ Service Completion": "1_Service_Completion", 
        "👥 Staff Requirement": "2_Staff_Requirement"
    }
    
    selected_page = st.selectbox(
        "Navigate to:",
        list(pages.keys()),
        index=0,
        key="navigation"
    )
    
    st.markdown("---")
    st.markdown("### Quick Links")
    st.markdown("- 📊 Dashboard")
    st.markdown("- 📋 Reports") 
    st.markdown("- ⚙️ Settings")
    st.markdown("- 💡 Help")

# Function to load and execute page modules
def load_page(page_name):
    try:
        if page_name == "Home":
            # Load Home.py from root directory
            spec = importlib.util.spec_from_file_location("home", "Home.py")
            if spec and spec.loader:
                home_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(home_module)
        else:
            # Load pages from pages directory
            page_file = f"pages/{page_name}.py"
            if Path(page_file).exists():
                spec = importlib.util.spec_from_file_location(page_name, page_file)
                if spec and spec.loader:
                    page_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(page_module)
            else:
                st.error(f"Page {page_file} not found!")
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")

# Load the selected page
page_to_load = pages[selected_page]
load_page(page_to_load)
