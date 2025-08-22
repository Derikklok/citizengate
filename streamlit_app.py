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

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    .css-1aumxhk {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        color: white;
    }
    
    /* Sidebar text styling */
    .css-1aumxhk .css-1v0mbdj {
        color: white !important;
    }
    
    .css-1aumxhk .css-10trblm {
        color: #ecf0f1 !important;
    }
    
    /* Logo and branding */
    .sidebar-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: rgba(52, 73, 94, 0.3);
        border-radius: 10px;
        border: 2px solid #3498db;
    }
    
    .logo-text {
        font-size: 24px;
        font-weight: 700;
        color: #3498db !important;
        text-align: center;
        margin: 0;
    }
    
    .logo-subtitle {
        font-size: 12px;
        color: #bdc3c7 !important;
        text-align: center;
        margin: 0;
        font-weight: 400;
    }
    
    /* Navigation styling */
    .nav-section {
        margin: 1.5rem 0;
        padding: 1rem;
        background: rgba(52, 73, 94, 0.2);
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }
    
    .nav-title {
        color: #3498db !important;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 1rem;
    }
    
    /* Quick links styling */
    .quick-link {
        color: #ecf0f1 !important;
        text-decoration: none;
        padding: 0.5rem 0;
        margin: 0.25rem 0;
        display: block;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .quick-link:hover {
        background: rgba(52, 152, 219, 0.2);
        padding-left: 1rem;
        color: #3498db !important;
    }
    
    /* Main content header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: #7f8c8d;
        line-height: 1.6;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-left: 0.5rem;
    }
    
    .status-online {
        background: #2ecc71;
        color: white;
    }
    
    .status-maintenance {
        background: #f39c12;
        color: white;
    }
    
    /* Footer */
    .app-footer {
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        border-radius: 12px;
        text-align: center;
    }
    
    /* Navigation selectbox styling */
    .stSelectbox > div > div {
        background-color: rgba(52, 73, 94, 0.8);
        border: 2px solid #3498db;
        border-radius: 8px;
        color: white;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .feature-card {
            margin-bottom: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    # Logo and branding
    st.markdown("""
    <div class="sidebar-logo">
        <div>
            <div class="logo-text">🏛️ CitizenGate</div>
            <div class="logo-subtitle">Government Service Management</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation section
    st.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.markdown('<div class="nav-title">🧭 Navigation</div>', unsafe_allow_html=True)
    
    # Navigation menu
    pages = {
        "🏠 Home": "Home",
        "✅ Service Completion": "1_Service_Completion", 
        "👥 Staff Requirement": "2_Staff_Requirement"
    }
    
    # Handle programmatic navigation
    nav_index = 0
    if 'programmatic_nav' in st.session_state:
        target_page = st.session_state.programmatic_nav
        if target_page in pages.keys():
            nav_index = list(pages.keys()).index(target_page)
        del st.session_state.programmatic_nav
    
    selected_page = st.selectbox(
        "Navigate to:",
        list(pages.keys()),
        index=nav_index,
        key="navigation"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System status
    st.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.markdown('<div class="nav-title">📊 System Status</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #ecf0f1;">
        • Service Completion <span class="status-indicator status-online">Online</span><br>
        • Staff Management <span class="status-indicator status-online">Online</span><br>
        • Data Analytics <span class="status-indicator status-online">Online</span><br>
        • Forecasting <span class="status-indicator status-online">Online</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick links
    st.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.markdown('<div class="nav-title">🔗 Quick Links</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="quick-link">📊 Live Dashboard</div>
    <div class="quick-link">📋 Generate Reports</div>
    <div class="quick-link">🔮 AI Predictions</div>
    <div class="quick-link">⚙️ System Settings</div>
    <div class="quick-link">💡 Help & Support</div>
    <div class="quick-link">📱 Mobile App</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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

# Show welcome message on first load
if 'first_load' not in st.session_state:
    st.session_state.first_load = True
    st.balloons()

# Load the selected page
page_to_load = pages[selected_page]
load_page(page_to_load)
