import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cpu import CPUScheduler, Process

class TestCPUScheduler(unittest.TestCase):
    def test_add_process(self):
        cpu = CPUScheduler(algorithm="RR", quantum=2)
        p = cpu.add_process("P1", 5)
        self.assertEqual(len(cpu.ready_queue), 1)
        self.assertEqual(cpu.ready_queue[0].pid, "P1")
        self.assertEqual(cpu.ready_queue[0].remaining_time, 5)

    def test_fcfs_scheduling(self):
        cpu = CPUScheduler(algorithm="FCFS", quantum=999) # large quantum simulates FCFS
        cpu.add_process("P1", 2)
        cpu.add_process("P2", 1)

        # Step 1: P1 runs
        self.assertTrue(cpu.step())
        self.assertEqual(cpu.current_process.pid, "P1")
        self.assertEqual(cpu.current_process.remaining_time, 1)

        # Step 2: P1 runs and finishes
        self.assertTrue(cpu.step())
        self.assertEqual(cpu.current_process.state, "COMPLETED")

        # Step 3: P2 runs
        self.assertTrue(cpu.step())
        self.assertEqual(cpu.current_process.pid, "P2")
        self.assertEqual(cpu.current_process.state, "COMPLETED")

        # Step 4: IDLE
        self.assertFalse(cpu.step())
        self.assertIsNone(cpu.current_process)
        self.assertEqual(len(cpu.completed_processes), 2)

    def test_rr_scheduling(self):
        cpu = CPUScheduler(algorithm="RR", quantum=2)
        cpu.add_process("P1", 3)
        cpu.add_process("P2", 2)

        # Step 1: P1 runs
        cpu.step()
        
        # Step 2: P1 runs and reaches quantum
        cpu.step()
        self.assertEqual(cpu.current_process.pid, "P1")
        self.assertEqual(cpu.current_process.remaining_time, 1)
        self.assertEqual(cpu.current_process.state, "READY")
        self.assertEqual(cpu.ready_queue[-1].pid, "P1") # Sent to back of queue
        
        # Step 3: P2 runs
        cpu.step()
        self.assertEqual(cpu.current_process.pid, "P2")
        
        # Step 4: P2 runs and finishes (exactly hits quantum)
        cpu.step()
        self.assertEqual(cpu.current_process.pid, "P2")
        self.assertEqual(cpu.current_process.state, "COMPLETED")
        
        # Step 5: P1 runs again
        cpu.step()
        self.assertEqual(cpu.current_process.pid, "P1")
        self.assertEqual(cpu.current_process.state, "COMPLETED")

if __name__ == '__main__':
    unittest.main()
