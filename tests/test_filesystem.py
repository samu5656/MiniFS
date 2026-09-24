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
            
if __name__ == '__main__':
    unittest.main()
