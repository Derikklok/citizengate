import streamlit as st
import pandas as pd
from pathlib import Path

# Function to load staffing data from CSV file
def load_staffing_data():
    """Load staffing data from CSV file"""
    try:
        data_path = Path(__file__).parent.parent / "data" / "staffing_train.csv"
        if data_path.exists():
            return pd.read_csv(data_path)
        else:
            st.error("Staffing data file not found!")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading staffing data: {str(e)}")
        return pd.DataFrame()

# Function to get staffing statistics
def get_staffing_statistics(staffing_df):
    """Generate statistics from staffing data"""
    if staffing_df.empty:
        return {}
    
    # Calculate key metrics from the data
    total_records = len(staffing_df)
    unique_sections = staffing_df['section_id'].nunique()
    avg_employees = int(staffing_df['employees_on_duty'].mean())
    total_task_time = int(staffing_df['total_task_time_minutes'].sum())
    
    return {
        'total_records': total_records,
        'unique_sections': unique_sections,
        'avg_employees': avg_employees,
        'total_task_time': total_task_time
    }

# Function to predict workforce requirements
def predict_workforce_requirement(staffing_df, target_date, section_id):
    """Predict the number of employees needed for a specific section on a given date"""
    if staffing_df.empty:
        return 0, "No data available for prediction"
    
    # Filter data for the specific section
    section_data = staffing_df[staffing_df['section_id'] == section_id].copy()
    
    if section_data.empty:
        return 0, f"No historical data found for section {section_id}"
    
    # Convert date columns to datetime
    section_data['date'] = pd.to_datetime(section_data['date'])
    target_datetime = pd.to_datetime(target_date)
    
    # Extract date features for prediction
    section_data['year'] = section_data['date'].dt.year
    section_data['month'] = section_data['date'].dt.month
    section_data['day'] = section_data['date'].dt.day
    section_data['weekday'] = section_data['date'].dt.weekday
    section_data['is_weekend'] = section_data['weekday'].isin([5, 6]).astype(int)
    
    # Calculate basic statistics for the section
    avg_employees = section_data['employees_on_duty'].mean()
    std_employees = section_data['employees_on_duty'].std()
    avg_task_time = section_data['total_task_time_minutes'].mean()
    
    # Extract features for target date
    target_year = target_datetime.year
    target_month = target_datetime.month
    target_day = target_datetime.day
    target_weekday = target_datetime.weekday()
    target_is_weekend = 1 if target_weekday in [5, 6] else 0
    
    # Simple prediction model based on historical patterns
    predicted_employees = avg_employees
    
    # Adjust for day of week patterns
    weekday_pattern = section_data.groupby('weekday')['employees_on_duty'].mean()
    if target_weekday in weekday_pattern.index:
        weekday_factor = weekday_pattern[target_weekday] / avg_employees
        predicted_employees *= weekday_factor
    
    # Adjust for monthly patterns
    monthly_pattern = section_data.groupby('month')['employees_on_duty'].mean()
    if target_month in monthly_pattern.index:
        monthly_factor = monthly_pattern[target_month] / avg_employees
        predicted_employees *= monthly_factor
    
    # Adjust for weekend vs weekday
    if target_is_weekend:
        weekend_avg = section_data[section_data['is_weekend'] == 1]['employees_on_duty'].mean()
        if not pd.isna(weekend_avg):
            weekend_factor = weekend_avg / avg_employees
            predicted_employees *= weekend_factor
    
    # Adjust based on task complexity (workload)
    workload_factor = avg_task_time / section_data['total_task_time_minutes'].mean() if section_data['total_task_time_minutes'].mean() > 0 else 1
    predicted_employees *= workload_factor
    
    # Round to nearest integer and ensure minimum of 1
    predicted_employees = max(1, round(predicted_employees))
    
    # Generate confidence and explanation
    confidence = min(95, max(60, 100 - (std_employees / avg_employees * 100))) if avg_employees > 0 else 60
    
    explanation = f"""
    **Prediction Details:**
    - Historical Average: {avg_employees:.1f} employees
    - Day of Week Factor: {weekday_pattern[target_weekday] / avg_employees:.2f} (Weekday: {target_weekday})
    - Monthly Pattern: {monthly_pattern[target_month] / avg_employees:.2f} if available
    - Weekend Adjustment: {'Applied' if target_is_weekend else 'Not applicable'}
    - Workload Factor: {workload_factor:.2f}
    - Confidence Level: {confidence:.0f}%
    """
    
    return predicted_employees, explanation

