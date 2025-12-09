import sys
import copy
from utils import read_input, print_metrics
# schedule_sjf fonksiyonunu import etmeyi unutmuyoruz
from algorithms import schedule_fcfs, schedule_sjf

if __name__ == "__main__":
    # Komut satırı argümanı kontrolü (Varsayılan: processes.txt)
    input_file = sys.argv[1] if len(sys.argv) > 1 else "processes.txt"

    # 1. Dosyayı Oku (Master veri)
    original_processes = read_input(input_file)
    print(f"File loaded: {input_file} with {len(original_processes)} processes.")

    # --- ALGORİTMA 1: FCFS ---
    # Veriyi kopyalıyoruz ki bir önceki algoritmanın hesapları diğerini etkilemesin
    fcfs_processes = copy.deepcopy(original_processes)
    schedule_fcfs(fcfs_processes)
    print_metrics(fcfs_processes, "FCFS")

    # --- ALGORİTMA 2: SJF ---
    sjf_processes = copy.deepcopy(original_processes)
    schedule_sjf(sjf_processes)
    print_metrics(sjf_processes, "SJF")

    # İleride buraya Priority ve RR gelecek...