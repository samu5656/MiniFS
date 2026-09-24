import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from filesystem import FileSystem
from disk import VirtualDisk
from permissions import PermissionManager

class TestPermissionsAndMetadata(unittest.TestCase):
    def setUp(self):
        self.disk = VirtualDisk(64, 64)
        self.fs = FileSystem(self.disk, current_user="user1")
        
    def test_permission_manager(self):
        self.assertTrue(PermissionManager.check_access("rw-r--r--", "user1", "user1", "write"))
        self.assertTrue(PermissionManager.check_access("rw-r--r--", "user1", "user1", "read"))
        self.assertFalse(PermissionManager.check_access("rw-r--r--", "user1", "user2", "write"))
        self.assertTrue(PermissionManager.check_access("rw-r--r--", "user1", "user2", "read"))
        self.assertFalse(PermissionManager.check_access("rw-r--r--", "user1", "user1", "execute"))
        
    def test_file_metadata(self):
        self.fs.create_file("test.txt")
        self.fs.write_file("test.txt", "data")
        meta = self.fs.get_metadata("test.txt")
        self.assertIn("Name: test.txt", meta)
        self.assertIn("Type: File", meta)
        self.assertIn("Owner: user1", meta)
        self.assertIn("Size: 4 bytes", meta)
        self.assertIn("Permissions: rw-r--r--", meta)
        
    def test_access_denied_read(self):
        self.fs.create_file("secret.txt")
        self.fs.write_file("secret.txt", "secret_data")
        self.fs.chmod("secret.txt", "rw-------") # only owner can read/write
        
        # change user
        self.fs.current_user = "user2"
        with self.assertRaises(Exception) as context:
            self.fs.read_file("secret.txt")
        self.assertIn("ACCESS DENIED", str(context.exception))
        
    def test_access_denied_write(self):
        self.fs.create_file("public.txt")
        self.fs.write_file("public.txt", "public_data")
        self.fs.chmod("public.txt", "rw-r--r--")
        
        self.fs.current_user = "user2"
        with self.assertRaises(Exception) as context:
            self.fs.write_file("public.txt", "hacked")
        self.assertIn("ACCESS DENIED", str(context.exception))
        
    def test_chmod_access_denied(self):
        self.fs.create_file("file.txt")
        self.fs.current_user = "user2"
        with self.assertRaises(Exception) as context:
            self.fs.chmod("file.txt", "rwxrwxrwx")
        self.assertIn("ACCESS DENIED", str(context.exception))

if __name__ == '__main__':
    unittest.main()