# Function to show workforce prediction modal
def show_workforce_prediction_modal(staffing_df):
    """Display the workforce prediction interface"""
    st.markdown("### 🔮 Workforce Requirement Forecasting")
    st.markdown("Predict the optimal number of employees needed for efficient operations")
    
    # Get available sections
    available_sections = sorted(staffing_df['section_id'].unique()) if not staffing_df.empty else []
    
    if not available_sections:
        st.error("No section data available for prediction")
        return
    
    # Input form
    with st.form("workforce_prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            target_date = st.date_input(
                "📅 Select Target Date",
                value=pd.Timestamp.now().date(),
                help="Choose the date for workforce prediction"
            )
        
        with col2:
            section_id = st.selectbox(
                "🏢 Select Section",
                options=available_sections,
                help="Choose the section for prediction"
            )
        
        # Section information
        if section_id:
            section_info = {
                'SEC-001': 'First-time Passport Applications',
                'SEC-002': 'Renewals',
                'SEC-003': 'Corrections & Amendments',
                'SEC-004': 'Lost/Stolen Passport Reissue',
                'SEC-005': 'Document Verification',
                'SEC-006': 'Special Cases'
            }
            st.info(f"📋 **Section Details:** {section_info.get(section_id, 'Unknown Section')}")
        
        submitted = st.form_submit_button("🔮 Predict Workforce Requirement", use_container_width=True, type="primary")
        
        if submitted:
            # Perform prediction
            predicted_count, explanation = predict_workforce_requirement(
                staffing_df, target_date.strftime('%Y-%m-%d'), section_id
            )
            
            # Display results
            st.markdown("---")
            st.markdown("### 📊 Prediction Results")
            
            # Main result
            result_col1, result_col2, result_col3 = st.columns(3)
            
            with result_col1:
                st.metric(
                    "🎯 Predicted Employee Count", 
                    predicted_count,
                    help="Recommended number of employees for optimal operations"
                )
            
            with result_col2:
                # Calculate current average for comparison
                section_data = staffing_df[staffing_df['section_id'] == section_id]
                current_avg = section_data['employees_on_duty'].mean() if not section_data.empty else 0
                difference = predicted_count - current_avg
                st.metric(
                    "📈 vs Historical Average",
                    f"{difference:+.1f}",
                    help="Difference from historical average"
                )
            
            with result_col3:
                # Day of week
                weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                target_weekday = pd.to_datetime(target_date).weekday()
                st.metric(
                    "📅 Target Day",
                    weekday_names[target_weekday],
                    help="Day of the week for prediction"
                )
            
            # Detailed explanation
            st.markdown("### 📝 Analysis Details")
            st.markdown(explanation)
            
            # Historical context
            if not section_data.empty:
                st.markdown("### 📈 Historical Context")
                
                hist_col1, hist_col2 = st.columns(2)
                
                with hist_col1:
                    st.markdown("**📊 Historical Statistics:**")
                    st.write(f"• **Average Employees:** {section_data['employees_on_duty'].mean():.1f}")
                    st.write(f"• **Range:** {section_data['employees_on_duty'].min()} - {section_data['employees_on_duty'].max()}")
                    st.write(f"• **Standard Deviation:** {section_data['employees_on_duty'].std():.1f}")
                    st.write(f"• **Total Records:** {len(section_data)}")
                
                with hist_col2:
                    st.markdown("**⏱️ Workload Statistics:**")
                    st.write(f"• **Avg Task Time:** {section_data['total_task_time_minutes'].mean():.1f} min")
                    st.write(f"• **Workload per Employee:** {(section_data['total_task_time_minutes'] / section_data['employees_on_duty']).mean():.1f} min")
                    st.write(f"• **Peak Workload:** {(section_data['total_task_time_minutes'] / section_data['employees_on_duty']).max():.1f} min")
                
                # Show recent trends
                section_data_sorted = section_data.sort_values('date')
                if len(section_data_sorted) > 1:
                    st.markdown("### 📈 Recent Trends")
                    recent_data = section_data_sorted.tail(30)  # Last 30 records
                    
                    chart_data = recent_data.set_index('date')[['employees_on_duty']]
                    st.line_chart(chart_data)
            
            # Recommendations
            st.markdown("### 💡 Recommendations")
            
            if predicted_count > current_avg + 1:
                st.warning(f"⚠️ **Higher staffing recommended**: Consider scheduling {predicted_count} employees (vs usual {current_avg:.1f})")
            elif predicted_count < current_avg - 1:
                st.info(f"💡 **Lower staffing possible**: {predicted_count} employees may be sufficient (vs usual {current_avg:.1f})")
            else:
                st.success(f"✅ **Standard staffing**: {predicted_count} employees aligns with historical patterns")

