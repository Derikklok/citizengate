import streamlit as st
import pandas as pd
from pathlib import Path
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Function to load booking data from CSV file
def load_booking_data():
    """Load booking data from CSV file"""
    try:
        # Try multiple potential paths for the CSV file
        potential_paths = [
            Path(__file__).parent.parent / "bookings_train.csv",  # Root directory
            Path(__file__).parent.parent / "data" / "bookings_train.csv",  # Data subdirectory
            Path("bookings_train.csv")  # Current directory
        ]
        
        for data_path in potential_paths:
            if data_path.exists():
                return pd.read_csv(data_path)
        
        st.error("Booking data file not found! Please ensure bookings_train.csv is in the project directory.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading booking data: {str(e)}")
        return pd.DataFrame()

# Function to get booking statistics
def get_booking_statistics(booking_df):
    """Generate statistics from booking data"""
    if booking_df.empty:
        return {}
    
    # Calculate key metrics from the data
    total_bookings = len(booking_df)
    unique_citizens = booking_df['citizen_id'].nunique()
    avg_satisfaction = booking_df['satisfaction_rating'].mean()
    
    # Calculate completion rate (bookings with check_out_time)
    completed_bookings = booking_df['check_out_time'].notna().sum()
    completion_rate = (completed_bookings / total_bookings * 100) if total_bookings > 0 else 0
    
    # Calculate average processing time for completed bookings
    booking_df_copy = booking_df.copy()
    booking_df_copy['check_in_time'] = pd.to_datetime(booking_df_copy['check_in_time'], errors='coerce')
    booking_df_copy['check_out_time'] = pd.to_datetime(booking_df_copy['check_out_time'], errors='coerce')
    
    completed = booking_df_copy.dropna(subset=['check_in_time', 'check_out_time']).copy()
    if not completed.empty:
        completed.loc[:, 'processing_time'] = (completed['check_out_time'] - completed['check_in_time']).dt.total_seconds() / 60
        avg_processing_time = completed['processing_time'].mean()
    else:
        avg_processing_time = 0
    
    return {
        'total_bookings': total_bookings,
        'unique_citizens': unique_citizens,
        'avg_satisfaction': avg_satisfaction,
        'completion_rate': completion_rate,
        'avg_processing_time': avg_processing_time,
        'completed_bookings': completed_bookings
    }

# Function to create booking analytics
def create_booking_analytics(booking_df):
    """Create analytics charts and insights"""
    if booking_df.empty:
        return None, None, None
    
    # Task distribution
    task_counts = booking_df['task_id'].value_counts()
    
    # Satisfaction rating distribution
    satisfaction_counts = booking_df['satisfaction_rating'].value_counts().sort_index()
    
    # Daily booking trends
    booking_df_copy = booking_df.copy()
    booking_df_copy['booking_date'] = pd.to_datetime(booking_df_copy['booking_date'])
    daily_bookings = booking_df_copy.groupby('booking_date').size().reset_index(name='count')
    
    return task_counts, satisfaction_counts, daily_bookings

# Load booking data
booking_df = load_booking_data()
stats = get_booking_statistics(booking_df)

# Page header with enhanced styling
st.markdown("""
<div class="main-header">
    <div class="header-title">📅 Booking Management Dashboard</div>
    <div class="header-subtitle">Comprehensive appointment and service booking analytics</div>
</div>
""", unsafe_allow_html=True)

# Header with action button
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown("#### 🎯 Real-time booking insights and citizen service analytics")

with header_col2:
    if st.button("📊 Analytics Report", key="booking_analytics_btn", use_container_width=True, type="primary"):
        st.session_state.show_analytics = not st.session_state.get('show_analytics', False)

# Show analytics report if toggled
if st.session_state.get('show_analytics', False):
    st.markdown("### 📈 Detailed Analytics Report")
    
    if not booking_df.empty:
        task_counts, satisfaction_counts, daily_bookings = create_booking_analytics(booking_df)
        
        # Analytics content
        analytics_col1, analytics_col2 = st.columns(2)
        
        with analytics_col1:
            st.markdown("#### 📊 Task Distribution")
            fig_tasks = px.bar(x=task_counts.index, y=task_counts.values, 
                              title="Bookings by Task Type")
            fig_tasks.update_layout(xaxis_title="Task ID", yaxis_title="Number of Bookings")
            st.plotly_chart(fig_tasks, use_container_width=True)
        
        with analytics_col2:
            st.markdown("#### 😊 Satisfaction Ratings")
            fig_satisfaction = px.pie(values=satisfaction_counts.values, names=satisfaction_counts.index,
                                    title="Satisfaction Rating Distribution")
            st.plotly_chart(fig_satisfaction, use_container_width=True)
        
        # Daily trends
        st.markdown("#### 📈 Daily Booking Trends")
        fig_daily = px.line(daily_bookings, x='booking_date', y='count',
                           title="Bookings Over Time")
        fig_daily.update_layout(xaxis_title="Date", yaxis_title="Number of Bookings")
        st.plotly_chart(fig_daily, use_container_width=True)
    else:
        st.info("No booking data available for analytics")
    
    # Add a button to go back to the main dashboard
    if st.button("🔙 Back to Dashboard", key="back_to_booking_dashboard", use_container_width=True):
        st.session_state.show_analytics = False
        st.rerun()
    
    # Stop execution here to hide the rest of the content
    st.stop()

