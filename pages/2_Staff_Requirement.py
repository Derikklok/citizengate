import streamlit as st

st.title("👥 Staff Requirement Management")
st.markdown("### Manage staffing needs and workforce planning")

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Staff", "245", "15")

with col2:
    st.metric("Active Positions", "38", "5")

with col3:
    st.metric("Open Vacancies", "12", "-3")

with col4:
    st.metric("Recruitment Rate", "85%", "8%")

st.markdown("---")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Department Overview", "🎯 Open Positions", "📝 Recruitment", "📈 Analytics"])

with tab1:
    st.subheader("Department Staffing Overview")
    
    import pandas as pd
    
    # Sample department data
    dept_data = {
        "Department": ["Customer Service", "IT Support", "Administration", "Finance", "Operations"],
        "Current Staff": [45, 23, 18, 12, 147],
        "Required Staff": [50, 25, 20, 15, 150],
        "Vacancy": [5, 2, 2, 3, 3],
        "Status": ["🟡 Understaffed", "🟡 Understaffed", "🟡 Understaffed", "🔴 Critical", "🟢 Adequate"]
    }
    
    dept_df = pd.DataFrame(dept_data)
    st.dataframe(dept_df, use_container_width=True)

with tab2:
    st.subheader("Current Open Positions")
    
    positions_data = {
        "Position": ["Senior Developer", "Customer Service Rep", "Data Analyst", "Project Manager"],
        "Department": ["IT Support", "Customer Service", "Administration", "Operations"],
        "Level": ["Senior", "Entry", "Mid", "Senior"],
        "Posted Date": ["2025-08-15", "2025-08-18", "2025-08-20", "2025-08-12"],
        "Applications": [23, 45, 12, 8],
        "Status": ["🔍 Reviewing", "📝 Interviewing", "🆕 Posted", "🔍 Reviewing"]
    }
    
    positions_df = pd.DataFrame(positions_data)
    st.dataframe(positions_df, use_container_width=True)
    
    if st.button("➕ Post New Position", use_container_width=True):
        st.info("Opening job posting form...")

with tab3:
    st.subheader("Recruitment Pipeline")
    
    # Recruitment funnel
    st.markdown("#### Current Recruitment Progress")
    
    pipeline_col1, pipeline_col2 = st.columns(2)
    
    with pipeline_col1:
        st.markdown("""
        **Application Review**
        - Applications Received: 156
        - Under Review: 45
        - Shortlisted: 23
        """)
    
    with pipeline_col2:
        st.markdown("""
        **Interview Process**
        - Phone Screening: 18
        - Technical Interview: 12
        - Final Interview: 8
        - Offers Extended: 5
        """)
    
    # Progress bars
    st.markdown("#### Recruitment Goals Progress")
    st.progress(0.7, text="Q3 Hiring Target: 70% Complete")
    st.progress(0.85, text="Customer Service Expansion: 85% Complete")
    st.progress(0.45, text="IT Department Growth: 45% Complete")

with tab4:
    st.subheader("Staffing Analytics")
    
    # Sample analytics data
    analytics_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'New Hires': [8, 12, 15, 6, 10, 14],
        'Departures': [3, 7, 4, 9, 5, 2],
        'Net Growth': [5, 5, 11, -3, 5, 12]
    })
    
    st.line_chart(analytics_data.set_index('Month'))
    
    # Department distribution
    st.markdown("#### Staff Distribution by Department")
    dept_chart_data = pd.DataFrame({
        'Department': dept_data['Department'],
        'Staff Count': dept_data['Current Staff']
    })
    st.bar_chart(dept_chart_data.set_index('Department'))

# Action buttons
st.markdown("---")
action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("📋 Workforce Planning", use_container_width=True):
        st.info("Opening workforce planning module...")

with action_col2:
    if st.button("📊 Generate Report", use_container_width=True):
        st.info("Generating staffing report...")

with action_col3:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")
