import streamlit as st

st.title("✅ Service Completion Dashboard")
st.markdown("### Manage and track your service requests")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Requests", "156", "12")

with col2:
    st.metric("Completed", "134", "8")

with col3:
    st.metric("In Progress", "18", "-2")

with col4:
    st.metric("Pending", "4", "0")

st.markdown("---")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["📋 Active Requests", "✅ Completed", "📊 Analytics"])

with tab1:
    st.subheader("Active Service Requests")
    
    # Sample data table
    import pandas as pd
    
    sample_data = {
        "Request ID": ["REQ-001", "REQ-002", "REQ-003"],
        "Service Type": ["Document Verification", "License Renewal", "Permit Application"],
        "Status": ["In Progress", "Under Review", "Pending Payment"],
        "Submitted": ["2025-08-20", "2025-08-19", "2025-08-18"],
        "Expected Completion": ["2025-08-25", "2025-08-24", "2025-08-23"]
    }
    
    df = pd.DataFrame(sample_data)
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Recently Completed Services")
    st.success("🎉 Great job! All recent requests have been processed successfully.")
    
    completed_data = {
        "Request ID": ["REQ-098", "REQ-099", "REQ-100"],
        "Service Type": ["Birth Certificate", "Tax Clearance", "Business Registration"],
        "Completed Date": ["2025-08-17", "2025-08-16", "2025-08-15"],
        "Rating": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    }
    
    completed_df = pd.DataFrame(completed_data)
    st.dataframe(completed_df, use_container_width=True)

with tab3:
    st.subheader("Service Completion Analytics")
    
    # Sample chart data
    chart_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Completed': [23, 45, 56, 78, 32, 67],
        'Pending': [5, 8, 12, 6, 15, 4]
    })
    
    st.line_chart(chart_data.set_index('Month'))

# Action buttons
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("🆕 New Request", use_container_width=True):
        st.info("Redirecting to new request form...")

with col_btn2:
    if st.button("📄 Generate Report", use_container_width=True):
        st.info("Generating service completion report...")

with col_btn3:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")
