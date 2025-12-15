import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import sys
import io
import copy

# Senin yazdığın modülleri import ediyoruz
from utils import read_input, print_metrics
from algorithms import schedule_fcfs, schedule_sjf, schedule_priority, schedule_rr


class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CS 305: Process Scheduling Simulator")
        self.root.geometry("800x600")

        # --- 1. Dosya Seçme Bölümü ---
        self.frame_top = tk.Frame(root)
        self.frame_top.pack(pady=10)

        self.btn_browse = tk.Button(self.frame_top, text="Dosya Seç (processes.txt)", command=self.browse_file)
        self.btn_browse.pack(side=tk.LEFT, padx=5)

        self.lbl_file = tk.Label(self.frame_top, text="Dosya seçilmedi", fg="red")
        self.lbl_file.pack(side=tk.LEFT, padx=5)

        self.selected_file = None

        # --- 2. Time Quantum Ayarı ---
        self.frame_tq = tk.Frame(root)
        self.frame_tq.pack(pady=5)

        tk.Label(self.frame_tq, text="Time Quantum (RR için):").pack(side=tk.LEFT, padx=5)
        self.entry_tq = tk.Entry(self.frame_tq, width=5)
        self.entry_tq.insert(0, "3")  # Varsayılan değer
        self.entry_tq.pack(side=tk.LEFT, padx=5)

        # --- 3. Çalıştır Butonu ---
        self.btn_run = tk.Button(root, text="SİMÜLASYONU BAŞLAT", command=self.run_simulation, bg="green", fg="white",
                                 font=("Arial", 10, "bold"))
        self.btn_run.pack(pady=10)

        # --- 4. Çıktı Ekranı (Text Area) ---
        self.text_area = scrolledtext.ScrolledText(root, width=90, height=30, font=("Consolas", 9))
        self.text_area.pack(pady=10, padx=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(title="Süreç Dosyasını Seç",
                                              filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if filename:
            self.selected_file = filename
            self.lbl_file.config(text=filename.split("/")[-1], fg="green")

    def run_simulation(self):
        if not self.selected_file:
            messagebox.showerror("Hata", "Lütfen önce bir dosya seçin!")
            return

        try:
            tq = int(self.entry_tq.get())
        except ValueError:
            messagebox.showerror("Hata", "Time Quantum bir tam sayı olmalıdır!")
            return

        # --- ÇIKTI YÖNLENDİRME SİHRİ ---
        # Normalde print() konsola yazar. Biz bunu yakalayıp ekrana yazdıracağız.
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        try:
            # Burası senin main.py mantığının aynısı
            print(f"Simulation started using: {self.selected_file} with TQ={tq}")
            original_processes = read_input(self.selected_file)

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

            # 4. RR
            rr_processes = copy.deepcopy(original_processes)
            schedule_rr(rr_processes, tq)
            print_metrics(rr_processes, "Round Robin")

        except Exception as e:
            print(f"\nBİR HATA OLUŞTU: {e}")

        # --- Çıktıyı Ekrana Bas ---
        output = new_stdout.getvalue()
        sys.stdout = old_stdout  # Konsolu eski haline getir

        self.text_area.delete(1.0, tk.END)  # Ekranı temizle
        self.text_area.insert(tk.END, output)  # Yeni çıktıyı bas


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()