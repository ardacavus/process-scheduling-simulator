import sys
import copy
from utils import read_input, print_metrics
# Import scheduling algorithms
from algorithms import schedule_fcfs, schedule_sjf, schedule_priority, schedule_rr

if __name__ == "__main__":
    # Default parameters
    input_file = "processes.txt"
    time_quantum = 3

    # Parse CLI arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    if len(sys.argv) > 2:
        try:
            time_quantum = int(sys.argv[2])
        except ValueError:
            print("Error: Time Quantum must be an integer.")
            sys.exit(1)

    print(f"Simulation started. Input: {input_file}, TQ: {time_quantum}")
    original_processes = read_input(input_file)

    # --- 1. FCFS (First-Come First-Served) ---
    fcfs_processes = copy.deepcopy(original_processes)
    schedule_fcfs(fcfs_processes)
    print_metrics(fcfs_processes, "FCFS")

    # --- 2. SJF (Shortest Job First) ---
    sjf_processes = copy.deepcopy(original_processes)
    schedule_sjf(sjf_processes)
    print_metrics(sjf_processes, "SJF")

    # --- 3. Priority Scheduling ---
    priority_processes = copy.deepcopy(original_processes)
    schedule_priority(priority_processes)
    print_metrics(priority_processes, "Priority")

    # --- 4. Round Robin ---
    rr_processes = copy.deepcopy(original_processes)
    schedule_rr(rr_processes, time_quantum)
    print_metrics(rr_processes, "Round Robin")