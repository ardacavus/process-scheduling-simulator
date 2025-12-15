import unittest
import copy
from process import Process
from algorithms import schedule_fcfs, schedule_sjf, schedule_priority, schedule_rr


class TestScheduler(unittest.TestCase):

    def setUp(self):
        # Her testten önce sıfır kilometre süreçler oluşturulur
        self.p1 = Process("P1", 0, 8, 1)
        self.p2 = Process("P2", 1, 4, 1)
        self.p3 = Process("P3", 2, 9, 1)
        # Karışık liste
        self.basic_load = [self.p1, self.p2, self.p3]

    def test_fcfs_basic(self):
        """Test 1: FCFS Temel Mantık"""
        # P1(0-8), P2(8-12), P3(12-21) olmalı
        schedule_fcfs(self.basic_load)

        self.assertEqual(self.p1.finish_time, 8)
        self.assertEqual(self.p2.finish_time, 12)
        self.assertEqual(self.p3.finish_time, 21)
        print("✅ FCFS Basic Test Passed")

    def test_sjf_ordering(self):
        """Test 2: SJF Kısa İşi Öne Alma"""
        # P1(0, 10), P2(1, 2) -> P1 non-preemptive olduğu için bitmeli, sonra P2 girmeli
        proc1 = Process("A", 0, 10, 1)
        proc2 = Process("B", 1, 2, 1)
        data = [proc1, proc2]

        schedule_sjf(data)

        # P1 0'da geldi, P2 gelene kadar P1 zaten CPU'daydı.
        # SJF Non-Preemptive olduğu için P1 bitmeden P2 giremez.
        self.assertEqual(proc1.finish_time, 10)
        self.assertEqual(proc2.finish_time, 12)
        print("✅ SJF Ordering Test Passed")

    def test_idle_time(self):
        """Test 3: CPU Boşluk (Idle Time) Kontrolü"""
        # P1(0-5), P2(10-15). Arada 5 sn boşluk var.
        p_early = Process("E", 0, 5, 1)
        p_late = Process("L", 10, 5, 1)
        data = [p_early, p_late]

        schedule_fcfs(data)

        self.assertEqual(p_early.finish_time, 5)
        self.assertEqual(p_late.start_time, 10)  # 5'te değil 10'da başlamalı
        self.assertEqual(p_late.finish_time, 15)
        print("✅ Idle Time Logic Passed")

    def test_round_robin_preemption(self):
        """Test 4: Round Robin Bölme İşlemi"""
        # P1(0, 5), TQ=2.
        # Çalışma: 0-2 (P1), 2-4 (P1), 4-5 (P1). Tek işlem olduğu için bölünse de devam eder.
        # İki işlem: P1(0,5), P2(1,5), TQ=2
        # 0-2: P1 (Rem:3) -> Kuyruk sonuna
        # 2-4: P2 (Rem:3) -> Kuyruk sonuna
        # 4-6: P1 (Rem:1)
        # 6-8: P2 (Rem:1)
        # 8-9: P1 (Biter)
        # 9-10: P2 (Biter)

        pa = Process("A", 0, 5, 1)
        pb = Process("B", 1, 5, 1)
        data = [pa, pb]

        schedule_rr(data, time_quantum=2)

        self.assertEqual(pa.finish_time, 9)
        self.assertEqual(pb.finish_time, 10)
        print("✅ Round Robin Logic Passed")

    def test_unordered_input(self):
        """Test 5: Karışık Giriş Sıralaması"""
        # Dosyada P2 önce, P1 sonra yazılmış olabilir. Algoritma bunu arrival'a göre dizmeli.
        p_late = Process("L", 10, 5, 1)
        p_early = Process("E", 0, 5, 1)
        data = [p_late, p_early]  # Ters veriyoruz

        schedule_fcfs(data)

        # İlk çalışanın "E" olması lazım
        self.assertEqual(data[0].pid, "E")
        print("✅ Unordered Input Handling Passed")


if __name__ == '__main__':
    unittest.main(verbosity=2)