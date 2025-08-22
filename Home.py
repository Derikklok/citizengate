import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Page header with enhanced styling
st.markdown("""
<div class="main-header">
    <div class="header-title">🏛️ Welcome to CitizenGate</div>
    <div class="header-subtitle">Advanced Government Service Management & Analytics Platform</div>
</div>
""", unsafe_allow_html=True)

# Real-time metrics dashboard
st.markdown("## 📊 Live System Overview")

# Create dynamic metrics
current_time = datetime.now()
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🎯 Active Services", 
        "156", 
        "+12 today",
        help="Currently active service requests"
    )

with col2:
    st.metric(
        "👥 Staff On Duty", 
        "89", 
        "+3 since morning",
        help="Total staff currently working"
    )

with col3:
    st.metric(
        "⚡ Completion Rate", 
        "94.2%", 
        "+2.1% this week",
        help="Service completion efficiency"
    )

with col4:
    st.metric(
        "⏱️ Avg. Processing", 
        "42 min", 
        "-8 min improved",
        help="Average processing time per service"
    )

with col5:
    st.metric(
        "📈 Satisfaction", 
        "4.8/5.0", 
        "+0.2 this month",
        help="Citizen satisfaction rating"
    )

st.markdown("---")

# Feature showcase
st.markdown("## 🚀 Platform Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">✅</div>
        <div class="feature-title">Service Completion Management</div>
        <div class="feature-description">
            Track, manage, and optimize service completion processes with real-time insights. 
            Monitor task progress, predict completion times, and analyze performance metrics 
            across all passport service sections.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔮</div>
        <div class="feature-title">AI-Powered Predictions</div>
        <div class="feature-description">
            Leverage machine learning algorithms to predict service processing times and 
            workforce requirements. Make data-driven decisions with confidence intervals 
            and historical pattern analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👥</div>
        <div class="feature-title">Workforce Management</div>
        <div class="feature-description">
            Optimize staff allocation across different service sections. Analyze workload 
            distribution, identify staffing gaps, and forecast future workforce needs 
            based on historical data and seasonal patterns.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Advanced Analytics</div>
        <div class="feature-description">
            Comprehensive dashboard with real-time analytics, performance trends, and 
            actionable insights. Generate detailed reports and visualizations for 
            strategic planning and operational optimization.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Quick action buttons
st.markdown("## 🎯 Quick Actions")

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("📋 View Service Dashboard", use_container_width=True, type="primary"):
        st.session_state.programmatic_nav = "✅ Service Completion"
        st.rerun()

with action_col2:
    if st.button("👥 Manage Workforce", use_container_width=True, type="primary"):
        st.session_state.programmatic_nav = "👥 Staff Requirement"
        st.rerun()

with action_col3:
    if st.button("🔮 AI Predictions", use_container_width=True):
        st.session_state.programmatic_nav = "✅ Service Completion"
        st.session_state.show_predictor = True
        st.rerun()

with action_col4:
    if st.button("📊 Generate Report", use_container_width=True):
        st.success("📄 Comprehensive system report generated!")
        st.balloons()

# System insights section
st.markdown("---")
st.markdown("## 💡 Today's Insights")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.info("""
    **🎯 Performance Highlight**
    
    Section SEC-005 (Document Verification) is operating at 98% efficiency - 
    the highest this month! Consider applying their best practices to other sections.
    """)

with insight_col2:
    st.warning("""
    **⚠️ Attention Required**
    
    Section SEC-004 (Lost/Stolen Passport) shows increased workload. 
    Consider workforce reallocation or additional staffing.
    """)

with insight_col3:
    st.success("""
    **📈 Improvement Trend**
    
    Overall processing time has improved by 18% this quarter. 
    AI predictions are 94% accurate for workforce planning.
    """)

# Recent activity feed
st.markdown("## 📱 Recent Activity")

# Simulate recent activities
activities = [
    "🔄 Service SEC-001-245 completed in 38 minutes",
    "👥 3 new staff members assigned to Section SEC-002",
    "📊 Weekly performance report generated",
    "🔮 AI predicted 15% increase in workload for tomorrow",
    "✅ 24 passport applications processed successfully",
    "⚙️ System performance optimized - 12% faster response time",
]

for i, activity in enumerate(activities[:4]):
    time_ago = f"{(i+1)*5} minutes ago"
    st.markdown(f"• **{time_ago}**: {activity}")

# Footer
st.markdown("""
<div class="app-footer">
    <h3>🏛️ CitizenGate Platform</h3>
    <p>Empowering efficient government service delivery through data-driven insights and AI-powered optimization.</p>
    <p><strong>Version 2.1.0</strong> | Last Updated: August 2025 | 🔒 Secure & Compliant</p>
</div>
""", unsafe_allow_html=True)
