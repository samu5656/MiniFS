import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from filesystem import FileSystem
from disk import VirtualDisk

class TestDirectoryManagement(unittest.TestCase):
    def setUp(self):
        self.disk = VirtualDisk(64, 64)
        self.fs = FileSystem(self.disk)
        
    def test_root_directory(self):
        self.assertEqual(self.fs.pwd(), "/")
        self.assertEqual(self.fs.ls(), [])
        
    def test_mkdir_and_ls(self):
        self.fs.mkdir("projects")
        self.assertIn("projects", self.fs.ls())
        
    def test_cd(self):
        self.fs.mkdir("projects")
        self.fs.cd("projects")
        self.assertEqual(self.fs.pwd(), "/projects")
        self.fs.cd("..")
        self.assertEqual(self.fs.pwd(), "/")
        self.fs.cd("projects")
        self.fs.cd("/")
        self.assertEqual(self.fs.pwd(), "/")

    def test_nested_directories(self):
        self.fs.mkdir("projects")
        self.fs.cd("projects")
        self.fs.mkdir("os")
        self.fs.cd("os")
        self.assertEqual(self.fs.pwd(), "/projects/os")
        
    def test_files_in_directories(self):
        self.fs.mkdir("projects")
        self.fs.cd("projects")
        self.fs.create_file("notes.txt")
        self.fs.write_file("notes.txt", "OS Notes")
        self.assertIn("notes.txt", self.fs.ls())
        self.assertEqual(self.fs.read_file("notes.txt"), "OS Notes")
        
    def test_rmdir(self):
        self.fs.mkdir("projects")
        self.fs.rmdir("projects")
        self.assertNotIn("projects", self.fs.ls())
        
    def test_rmdir_not_empty(self):
        self.fs.mkdir("projects")
        self.fs.cd("projects")
        self.fs.create_file("notes.txt")
        self.fs.cd("..")
        with self.assertRaises(Exception):
            self.fs.rmdir("projects")
            
    def test_invalid_cd(self):
        with self.assertRaises(Exception):
            self.fs.cd("ghost")
            
if __name__ == '__main__':
    unittest.main()
