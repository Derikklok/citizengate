import streamlit as st

# Home page content
st.title("🏛️ Welcome to CitizenGate")
st.markdown("### Your Gateway to Digital Government Services")

# Create columns for better layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🎯 Our Mission
    Providing efficient and transparent digital services to citizens through innovative technology solutions.
    """)

with col2:
    st.markdown("""
    #### 📊 Service Statistics
    - **Active Services**: 25+
    - **Users Served**: 10,000+
    - **Satisfaction Rate**: 98%
    """)

with col3:
    st.markdown("""
    #### 🚀 Quick Actions
    - Submit New Request
    - Track Application
    - Download Documents
    """)

st.markdown("---")

# Recent updates section
st.subheader("📢 Recent Updates")
st.info("🔔 New digital identity verification system is now live!")
st.success("✅ Service completion processing time reduced by 40%")

# Featured services
st.subheader("🌟 Featured Services")
service_col1, service_col2 = st.columns(2)

with service_col1:
    with st.container():
        st.markdown("#### ✅ Service Completion")
        st.write("Track and manage your service requests efficiently")
        if st.button("Access Service Completion", key="service_btn"):
            st.switch_page("pages/1_Service_Completion.py")

with service_col2:
    with st.container():
        st.markdown("#### 👥 Staff Requirement")
        st.write("Manage staffing needs and requirements")
        if st.button("Access Staff Management", key="staff_btn"):
            st.switch_page("pages/2_Staff_Requirement.py")
