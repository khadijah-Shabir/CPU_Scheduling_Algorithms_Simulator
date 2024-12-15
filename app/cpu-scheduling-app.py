import streamlit as st
import pandas as pd
import numpy as np

# Import scheduling algorithm modules
from fcfs import fcfs_scheduling
from sjf import sjf_scheduling
from priority import priority_scheduling
from round_robin import round_robin_scheduling

# Page configuration
st.set_page_config(page_title="CPU Scheduling Simulator", page_icon=":computer:")

def main():
    # Initialize session state variables
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'selected_algorithm' not in st.session_state:
        st.session_state.selected_algorithm = None
    if 'processes' not in st.session_state:
        st.session_state.processes = []

    # Routing based on current page
    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'input':
        input_page()
    elif st.session_state.current_page == 'process_table':
        process_table_page()
    elif st.session_state.current_page == 'simulation':
        simulation_page()

def home_page():
    st.title("Welcome to CPU Scheduling Algorithms Simulator")
    
    # Scheduling Algorithms
    algorithms = [
        "First Come First Serve (FCFS)",
        "Shortest Job First (Non-Preemptive)",
        "Shortest Job First (Preemptive)",
        "Priority Scheduling (Non-Preemptive)",
        "Priority Scheduling (Preemptive)",
        "Round Robin"
    ]
    
    # Algorithm Selection
    st.write("Select a Scheduling Algorithm:")
    selected_algo = st.radio("Choose an Algorithm", algorithms)
    
    # Confirm Button
    if st.button("Proceed to Input"):
        # Map selected algorithm to a simplified identifier
        algo_mapping = {
            "First Come First Serve (FCFS)": "FCFS",
            "Shortest Job First (Non-Preemptive)": "SJF_NP",
            "Shortest Job First (Preemptive)": "SJF_P",
            "Priority Scheduling (Non-Preemptive)": "PRIORITY_NP",
            "Priority Scheduling (Preemptive)": "PRIORITY_P",
            "Round Robin": "RR"
        }
        
        st.session_state.selected_algorithm = algo_mapping[selected_algo]
        st.session_state.current_page = 'input'


def input_page():
    st.title(f"Input for {st.session_state.selected_algorithm}")
    
    # Number of Processes
    num_processes = st.number_input("Enter Number of Processes", min_value=1, max_value=10, value=3)
    
    # Prepare process input form based on algorithm
    processes = []
    for i in range(num_processes):
        process = {"Process": f"P{i+1}"}
        
        # Burst Time (Common for all)
        process['Burst Time'] = st.number_input(f"Enter Burst Time for P{i+1}", min_value=1)
        
        # Conditional inputs based on algorithm
        if st.session_state.selected_algorithm in ['SJF_NP', 'SJF_P', 'PRIORITY_NP', 'PRIORITY_P']:
            process['Arrival Time'] = st.number_input(f"Enter Arrival Time for P{i+1}", min_value=0)
        
        if st.session_state.selected_algorithm in ['PRIORITY_NP', 'PRIORITY_P']:
            process['Priority'] = st.number_input(f"Enter Priority for P{i+1}", min_value=1)
        
        processes.append(process)
    
    # Add Processes Button
    if st.button("Add Processes"):
        st.session_state.processes = processes
        st.session_state.current_page = 'process_table'
       

def process_table_page():
    st.title(f"Process Table for {st.session_state.selected_algorithm}")
    
    # Create DataFrame
    df = pd.DataFrame(st.session_state.processes)
    st.dataframe(df)
    
    # Simulate Button
    if st.button("Start Simulation"):
        st.session_state.current_page = 'simulation'
      

def simulation_page():
    st.title(f"Simulation Results - {st.session_state.selected_algorithm}")
    
    # Call appropriate scheduling algorithm based on selection
    if st.session_state.selected_algorithm == 'FCFS':
        result = fcfs_scheduling(st.session_state.processes)
    elif st.session_state.selected_algorithm == 'SJF_NP':
        result = sjf_scheduling(st.session_state.processes, preemptive=False)
    # Add other algorithm calls similarly
    
    # Display Results
    st.write("Simulation Results:")
    st.write(f"Average Waiting Time: {result['avg_waiting_time']}")
    st.write(f"Average Turnaround Time: {result['avg_turnaround_time']}")
    
    # Gantt Chart
    st.write("Gantt Chart")
    # Implement Gantt chart visualization
    
    # Restart Option
    if st.button("Start Over"):
        st.session_state.current_page = 'home'
        st.session_state.selected_algorithm = None
        st.session_state.processes = []
  

if __name__ == "__main__":
    main()
