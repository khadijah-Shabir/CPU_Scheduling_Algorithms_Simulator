import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(page_title="CPU Process Scheduler", page_icon="🖥️", layout="wide")

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
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("CPU Process Scheduler Visualization")
st.markdown("""
    This tool helps you understand various CPU scheduling algorithms through interactive
    visualization. Add processes, select an algorithm, and see the results in real-time.
""")

# Sidebar for input and configuration
with st.sidebar:
    st.header("Configuration")
    
    algorithm = st.selectbox(
        "Select Scheduling Algorithm",
        [
            "First Come First Serve (FCFS)",
            "Shortest Job First (SJF)",
            "Shortest Remaining Time First (SRTF)",
            "Round Robin (RR)",
            "Priority (Non-Preemptive)",
            "Priority (Preemptive)"
        ]
    )
    
    if algorithm == "Round Robin (RR)":
        time_quantum = st.number_input("Time Quantum", min_value=1, value=2)
    
    context_switch_time = st.number_input("Context Switch Time", min_value=0, value=0)

# Initialize session state for processes
if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame(columns=['Process ID', 'Arrival Time', 'Burst Time', 'Priority'])

# Process input form
st.header("Add Process")
with st.form("process_input_form"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        process_id = st.text_input("Process ID")
    with col2:
        arrival_time = st.number_input("Arrival Time", min_value=0)
    with col3:
        burst_time = st.number_input("Burst Time", min_value=1)
    with col4:
        priority = st.number_input("Priority", min_value=1)
    
    submitted = st.form_submit_button("Add Process")
    if submitted:
        new_process = pd.DataFrame({
            'Process ID': [process_id],
            'Arrival Time': [arrival_time],
            'Burst Time': [burst_time],
            'Priority': [priority]
        })
        st.session_state.processes = pd.concat([st.session_state.processes, new_process], ignore_index=True)

# Display and edit processes
st.subheader("Current Processes")
edited_df = st.data_editor(
    st.session_state.processes,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
)
st.session_state.processes = edited_df

if st.button("Clear All Processes"):
    st.session_state.processes = pd.DataFrame(columns=['Process ID', 'Arrival Time', 'Burst Time', 'Priority'])
    st.rerun()

# Scheduling algorithms
def fcfs(processes):
    processes = processes.sort_values('Arrival Time')
    current_time = 0
    schedule = []
    
    for _, process in processes.iterrows():
        if current_time < process['Arrival Time']:
            current_time = process['Arrival Time']
        
        start_time = current_time
        end_time = current_time + process['Burst Time']
        
        schedule.append({
            'Task': process['Process ID'],
            'Start': start_time,
            'Finish': end_time,
            'Resource': 'CPU'
        })
        
        current_time = end_time + context_switch_time
    
    return pd.DataFrame(schedule)

def sjf(processes):
    processes = processes.sort_values('Arrival Time')
    current_time = 0
    remaining_processes = processes.copy()
    schedule = []
    
    while not remaining_processes.empty:
        available_processes = remaining_processes[remaining_processes['Arrival Time'] <= current_time]
        
        if available_processes.empty:
            current_time = remaining_processes['Arrival Time'].min()
            continue
        
        next_process = available_processes.loc[available_processes['Burst Time'].idxmin()]
        
        start_time = current_time
        end_time = current_time + next_process['Burst Time']
        
        schedule.append({
            'Task': next_process['Process ID'],
            'Start': start_time,
            'Finish': end_time,
            'Resource': 'CPU'
        })
        
        current_time = end_time + context_switch_time
        remaining_processes = remaining_processes[remaining_processes['Process ID'] != next_process['Process ID']]
    
    return pd.DataFrame(schedule)

def srtf(processes):
    processes = processes.copy()
    processes['Remaining Time'] = processes['Burst Time']
    current_time = 0
    schedule = []
    
    while not processes.empty:
        available_processes = processes[processes['Arrival Time'] <= current_time]
        
        if available_processes.empty:
            current_time = processes['Arrival Time'].min()
            continue
        
        next_process = available_processes.loc[available_processes['Remaining Time'].idxmin()]
        
        start_time = current_time
        run_time = min(1, next_process['Remaining Time'])  # Run for 1 time unit or until completion
        end_time = current_time + run_time
        
        schedule.append({
            'Task': next_process['Process ID'],
            'Start': start_time,
            'Finish': end_time,
            'Resource': 'CPU'
        })
        
        current_time = end_time
        processes.loc[next_process.name, 'Remaining Time'] -= run_time
        
        if processes.loc[next_process.name, 'Remaining Time'] == 0:
            processes = processes[processes['Process ID'] != next_process['Process ID']]
        
        current_time += context_switch_time
    
    return pd.DataFrame(schedule)

def round_robin(processes, time_quantum):
    processes = processes.copy()
    processes['Remaining Time'] = processes['Burst Time']
    current_time = 0
    schedule = []
    
    while not processes.empty:
        for index, process in processes.iterrows():
            if process['Arrival Time'] <= current_time:
                start_time = current_time
                run_time = min(time_quantum, process['Remaining Time'])
                end_time = current_time + run_time
                
                schedule.append({
                    'Task': process['Process ID'],
                    'Start': start_time,
                    'Finish': end_time,
                    'Resource': 'CPU'
                })
                
                current_time = end_time
                processes.loc[index, 'Remaining Time'] -= run_time
                
                if processes.loc[index, 'Remaining Time'] == 0:
                    processes = processes.drop(index)
                
                current_time += context_switch_time
        
        if processes.empty:
            break
        
        current_time = max(current_time, processes['Arrival Time'].min())
    
    return pd.DataFrame(schedule)

def priority_non_preemptive(processes):
    processes = processes.sort_values('Arrival Time')
    current_time = 0
    remaining_processes = processes.copy()
    schedule = []
    
    while not remaining_processes.empty:
        available_processes = remaining_processes[remaining_processes['Arrival Time'] <= current_time]
        
        if available_processes.empty:
            current_time = remaining_processes['Arrival Time'].min()
            continue
        
        next_process = available_processes.loc[available_processes['Priority'].idxmin()]
        
        start_time = current_time
        end_time = current_time + next_process['Burst Time']
        
        schedule.append({
            'Task': next_process['Process ID'],
            'Start': start_time,
            'Finish': end_time,
            'Resource': 'CPU'
        })
        
        current_time = end_time + context_switch_time
        remaining_processes = remaining_processes[remaining_processes['Process ID'] != next_process['Process ID']]
    
    return pd.DataFrame(schedule)

def priority_preemptive(processes):
    processes = processes.copy()
    processes['Remaining Time'] = processes['Burst Time']
    current_time = 0
    schedule = []
    
    while not processes.empty:
        available_processes = processes[processes['Arrival Time'] <= current_time]
        
        if available_processes.empty:
            current_time = processes['Arrival Time'].min()
            continue
        
        next_process = available_processes.loc[available_processes['Priority'].idxmin()]
        
        start_time = current_time
        run_time = 1  # Run for 1 time unit
        end_time = current_time + run_time
        
        schedule.append({
            'Task': next_process['Process ID'],
            'Start': start_time,
            'Finish': end_time,
            'Resource': 'CPU'
        })
        
        current_time = end_time
        processes.loc[next_process.name, 'Remaining Time'] -= run_time
        
        if processes.loc[next_process.name, 'Remaining Time'] == 0:
            processes = processes[processes['Process ID'] != next_process['Process ID']]
        
        current_time += context_switch_time
    
    return pd.DataFrame(schedule)

# Function to create Gantt chart
def create_gantt_chart(schedule):
    fig = ff.create_gantt(schedule, index_col='Resource', show_colorbar=True, group_tasks=True)
    fig.update_layout(title="Process Execution Gantt Chart", xaxis_title="Time", height=400)
    return fig

# Calculate schedule based on selected algorithm
if st.button("Calculate Schedule"):
    if st.session_state.processes.empty:
        st.warning("Please add processes before calculating the schedule.")
    else:
        if algorithm == "First Come First Serve (FCFS)":
            schedule = fcfs(st.session_state.processes)
        elif algorithm == "Shortest Job First (SJF)":
            schedule = sjf(st.session_state.processes)
        elif algorithm == "Shortest Remaining Time First (SRTF)":
            schedule = srtf(st.session_state.processes)
        elif algorithm == "Round Robin (RR)":
            schedule = round_robin(st.session_state.processes, time_quantum)
        elif algorithm == "Priority (Non-Preemptive)":
            schedule = priority_non_preemptive(st.session_state.processes)
        elif algorithm == "Priority (Preemptive)":
            schedule = priority_preemptive(st.session_state.processes)
        
        # Display Gantt chart
        st.plotly_chart(create_gantt_chart(schedule), use_container_width=True)
        
        # Calculate and display metrics
        completion_times = schedule.groupby('Task')['Finish'].max()
        arrival_times = st.session_state.processes.set_index('Process ID')['Arrival Time']
        burst_times = st.session_state.processes.set_index('Process ID')['Burst Time']
        
        turnaround_times = completion_times - arrival_times
        waiting_times = turnaround_times - burst_times
        
        metrics = pd.DataFrame({
            'Completion Time': completion_times,
            'Turnaround Time': turnaround_times,
            'Waiting Time': waiting_times
        })
        
        st.subheader("Process Metrics")
        st.dataframe(metrics)
        
        # Display average metrics
        st.subheader("Average Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg. Turnaround Time", f"{turnaround_times.mean():.2f}")
        col2.metric("Avg. Waiting Time", f"{waiting_times.mean():.2f}")
        col3.metric("Throughput", f"{len(schedule) / schedule['Finish'].max():.2f} processes/unit time")
        
        # Comparison chart
        st.subheader("Metrics Comparison")
        comparison_df = pd.melt(metrics.reset_index(), id_vars=['Task'], var_name='Metric', value_name='Time')
        fig = px.bar(comparison_df, x='Task', y='Time', color='Metric', barmode='group')
        fig.update_layout(title="Process Metrics Comparison", xaxis_title="Process", yaxis_title="Time")
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Created for educational purposes. Use this tool to understand CPU scheduling algorithms better.</p>
    </div>
""", unsafe_allow_html=True)
