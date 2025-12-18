# CPU Scheduling Simulator

This project is a **Process Scheduling Simulator** developed as part of the **CS 305 – Operating Systems** course.

The simulator visualizes and analyzes classic CPU scheduling algorithms using Gantt charts and performance metrics.

---

## Supported Scheduling Algorithms

- First-Come, First-Served (FCFS)
- Shortest Job First (SJF) – Non-Preemptive
- Priority Scheduling – Non-Preemptive
- Round Robin (RR) – Preemptive (Configurable Time Quantum)

---

## Features

- GUI-based simulation using CustomTkinter (Dark Mode)
- Gantt chart visualization with Matplotlib
- Calculation of:
  - Average Waiting Time
  - Average Turnaround Time
  - CPU Utilization
- Export of simulation results to CSV format for further analysis
- **Starvation Detection:** Automatically detects and alerts if processes suffer from starvation in SJF and Priority algorithms.

> **Note:** The graphical interface and CSV export features are optional and do not affect the correctness of the scheduling algorithms or metric calculations.

---

## Requirements

- Python 3.x
- Required libraries are listed in `requirements.txt`

---

## 📥 Installation & Setup

Choose one of the following methods to run the simulator:

### Option 1: Download Executable (No Python Required)
The easiest way to run the application without installing dependencies.

1.  Download the **[Latest Release](https://github.com/ardacavus/process-scheduling-simulator/releases/latest)** from this repository.
2.  Unzip the file (if archived) or find the `.exe` file.
3.  Double-click to run the application directly.

### Option 2: Run from Source Code
If you want to run the Python script directly:

**Step 1: Get the Code**
* **Clone via Git:**
    ```bash
    git clone [https://github.com/ardacavus/process-scheduling-simulator.git](https://github.com/ardacavus/process-scheduling-simulator.git)
    cd process-scheduling-simulator
    ```
* **Or Extract ZIP:** Unzip the submission archive and navigate to the folder in your terminal.

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt

**Step 3: Run the App**
```bash
python gui.py
```

Building from Source (Optional)
If you wish to create a standalone .exe file yourself:
```bash
python build.py
```

🧪 Test Scenarios & Sample Inputs
The project includes pre-configured input files to demonstrate specific scheduling behaviors. Use the "📂 Load File" button in the application to select these files:

1. Standard Simulation (processes.txt)
Use for: Observing normal scheduling behavior and comparing algorithms.

Description: Contains a balanced set of processes with varying burst times and priorities.

2. Starvation Demonstration (starvation.txt)
Use for: Testing the Starvation Detection mechanism.

Observation: Run the simulation with SJF or Priority algorithms.

Result: A warning popup will appear, alerting that specific processes (e.g., P2, P3) have waited excessively (>50ms) due to a long-running process (P1) blocking the CPU.

💻 Technologies

Language: Python 3.x

UI Framework: CustomTkinter

Data Visualization: Matplotlib

Packaging: PyInstaller