# Key Performance Metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "📅 Total Bookings", 
        f"{stats.get('total_bookings', 0):,}",
        help="Total number of bookings in the system"
    )

with col2:
    st.metric(
        "👥 Unique Citizens", 
        f"{stats.get('unique_citizens', 0):,}",
        help="Number of unique citizens served"
    )

with col3:
    st.metric(
        "✅ Completion Rate", 
        f"{stats.get('completion_rate', 0):.1f}%",
        help="Percentage of bookings completed successfully"
    )

with col4:
    st.metric(
        "⏱️ Avg. Processing", 
        f"{stats.get('avg_processing_time', 0):.0f} min",
        help="Average time from check-in to check-out"
    )

with col5:
    st.metric(
        "😊 Satisfaction", 
        f"{stats.get('avg_satisfaction', 0):.1f}/5.0",
        help="Average citizen satisfaction rating"
    )

st.markdown("---")

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📋 Booking Records", "🕐 Queue Management", "📊 Performance Analytics", "🔍 Search & Filter"])

with tab1:
    st.subheader("📅 Booking Records Overview")
    
    if not booking_df.empty:
        # Display sample of booking data
        st.markdown("#### Recent Bookings")
        
        # Show data with specific columns
        display_columns = [
            'booking_id', 'citizen_id', 'booking_date', 'appointment_date', 
            'appointment_time', 'task_id', 'queue_number', 'satisfaction_rating'
        ]
        
        # Filter to display columns that exist in the dataframe
        available_columns = [col for col in display_columns if col in booking_df.columns]
        recent_bookings = booking_df[available_columns].head(50)
        
        st.dataframe(recent_bookings, use_container_width=True)
        
        # Quick insights
        st.markdown("---")
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("#### 📊 Booking Status Distribution")
            completed = booking_df['check_out_time'].notna().sum()
            pending = booking_df['check_out_time'].isna().sum()
            
            status_data = pd.DataFrame({
                'Status': ['Completed', 'Pending'],
                'Count': [completed, pending]
            })
            
            fig_status = px.pie(status_data, values='Count', names='Status',
                              title="Booking Status Distribution")
            st.plotly_chart(fig_status, use_container_width=True)
        
        with insight_col2:
            st.markdown("#### ⏰ Peak Appointment Hours")
            booking_df_copy = booking_df.copy()
            booking_df_copy['hour'] = pd.to_datetime(booking_df_copy['appointment_time'], format='%H:%M', errors='coerce').dt.hour
            hourly_bookings = booking_df_copy['hour'].value_counts().sort_index()
            
            fig_hourly = px.bar(x=hourly_bookings.index, y=hourly_bookings.values,
                               title="Bookings by Hour of Day")
            fig_hourly.update_layout(xaxis_title="Hour", yaxis_title="Number of Bookings")
            st.plotly_chart(fig_hourly, use_container_width=True)
    else:
        st.info("No booking data available.")

