import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page navigation
if "page" not in st.session_state:
    st.session_state.page = 1

# Session storage for CRUD and simulation data
if "processes" not in st.session_state:
    st.session_state.processes = []
if "selected_algorithm" not in st.session_state:
    st.session_state.selected_algorithm = ""

def reset():
    st.session_state.page = 1
    st.session_state.processes = []
    st.session_state.selected_algorithm = ""

# Helper function to reset inputs
def reset_inputs():
    st.session_state.process_id = ""
    st.session_state.burst_time = ""
    st.session_state.arrival_time = ""
    st.session_state.priority = ""

# Helper function to calculate Gantt chart and metrics
def simulate_fcfs(processes):
    processes.sort(key=lambda x: x["Arrival Time"])
    current_time = 0
    waiting_times = []
    turnaround_times = []
    gantt_chart = []

    for process in processes:
        if current_time < process["Arrival Time"]:
            current_time = process["Arrival Time"]
        waiting_time = current_time - process["Arrival Time"]
        turnaround_time = waiting_time + process["Burst Time"]
        waiting_times.append(waiting_time)
        turnaround_times.append(turnaround_time)
        gantt_chart.append((process["Process ID"], current_time, current_time + process["Burst Time"]))
        current_time += process["Burst Time"]

    avg_waiting_time = sum(waiting_times) / len(processes)
    avg_turnaround_time = sum(turnaround_times) / len(processes)
    return gantt_chart, avg_waiting_time, avg_turnaround_time, waiting_times, turnaround_times

def display_gantt_chart(gantt_chart):
    fig, ax = plt.subplots(figsize=(10, 2))
    for idx, (pid, start, end) in enumerate(gantt_chart):
        ax.barh(0, end - start, left=start, height=0.5)
        ax.text((start + end) / 2, 0, pid, ha="center", va="center", color="white")
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title("Gantt Chart")
    st.pyplot(fig)

# Page 1: Welcome and Algorithm Selection
if st.session_state.page == 1:
    st.title("Welcome to CPU Scheduling Algorithms Simulator")

    st.subheader("Select a Scheduling Algorithm to Simulate")
    algorithms = [
        "First Come First Serve",
        "Shortest Job First (Non-Preemptive)",
        "Shortest Job First (Preemptive)",
        "Priority Scheduling (Non-Preemptive)",
        "Priority Scheduling (Preemptive)",
        "Round Robin",
    ]

    algorithm_choice = st.selectbox("Choose an Algorithm", algorithms, index=0)
    if st.button("Next"):
        st.session_state.selected_algorithm = algorithm_choice
        st.session_state.page = 2

# Page 2: Input Process Information
elif st.session_state.page == 2:
    st.title(f"Simulation: {st.session_state.selected_algorithm}")

    num_processes = st.number_input("Enter the number of processes to simulate:", min_value=1, step=1)

    if "process_id" not in st.session_state:
        reset_inputs()

    if num_processes > 0:
        with st.form("process_input_form"):
            st.subheader("Enter Process Information")
            for i in range(1, num_processes + 1):
                st.write(f"Process P{i}")
                st.number_input(f"Enter Burst Time of P{i}:", key=f"burst_time_{i}")
                st.number_input(f"Enter Arrival Time of P{i}:", key=f"arrival_time_{i}")
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.session_state.processes = [
                    {
                        "Process ID": f"P{i}",
                        "Burst Time": st.session_state[f"burst_time_{i}"],
                        "Arrival Time": st.session_state.get(f"arrival_time_{i}", 0),
                    }
                    for i in range(1, num_processes + 1)
                ]
                st.session_state.page = 3

# Page 3: Display and Edit Processes
elif st.session_state.page == 3:
    st.title(f"Simulation: {st.session_state.selected_algorithm}")

    if st.session_state.processes:
        st.write("### Current Processes")
        process_df = pd.DataFrame(st.session_state.processes)
        st.table(process_df)

        if st.button("Simulate Processes"):
            st.session_state.page = 4

# Page 4: Simulation Results
elif st.session_state.page == 4:
    st.title(f"Simulation Results: {st.session_state.selected_algorithm}")

    if st.session_state.selected_algorithm == "First Come First Serve":
        gantt_chart, avg_wt, avg_tat, wt, tat = simulate_fcfs(st.session_state.processes)
        st.write("### Gantt Chart")
        display_gantt_chart(gantt_chart)

        st.write("### Simulation Metrics")
        st.write(f"Average Waiting Time: {avg_wt:.2f}")
        st.write(f"Average Turnaround Time: {avg_tat:.2f}")

        st.write("### Waiting and Turnaround Time for Each Process")
        results_df = pd.DataFrame({
            "Process ID": [p["Process ID"] for p in st.session_state.processes],
            "Waiting Time": wt,
            "Turnaround Time": tat,
        })
        st.table(results_df)

    if st.button("Restart Simulation"):
        reset()
