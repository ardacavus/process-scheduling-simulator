import unittest
import copy
from process import Process
from algorithms import schedule_fcfs, schedule_sjf, schedule_priority, schedule_rr


class TestScheduler(unittest.TestCase):
    """
    Unit Tests to verify the correctness of scheduling algorithms.
    """

    def setUp(self):
        # Initialize a basic dataset for each test
        self.p1 = Process("P1", 0, 8, 1)
        self.p2 = Process("P2", 1, 4, 1)
        self.p3 = Process("P3", 2, 9, 1)
        self.basic_load = [self.p1, self.p2, self.p3]

    def test_fcfs_basic(self):
        """Test 1: FCFS Basic Logic (Strict Arrival Order)"""
        # Expected: P1(0-8), P2(8-12), P3(12-21)
        schedule_fcfs(self.basic_load)

        self.assertEqual(self.p1.finish_time, 8)
        self.assertEqual(self.p2.finish_time, 12)
        self.assertEqual(self.p3.finish_time, 21)
        print("✅ FCFS Basic Test Passed")

    def test_sjf_ordering(self):
        """Test 2: SJF Ordering (Shortest Job First)"""
        # P1(0, 10), P2(1, 2). Since SJF is Non-Preemptive, P1 must finish first.
        proc1 = Process("A", 0, 10, 1)
        proc2 = Process("B", 1, 2, 1)
        data = [proc1, proc2]

        schedule_sjf(data)

        self.assertEqual(proc1.finish_time, 10)
        self.assertEqual(proc2.finish_time, 12)
        print("✅ SJF Ordering Test Passed")

    def test_idle_time(self):
        """Test 3: CPU Idle Time Handling"""
        # Gap between P1(0-5) and P2(10-15). CPU should remain idle for 5s.
        p_early = Process("E", 0, 5, 1)
        p_late = Process("L", 10, 5, 1)
        data = [p_early, p_late]

        schedule_fcfs(data)

        self.assertEqual(p_early.finish_time, 5)
        self.assertEqual(p_late.start_time, 10)  # Must start at 10, not 5
        self.assertEqual(p_late.finish_time, 15)
        print("✅ Idle Time Logic Passed")

    def test_round_robin_preemption(self):
        """Test 4: Round Robin Time Slicing"""
        # Scenario: Two processes with TQ=2. They should switch context every 2 units.
        pa = Process("A", 0, 5, 1)
        pb = Process("B", 1, 5, 1)
        data = [pa, pb]

        schedule_rr(data, time_quantum=2)

        # Expected completion times calculated manually
        self.assertEqual(pa.finish_time, 9)
        self.assertEqual(pb.finish_time, 10)
        print("✅ Round Robin Logic Passed")

    def test_unordered_input(self):
        """Test 5: Handling Unordered Input Data"""
        # Processes arriving in mixed order should be sorted by arrival time internally.
        p_late = Process("L", 10, 5, 1)
        p_early = Process("E", 0, 5, 1)
        data = [p_late, p_early]

        schedule_fcfs(data)

        # First executed process should be 'E'
        self.assertEqual(data[0].pid, "E")
        print("✅ Unordered Input Handling Passed")


if __name__ == '__main__':
    unittest.main(verbosity=2)