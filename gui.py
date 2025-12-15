import customtkinter as ctk
from tkinter import filedialog, messagebox
import sys
import os
import copy
import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importing local modules
from utils import read_input
from algorithms import schedule_fcfs, schedule_sjf, schedule_priority, schedule_rr

# --- VISUAL SETTINGS ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
COLORS = ['#3B8ED0', '#E04F5F', '#2CC985', '#E5B350', '#82589F', '#F8EFBA', '#58B19F']


class SchedulerApp(ctk.CTk):
    """
    Main GUI Application Class.
    Handles user interaction, simulation orchestration, and result visualization.
    """
    def __init__(self):
        super().__init__()

        self.title("CS 305: Scheduler Ultimate Edition")
        self.geometry("1300x850")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Control Panel) ---
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo = ctk.CTkLabel(self.sidebar, text="SCHEDULER\nULTIMATE", font=ctk.CTkFont(size=26, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(40, 30))

        # File Selection Button
        self.btn_browse = ctk.CTkButton(self.sidebar, text="📂 Load File", command=self.browse_file, height=45,
                                        fg_color="#333333", border_width=1, border_color="gray")
        self.btn_browse.grid(row=1, column=0, padx=20, pady=10)

        self.lbl_filename = ctk.CTkLabel(self.sidebar, text="File: None", text_color="#A0A0A0")
        self.lbl_filename.grid(row=2, column=0, padx=20, pady=(0, 20))

        # Round Robin Time Quantum Input
        ctk.CTkLabel(self.sidebar, text="Time Quantum (RR):", anchor="w", font=("Arial", 14, "bold")).grid(row=3,
                                                                                                           column=0,
                                                                                                           padx=20,
                                                                                                           pady=(20, 5))
        self.entry_tq = ctk.CTkEntry(self.sidebar, placeholder_text="3", height=35)
        self.entry_tq.insert(0, "3")
        self.entry_tq.grid(row=4, column=0, padx=20, pady=(0, 30))

        # Main Simulation Trigger
        self.btn_run = ctk.CTkButton(self.sidebar, text="🚀 START SIMULATION", command=self.run_simulation, height=60,
                                     fg_color="#1f6aa5", font=ctk.CTkFont(size=18, weight="bold"))
        self.btn_run.grid(row=5, column=0, padx=20, pady=10)

        # Export Results Button
        self.btn_export = ctk.CTkButton(self.sidebar, text="💾 Save Report (CSV)", command=self.save_report, height=40,
                                        fg_color="#27ae60", state="disabled")
        self.btn_export.grid(row=6, column=0, padx=20, pady=(50, 10))

        # --- RIGHT SIDE (Results View) ---
        self.tabview = ctk.CTkTabview(self, anchor="nw")
        self.tabview.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        self.tab_overview = self.tabview.add("📊 Overview")
        self.tab_fcfs = self.tabview.add("FCFS")
        self.tab_sjf = self.tabview.add("SJF")
        self.tab_prio = self.tabview.add("Priority")
        self.tab_rr = self.tabview.add("Round Robin")

        self.selected_file = None
        self.current_tq = 3
        self.simulation_results = {}

    def browse_file(self):
        """Opens file dialog for user to select the process list."""
        filename = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if filename:
            self.selected_file = filename
            self.lbl_filename.configure(text=os.path.basename(filename), text_color="#4ade80")
            self.btn_export.configure(state="disabled")

    def run_simulation(self):
        """Executes all scheduling algorithms and updates the UI."""
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected!")
            return
        try:
            self.current_tq = int(self.entry_tq.get())
        except ValueError:
            messagebox.showerror("Error", "Time Quantum must be an integer!")
            return

        original = read_input(self.selected_file)
        self.simulation_results = {}

        # --- EXECUTE ALGORITHMS ---
        # Note: deepcopy is used to ensure each algorithm starts with a fresh dataset

        # 1. FCFS
        p_fcfs = copy.deepcopy(original)
        gantt_fcfs = schedule_fcfs(p_fcfs)
        self.render_algorithm_tab(self.tab_fcfs, p_fcfs, gantt_fcfs)
        self.simulation_results['FCFS'] = self.calculate_avg_waiting(p_fcfs)

        # 2. SJF
        p_sjf = copy.deepcopy(original)
        gantt_sjf = schedule_sjf(p_sjf)
        self.render_algorithm_tab(self.tab_sjf, p_sjf, gantt_sjf)
        self.simulation_results['SJF'] = self.calculate_avg_waiting(p_sjf)

        # 3. Priority
        p_prio = copy.deepcopy(original)
        gantt_prio = schedule_priority(p_prio)
        self.render_algorithm_tab(self.tab_prio, p_prio, gantt_prio)
        self.simulation_results['Priority'] = self.calculate_avg_waiting(p_prio)

        # 4. Round Robin
        p_rr = copy.deepcopy(original)
        gantt_rr = schedule_rr(p_rr, self.current_tq)
        self.render_algorithm_tab(self.tab_rr, p_rr, gantt_rr)
        self.simulation_results[f'RR (TQ={self.current_tq})'] = self.calculate_avg_waiting(p_rr)

        # --- UPDATE DASHBOARD ---
        self.render_overview_tab(self.simulation_results)
        self.tabview.set("📊 Overview")

        # Enable export button
        self.btn_export.configure(state="normal")

    def save_report(self):
        """Exports simulation results to a CSV file."""
        if not self.simulation_results:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    # Headers
                    writer.writerow(["Algorithm", "Average Waiting Time (ms)", "Date"])
                    # Data Rows
                    for algo, score in self.simulation_results.items():
                        writer.writerow([algo, f"{score:.2f}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")])

                messagebox.showinfo("Success", f"Report saved successfully:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def render_algorithm_tab(self, tab, processes, gantt_data):
        """Populates a tab with Metrics, Gantt Chart, and Data Grid."""
        for widget in tab.winfo_children(): widget.destroy()

        # 1. Metrics Cards
        metrics_frame = ctk.CTkFrame(tab, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=10)

        avg_wait = self.calculate_avg_waiting(processes)
        avg_turn = sum(p.turnaround_time for p in processes) / len(processes)

        last_finish = max(p.finish_time for p in processes)
        first_arrival = min(p.arrival_time for p in processes)
        total_burst = sum(p.burst_time for p in processes)
        utilization = (total_burst / (last_finish - first_arrival)) * 100 if (last_finish - first_arrival) > 0 else 0

        self.create_metric_card(metrics_frame, "Avg Waiting", f"{avg_wait:.2f} ms", "#E04F5F").pack(side="left",
                                                                                                    fill="x",
                                                                                                    expand=True, padx=5)
        self.create_metric_card(metrics_frame, "Avg Turnaround", f"{avg_turn:.2f} ms", "#3B8ED0").pack(side="left",
                                                                                                       fill="x",
                                                                                                       expand=True,
                                                                                                       padx=5)
        self.create_metric_card(metrics_frame, "CPU Utilization", f"%{utilization:.1f}", "#2CC985").pack(side="left",
                                                                                                         fill="x",
                                                                                                         expand=True,
                                                                                                         padx=5)

        # 2. Gantt Chart Visualization (Matplotlib)
        chart_frame = ctk.CTkFrame(tab, fg_color="#2B2B2B")
        chart_frame.pack(fill="x", pady=10, padx=5)
        fig, ax = plt.subplots(figsize=(10, 2), dpi=100)
        fig.patch.set_facecolor('#2B2B2B')
        ax.set_facecolor('#2B2B2B')

        y_pos = 10
        for pid, start, end in gantt_data:
            duration = end - start
            p_idx = int(''.join(filter(str.isdigit, pid))) if any(c.isdigit() for c in pid) else 1
            color = COLORS[p_idx % len(COLORS)]
            ax.barh(y_pos, duration, left=start, height=5, color=color, edgecolor='black', alpha=0.9)
            if duration >= 1:
                ax.text(start + duration / 2, y_pos, pid, ha='center', va='center', color='white', fontweight='bold',
                        fontsize=9)

        ax.set_yticks([])
        ax.tick_params(axis='x', colors='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.set_xlim(left=0)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

        # 3. Data Grid (Detailed Table)
        table_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        headers = ["PID", "Arrival", "Burst", "Priority", "Finish", "Turnaround", "Waiting"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"), text_color="white").grid(row=0, column=i,
                                                                                                        padx=10, pady=5,
                                                                                                        sticky="w")
        ctk.CTkFrame(table_frame, height=2, fg_color="gray").grid(row=1, column=0, columnspan=7, sticky="ew",
                                                                  pady=(0, 5))

        for i, p in enumerate(processes):
            color = "#333333" if i % 2 == 0 else "transparent"
            vals = [p.pid, p.arrival_time, p.burst_time, p.priority, p.finish_time, p.turnaround_time, p.waiting_time]
            for col, val in enumerate(vals):
                lbl = ctk.CTkLabel(table_frame, text=str(val), font=("Consolas", 12), fg_color=color, corner_radius=3)
                lbl.grid(row=i + 2, column=col, padx=2, pady=1, sticky="ew")

    def create_metric_card(self, parent, title, value, color):
        """Helper to create a styled statistics card."""
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=8)
        ctk.CTkLabel(card, text=title, font=("Arial", 11, "bold"), text_color="white").pack(pady=(5, 0))
        ctk.CTkLabel(card, text=value, font=("Arial", 20, "bold"), text_color="white").pack(pady=(0, 5))
        return card

    def calculate_avg_waiting(self, processes):
        if not processes: return 0
        return sum(p.waiting_time for p in processes) / len(processes)

    def render_overview_tab(self, data):
        """Renders the performance comparison chart."""
        for widget in self.tab_overview.winfo_children():
            widget.destroy()

        chart_frame = ctk.CTkFrame(self.tab_overview, fg_color="transparent")
        chart_frame.pack(fill="both", expand=True, padx=20, pady=20)

        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        fig.patch.set_facecolor('#242424')
        ax.set_facecolor('#242424')

        algorithms = list(data.keys())
        times = list(data.values())

        colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#1A535C']

        bars = ax.bar(algorithms, times, color=colors, width=0.5)

        ax.set_ylabel('Avg Waiting Time (ms)', color='white')
        ax.set_title('Performance Comparison', color='white', pad=20)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', color='white', fontweight='bold')

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = SchedulerApp()
    app.mainloop()