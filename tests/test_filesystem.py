import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from filesystem import FileSystem
from disk import VirtualDisk

class TestFileSystem(unittest.TestCase):
    def setUp(self):
        self.disk = VirtualDisk(64, 64)
        self.fs = FileSystem(self.disk)
        
    def test_create_file(self):
        self.fs.create_file("test.txt")
        self.assertIn("test.txt", self.fs.current_directory.children)
        
    def test_create_duplicate(self):
        self.fs.create_file("test.txt")
        with self.assertRaises(Exception):
            self.fs.create_file("test.txt")
            
    def test_write_read_file(self):
        self.fs.create_file("notes.txt")
        self.fs.write_file("notes.txt", "Operating Systems")
        content = self.fs.read_file("notes.txt")
        self.assertEqual(content, "Operating Systems")
        file_obj = self.fs.current_directory.children["notes.txt"]
        self.assertEqual(len(file_obj.allocated_blocks), 1) # 17 bytes < 64 bytes block size
        
    def test_delete_file(self):
        self.fs.create_file("notes.txt")
        self.fs.write_file("notes.txt", "OS")
        self.assertEqual(self.disk.get_used_blocks(), 1)
        self.fs.delete_file("notes.txt")
        self.assertNotIn("notes.txt", self.fs.current_directory.children)
        self.assertEqual(self.disk.get_used_blocks(), 0)
        
    def test_rename_file(self):
        self.fs.create_file("notes.txt")
        self.fs.write_file("notes.txt", "data")
        blocks = self.fs.current_directory.children["notes.txt"].allocated_blocks
        
        self.fs.rename_file("notes.txt", "new_notes.txt")
        self.assertNotIn("notes.txt", self.fs.current_directory.children)
        self.assertIn("new_notes.txt", self.fs.current_directory.children)
        self.assertEqual(self.fs.read_file("new_notes.txt"), "data")
        self.assertEqual(self.fs.current_directory.children["new_notes.txt"].allocated_blocks, blocks)
        
    def test_large_file(self):
        self.fs.create_file("large.txt")
        content = "A" * 200 # requires 4 blocks (200 / 64 = 3.125 -> 4)
        self.fs.write_file("large.txt", content)
        self.assertEqual(self.disk.get_used_blocks(), 4)
        
    def test_file_not_found(self):
        with self.assertRaises(Exception):
            self.fs.read_file("ghost.txt")

    def test_defragment(self):
        self.fs.create_file("file1.txt")
        self.fs.write_file("file1.txt", "A" * 64) # 1 block
        
        self.fs.create_file("file2.txt")
        self.fs.write_file("file2.txt", "B" * 64) # 1 block
        
        self.fs.create_file("file3.txt")
        self.fs.write_file("file3.txt", "C" * 64) # 1 block
        
        # Delete file2 to create fragmentation
        self.fs.delete_file("file2.txt")
        
        # Current disk: [USED, FREE, USED]
        self.assertEqual(self.disk.blocks[:3], ["USED", "FREE", "USED"])
        self.assertEqual(self.disk.get_fragmentation(), 2)
        
        # Defragment
        self.fs.defragment()
        
        # Disk should now be: [USED, USED, FREE]
        self.assertEqual(self.disk.blocks[:3], ["USED", "USED", "FREE"])
        self.assertEqual(self.disk.get_fragmentation(), 1)
        self.assertEqual(self.fs.current_directory.children["file1.txt"].allocated_blocks, [0])
        self.assertEqual(self.fs.current_directory.children["file3.txt"].allocated_blocks, [1])
    def test_file_locking(self):
        self.fs.create_file("locked.txt")
        self.fs.write_file("locked.txt", "data")
        
        self.fs.toggle_lock("locked.txt")
        self.assertTrue(self.fs.current_directory.children["locked.txt"].locked)
        
        with self.assertRaisesRegex(Exception, "File in Use"):
            self.fs.write_file("locked.txt", "new data")
            
        with self.assertRaisesRegex(Exception, "File in Use"):
            self.fs.read_file("locked.txt")
            
        with self.assertRaisesRegex(Exception, "File in Use"):
            self.fs.delete_file("locked.txt")
            
        with self.assertRaisesRegex(Exception, "File in Use"):
            self.fs.rename_file("locked.txt", "new_locked.txt")
            
        self.fs.toggle_lock("locked.txt")
        self.fs.read_file("locked.txt") # should work now

    def test_buffer_cache(self):
        self.fs.create_file("cache.txt")
        self.fs.write_file("cache.txt", "A" * 200) # 4 blocks
        blocks = self.fs.current_directory.children["cache.txt"].allocated_blocks
        
        # Read the file
        self.fs.read_file("cache.txt")
        
        self.assertEqual(self.fs.cache.misses, 4)
        self.assertEqual(self.fs.cache.hits, 0)
        
        # Read it again
        self.fs.read_file("cache.txt")
        
        self.assertEqual(self.fs.cache.misses, 4)
        self.assertEqual(self.fs.cache.hits, 4)
        
        # Test capacity and eviction
        self.fs.create_file("cache2.txt")
        self.fs.write_file("cache2.txt", "B" * 150) # 3 blocks
        self.fs.read_file("cache2.txt")
        
        # Capacity is 5, we have read 4 + 3 = 7 blocks, 2 should be evicted
        self.assertEqual(len(self.fs.cache.cache), 5)
        
if __name__ == '__main__':
    unittest.main()
