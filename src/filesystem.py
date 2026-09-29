import math
import time
from datetime import datetime
from disk import VirtualDisk
from models import File, Directory
from permissions import PermissionManager

class BufferCache:
    def __init__(self, capacity=5, policy="LRU"):
        self.capacity = capacity
        self.policy = policy
        self.cache = {} # block_index -> bool (just simulating presence)
        self.order = []
        self.hits = 0
        self.misses = 0

    def access_block(self, block_index):
        if block_index in self.cache:
            self.hits += 1
            if self.policy == "LRU":
                self.order.remove(block_index)
                self.order.append(block_index)
            return True
        else:
            self.misses += 1
            if len(self.cache) >= self.capacity:
                self.evict()
            self.cache[block_index] = True
            self.order.append(block_index)
            return False

    def evict(self):
        if not self.order: return
        evicted = self.order.pop(0)
        del self.cache[evicted]

    def get_stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return f"Hits: {self.hits} | Misses: {self.misses} | Rate: {hit_rate:.1f}% | Cache: {list(self.cache.keys())}"

class FileSystem:
    def __init__(self, disk=None, current_user="user"):
        """Initialize the file system with a virtual disk, root directory, and current user."""
        self.disk = disk if disk else VirtualDisk()
        self.root = Directory("/", owner=current_user)
        self.current_directory = self.root
        self.current_user = current_user
        self.cache = BufferCache(capacity=5, policy="LRU")

    def mkdir(self, name):
        """Create a new directory in the current directory."""
        if name in self.current_directory.children:
            raise Exception("Directory or file already exists.")
        
        new_dir = Directory(name, parent=self.current_directory, owner=self.current_user)
        self.current_directory.children[name] = new_dir

    def rmdir(self, name):
        """Remove an empty directory."""
        if name not in self.current_directory.children:
            raise Exception("Directory not found.")
        
        dir_obj = self.current_directory.children[name]
        if dir_obj.type != "directory":
            raise Exception(f"'{name}' is not a directory.")
            
        if not PermissionManager.check_access(dir_obj.permissions, dir_obj.owner, self.current_user, "write"):
            raise Exception("ACCESS DENIED")
            
        if len(dir_obj.children) > 0:
            raise Exception("Directory is not empty.")
            
        del self.current_directory.children[name]

    def cd(self, path):
        """Change current directory."""
        if path == "/":
            self.current_directory = self.root
        elif path == ".":
            pass
        elif path == "..":
            if self.current_directory.parent is not None:
                self.current_directory = self.current_directory.parent
        else:
            if path not in self.current_directory.children:
                raise Exception("Directory not found.")
            target = self.current_directory.children[path]
            if target.type != "directory":
                raise Exception(f"'{path}' is not a directory.")
            
            if not PermissionManager.check_access(target.permissions, target.owner, self.current_user, "execute"):
                raise Exception("ACCESS DENIED")
                
            self.current_directory = target

    def pwd(self):
        """Return the current path."""
        path_parts = []
        current = self.current_directory
        while current is not None:
            if current.name != "/":
                path_parts.insert(0, current.name)
            current = current.parent
        if not path_parts:
            return "/"
        return "/" + "/".join(path_parts)

    def ls(self):
        """List contents of the current directory."""
        if not PermissionManager.check_access(self.current_directory.permissions, self.current_directory.owner, self.current_user, "read"):
            raise Exception("ACCESS DENIED")
        return list(self.current_directory.children.keys())

    def create_file(self, name):
        """Create a new empty file in the current directory."""
        if name in self.current_directory.children:
            raise Exception("File or directory already exists.")
        
        # We need write permissions in the current directory to create a file
        if not PermissionManager.check_access(self.current_directory.permissions, self.current_directory.owner, self.current_user, "write"):
            raise Exception("ACCESS DENIED")
            
        new_file = File(name, owner=self.current_user)
        self.current_directory.children[name] = new_file
        return new_file

    def write_file(self, name, content):
        """Write content to a file, allocating virtual disk blocks as needed."""
        if name not in self.current_directory.children:
            raise Exception("File not found.")
            
        file_obj = self.current_directory.children[name]
        if file_obj.type != "file":
            raise Exception(f"'{name}' is not a file.")
            
        if getattr(file_obj, 'locked', False):
            raise Exception("File in Use")
            
        if not PermissionManager.check_access(file_obj.permissions, file_obj.owner, self.current_user, "write"):
            raise Exception("ACCESS DENIED")
        
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
                file_obj.size = 0
                file_obj.content = ""
                raise Exception(f"Not enough free disk space: {str(e)}")
                
        file_obj.modified_at = time.time()

    def read_file(self, name):
        """Read content from a file."""
        if name not in self.current_directory.children:
            raise Exception("File not found.")
            
        file_obj = self.current_directory.children[name]
        if file_obj.type != "file":
            raise Exception(f"'{name}' is not a file.")
            
        if getattr(file_obj, 'locked', False):
            raise Exception("File in Use")
            
        if not PermissionManager.check_access(file_obj.permissions, file_obj.owner, self.current_user, "read"):
            raise Exception("ACCESS DENIED")
            
        # Simulate caching blocks
        for block in file_obj.allocated_blocks:
            self.cache.access_block(block)
            
        return file_obj.content

    def delete_file(self, name):
        """Delete a file and free its allocated blocks."""
        if name not in self.current_directory.children:
            raise Exception("File not found.")
            
        file_obj = self.current_directory.children[name]
        if file_obj.type != "file":
            raise Exception(f"'{name}' is not a file.")
            
        if getattr(file_obj, 'locked', False):
            raise Exception("File in Use")
            
        # Require write access on the directory or the file itself?
        # Usually, deleting a file requires write access on the directory.
        if not PermissionManager.check_access(self.current_directory.permissions, self.current_directory.owner, self.current_user, "write"):
            raise Exception("ACCESS DENIED")
            
        if file_obj.allocated_blocks:
            self.disk.free_blocks(file_obj.allocated_blocks)
            
        del self.current_directory.children[name]

    def rename_file(self, old_name, new_name):
        """Rename an existing file, preserving content and metadata."""
        if old_name not in self.current_directory.children:
            raise Exception("File not found.")
        if new_name in self.current_directory.children:
            raise Exception("File or directory already exists.")
            
        # Require write access on the directory
        if not PermissionManager.check_access(self.current_directory.permissions, self.current_directory.owner, self.current_user, "write"):
            raise Exception("ACCESS DENIED")
            
        file_obj = self.current_directory.children[old_name]
        if file_obj.type != "file":
            raise Exception(f"'{old_name}' is not a file.")
            
        if getattr(file_obj, 'locked', False):
            raise Exception("File in Use")
            
        file_obj.name = new_name
        file_obj.modified_at = time.time()
        
        self.current_directory.children[new_name] = file_obj
        del self.current_directory.children[old_name]

    def get_metadata(self, name):
        """Get formatted metadata for a file or directory."""
        if name not in self.current_directory.children:
            raise Exception("File or directory not found.")
            
        obj = self.current_directory.children[name]
        
        created_str = datetime.fromtimestamp(obj.created_at).strftime('%Y-%m-%d %H:%M:%S')
        modified_str = datetime.fromtimestamp(obj.modified_at).strftime('%Y-%m-%d %H:%M:%S')
        
        meta = [
            f"Name: {obj.name}",
            f"Type: {'File' if obj.type == 'file' else 'Directory'}",
            f"Owner: {obj.owner}",
            f"Permissions: {obj.permissions}",
            f"Created Time: {created_str}",
            f"Modified Time: {modified_str}"
        ]
        
        if obj.type == "file":
            meta.insert(2, f"Size: {obj.size} bytes")
            meta.insert(3, f"Locked: {'Yes' if getattr(obj, 'locked', False) else 'No'}")
            if self.disk.allocation_strategy == "indexed" and obj.allocated_blocks:
                meta.append(f"Index Block: {obj.allocated_blocks[0]}")
                meta.append(f"Data Blocks: {obj.allocated_blocks[1:]}")
            else:
                meta.append(f"Allocated Blocks: {obj.allocated_blocks}")
            
        return "\n".join(meta)

    def toggle_lock(self, name):
        """Toggle the lock status of a file."""
        if name not in self.current_directory.children:
            raise Exception("File not found.")
            
        file_obj = self.current_directory.children[name]
        if file_obj.type != "file":
            raise Exception(f"'{name}' is not a file.")
            
        file_obj.locked = not getattr(file_obj, 'locked', False)
        return file_obj.locked

    def chmod(self, name, permissions):
        """Change permissions of a file or directory."""
        if name not in self.current_directory.children:
            raise Exception("File or directory not found.")
            
        obj = self.current_directory.children[name]
        if obj.owner != self.current_user and self.current_user != "root":
            raise Exception("ACCESS DENIED")
            
        if len(permissions) != 9:
            raise Exception("Invalid permission format. Expected 9 characters like 'rw-r--r--'.")
            
        obj.permissions = permissions
        obj.modified_at = time.time()

    def defragment(self):
        """Compact the virtual disk by moving all files to the beginning."""
        all_files = []
        def collect_files(directory):
            for name, obj in directory.children.items():
                if obj.type == "file" and obj.allocated_blocks:
                    all_files.append(obj)
                elif obj.type == "directory":
                    collect_files(obj)
                    
        collect_files(self.root)
        
        # Sort files by their current starting block to maintain relative order
        all_files.sort(key=lambda f: f.allocated_blocks[0])
        
        # Wipe the virtual disk
        self.disk.blocks = ["FREE"] * self.disk.total_blocks
        if hasattr(self.disk, 'fat'):
            self.disk.fat = {i: None for i in range(self.disk.total_blocks)}
            
        # Reallocate for each file using its original data size
        for f in all_files:
            blocks_needed = math.ceil(f.size / self.disk.block_size)
            if blocks_needed > 0:
                f.allocated_blocks = self.disk.allocate_blocks(blocks_needed)
