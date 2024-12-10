import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="CPU Process Scheduler",
    page_icon="🖥️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton button {
        width: 100%;
    }
    .stSelectbox select {
        background-color: white;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("CPU Process Scheduler Visualization")
st.markdown("""
    This tool helps you understand various CPU scheduling algorithms through interactive
    visualization. Add processes, configure parameters, and see real-time results.
""")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    # Algorithm selection
    algorithm = st.selectbox(
        "Select Scheduling Algorithm",
        [
            "First Come First Serve (FCFS)",
            "Shortest Job First (SJF)",
            "Shortest Remaining Time First (SRTF)",
            "Round Robin (RR)",
            "Priority (Non-Preemptive)",
            "Priority (Preemptive)",
            "Longest Remaining Time First (LRTF)",
            "Highest Response Ratio Next (HRRN)"
        ]
    )
    
    # Time quantum for Round Robin
    if algorithm == "Round Robin (RR)":
        time_quantum = st.number_input("Time Quantum", min_value=1, value=2)
    
    # Context switch time
    context_switch_time = st.number_input("Context Switch Time", min_value=0, value=1)
    
    st.divider()
    
    # Instructions
    st.markdown("""
        ### Instructions:
        1. Select scheduling algorithm
        2. Add processes with arrival time and burst time
        3. Configure additional parameters if needed
        4. Click Calculate to see results
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Process input section
    st.subheader("Process Information")
    
    # Create a dataframe for processes
    if 'processes' not in st.session_state:
        st.session_state.processes = pd.DataFrame({
            'Process ID': ['P1'],
            'Arrival Time': [0],
            'Burst Time': [1],
            'Priority': [1]
        })
    
    # Edit processes in a data editor
    edited_df = st.data_editor(
        st.session_state.processes,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Process ID": st.column_config.TextColumn(
                "Process ID",
                help="Unique identifier for the process",
                width="medium",
            ),
            "Arrival Time": st.column_config.NumberColumn(
                "Arrival Time",
                help="Time at which process arrives",
                min_value=0,
                width="medium",
            ),
            "Burst Time": st.column_config.NumberColumn(
                "Burst Time",
                help="CPU time required by the process",
                min_value=1,
                width="medium",
            ),
            "Priority": st.column_config.NumberColumn(
                "Priority",
                help="Process priority (lower number = higher priority)",
                min_value=1,
                width="medium",
            ),
        }
    )
    
    st.session_state.processes = edited_df

with col2:
    # Statistics and metrics
    st.subheader("Process Statistics")
    metrics_df = pd.DataFrame({
        'Metric': ['Average Waiting Time', 'Average Turnaround Time', 
                  'Average Response Time', 'CPU Utilization'],
        'Value': ['0.0 ms', '0.0 ms', '0.0 ms', '0%']
    })
    st.dataframe(metrics_df, hide_index=True)

# Visualization section
st.subheader("Process Visualization")

# Tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["Gantt Chart", "Timeline", "Comparison Metrics"])

with tab1:
    # Sample Gantt chart
    df = pd.DataFrame([
        dict(Task="P1", Start=0, Finish=4, Resource="CPU"),
        dict(Task="P2", Start=4, Finish=8, Resource="CPU"),
        dict(Task="P3", Start=8, Finish=12, Resource="CPU"),
    ])
    
    fig = ff.create_gantt(df, colors=['#779ECB'], 
                         show_colorbar=True,
                         group_tasks=True, 
                         showgrid_x=True, 
                         showgrid_y=True)
    
    fig.update_layout(
        title="Process Execution Gantt Chart",
        xaxis_title="Time (ms)",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Timeline visualization
    timeline_fig = go.Figure()
    
    for idx, process in enumerate(['P1', 'P2', 'P3']):
        timeline_fig.add_trace(go.Scatter(
            x=[0, 4, 8, 12],
            y=[idx, idx, idx, idx],
            mode='lines+markers',
            name=process,
            line=dict(width=20)
        ))
    
    timeline_fig.update_layout(
        title="Process Timeline",
        xaxis_title="Time (ms)",
        yaxis_title="Process",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(timeline_fig, use_container_width=True)

with tab3:
    # Comparison metrics visualization
    metrics = {
        'Completion Time': [60, 45, 50],
        'Turn Around Time': [58, 42, 45],
        'Waiting Time': [48, 32, 35],
        'Response Time': [10, 8, 12]
    }
    
    comparison_df = pd.DataFrame(metrics)
    comparison_fig = px.bar(
        comparison_df, 
        barmode='group',
        title="Process Metrics Comparison"
    )
    
    comparison_fig.update_layout(
        xaxis_title="Metrics",
        yaxis_title="Time (ms)",
        height=400
    )
    
    st.plotly_chart(comparison_fig, use_container_width=True)

# Control buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Calculate", type="primary"):
        with st.spinner("Calculating..."):
            time.sleep(1)  # Simulate calculation
            st.success("Calculation completed!")

with col2:
    if st.button("Reset"):
        st.session_state.processes = pd.DataFrame({
            'Process ID': ['P1'],
            'Arrival Time': [0],
            'Burst Time': [1],
            'Priority': [1]
        })
        st.rerun()

with col3:
    if st.button("Animate"):
        with st.spinner("Animating process execution..."):
            time.sleep(1)  # Simulate animation
            st.info("Animation completed!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Created for educational purposes. Use this tool to understand CPU scheduling algorithms better.</p>
    </div>
""", unsafe_allow_html=True)
