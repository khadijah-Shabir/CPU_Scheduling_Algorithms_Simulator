def priority_scheduling(processes, preemptive=False):
    """
    Perform Priority Scheduling
    
    :param processes: List of dictionaries containing process information
    :param preemptive: Boolean to determine preemptive or non-preemptive priority scheduling
    :return: Dictionary with scheduling results
    """
    # Sort processes by priority (lower number = higher priority)
    sorted_processes = sorted(processes, key=lambda x: x.get('Priority', 1))
    
    # Placeholder implementation
    result = {
        'avg_waiting_time': 0,
        'avg_turnaround_time': 0
    }
    
    return result

def test_priority():
    test_processes = [
        {'Process': 'P1', 'Arrival Time': 0, 'Burst Time': 10, 'Priority': 3},
        {'Process': 'P2', 'Arrival Time': 1, 'Burst Time': 5, 'Priority': 1},
        {'Process': 'P3', 'Arrival Time': 2, 'Burst Time': 8, 'Priority': 2}
    ]
    
    # Test Non-Preemptive Priority Scheduling
    result_np = priority_scheduling(test_processes, preemptive=False)
    
    # Test Preemptive Priority Scheduling
    result_p = priority_scheduling(test_processes, preemptive=True)

if __name__ == "__main__":
    test_priority()