with tab2:
    st.subheader("🕐 Queue Management")
    
    if not booking_df.empty:
        # Queue analysis
        queue_col1, queue_col2 = st.columns(2)
        
        with queue_col1:
            st.markdown("#### 📈 Queue Performance Metrics")
            
            avg_queue_number = booking_df['queue_number'].mean()
            max_queue_number = booking_df['queue_number'].max()
            
            st.metric("Average Queue Position", f"{avg_queue_number:.1f}")
            st.metric("Peak Queue Length", f"{max_queue_number}")
            
            # Queue distribution
            queue_dist = booking_df['queue_number'].value_counts().sort_index().head(20)
            fig_queue = px.bar(x=queue_dist.index, y=queue_dist.values,
                              title="Queue Position Distribution (Top 20)")
            fig_queue.update_layout(xaxis_title="Queue Position", yaxis_title="Number of Bookings")
            st.plotly_chart(fig_queue, use_container_width=True)
        
        with queue_col2:
            st.markdown("#### ⏱️ Wait Time Analysis")
            
            # Calculate wait times for bookings with check-in times
            booking_df_copy = booking_df.copy()
            booking_df_copy['appointment_datetime'] = pd.to_datetime(
                booking_df_copy['appointment_date'].astype(str) + ' ' + booking_df_copy['appointment_time'].astype(str),
                errors='coerce'
            )
            booking_df_copy['check_in_time'] = pd.to_datetime(booking_df_copy['check_in_time'], errors='coerce')
            
            valid_times = booking_df_copy.dropna(subset=['appointment_datetime', 'check_in_time']).copy()
            
            if not valid_times.empty:
                valid_times.loc[:, 'wait_time_minutes'] = (
                    valid_times['check_in_time'] - valid_times['appointment_datetime']
                ).dt.total_seconds() / 60
                
                avg_wait_time = valid_times['wait_time_minutes'].mean()
                st.metric("Average Wait Time", f"{avg_wait_time:.1f} min")
                
                # Wait time distribution
                wait_time_bins = pd.cut(valid_times['wait_time_minutes'], 
                                      bins=[-float('inf'), -30, -10, 0, 10, 30, float('inf')],
                                      labels=['Early >30min', 'Early 10-30min', 'Early <10min', 
                                             'Late <10min', 'Late 10-30min', 'Late >30min'])
                
                wait_dist = wait_time_bins.value_counts()
                fig_wait = px.bar(x=wait_dist.index, y=wait_dist.values,
                                 title="Check-in Time vs Appointment Time")
                fig_wait.update_layout(xaxis_title="Wait Time Category", yaxis_title="Number of Bookings")
                st.plotly_chart(fig_wait, use_container_width=True)
            else:
                st.info("No valid time data available for wait time analysis")
    else:
        st.info("No queue data available.")

with tab3:
    st.subheader("📊 Performance Analytics")
    
    if not booking_df.empty:
        # Performance metrics
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.markdown("#### 🎯 Task Performance")
            
            # Task completion rates
            task_performance = booking_df.groupby('task_id').agg({
                'check_out_time': lambda x: x.notna().sum(),
                'booking_id': 'count'
            }).rename(columns={'check_out_time': 'completed', 'booking_id': 'total'})
            
            task_performance['completion_rate'] = (task_performance['completed'] / task_performance['total'] * 100).round(1)
            task_performance = task_performance.reset_index()
            
            st.dataframe(task_performance, use_container_width=True)
            
            # Task completion rate chart
            fig_task_perf = px.bar(task_performance, x='task_id', y='completion_rate',
                                  title="Task Completion Rates")
            fig_task_perf.update_layout(xaxis_title="Task ID", yaxis_title="Completion Rate (%)")
            st.plotly_chart(fig_task_perf, use_container_width=True)
        
        with perf_col2:
            st.markdown("#### 📄 Document Processing")
            
            # Document analysis
            doc_stats = booking_df['num_documents'].describe()
            st.metric("Average Documents per Booking", f"{doc_stats['mean']:.1f}")
            st.metric("Max Documents Processed", f"{doc_stats['max']:.0f}")
            
            # Document distribution
            doc_dist = booking_df['num_documents'].value_counts().sort_index()
            fig_docs = px.bar(x=doc_dist.index, y=doc_dist.values,
                             title="Number of Documents per Booking")
            fig_docs.update_layout(xaxis_title="Number of Documents", yaxis_title="Number of Bookings")
            st.plotly_chart(fig_docs, use_container_width=True)
        
        # Satisfaction analysis
        st.markdown("---")
        st.markdown("#### 😊 Satisfaction Analysis")
        
        sat_col1, sat_col2 = st.columns(2)
        
        with sat_col1:
            # Satisfaction by task
            sat_by_task = booking_df.groupby('task_id')['satisfaction_rating'].mean().reset_index()
            fig_sat_task = px.bar(sat_by_task, x='task_id', y='satisfaction_rating',
                                 title="Average Satisfaction by Task")
            fig_sat_task.update_layout(xaxis_title="Task ID", yaxis_title="Average Satisfaction")
            st.plotly_chart(fig_sat_task, use_container_width=True)
        
        with sat_col2:
            # Satisfaction trends over time
            booking_df_copy = booking_df.copy()
            booking_df_copy['booking_date'] = pd.to_datetime(booking_df_copy['booking_date'])
            sat_trends = booking_df_copy.groupby('booking_date')['satisfaction_rating'].mean().reset_index()
            
            fig_sat_trend = px.line(sat_trends, x='booking_date', y='satisfaction_rating',
                                   title="Satisfaction Trends Over Time")
            fig_sat_trend.update_layout(xaxis_title="Date", yaxis_title="Average Satisfaction")
            st.plotly_chart(fig_sat_trend, use_container_width=True)
    else:
        st.info("No performance data available.")

