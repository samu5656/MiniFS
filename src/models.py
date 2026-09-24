import time

class File:
    def __init__(self, name, file_type="file", owner="user", permissions="rw-r--r--"):
        self.name = name
        self.type = file_type
        self.size = 0
        self.content = ""
        self.owner = owner
        self.permissions = permissions
        self.created_at = time.time()
        self.modified_at = self.created_at
        self.allocated_blocks = []

class Directory:
    def __init__(self, name, parent=None, owner="user", permissions="rwxr-xr-x"):
        self.name = name
        self.type = "directory"
        self.children = {}
        self.parent = parent
        self.owner = owner
        self.permissions = permissions
        self.created_at = time.time()
        self.modified_at = self.created_at
