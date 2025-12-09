from typing import List
from process import Process
from utils import print_gantt_chart


def schedule_fcfs(processes: List[Process]):
    """
    First-Come, First-Served (FCFS) Algoritması
    """
    # 1. Varış zamanına göre sırala
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    gantt_chart = []

    print("\n--- Scheduling Algorithm: FCFS ---")

    for p in processes:
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


def schedule_sjf(processes: List[Process]):
    """
    Shortest Job First (SJF) Algoritması
    """
    # Önce geliş zamanına göre sırala (Eşitlik durumunda FCFS olması için)
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    completed_processes = 0
    n = len(processes)
    gantt_chart = []

    print("\n--- Scheduling Algorithm: SJF ---")

    while completed_processes < n:
        # Hazır kuyruğu: Gelmiş ve bitmemiş olanlar
        ready_queue = [p for p in processes if p.arrival_time <= current_time and p.finish_time == 0]

        if not ready_queue:
            remaining_processes = [p for p in processes if p.finish_time == 0]
            if remaining_processes:
                next_arrival = min(remaining_processes, key=lambda x: x.arrival_time).arrival_time
                current_time = next_arrival
            continue

        # Burst time'ı en küçük olanı seç
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