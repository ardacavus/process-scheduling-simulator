# algorithms.py
from typing import List
from process import Process
from utils import print_gantt_chart


def schedule_fcfs(processes: List[Process]):
    """
    First-Come, First-Served (FCFS) Algoritması
    Kriter: Varış zamanı (Arrival Time)
    Mod: Non-Preemptive (Kesintisiz)
    """
    # 1. Varış zamanına göre sırala
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    gantt_chart = []

    print("\n--- Scheduling Algorithm: FCFS ---")

    for p in processes:
        # CPU Boşta ise (Idle Time)
        if current_time < p.arrival_time:
            current_time = p.arrival_time

        # İşlemi Başlat
        if p.start_time == -1:
            p.start_time = current_time

        # Gantt verisi ekle
        gantt_chart.append((p.pid, current_time, current_time + p.burst_time))

        # Zamanı ilerlet
        current_time += p.burst_time

        # Metrikleri kaydet
        p.finish_time = current_time
        p.turnaround_time = p.finish_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

    print_gantt_chart(gantt_chart)