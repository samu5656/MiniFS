import math
import time
from disk import VirtualDisk
from models import File

class FileSystem:
    def __init__(self, disk=None):
        """Initialize the file system with a virtual disk."""
        self.disk = disk if disk else VirtualDisk()
        # For Phase 2, a flat dictionary simulating a root directory is sufficient.
        self.files = {}

    def create_file(self, name):
        """Create a new empty file."""
        if name in self.files:
            raise Exception("File already exists.")
        
        new_file = File(name)
        self.files[name] = new_file
        return new_file

    def write_file(self, name, content):
        """Write content to a file, allocating virtual disk blocks as needed."""
        if name not in self.files:
            raise Exception("File not found.")
            
        file_obj = self.files[name]
        
        # Free previously allocated blocks if any
        if file_obj.allocated_blocks:
            self.disk.free_blocks(file_obj.allocated_blocks)
            file_obj.allocated_blocks = []
            
        file_obj.content = content
        file_obj.size = len(content)
        
        # Calculate blocks needed
        blocks_needed = math.ceil(file_obj.size / self.disk.block_size)
        
        if blocks_needed > 0:
            try:
                allocated = self.disk.allocate_blocks(blocks_needed)
                file_obj.allocated_blocks = allocated
            except Exception as e:
                # If allocation fails, the file becomes empty in this simple simulation
                file_obj.size = 0
                file_obj.content = ""
                raise Exception(f"Not enough free disk space: {str(e)}")
                
        file_obj.modified_at = time.time()

    def read_file(self, name):
        """Read content from a file."""
        if name not in self.files:
            raise Exception("File not found.")
        return self.files[name].content

    def delete_file(self, name):
        """Delete a file and free its allocated blocks."""
        if name not in self.files:
            raise Exception("File not found.")
            
        file_obj = self.files[name]
        if file_obj.allocated_blocks:
            self.disk.free_blocks(file_obj.allocated_blocks)
            
        del self.files[name]

    def rename_file(self, old_name, new_name):
        """Rename an existing file, preserving content and metadata."""
        if old_name not in self.files:
            raise Exception("File not found.")
        if new_name in self.files:
            raise Exception("File already exists.")
            
        file_obj = self.files[old_name]
        file_obj.name = new_name
        file_obj.modified_at = time.time()
        
        self.files[new_name] = file_obj
        del self.files[old_name]
