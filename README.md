# �️ CitizenGate - Government Service Management Platform

**Advanced AI-Powered Government Service Management & Analytics Platform**

CitizenGate is a comprehensive digital solution designed to streamline government service delivery through intelligent automation, data-driven insights, and predictive analytics.

[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](https://github.com/your-repo/citizengate)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## 🚀 Key Features

### 📊 Service Completion Management
- **Real-time Tracking**: Monitor service requests across all government sections
- **Performance Analytics**: Comprehensive dashboards with KPIs and metrics
- **Task Management**: Track individual tasks and completion rates
- **Quality Assurance**: Monitor service quality and citizen satisfaction

### 🔮 AI-Powered Predictions
- **Processing Time Prediction**: ML algorithms predict service completion times
- **Confidence Intervals**: Statistical reliability measures for predictions
- **Historical Analysis**: Pattern recognition from historical data
- **Trend Forecasting**: Predict future workload and resource needs

### 👥 Workforce Management
- **Staff Optimization**: Intelligent workforce allocation across sections
- **Workload Analysis**: Analyze employee efficiency and section performance
- **Demand Forecasting**: Predict staffing requirements for any given date
- **Performance Insights**: Identify top-performing sections and practices

### 📈 Advanced Analytics
- **Interactive Dashboards**: Real-time visualizations and charts
- **Custom Reports**: Generate detailed performance reports
- **Data Export**: Export analytics data for further analysis
- **Trend Analysis**: Identify patterns and optimization opportunities

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python-based web framework)
- **Backend**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (time series prediction)
- **Visualization**: Streamlit charts, Plotly
- **Styling**: Custom CSS with responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/citizengate.git
   cd citizengate
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Access the application**
   - Open your browser to `http://localhost:8501`
   - The application will launch with the welcome screen

## 📊 Data Sources

### Tasks Data (`final_tasks.csv`)
Contains 19 different passport service tasks across 6 sections:
- **SEC-001**: First-time Passport Applications
- **SEC-002**: Renewals  
- **SEC-003**: Corrections & Amendments
- **SEC-004**: Lost/Stolen Passport Reissue
- **SEC-005**: Document Verification
- **SEC-006**: Special Cases

### Staffing Data (`staffing_train.csv`)
Historical staffing data with 5,800+ records including:
- `date`: Service date (YYYY-MM-DD)
- `section_id`: Government section identifier
- `employees_on_duty`: Number of staff members working
- `total_task_time_minutes`: Total task processing time

## 🔮 AI/ML Features

### Time Prediction Model
- **Input**: Task ID, Service type, Peak hours, Special factors
- **Output**: Predicted processing time with confidence interval
- **Algorithm**: Regression model with historical pattern analysis

### Workforce Forecasting
- **Input**: Target date, Section ID
- **Output**: Recommended number of employees
- **Features**: Weekday patterns, Monthly seasonality, Workload factors

---

**Made with ❤️ for efficient government service delivery**

*CitizenGate - Transforming government services through technology*
