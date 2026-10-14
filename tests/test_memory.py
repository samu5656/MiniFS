import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from disk import VirtualDisk
from filesystem import FileSystem
from memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.disk = VirtualDisk(64, 64)
        self.mem = MemoryManager(self.disk, ram_size=16, swap_start=48, swap_size=16)

    def test_start_and_stop_process(self):
        self.mem.start_process("P1", 4)
        self.assertEqual(self.mem.ram[:4], ["P1", "P1", "P1", "P1"])
        self.assertEqual(self.mem.processes["P1"].state, "RUNNING")
        
        self.mem.stop_process("P1")
        self.assertEqual(self.mem.ram[:4], ["FREE", "FREE", "FREE", "FREE"])
        self.assertNotIn("P1", self.mem.processes)

    def test_ram_swapping(self):
        # Fill RAM (6 + 6 + 4 = 16 blocks)
        self.mem.start_process("P1", 6)
        self.mem.start_process("P2", 6)
        self.mem.start_process("P3", 4)
        self.assertEqual(self.mem.ram.count("FREE"), 0)
        
        # Start P4 requiring 4 blocks -> P1 should be evicted (LRU) to Swap
        evicted = self.mem.start_process("P4", 4)
        self.assertEqual(evicted, ["P1"])
        self.assertEqual(self.mem.processes["P1"].state, "SWAPPED")
        self.assertEqual(self.mem.processes["P4"].state, "RUNNING")
        
        # Verify swap blocks on disk
        swap_blocks = [self.disk.blocks[i] for i in range(48, 54)]
        self.assertEqual(swap_blocks, ["SWAP_P1"] * 6)
        
        # Verify RAM layout (P1 blocks freed, P4 placed in first 4 slots)
        self.assertEqual(self.mem.ram[:4], ["P4", "P4", "P4", "P4"])
        self.assertEqual(self.mem.ram[4:6], ["FREE", "FREE"])

    def test_swap_preserved_after_defragment(self):
        fs = FileSystem(self.disk)
        fs.create_file("test1.txt")
        fs.write_file("test1.txt", "A" * 64)
        fs.create_file("test2.txt")
        fs.write_file("test2.txt", "B" * 64)
        fs.delete_file("test1.txt")
        
        # Defragment disk
        fs.defragment()
        
        # Ensure swap space is intact
        for i in range(48, 64):
            self.assertEqual(self.disk.blocks[i], "SWAP_FREE")
            
        # Start processes and trigger swapping
        self.mem.start_process("P1", 6)
        self.mem.start_process("P2", 6)
        self.mem.start_process("P3", 4)
        evicted = self.mem.start_process("P4", 4)
        
        self.assertEqual(evicted, ["P1"])
        self.assertEqual(self.disk.blocks[48:54], ["SWAP_P1"] * 6)

    def test_stop_swapped_process(self):
        self.mem.start_process("P1", 6)
        self.mem.start_process("P2", 6)
        self.mem.start_process("P3", 4)
        self.mem.start_process("P4", 4) # P1 is swapped
        
        # Stopping P1 should clear its swap blocks back to SWAP_FREE
        self.mem.stop_process("P1")
        self.assertEqual(self.disk.blocks[48:54], ["SWAP_FREE"] * 6)
        self.assertNotIn("P1", self.mem.processes)

    def test_process_exceeds_ram(self):
        with self.assertRaises(Exception):
            self.mem.start_process("P_BIG", 20)

if __name__ == '__main__':
    unittest.main()
