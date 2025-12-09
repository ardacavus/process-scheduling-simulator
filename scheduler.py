import sys
import copy


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        self.priority = int(priority)

        # Simülasyon sırasında değişecek veya hesaplanacak değerler
        self.remaining_time = self.burst_time  # Round Robin ve SRTF için gerekli
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = -1  # Gantt şeması için ilk başlama anı

    # Nesneyi yazdırdığımızda güzel görünmesi için (Debug yaparken işe yarar)
    def __repr__(self):
        return f"Job({self.pid}, Arr:{self.arrival_time}, Burst:{self.burst_time}, Prio:{self.priority})"


def read_input(filename):
    processes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Satırları temizle ve virgülle ayır
                parts = line.strip().split(',')
                if len(parts) == 4:
                    pid = parts[0].strip()
                    arrival = parts[1].strip()
                    burst = parts[2].strip()
                    priority = parts[3].strip()
                    processes.append(Process(pid, arrival, burst, priority))
    except FileNotFoundError:
        print(f"Hata: '{filename}' dosyası bulunamadı.")
        sys.exit(1)
    return processes


def print_metrics(processes, algorithm_name):
    # Bu fonksiyonu daha sonra detaylandıracağız, şimdilik yer tutucu.
    print(f"\n--- Scheduling Algorithm: {algorithm_name} ---")
    # Hesaplamalar buraya gelecek
    total_turnaround = 0
    total_waiting = 0

    print(f"{'Process':<10} | {'Finish':<8} | {'Turnaround':<12} | {'Waiting':<8}")
    print("-" * 46)

    for p in processes:
        print(f"{p.pid:<10} | {p.finish_time:<8} | {p.turnaround_time:<12} | {p.waiting_time:<8}")
        total_turnaround += p.turnaround_time
        total_waiting += p.waiting_time

    if len(processes) > 0:
        avg_turnaround = total_turnaround / len(processes)
        avg_waiting = total_waiting / len(processes)
        print(f"\nAverage Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Waiting Time: {avg_waiting:.2f}")


# --- Main Kısmı ---
if __name__ == "__main__":
    # Komut satırından dosya adı alacağız, yoksa varsayılan 'processes.txt' olsun
    input_file = sys.argv[1] if len(sys.argv) > 1 else "processes.txt"

    # Dosyayı oku
    original_processes = read_input(input_file)

    # Okunduğunu test etmek için:
    print("Okunan Süreçler:")
    for p in original_processes:
        print(p)

    # NOT: Algoritmaları çağırmadan önce listeyi kopyalayacağız (deepcopy)
    # Çünkü bir algoritma process nesnesini değiştirirse (remaining_time vs)
    # diğer algoritma bozuk veriyle başlamasın.