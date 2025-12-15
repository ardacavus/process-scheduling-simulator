# 🚀 CPU Scheduling Simulator - Ultimate Edition

A comprehensive, GUI-based **Process Scheduling Simulator** built with Python. This tool visualizes classic CPU scheduling algorithms with interactive Gantt charts, detailed metrics, and CSV reporting features.

![Dashboard Screenshot](assets/screenshot.png)

## ✨ Features

* **Algorithms Supported:**
    * First-Come, First-Served (FCFS)
    * Shortest Job First (SJF) - *Non-Preemptive*
    * Priority Scheduling - *Non-Preemptive*
    * Round Robin (RR) - *Preemptive with customizable Time Quantum*
* **Modern GUI:** Built with `customtkinter` (Dark Mode enabled).
* **Visual Analytics:** Interactive Matplotlib Gantt charts.
* **Performance Metrics:** Calculates Average Waiting Time, Turnaround Time, and CPU Utilization.
* **Export Data:** Save simulation results to CSV for external analysis.
* **Portable:** Can be built into a standalone `.exe` file.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ardacavus/process-scheduling-simulator.git](https://github.com/ardacavus/process-scheduling-simulator.git)
    cd process-scheduling-simulator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Usage

### Option 1: Run via Python
```bash
python gui.py
```

Option 2: Run the Executable
Download the latest .exe from the Releases page.

🏗️ Building from Source
To create a standalone .exe file:

```bash
python build.py
```

💻 Technologies
*Language: Python 3.x

*UI Framework: CustomTkinter

*Data Visualization: Matplotlib

*Packaging: PyInstaller

📄 License
This project is licensed under the MIT License.