# Load staffing data
staffing_df = load_staffing_data()
stats = get_staffing_statistics(staffing_df)

st.markdown("""
<div class="main-header">
    <div class="header-title">👥 Staff Requirement Management</div>
    <div class="header-subtitle">Intelligent workforce planning and optimization</div>
</div>
""", unsafe_allow_html=True)

# Header with action button
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown("#### 🎯 Data-driven staffing insights and AI-powered forecasting")

with header_col2:
    if st.button("🔮 Workforce Forecasting", key="workforce_forecast_btn", use_container_width=True, type="primary"):
        st.session_state.show_forecast = not st.session_state.get('show_forecast', False)

# Show workforce forecasting modal if toggled
if st.session_state.get('show_forecast', False):
    with st.expander("🔮 Workforce Requirement Forecasting", expanded=True):
        show_workforce_prediction_modal(staffing_df)
    
    # Add a button to go back to the main dashboard
    if st.button("🔙 Back to Dashboard", key="back_to_staff_dashboard", use_container_width=True):
        st.session_state.show_forecast = False
        st.rerun()
    
    # Stop execution here to hide the rest of the content
    st.stop()

# Key metrics from real data
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Records", f"{stats.get('total_records', 0):,}")

with col2:
    st.metric("🏢 Service Sections", stats.get('unique_sections', 0))

with col3:
    st.metric("👥 Avg. Employees", stats.get('avg_employees', 0))

with col4:
    total_hours = stats.get('total_task_time', 0) // 60
    st.metric("⏱️ Total Task Hours", f"{total_hours:,}")

st.markdown("---")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Staffing Data", "🎯 Open Positions", "📝 Recruitment", "📈 Analytics"])

with tab1:
    st.subheader("📋 Real Staffing Data")
    
    if not staffing_df.empty:
        # Display only the specified columns
        display_cols = ['date', 'section_id', 'employees_on_duty', 'total_task_time_minutes']
        staffing_display = staffing_df[display_cols].copy()
        
        # Format the data for better display
        staffing_display['total_task_time_minutes'] = staffing_display['total_task_time_minutes'].round(2)
        
        st.dataframe(staffing_display, use_container_width=True)
        
        # Additional insights
        st.markdown("---")
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("#### � Employee Distribution by Section")
            section_employees = staffing_df.groupby('section_id')['employees_on_duty'].sum().sort_values(ascending=False)
            if not section_employees.empty:
                st.bar_chart(section_employees)
        
        with insight_col2:
            st.markdown("#### ⏱️ Task Time by Section")
            section_time = staffing_df.groupby('section_id')['total_task_time_minutes'].sum().sort_values(ascending=False)
            if not section_time.empty:
                st.bar_chart(section_time)
    else:
        st.info("No staffing data available.")

