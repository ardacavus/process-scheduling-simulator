import sys
import copy
from utils import read_input, print_metrics
# schedule_priority eklendi
from algorithms import schedule_fcfs, schedule_sjf, schedule_priority

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "processes.txt"

    original_processes = read_input(input_file)
    print(f"File loaded: {input_file} with {len(original_processes)} processes.")

    # 1. FCFS
    fcfs_processes = copy.deepcopy(original_processes)
    schedule_fcfs(fcfs_processes)
    print_metrics(fcfs_processes, "FCFS")

    # 2. SJF
    sjf_processes = copy.deepcopy(original_processes)
    schedule_sjf(sjf_processes)
    print_metrics(sjf_processes, "SJF")

    # 3. Priority
    priority_processes = copy.deepcopy(original_processes)
    schedule_priority(priority_processes)
    print_metrics(priority_processes, "Priority")