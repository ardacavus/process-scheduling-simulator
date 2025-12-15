class Process:
    """
    Represents a Process Control Block (PCB) for the simulation.
    Stores static attributes (ID, Arrival, Burst) and dynamic execution metrics.
    """

    def __init__(self, pid: str, arrival_time: int, burst_time: int, priority: int):
        # Static attributes loaded from input
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority  # Lower value implies higher priority

        # Dynamic attributes (Mutable state during simulation)
        self.remaining_time = burst_time  # Critical for Preemptive algorithms (e.g., RR)
        self.start_time = -1  # Timestamp when the CPU first executes this process
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def reset(self):
        """
        Resets dynamic attributes to initial state.
        Useful when reusing the same process object for multiple algorithms.
        """
        self.remaining_time = self.burst_time
        self.start_time = -1
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def __repr__(self):
        return f"Process(ID={self.pid}, Arr={self.arrival_time}, Burst={self.burst_time}, Prio={self.priority})"