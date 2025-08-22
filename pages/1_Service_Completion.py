import streamlit as st
import pandas as pd
import importlib.util
import sys
from pathlib import Path
import random
from datetime import datetime, timedelta

# Function to load tasks data from CSV file
def load_tasks_data():
    """Load tasks data from CSV file"""
    try:
        data_path = Path(__file__).parent.parent / "data" / "final_tasks.csv"
        if data_path.exists():
            return pd.read_csv(data_path)
        else:
            st.error("Tasks data file not found!")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading tasks data: {str(e)}")
        return pd.DataFrame()

# Function to generate sample request data based on real tasks
def generate_sample_requests(tasks_df):
    """Generate sample request data using real tasks - only showing required fields"""
    if tasks_df.empty:
        return pd.DataFrame()
    
    # Sample request IDs and statuses
    request_ids = [f"REQ-{str(i).zfill(3)}" for i in range(1, 11)]
    statuses = ["🔄 In Progress", "👀 Under Review", "💳 Pending Payment", "✅ Completed", "⏳ Pending"]
    
    # Generate sample data with only required fields
    sample_requests = []
    for req_id in request_ids:
        # Random task selection
        task = tasks_df.sample(1).iloc[0]
        
        # Generate realistic dates
        submitted_date = datetime.now().date() - timedelta(days=random.randint(1, 30))
        completion_date = submitted_date + timedelta(days=random.randint(3, 15))
        
        # Estimate processing time based on task complexity
        base_times = {
            'TASK-001': 45, 'TASK-002': 30, 'TASK-003': 35, 'TASK-004': 25, 'TASK-005': 40,
            'TASK-006': 50, 'TASK-007': 35, 'TASK-008': 40, 'TASK-009': 45, 'TASK-010': 30,
            'TASK-011': 50, 'TASK-012': 90, 'TASK-013': 25, 'TASK-014': 35, 'TASK-015': 45,
            'TASK-016': 120, 'TASK-017': 60, 'TASK-018': 75, 'TASK-019': 90
        }
        
        predicted_time = base_times.get(task['task_id'], 45) + random.randint(-10, 20)
        
        sample_requests.append({
            'Request ID': req_id,
            'Task ID': task['task_id'],
            'Task Name': task['task_name'],
            'Section ID': task['section_id'],
            'Section Name': task['section_name'],
            'Status': random.choice(statuses),
            'Submitted': submitted_date.strftime('%Y-%m-%d'),
            'Expected Completion': completion_date.strftime('%Y-%m-%d'),
            'Predicted Time': f"{predicted_time} min"
        })
    
    return pd.DataFrame(sample_requests)

# Function to get task statistics
def get_task_statistics(tasks_df):
    """Generate statistics from tasks data"""
    if tasks_df.empty:
        return {}
    
    total_tasks = len(tasks_df)
    sections = tasks_df['section_name'].nunique()
    
    # Simulate some metrics
    total_requests = random.randint(150, 200)
    completed = int(total_requests * 0.85)
    in_progress = int(total_requests * 0.12)
    pending = total_requests - completed - in_progress
    avg_processing = random.randint(50, 80)
    
    return {
        'total_tasks': total_tasks,
        'sections': sections,
        'total_requests': total_requests,
        'completed': completed,
        'in_progress': in_progress,
        'pending': pending,
        'avg_processing': avg_processing
    }

# Function to load time predictor component
def load_time_predictor():
    """Load time predictor functions from the components directory"""
    try:
        # Get the path to the time predictor component
        predictor_path = Path(__file__).parent.parent / "components" / "time_predictor.py"
        
        if predictor_path.exists():
            # Load the predictor module
            spec = importlib.util.spec_from_file_location("time_predictor", predictor_path)
            predictor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(predictor_module)
            
            return predictor_module.show_prediction_interface
        else:
            # Fallback function if predictor file doesn't exist
            def show_prediction_interface():
                st.info("Time prediction functionality is being loaded...")
            
            return show_prediction_interface
            
    except Exception as e:
        st.error(f"Error loading time predictor: {str(e)}")
        
        # Fallback function
        def show_prediction_interface():
            st.info("Time prediction functionality is being loaded...")
        
        return show_prediction_interface

# Load components and data
show_prediction_interface = load_time_predictor()
tasks_df = load_tasks_data()
stats = get_task_statistics(tasks_df)
sample_requests_df = generate_sample_requests(tasks_df)

# Page header with action button
st.markdown("""
<div class="main-header">
    <div class="header-title">⚡ Service Completion Dashboard</div>
    <div class="header-subtitle">Real-time service tracking and AI-powered time predictions</div>
</div>
""", unsafe_allow_html=True)

header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown("#### 📊 Comprehensive service management with predictive analytics")

with header_col2:
    if st.button("🔮 Predict Time", key="predict_time_btn", use_container_width=True, type="primary"):
        st.session_state.show_predictor = not st.session_state.get('show_predictor', False)