with tab4:
    st.subheader("🔍 Search & Filter Bookings")
    
    if not booking_df.empty:
        # Search and filter interface
        search_col1, search_col2, search_col3 = st.columns(3)
        
        with search_col1:
            # Citizen ID search
            citizen_id = st.text_input("🔍 Search by Citizen ID", placeholder="Enter citizen ID...")
            
            # Task filter
            available_tasks = ['All'] + sorted(booking_df['task_id'].unique().tolist())
            selected_task = st.selectbox("📋 Filter by Task", available_tasks)
        
        with search_col2:
            # Date range filter
            min_date = pd.to_datetime(booking_df['booking_date']).min().date()
            max_date = pd.to_datetime(booking_df['booking_date']).max().date()
            
            start_date = st.date_input("📅 Start Date", value=min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("📅 End Date", value=max_date, min_value=min_date, max_value=max_date)
        
        with search_col3:
            # Satisfaction filter
            satisfaction_options = ['All'] + sorted(booking_df['satisfaction_rating'].dropna().unique().tolist())
            selected_satisfaction = st.selectbox("😊 Filter by Satisfaction", satisfaction_options)
            
            # Status filter
            status_options = ['All', 'Completed', 'Pending']
            selected_status = st.selectbox("📊 Filter by Status", status_options)
        
        # Apply filters
        filtered_df = booking_df.copy()
        
        if citizen_id:
            filtered_df = filtered_df[filtered_df['citizen_id'].astype(str).str.contains(citizen_id, na=False)]
        
        if selected_task != 'All':
            filtered_df = filtered_df[filtered_df['task_id'] == selected_task]
        
        # Date filter
        filtered_df = filtered_df.copy()  # Ensure we have a proper copy
        filtered_df.loc[:, 'booking_date'] = pd.to_datetime(filtered_df['booking_date']).dt.date
        filtered_df = filtered_df[
            (filtered_df['booking_date'] >= start_date) & 
            (filtered_df['booking_date'] <= end_date)
        ]
        
        if selected_satisfaction != 'All':
            filtered_df = filtered_df[filtered_df['satisfaction_rating'] == int(selected_satisfaction)]
        
        if selected_status != 'All':
            if selected_status == 'Completed':
                filtered_df = filtered_df[filtered_df['check_out_time'].notna()]
            else:  # Pending
                filtered_df = filtered_df[filtered_df['check_out_time'].isna()]
        
        # Display filtered results
        st.markdown(f"#### 📊 Filtered Results ({len(filtered_df)} bookings)")
        
        if not filtered_df.empty:
            # Show all columns for filtered results
            st.dataframe(filtered_df, use_container_width=True)
            
            # Export option
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data",
                data=csv,
                file_name=f"filtered_bookings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No bookings match the selected filters.")
    else:
        st.info("No booking data available for search.")

# Action buttons
st.markdown("---")
st.markdown("### 🛠️ Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("📊 Generate Booking Report", use_container_width=True, type="primary"):
        if not booking_df.empty:
            st.success("📄 Comprehensive booking report generated!")
            st.info(f"Report includes analysis of {len(booking_df):,} bookings from {stats.get('unique_citizens', 0):,} citizens")
        else:
            st.error("No data available for report generation")

with action_col2:
    if st.button("📅 Optimize Scheduling", use_container_width=True):
        if not booking_df.empty:
            # Find peak hours
            booking_df_copy = booking_df.copy()
            booking_df_copy['hour'] = pd.to_datetime(booking_df_copy['appointment_time'], format='%H:%M', errors='coerce').dt.hour
            peak_hour = booking_df_copy['hour'].mode().iloc[0] if not booking_df_copy['hour'].empty else 'N/A'
            
            st.success("🔄 Scheduling optimization complete!")
            st.info(f"💡 Peak booking hour: {peak_hour}:00. Consider additional staff during this time.")
        else:
            st.error("No data available for optimization")

with action_col3:
    if st.button("🏠 Back to Home", use_container_width=True):
        # Use programmatic navigation to avoid session state conflicts
        st.session_state.programmatic_nav = "🏠 Home"
        st.rerun()
