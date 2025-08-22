# CitizenGate Configuration File
# Customize your application settings here

# Application Metadata
APP_CONFIG = {
    "title": "CitizenGate - Government Service Management",
    "version": "2.1.0",
    "description": "Advanced Government Service Management & Analytics Platform",
    "icon": "🏛️",
    "layout": "wide"
}

# Color Theme
COLORS = {
    "primary": "#3498db",
    "secondary": "#2c3e50", 
    "success": "#2ecc71",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40"
}

# Navigation Configuration
NAVIGATION = {
    "🏠 Home": {
        "file": "Home",
        "description": "Main dashboard and overview"
    },
    "✅ Service Completion": {
        "file": "1_Service_Completion",
        "description": "Track and manage service completion processes"
    },
    "👥 Staff Requirement": {
        "file": "2_Staff_Requirement", 
        "description": "Workforce management and planning"
    }
}

# Feature Flags
FEATURES = {
    "ai_predictions": True,
    "workforce_forecasting": True,
    "real_time_analytics": True,
    "advanced_reporting": True,
    "mobile_responsive": True,
    "dark_mode": False  # Future feature
}

# Data Configuration
DATA_CONFIG = {
    "tasks_file": "data/final_tasks.csv",
    "staffing_file": "data/staffing_train.csv",
    "refresh_interval": 300,  # seconds
    "cache_duration": 3600    # seconds
}

# UI Settings
UI_SETTINGS = {
    "show_welcome_splash": True,
    "enable_animations": True,
    "sidebar_collapsed": False,
    "theme": "professional"  # professional, minimal, colorful
}

# Performance Settings
PERFORMANCE = {
    "max_data_rows": 10000,
    "chart_max_points": 1000,
    "prediction_cache_size": 100
}
