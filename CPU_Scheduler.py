import streamlit as st
import pandas as pd

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
                if "Shortest Job First" in st.session_state.selected_algorithm or "Priority Scheduling" in st.session_state.selected_algorithm:
                    st.number_input(f"Enter Arrival Time of P{i}:", key=f"arrival_time_{i}")
                if "Priority Scheduling" in st.session_state.selected_algorithm:
                    st.number_input(f"Enter Priority of P{i}:", key=f"priority_{i}")

            submitted = st.form_submit_button("Submit")
            if submitted:
                st.session_state.processes = [
                    {
                        "Process ID": f"P{i}",
                        "Burst Time": st.session_state[f"burst_time_{i}"],
                        "Arrival Time": st.session_state.get(f"arrival_time_{i}", None),
                        "Priority": st.session_state.get(f"priority_{i}", None),
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

        st.write("### Modify Processes")
        option = st.selectbox("Choose an option", ["Add", "Delete", "Update"])

        if option == "Add":
            with st.form("add_form"):
                process_id = st.text_input("Enter Process ID:")
                burst_time = st.number_input("Enter Burst Time:", min_value=1)
                arrival_time = None
                priority = None

                if "Shortest Job First" in st.session_state.selected_algorithm or "Priority Scheduling" in st.session_state.selected_algorithm:
                    arrival_time = st.number_input("Enter Arrival Time:")
                if "Priority Scheduling" in st.session_state.selected_algorithm:
                    priority = st.number_input("Enter Priority:")

                submitted = st.form_submit_button("Add Process")
                if submitted:
                    st.session_state.processes.append(
                        {
                            "Process ID": process_id,
                            "Burst Time": burst_time,
                            "Arrival Time": arrival_time,
                            "Priority": priority,
                        }
                    )
                    st.experimental_rerun()

        elif option == "Delete":
            process_id = st.selectbox("Select Process to Delete", [p["Process ID"] for p in st.session_state.processes])
            if st.button("Delete Process"):
                st.session_state.processes = [p for p in st.session_state.processes if p["Process ID"] != process_id]
                st.experimental_rerun()

        elif option == "Update":
            process_id = st.selectbox("Select Process to Update", [p["Process ID"] for p in st.session_state.processes])
            process = next(p for p in st.session_state.processes if p["Process ID"] == process_id)
            with st.form("update_form"):
                burst_time = st.number_input("Update Burst Time:", value=process["Burst Time"])
                arrival_time = process["Arrival Time"]
                priority = process["Priority"]

                if arrival_time is not None:
                    arrival_time = st.number_input("Update Arrival Time:", value=arrival_time)
                if priority is not None:
                    priority = st.number_input("Update Priority:", value=priority)

                submitted = st.form_submit_button("Update Process")
                if submitted:
                    process.update(
                        {
                            "Burst Time": burst_time,
                            "Arrival Time": arrival_time,
                            "Priority": priority,
                        }
                    )
                    st.experimental_rerun()

        if st.button("Simulate Processes"):
            st.session_state.page = 4

# Page 4: Simulation Results
elif st.session_state.page == 4:
    st.title(f"Simulation Results: {st.session_state.selected_algorithm}")

    # Placeholder for Gantt chart and calculations
    st.write("### Gantt Chart")
    st.write("(Gantt Chart will be displayed here)")

    st.write("### Simulation Metrics")
    st.write("Average Waiting Time: (Calculated value)")
    st.write("Average Turnaround Time: (Calculated value)")

    st.write("### Waiting and Turnaround Time for Each Process")
    st.write("(Chart will be displayed here)")

    if st.button("Restart Simulation"):
        reset()
