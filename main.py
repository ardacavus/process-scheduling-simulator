# main.py
import sys
import copy
from utils import read_input, print_metrics
from algorithms import schedule_fcfs

if __name__ == "__main__":
    # Komut satırı argümanı kontrolü
    input_file = sys.argv[1] if len(sys.argv) > 1 else "processes.txt"

    # 1. Dosyayı Oku
    original_processes = read_input(input_file)

    # 2. FCFS Çalıştır
    # Deepcopy önemli: Orijinal listeyi bozmamak için kopyalıyoruz
    fcfs_processes = copy.deepcopy(original_processes)
    schedule_fcfs(fcfs_processes)
    print_metrics(fcfs_processes, "FCFS")

    # Buraya ileride diğer algoritmalar gelecek (SJF, RR, Priority...)