from collections import deque
from typing import List
from process import Process
from utils import print_gantt_chart


def schedule_fcfs(processes: List[Process]):
    """
    First-Come, First-Served (FCFS) Algorithm.
    Non-Preemptive: Processes are executed strictly by arrival order.
    """
    # Sort by arrival time to ensure chronological execution
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    gantt_chart = []

    print("\n--- Scheduling Algorithm: FCFS ---")

    for p in processes:
        # Handle Idle Time: If CPU is free before process arrives, jump time
        if current_time < p.arrival_time:
            current_time = p.arrival_time

        if p.start_time == -1:
            p.start_time = current_time

        # Execute process fully (Non-preemptive)
        gantt_chart.append((p.pid, current_time, current_time + p.burst_time))
        current_time += p.burst_time

        # Update metrics
        p.finish_time = current_time
        p.turnaround_time = p.finish_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

    print_gantt_chart(gantt_chart)
    return gantt_chart


def schedule_sjf(processes: List[Process]):
    """
    Shortest Job First (SJF) Algorithm - Non-Preemptive.
    Greedy Approach: Selects the waiting process with the smallest burst time.
    """
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    completed_processes = 0
    n = len(processes)
    gantt_chart = []

    print("\n--- Scheduling Algorithm: SJF ---")

    while completed_processes < n:
        # Filter processes that have arrived and are not yet completed
        ready_queue = [p for p in processes if p.arrival_time <= current_time and p.finish_time == 0]

        if not ready_queue:
            # If no process is ready, advance time to the next arrival
            remaining_processes = [p for p in processes if p.finish_time == 0]
            if remaining_processes:
                next_arrival = min(remaining_processes, key=lambda x: x.arrival_time).arrival_time
                current_time = next_arrival
            continue

        # Select process with minimum burst time
        current_process = min(ready_queue, key=lambda x: x.burst_time)

        start_time = current_time
        if current_process.start_time == -1:
            current_process.start_time = start_time

        current_time += current_process.burst_time

        current_process.finish_time = current_time
        current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

        gantt_chart.append((current_process.pid, start_time, current_time))
        completed_processes += 1

    print_gantt_chart(gantt_chart)
    return gantt_chart


def schedule_priority(processes: List[Process]):
    """
    Priority Scheduling - Non-Preemptive.
    Selects the process with the highest priority (Lowest integer value).
    """
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    completed_processes = 0
    n = len(processes)
    gantt_chart = []

    print("\n--- Scheduling Algorithm: Priority ---")

    while completed_processes < n:
        ready_queue = [p for p in processes if p.arrival_time <= current_time and p.finish_time == 0]

        if not ready_queue:
            remaining_processes = [p for p in processes if p.finish_time == 0]
            if remaining_processes:
                next_arrival = min(remaining_processes, key=lambda x: x.arrival_time).arrival_time
                current_time = next_arrival
            continue

        # Select process with minimum priority value (Higher Importance)
        current_process = min(ready_queue, key=lambda x: x.priority)

        start_time = current_time
        if current_process.start_time == -1:
            current_process.start_time = start_time

        current_time += current_process.burst_time

        current_process.finish_time = current_time
        current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

        gantt_chart.append((current_process.pid, start_time, current_time))
        completed_processes += 1

    print_gantt_chart(gantt_chart)
    return gantt_chart


def schedule_rr(processes: List[Process], time_quantum: int):
    """
    Round Robin (RR) Algorithm - Preemptive.
    Uses a FIFO queue to cycle through processes with a fixed Time Quantum.
    """
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    completed_processes = 0
    n = len(processes)
    gantt_chart = []

    queue = deque()
    process_idx = 0

    print(f"\n--- Scheduling Algorithm: Round Robin (TQ={time_quantum}) ---")

    while completed_processes < n:
        # Add newly arrived processes to the queue
        while process_idx < n and processes[process_idx].arrival_time <= current_time:
            queue.append(processes[process_idx])
            process_idx += 1

        if not queue:
            # Jump to next arrival if queue is empty
            if process_idx < n:
                current_time = processes[process_idx].arrival_time
                continue

        current_process = queue.popleft()

        if current_process.start_time == -1:
            current_process.start_time = current_time

        # Execute for Time Quantum or Remaining Time (whichever is smaller)
        time_to_run = min(current_process.remaining_time, time_quantum)

        gantt_chart.append((current_process.pid, current_time, current_time + time_to_run))

        current_time += time_to_run
        current_process.remaining_time -= time_to_run

        # Check for new arrivals during the execution window
        while process_idx < n and processes[process_idx].arrival_time <= current_time:
            queue.append(processes[process_idx])
            process_idx += 1

        if current_process.remaining_time == 0:
            # Process Completed
            current_process.finish_time = current_time
            current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed_processes += 1
        else:
            # Re-queue if not finished
            queue.append(current_process)

    print_gantt_chart(gantt_chart)
    return gantt_chart


def check_starvation(processes: List[Process], threshold: int = 50):
    """
    Checks if any process has waited longer than the threshold.
    Returns a list of starved process IDs.
    """
    starved_procs = []
    for p in processes:
        if p.waiting_time > threshold:
            starved_procs.append(f"{p.pid} (Wait: {p.waiting_time}ms)")

    return starved_procs