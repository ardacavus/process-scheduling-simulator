# process.py
class Process:
    """
    Bir işletim sistemi sürecini (process) temsil eden sınıf.
    """

    def __init__(self, pid: str, arrival_time: int, burst_time: int, priority: int):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        # Değişken durumlar (Mutable states)
        self.remaining_time = burst_time  # Round Robin için
        self.start_time = -1  # İlk ne zaman CPU'ya girdi
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def reset(self):
        """Süreci başlangıç durumuna döndürür (tekrar kullanım için)."""
        self.remaining_time = self.burst_time
        self.start_time = -1
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def __repr__(self):
        return f"Process(ID={self.pid}, Arr={self.arrival_time}, Burst={self.burst_time}, Prio={self.priority})"