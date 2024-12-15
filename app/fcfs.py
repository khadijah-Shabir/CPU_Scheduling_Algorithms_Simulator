def fcfs_scheduling(processes):
    """
    Perform First Come First Serve (FCFS) Scheduling
    
    :param processes: List of dictionaries containing process information
    :return: Dictionary with scheduling results
    """
    # Sort processes based on their order (assuming they are in order of arrival)
    sorted_processes = sorted(processes, key=lambda x: processes.index(x))
    
    # Initialize variables
    current_time = 0
    waiting_times = []
    turnaround_times = []
    completion_times = []
    
    # Calculate times for each process
    for process in sorted_processes:
        # Waiting time is the current time
        waiting_time = current_time
        waiting_times.append(waiting_time)
        
        # Completion time
        current_time += process['Burst Time']
        completion_times.append(current_time)
        
        # Turnaround time is completion time - arrival time (0 for FCFS)
        turnaround_time = current_time
        turnaround_times.append(turnaround_time)
    
    # Calculate averages
    avg_waiting_time = sum(waiting_times) / len(waiting_times)
    avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
    
    # Prepare result
    result = {
        'processes': sorted_processes,
        'waiting_times': waiting_times,
        'turnaround_times': turnaround_times,
        'completion_times': completion_times,
        'avg_waiting_time': avg_waiting_time,
        'avg_turnaround_time': avg_turnaround_time
    }
    
    return result

# Optional: Add a sample test function
def test_fcfs():
    test_processes = [
        {'Process': 'P1', 'Burst Time': 10},
        {'Process': 'P2', 'Burst Time': 5},
        {'Process': 'P3', 'Burst Time': 8}
    ]
    
    result = fcfs_scheduling(test_processes)
    print("FCFS Scheduling Result:")
    print(f"Average Waiting Time: {result['avg_waiting_time']}")
    print(f"Average Turnaround Time: {result['avg_turnaround_time']}")

if __name__ == "__main__":
    test_fcfs()