# Show time predictor if toggled
if st.session_state.get('show_predictor', False):
    with st.expander("⏱️ Service Processing Time Predictor", expanded=True):
        show_prediction_interface("prediction_form_expander")
    
    # Add a button to go back to the main dashboard
    if st.button("🔙 Back to Dashboard", key="back_to_dashboard", use_container_width=True):
        st.session_state.show_predictor = False
        st.rerun()
    
    # Stop execution here to hide the rest of the content
    st.stop()

# Key Performance Metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("⚡ Total Requests", stats.get('total_requests', 156), "+12")

with col2:
    st.metric("✅ Completed", stats.get('completed', 134), "+8")

with col3:
    st.metric("🔄 In Progress", stats.get('in_progress', 18), "-2")

with col4:
    st.metric("⏳ Pending", stats.get('pending', 4), "0")

with col5:
    st.metric("⏱️ Avg. Processing", f"{stats.get('avg_processing', 68)} min", "-5 min")

st.markdown("---")

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📋 Active Requests", "✅ Completed", "📊 Analytics", "🔮 Time Predictions"])

with tab1:
    st.subheader("📋 Active Service Requests")
    
    # Display real task-based data
    if not sample_requests_df.empty:
        # Filter for active requests (not completed)
        active_requests = sample_requests_df[~sample_requests_df['Status'].str.contains('✅ Completed')].copy()
        
        if not active_requests.empty:
            st.dataframe(active_requests, use_container_width=True)
            
            # Additional insights
            st.markdown("---")
            col_insight1, col_insight2 = st.columns(2)
            
            with col_insight1:
                st.markdown("#### � Request Distribution by Section")
                section_counts = active_requests['Section Name'].value_counts()
                if not section_counts.empty:
                    st.bar_chart(section_counts)
            
            with col_insight2:
                st.markdown("#### ⏱️ Processing Time Overview")
                # Extract numeric values from predicted time
                active_requests['Time_Minutes'] = active_requests['Predicted Time'].str.extract(r'(\d+)').astype(int)
                avg_time = active_requests['Time_Minutes'].mean()
                max_time = active_requests['Time_Minutes'].max()
                min_time = active_requests['Time_Minutes'].min()
                
                st.metric("Average Time", f"{avg_time:.0f} min")
                st.metric("Longest Task", f"{max_time} min")
                st.metric("Shortest Task", f"{min_time} min")
        else:
            st.info("No active requests at the moment.")
    else:
        st.error("Unable to load request data.")

