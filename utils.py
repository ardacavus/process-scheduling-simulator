import sys
from typing import List
from process import Process


def read_input(filename: str) -> List[Process]:
    """
    Parses the input text file and generates a list of Process objects.
    Expected Format: Process_ID, Arrival_Time, Burst_Time, Priority
    """
    processes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Skip empty lines or comments
                if not line.strip() or line.startswith("#"):
                    continue

                parts = line.strip().split(',')
                if len(parts) >= 3:
                    pid = parts[0].strip()
                    arrival = int(parts[1].strip())
                    burst = int(parts[2].strip())
                    # Default priority to 0 if not specified
                    priority = int(parts[3].strip()) if len(parts) > 3 else 0

                    processes.append(Process(pid, arrival, burst, priority))

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except ValueError:
        print("Error: Invalid file format. Ensure time values are integers.")
        sys.exit(1)

    return processes


def print_metrics(processes: List[Process], algorithm_name: str):
    """
    Calculates and displays performance metrics (Turnaround, Waiting, Utilization).
    """
    total_turnaround = 0
    total_waiting = 0
    total_burst = 0

    print(f"\n{'Process':<10} | {'Finish':<8} | {'Turnaround':<12} | {'Waiting':<8}")
    print("-" * 46)

    for p in processes:
        print(f"{p.pid:<10} | {p.finish_time:<8} | {p.turnaround_time:<12} | {p.waiting_time:<8}")
        total_turnaround += p.turnaround_time
        total_waiting += p.waiting_time
        total_burst += p.burst_time

    if len(processes) > 0:
        avg_turnaround = total_turnaround / len(processes)
        avg_waiting = total_waiting / len(processes)

        # --- CPU UTILIZATION CALCULATION ---
        # Formula: (Total Burst Time / Total Simulation Duration) * 100

        last_finish_time = max(p.finish_time for p in processes)
        first_arrival = min(p.arrival_time for p in processes)
        total_duration = last_finish_time - first_arrival

        if total_duration > 0:
            utilization = (total_burst / total_duration) * 100
        else:
            utilization = 0.0

        print(f"\nAverage Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Waiting Time: {avg_waiting:.2f}")
        print(f"CPU Utilization: {utilization:.2f}%")


def print_gantt_chart(gantt_data: List[tuple]):
    """
    Visualizes the execution timeline in the console.
    Data Format: [(PID, Start, End), ...]
    """
    print("Gantt Chart: ", end="")
    for pid, start, end in gantt_data:
        print(f"[{start}]--{pid}--[{end}]", end="")
    print()