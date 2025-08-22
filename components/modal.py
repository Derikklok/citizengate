import streamlit as st

def show_service_request_modal():
    """
    Display a modal dialog for creating a new service request
    """
    # Initialize session state for modal
    if "show_modal" not in st.session_state:
        st.session_state.show_modal = False
    
    # Modal content
    if st.session_state.show_modal:
        # Create a container for the modal
        modal_container = st.container()
        
        with modal_container:
            # Modal header
            st.markdown("""
            <div style="
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border: 2px solid #007bff;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            ">
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([6, 1])
            
            with col1:
                st.markdown("### 🆕 Create New Service Request")
            
            with col2:
                if st.button("✖️", key="close_modal", help="Close Modal"):
                    st.session_state.show_modal = False
                    st.rerun()
            
            st.markdown("---")
            
            # Modal form content
            with st.form("new_service_request_form"):
                st.markdown("#### Request Details")
                
                # Form fields
                col_form1, col_form2 = st.columns(2)
                
                with col_form1:
                    service_type = st.selectbox(
                        "Service Type *",
                        ["Document Verification", "License Renewal", "Permit Application", 
                         "Birth Certificate", "Tax Clearance", "Business Registration", "Other"],
                        index=0
                    )
                    
                    priority = st.selectbox(
                        "Priority Level *",
                        ["Low", "Medium", "High", "Urgent"],
                        index=1
                    )
                
                with col_form2:
                    requester_name = st.text_input("Requester Name *", placeholder="Enter your full name")
                    
                    contact_email = st.text_input("Contact Email *", placeholder="your.email@example.com")
                
                # Description
                description = st.text_area(
                    "Request Description *",
                    placeholder="Please provide detailed information about your service request...",
                    height=100
                )
                
                # File upload
                uploaded_files = st.file_uploader(
                    "Attach Supporting Documents",
                    type=['pdf', 'doc', 'docx', 'jpg', 'png'],
                    accept_multiple_files=True,
                    help="Upload any supporting documents (PDF, DOC, JPG, PNG)"
                )
                
                # Additional options
                st.markdown("#### Additional Options")
                
                col_opts1, col_opts2 = st.columns(2)
                
                with col_opts1:
                    rush_service = st.checkbox("Rush Service (+$25 fee)")
                    email_notifications = st.checkbox("Email Notifications", value=True)
                
                with col_opts2:
                    sms_notifications = st.checkbox("SMS Notifications")
                    pickup_location = st.selectbox(
                        "Document Pickup Location",
                        ["Main Office", "Branch Office A", "Branch Office B", "Home Delivery (+$10)"]
                    )
                
                # Form submission buttons
                st.markdown("---")
                col_submit1, col_submit2, col_submit3 = st.columns([2, 1, 1])
                
                with col_submit2:
                    submitted = st.form_submit_button("🚀 Submit Request", use_container_width=True)
                
                with col_submit3:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state.show_modal = False
                        st.rerun()
                
                # Handle form submission
                if submitted:
                    # Validation
                    if not requester_name or not contact_email or not description:
                        st.error("⚠️ Please fill in all required fields marked with *")
                    elif "@" not in contact_email:
                        st.error("⚠️ Please enter a valid email address")
                    else:
                        # Simulate successful submission
                        import random
                        request_id = f"REQ-{random.randint(1000, 9999)}"
                        
                        st.success(f"✅ Service request submitted successfully!")
                        st.info(f"📋 **Request ID:** {request_id}")
                        st.info(f"📧 Confirmation email sent to: {contact_email}")
                        
                        # Show summary
                        with st.expander("📝 Request Summary", expanded=True):
                            st.write(f"**Service Type:** {service_type}")
                            st.write(f"**Priority:** {priority}")
                            st.write(f"**Requester:** {requester_name}")
                            st.write(f"**Contact:** {contact_email}")
                            st.write(f"**Description:** {description}")
                            if rush_service:
                                st.write("**Rush Service:** Yes (+$25)")
                            if uploaded_files:
                                st.write(f"**Attached Files:** {len(uploaded_files)} file(s)")
                        
                        # Auto-close modal after submission (optional)
                        if st.button("🏠 Return to Dashboard"):
                            st.session_state.show_modal = False
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

def open_modal():
    """Function to open the modal"""
    st.session_state.show_modal = True

def close_modal():
    """Function to close the modal"""
    st.session_state.show_modal = False
