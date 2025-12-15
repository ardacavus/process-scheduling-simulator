# utils.py
import sys
from typing import List
from process import Process


def read_input(filename: str) -> List[Process]:
    """
    Verilen dosyadan süreçleri okur ve Process nesneleri listesi döndürür.
    Format: Process_ID, Arrival_Time, Burst_Time, Priority
    """
    processes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    pid = parts[0].strip()
                    arrival = int(parts[1].strip())
                    burst = int(parts[2].strip())
                    priority = int(parts[3].strip())
                    processes.append(Process(pid, arrival, burst, priority))
    except FileNotFoundError:
        print(f"Hata: '{filename}' dosyası bulunamadı.")
        sys.exit(1)
    except ValueError:
        print("Hata: Dosya formatı geçersiz. Sayısal değerler kontrol edilmeli.")
        sys.exit(1)
    return processes


def print_metrics(processes: List[Process], algorithm_name: str):
    """
    Hesaplanan metrikleri ve sonuç tablosunu ekrana basar.
    """
    total_turnaround = 0
    total_waiting = 0
    total_burst = 0  # Toplam iş süresi (CPU'nun dolu olduğu süre)

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

        # --- GERÇEK CPU UTILIZATION HESABI ---
        # Formül: (Toplam Burst Süresi / Toplam Geçen Süre) * 100

        # Simülasyonun bittiği son an
        last_finish_time = max(p.finish_time for p in processes)
        # Simülasyonun başladığı ilk an (Genelde ilk gelenin varış zamanı)
        first_arrival = min(p.arrival_time for p in processes)

        # Toplam geçen süre (Simülasyon süresi)
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
    Gantt şemasını görselleştirir.
    Veri formatı: [(PID, Start, End), ...]
    """
    print("Gantt Chart: ", end="")
    for pid, start, end in gantt_data:
        print(f"[{start}]--{pid}--[{end}]", end="")
    print()