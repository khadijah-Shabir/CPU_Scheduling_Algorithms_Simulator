def sjf_scheduling(processes, preemptive=False):
    """
    Perform Shortest Job First (SJF) Scheduling
    
    :param processes: List of dictionaries containing process information
    :param preemptive: Boolean to determine preemptive or non-preemptive SJF
    :return: Dictionary with scheduling results
    """
    # Sort processes by arrival time
    sorted_processes = sorted(processes, key=lambda x: x.get('Arrival Time', 0))
    
    # Placeholder implementation
    result = {
        'avg_waiting_time': 0,
        'avg_turnaround_time': 0
    }
    
    return result

def test_sjf():
    test_processes = [
        {'Process': 'P1', 'Arrival Time': 0, 'Burst Time': 10},
        {'Process': 'P2', 'Arrival Time': 1, 'Burst Time': 5},
        {'Process': 'P3', 'Arrival Time': 2, 'Burst Time': 8}
    ]
    
    # Test Non-Preemptive SJF
    result_np = sjf_scheduling(test_processes, preemptive=False)
    
    # Test Preemptive SJF
    result_p = sjf_scheduling(test_processes, preemptive=True)

if __name__ == "__main__":
    test_sjf()