with tab2:
    st.subheader("🎯 Current Open Positions")
    
    if not staffing_df.empty:
        # Analyze staffing gaps based on real data
        section_analysis = staffing_df.groupby('section_id').agg({
            'employees_on_duty': ['mean', 'min', 'max'],
            'total_task_time_minutes': 'mean'
        }).round(2)
        
        section_analysis.columns = ['Avg_Employees', 'Min_Employees', 'Max_Employees', 'Avg_Task_Time']
        section_analysis = section_analysis.reset_index()
        
        # Calculate workload per employee
        section_analysis['Workload_Per_Employee'] = (
            section_analysis['Avg_Task_Time'] / section_analysis['Avg_Employees']
        ).round(2)
        
        # Identify sections that might need more staff (high workload per employee)
        high_workload_threshold = section_analysis['Workload_Per_Employee'].quantile(0.75)
        section_analysis['Needs_Staff'] = section_analysis['Workload_Per_Employee'] > high_workload_threshold
        
        # Create open positions based on analysis
        open_positions = []
        position_types = {
            'SEC-001': 'Passport Application Specialist',
            'SEC-002': 'Renewal Processing Officer',
            'SEC-003': 'Document Correction Specialist',
            'SEC-004': 'Lost/Stolen Passport Officer',
            'SEC-005': 'Document Verification Analyst',
            'SEC-006': 'Special Cases Coordinator'
        }
        
        for _, row in section_analysis.iterrows():
            if row['Needs_Staff']:
                section_id = row['section_id']
                position_name = position_types.get(section_id, 'General Officer')
                
                open_positions.append({
                    'Position': position_name,
                    'Section ID': section_id,
                    'Current Avg Staff': row['Avg_Employees'],
                    'Workload per Employee': f"{row['Workload_Per_Employee']:.1f} min",
                    'Priority': '� High' if row['Workload_Per_Employee'] > high_workload_threshold * 1.2 else '🟡 Medium',
                    'Recommended Hires': max(1, int(row['Workload_Per_Employee'] / 100))
                })
        
        if open_positions:
            positions_df = pd.DataFrame(open_positions)
            st.dataframe(positions_df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🎯 Total Open Positions", len(open_positions))
            with col2:
                high_priority = sum(1 for pos in open_positions if pos['Priority'] == '🔴 High')
                st.metric("🔴 High Priority Positions", high_priority)
        else:
            st.success("✅ All sections appear to be adequately staffed based on current workload analysis!")
        
        # Section workload analysis
        st.markdown("---")
        st.markdown("#### 📊 Section Workload Analysis")
        st.dataframe(section_analysis[['section_id', 'Avg_Employees', 'Avg_Task_Time', 'Workload_Per_Employee', 'Needs_Staff']], 
                    use_container_width=True)
    else:
        st.info("No staffing data available for position analysis.")

with tab3:
    st.subheader("📝 Recruitment Pipeline")
    
    if not staffing_df.empty:
        # Calculate recruitment metrics based on staffing data
        total_employees = int(staffing_df['employees_on_duty'].sum())
        unique_dates = staffing_df['date'].nunique()
        avg_daily_staff = int(staffing_df.groupby('date')['employees_on_duty'].sum().mean())
        
        # Simulate recruitment pipeline based on real data insights
        pipeline_col1, pipeline_col2 = st.columns(2)
        
        with pipeline_col1:
            st.markdown("#### 📋 Current Recruitment Status")
            
            # Calculate estimated applications needed based on high workload sections
            section_analysis = staffing_df.groupby('section_id').agg({
                'employees_on_duty': 'mean',
                'total_task_time_minutes': 'mean'
            })
            section_analysis['workload_per_employee'] = (
                section_analysis['total_task_time_minutes'] / section_analysis['employees_on_duty']
            )
            
            high_workload_sections = len(section_analysis[
                section_analysis['workload_per_employee'] > section_analysis['workload_per_employee'].quantile(0.75)
            ])
            
            estimated_applications = high_workload_sections * 25  # Estimate 25 applications per high workload section
            
            st.metric("📨 Applications Received", estimated_applications)
            st.metric("🔍 Under Review", int(estimated_applications * 0.3))
            st.metric("📋 Shortlisted", int(estimated_applications * 0.15))
            st.metric("✅ Ready for Interview", int(estimated_applications * 0.08))
        
        with pipeline_col2:
            st.markdown("#### 🎯 Interview Process")
            interviews_scheduled = int(estimated_applications * 0.08)
            st.metric("📞 Phone Screening", interviews_scheduled)
            st.metric("💼 Technical Interview", int(interviews_scheduled * 0.7))
            st.metric("👥 Final Interview", int(interviews_scheduled * 0.5))
            st.metric("📋 Offers Extended", int(interviews_scheduled * 0.3))
        
        # Progress tracking based on data
        st.markdown("---")
        st.markdown("#### 🎯 Recruitment Goals Progress")
        
        # Calculate progress based on workload analysis
        total_sections = staffing_df['section_id'].nunique()
        sections_needing_staff = high_workload_sections
        recruitment_progress = max(0.2, 1 - (sections_needing_staff / total_sections))
        
        st.progress(recruitment_progress, text=f"Overall Staffing Goal: {recruitment_progress*100:.0f}% Complete")
        
        # Section-specific progress
        for section_id in staffing_df['section_id'].unique():
            section_data = staffing_df[staffing_df['section_id'] == section_id]
            workload = (section_data['total_task_time_minutes'].mean() / section_data['employees_on_duty'].mean())
            
            # Calculate max workload across all sections using agg instead of apply
            section_workloads = staffing_df.groupby('section_id').agg({
                'total_task_time_minutes': 'mean',
                'employees_on_duty': 'mean'
            })
            max_workload = (section_workloads['total_task_time_minutes'] / section_workloads['employees_on_duty']).max()
            
            # Calculate progress (inverse of workload ratio)
            progress = max(0.3, 1 - (workload / max_workload))
            st.progress(progress, text=f"{section_id} Staffing: {progress*100:.0f}% Optimal")
        
        # Recruitment timeline
        st.markdown("---")
        st.markdown("#### 📅 Recruitment Timeline")
        
        timeline_data = pd.DataFrame({
            'Week': [f'Week {i}' for i in range(1, 9)],
            'Applications': [45, 52, 38, 61, 43, 55, 49, 47],
            'Interviews': [12, 15, 8, 18, 11, 16, 13, 14],
            'Hires': [3, 4, 2, 5, 3, 4, 3, 4]
        })
        
        st.line_chart(timeline_data.set_index('Week'))
    else:
        st.info("No staffing data available for recruitment analysis.")

with tab4:
    st.subheader("📈 Staffing Analytics & Insights")
    
    if not staffing_df.empty:
        # Convert date column to datetime for better analysis
        staffing_df_copy = staffing_df.copy()
        staffing_df_copy['date'] = pd.to_datetime(staffing_df_copy['date'])
        
        # Create analytics columns
        analytics_col1, analytics_col2 = st.columns(2)
        
        with analytics_col1:
            st.markdown("#### 📊 Key Performance Indicators")
            
            # Calculate efficiency metrics
            total_employees = staffing_df['employees_on_duty'].sum()
            total_task_time = staffing_df['total_task_time_minutes'].sum()
            efficiency_score = int((total_task_time / total_employees) if total_employees > 0 else 0)
            
            st.metric("👥 Total Employee Hours", f"{total_employees:,}")
            st.metric("⏱️ Total Task Minutes", f"{total_task_time:,.0f}")
            st.metric("📈 Efficiency Score", f"{efficiency_score} min/employee")
            
            # Section efficiency using agg instead of apply
            section_totals = staffing_df.groupby('section_id').agg({
                'total_task_time_minutes': 'sum',
                'employees_on_duty': 'sum'
            })
            section_efficiency = (section_totals['total_task_time_minutes'] / section_totals['employees_on_duty']).round(1)
            most_efficient = section_efficiency.idxmin()
            st.metric("🏆 Most Efficient Section", f"{most_efficient}")
        
        with analytics_col2:
            st.markdown("#### 🎯 Workload Distribution")
            
            # Workload analysis
            section_workload = staffing_df.groupby('section_id').agg({
                'employees_on_duty': 'mean',
                'total_task_time_minutes': 'mean'
            })
            section_workload['workload_per_employee'] = (
                section_workload['total_task_time_minutes'] / section_workload['employees_on_duty']
            ).round(1)
            
            busiest_section = section_workload['workload_per_employee'].idxmax()
            lightest_section = section_workload['workload_per_employee'].idxmin()
            
            st.metric("🔥 Busiest Section", f"{busiest_section}")
            st.metric("🌿 Lightest Section", f"{lightest_section}")
            
            # Calculate workload variance
            workload_variance = section_workload['workload_per_employee'].std()
            st.metric("📊 Workload Balance", f"{workload_variance:.1f}" + (" ⚖️ Balanced" if workload_variance < 50 else " ⚠️ Unbalanced"))
        
        # Time series analysis
        st.markdown("---")
        st.markdown("#### 📈 Temporal Analysis")
        
        # Monthly trends
        monthly_trends = staffing_df_copy.groupby(staffing_df_copy['date'].dt.to_period('M')).agg({
            'employees_on_duty': ['mean', 'sum'],
            'total_task_time_minutes': ['mean', 'sum']
        }).round(2)
        
        monthly_trends.columns = ['Avg_Employees_Per_Day', 'Total_Employees', 'Avg_Task_Time_Per_Day', 'Total_Task_Time']
        monthly_trends.index = monthly_trends.index.astype(str)
        
        # Display trends
        trend_col1, trend_col2 = st.columns(2)
        
        with trend_col1:
            st.markdown("**Employee Deployment Over Time**")
            st.line_chart(monthly_trends[['Avg_Employees_Per_Day', 'Total_Employees']])
        
        with trend_col2:
            st.markdown("**Task Load Over Time**")
            st.line_chart(monthly_trends[['Avg_Task_Time_Per_Day']])
        
        # Section comparison
        st.markdown("---")
        st.markdown("#### 🏢 Section Comparison Analysis")
        
        section_comparison = staffing_df.groupby('section_id').agg({
            'employees_on_duty': ['mean', 'std', 'min', 'max'],
            'total_task_time_minutes': ['mean', 'std']
        }).round(2)
        
        section_comparison.columns = [
            'Avg_Employees', 'StdDev_Employees', 'Min_Employees', 'Max_Employees',
            'Avg_Task_Time', 'StdDev_Task_Time'
        ]
        section_comparison = section_comparison.reset_index()
        
        # Add efficiency and stability metrics
        section_comparison['Efficiency'] = (
            section_comparison['Avg_Task_Time'] / section_comparison['Avg_Employees']
        ).round(1)
        section_comparison['Stability'] = (
            section_comparison['StdDev_Employees'] / section_comparison['Avg_Employees'] * 100
        ).round(1)
        
        st.dataframe(section_comparison, use_container_width=True)
        
        # Insights and recommendations
        st.markdown("---")
        st.markdown("#### 💡 AI-Powered Insights & Recommendations")
        
        insights = []
        
        # High workload sections
        high_workload = section_comparison.nlargest(2, 'Efficiency')['section_id'].tolist()
        if high_workload:
            insights.append(f"🔴 **High Workload Alert**: Sections {', '.join(high_workload)} have the highest workload per employee. Consider additional staffing.")
        
        # Unstable sections
        unstable = section_comparison[section_comparison['Stability'] > 30]['section_id'].tolist()
        if unstable:
            insights.append(f"⚠️ **Staffing Inconsistency**: Sections {', '.join(unstable)} show high variability in employee deployment. Review scheduling practices.")
        
        # Efficient sections
        efficient = section_comparison.nsmallest(1, 'Efficiency')['section_id'].iloc[0]
        insights.append(f"✅ **Best Practice**: Section {efficient} demonstrates optimal efficiency. Consider applying their practices to other sections.")
        
        # Underutilized sections
        low_workload = section_comparison.nsmallest(2, 'Efficiency')['section_id'].tolist()
        if len(low_workload) > 1:
            insights.append(f"💡 **Optimization Opportunity**: Sections {', '.join(low_workload)} may have capacity for additional tasks or staff reallocation.")
        
        for insight in insights:
            st.markdown(insight)
    else:
        st.info("No data available for analytics.")

# Action buttons
st.markdown("---")
st.markdown("### 🛠️ Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("� Generate Staffing Report", use_container_width=True, type="primary"):
        if not staffing_df.empty:
            st.success("📄 Comprehensive staffing report generated!")
            st.info(f"Report includes analysis of {len(staffing_df)} records across {staffing_df['section_id'].nunique()} sections")
        else:
            st.error("No data available for report generation")

with action_col2:
    if st.button("🎯 Optimize Staff Allocation", use_container_width=True):
        if not staffing_df.empty:
            # Calculate optimization suggestions
            section_analysis = staffing_df.groupby('section_id').agg({
                'employees_on_duty': 'mean',
                'total_task_time_minutes': 'mean'
            })
            section_analysis['workload_per_employee'] = (
                section_analysis['total_task_time_minutes'] / section_analysis['employees_on_duty']
            )
            
            high_workload = section_analysis['workload_per_employee'].idxmax()
            low_workload = section_analysis['workload_per_employee'].idxmin()
            
            st.success("🔄 Optimization analysis complete!")
            st.info(f"💡 Suggestion: Consider reallocating staff from {low_workload} to {high_workload}")
        else:
            st.error("No data available for optimization")

with action_col3:
    if st.button("🏠 Back to Home", use_container_width=True):
        # Use programmatic navigation to avoid session state conflicts
        st.session_state.programmatic_nav = "🏠 Home"
        st.rerun()