with tab2:
    st.subheader("✅ Recently Completed Services")
    st.success("🎉 Great job! All recent requests have been processed successfully.")
    
    # Display completed requests from real data
    if not sample_requests_df.empty:
        completed_requests = sample_requests_df[sample_requests_df['Status'].str.contains('✅ Completed')].copy()
        
        if not completed_requests.empty:
            # Add actual completion time and rating
            completed_display = completed_requests.copy()
            completed_display['Actual Time'] = completed_display['Predicted Time'].apply(
                lambda x: f"{int(x.split()[0]) + random.randint(-10, 10)} min"
            )
            completed_display['Rating'] = [random.choice(["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]) for _ in range(len(completed_display))]
            completed_display['Completed Date'] = completed_display['Expected Completion']
            
            # Select relevant columns for display
            display_cols = ['Request ID', 'Task Name', 'Section Name', 'Completed Date', 'Actual Time', 'Rating']
            st.dataframe(completed_display[display_cols], use_container_width=True)
            
            # Completion analytics
            st.markdown("---")
            st.markdown("#### 📈 Completion Analytics")
            
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.markdown("**⚡ Efficiency Metrics:**")
                efficiency_score = random.randint(85, 98)
                on_time_delivery = random.randint(88, 96)
                st.metric("Efficiency Score", f"{efficiency_score}%")
                st.metric("On-time Delivery", f"{on_time_delivery}%")
            
            with comp_col2:
                st.markdown("**📊 Section Performance:**")
                section_performance = completed_display['Section Name'].value_counts()
                if not section_performance.empty:
                    st.bar_chart(section_performance)
        else:
            # Generate some completed tasks for display
            completed_sample = tasks_df.sample(min(3, len(tasks_df))).copy() if not tasks_df.empty else pd.DataFrame()
            if not completed_sample.empty:
                completed_display = []
                for _, task in completed_sample.iterrows():
                    completed_display.append({
                        'Request ID': f"REQ-{random.randint(90, 99):03d}",
                        'Task Name': task['task_name'],
                        'Section Name': task['section_name'],
                        'Completed Date': (datetime.now().date() - timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d'),
                        'Actual Time': f"{random.randint(30, 90)} min",
                        'Rating': random.choice(["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
                    })
                
                completed_df = pd.DataFrame(completed_display)
                st.dataframe(completed_df, use_container_width=True)
    else:
        st.error("Unable to load completion data.")

with tab3:
    st.subheader("📊 Service Completion Analytics")
    
    # Monthly trend chart (simulated)
    chart_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Completed': [23, 45, 56, 78, 32, 67],
        'Pending': [5, 8, 12, 6, 15, 4]
    })
    
    st.line_chart(chart_data.set_index('Month'))
    
    # Real data analytics
    analytics_col1, analytics_col2 = st.columns(2)
    
    with analytics_col1:
        st.markdown("#### ⏱️ Processing Time by Task Type")
        if not tasks_df.empty:
            # Create processing time analysis based on real tasks
            task_time_data = []
            for _, task in tasks_df.iterrows():
                # Estimate base time based on task complexity
                base_times = {
                    'TASK-001': 45, 'TASK-002': 30, 'TASK-003': 35, 'TASK-004': 25, 'TASK-005': 40,
                    'TASK-006': 50, 'TASK-007': 35, 'TASK-008': 40, 'TASK-009': 45, 'TASK-010': 30,
                    'TASK-011': 50, 'TASK-012': 90, 'TASK-013': 25, 'TASK-014': 35, 'TASK-015': 45,
                    'TASK-016': 120, 'TASK-017': 60, 'TASK-018': 75, 'TASK-019': 90
                }
                
                task_time_data.append({
                    'Task': task['task_id'],
                    'Avg Time (min)': base_times.get(task['task_id'], 45)
                })
            
            time_df = pd.DataFrame(task_time_data)
            # Show top 10 tasks by processing time
            top_tasks = time_df.nlargest(10, 'Avg Time (min)')
            st.bar_chart(top_tasks.set_index('Task'))
        else:
            st.info("No task data available for analysis")
    
    with analytics_col2:
        st.markdown("#### 🎯 Performance Metrics")
        
        # Task distribution by section
        if not tasks_df.empty:
            st.markdown("**📋 Tasks by Section:**")
            section_counts = tasks_df['section_name'].value_counts()
            for section, count in section_counts.items():
                st.write(f"• {section}: {count} tasks")
            
            st.markdown("---")
            st.metric("📊 Total Task Types", f"{len(tasks_df)}")
            st.metric("🏢 Service Sections", f"{tasks_df['section_name'].nunique()}")
            st.metric("⚡ Efficiency Score", "94%", "2%")
        else:
            st.metric("🔮 Prediction Accuracy", "89%", "5%")
            st.metric("📊 Time Variance", "±12 min", "-3 min")
            st.metric("⚡ Efficiency Score", "94%", "2%")
    
    # Section performance breakdown
    if not tasks_df.empty:
        st.markdown("---")
        st.markdown("#### 🏢 Section Performance Overview")
        
        section_perf_col1, section_perf_col2 = st.columns(2)
        
        with section_perf_col1:
            st.markdown("**📊 Task Distribution:**")
            section_chart = tasks_df['section_name'].value_counts()
            st.bar_chart(section_chart)
        
        with section_perf_col2:
            st.markdown("**📋 Section Details:**")
            section_summary = tasks_df.groupby('section_name').agg({
                'task_id': 'count'
            }).rename(columns={'task_id': 'Task Count'})
            
            section_summary['Avg Processing (est)'] = section_summary.index.map({
                'First-time Passport Applications': '38 min',
                'Renewals': '42 min', 
                'Corrections & Amendments': '40 min',
                'Lost/Stolen Passport Reissue': '57 min',
                'Document Verification': '35 min',
                'Special Cases': '86 min'
            })
            
            st.dataframe(section_summary, use_container_width=True)

with tab4:
    st.subheader("🔮 Service Time Predictions")
    
    # Show the prediction interface in this tab
    show_prediction_interface("prediction_form_tab")
    
    # Historical prediction accuracy
    st.markdown("---")
    st.markdown("#### 📈 Prediction Performance")
    
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        st.markdown("**🎯 Recent Accuracy:**")
        accuracy_data = {
            "Date": ["2025-08-19", "2025-08-20", "2025-08-21"],
            "Predictions Made": [15, 18, 12],
            "Accuracy %": [91, 87, 94]
        }
        accuracy_df = pd.DataFrame(accuracy_data)
        st.dataframe(accuracy_df, use_container_width=True)
    
    with perf_col2:
        st.markdown("**⚡ Model Performance:**")
        st.progress(0.89, text="Overall Accuracy: 89%")
        st.progress(0.76, text="Time Variance: 24%")
        st.progress(0.94, text="User Satisfaction: 94%")

# Action buttons
st.markdown("---")
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

with col_btn1:
    if st.button("📊 View Analytics", use_container_width=True):
        st.info("Opening detailed analytics view...")

with col_btn2:
    if st.button("📄 Generate Report", use_container_width=True):
        st.info("Generating service completion report...")

with col_btn3:
    if st.button("⚡ Quick Predict", use_container_width=True):
        st.session_state.show_predictor = True
        st.rerun()

with col_btn4:
    if st.button("🏠 Back to Home", use_container_width=True):
        # Use programmatic navigation to avoid session state conflicts
        st.session_state.programmatic_nav = "🏠 Home"
        st.rerun()
