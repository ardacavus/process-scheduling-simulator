from collections import deque
from typing import List
from process import Process
from utils import print_gantt_chart


def schedule_fcfs(processes: List[Process]):
    """
    First-Come, First-Served (FCFS) Algoritması
    """
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    gantt_chart = []

    print("\n--- Scheduling Algorithm: FCFS ---")

    for p in processes:
        # Idle Time Kontrolü
        if current_time < p.arrival_time:
            current_time = p.arrival_time

        if p.start_time == -1:
            p.start_time = current_time

        gantt_chart.append((p.pid, current_time, current_time + p.burst_time))
        current_time += p.burst_time

        p.finish_time = current_time
        p.turnaround_time = p.finish_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

    print_gantt_chart(gantt_chart)
    return gantt_chart


def schedule_sjf(processes: List[Process]):
    """
    Shortest Job First (SJF) Algoritması
    """
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    completed_processes = 0
    n = len(processes)
    gantt_chart = []

    print("\n--- Scheduling Algorithm: SJF ---")

    while completed_processes < n:
        ready_queue = [p for p in processes if p.arrival_time <= current_time and p.finish_time == 0]

        if not ready_queue:
            remaining_processes = [p for p in processes if p.finish_time == 0]
            if remaining_processes:
                next_arrival = min(remaining_processes, key=lambda x: x.arrival_time).arrival_time
                current_time = next_arrival
            continue

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
    Priority Scheduling (Non-Preemptive)
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
    Round Robin (RR) Algoritması (Preemptive)
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
        # Yeni gelenleri kuyruğa ekle
        while process_idx < n and processes[process_idx].arrival_time <= current_time:
            queue.append(processes[process_idx])
            process_idx += 1

        if not queue:
            if process_idx < n:
                current_time = processes[process_idx].arrival_time
                continue

        current_process = queue.popleft()

        if current_process.start_time == -1:
            current_process.start_time = current_time

        time_to_run = min(current_process.remaining_time, time_quantum)

        gantt_chart.append((current_process.pid, current_time, current_time + time_to_run))

        current_time += time_to_run
        current_process.remaining_time -= time_to_run

        # Çalışırken yeni gelen var mı? Varsa önce onları ekle
        while process_idx < n and processes[process_idx].arrival_time <= current_time:
            queue.append(processes[process_idx])
            process_idx += 1

        if current_process.remaining_time == 0:
            current_process.finish_time = current_time
            current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed_processes += 1
        else:
            queue.append(current_process)

    print_gantt_chart(gantt_chart)
    return gantt_chart