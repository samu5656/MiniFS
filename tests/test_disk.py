import unittest
import sys
import os

# Add src to path so we can import disk
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from disk import VirtualDisk

class TestVirtualDisk(unittest.TestCase):
    def test_initialization(self):
        disk = VirtualDisk(64, 64)
        self.assertEqual(disk.total_blocks, 64)
        self.assertEqual(disk.block_size, 64)
        self.assertEqual(disk.get_free_blocks(), 64)
        self.assertEqual(disk.get_used_blocks(), 0)
        self.assertEqual(disk.get_usage(), 0.0)

    def test_allocate_blocks(self):
        disk = VirtualDisk()
        allocated = disk.allocate_blocks(3)
        self.assertEqual(allocated, [0, 1, 2])
        self.assertEqual(disk.get_used_blocks(), 3)
        self.assertEqual(disk.get_free_blocks(), 61)

    def test_free_blocks(self):
        disk = VirtualDisk()
        allocated = disk.allocate_blocks(3)
        disk.free_blocks(allocated)
        self.assertEqual(disk.get_used_blocks(), 0)
        self.assertEqual(disk.get_free_blocks(), 64)

    def test_insufficient_space(self):
        disk = VirtualDisk(10, 64)
        with self.assertRaises(Exception):
            disk.allocate_blocks(11)

    def test_fragmentation(self):
        disk = VirtualDisk(10, 64)
        alloc1 = disk.allocate_blocks(3) # 0, 1, 2
        alloc2 = disk.allocate_blocks(3) # 3, 4, 5
        disk.free_blocks(alloc1) # 0, 1, 2 are FREE
        with self.assertRaises(Exception):
            disk.allocate_blocks(5) # not enough contiguous

    def test_statistics(self):
        disk = VirtualDisk(64, 64)
        disk.allocate_blocks(10)
        stats = disk.get_statistics()
        self.assertEqual(stats["Total Blocks"], 64)
        self.assertEqual(stats["Used Blocks"], 10)
        self.assertEqual(stats["Free Blocks"], 54)

if __name__ == '__main__':
    unittest.main()
