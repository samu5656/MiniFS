class Process:
    def __init__(self, pid, blocks_needed):
        self.pid = pid
        self.blocks_needed = blocks_needed
        self.state = "NEW" # NEW, RUNNING, SWAPPED
        self.ram_blocks = []
        self.swap_blocks = []

class MemoryManager:
    def __init__(self, disk, ram_size=16, swap_start=48, swap_size=16):
        self.disk = disk
        self.ram_size = ram_size
        self.ram = ["FREE"] * ram_size
        self.swap_start = swap_start
        self.swap_size = swap_size
        
        # Reserve swap space on disk
        for i in range(swap_start, swap_start + swap_size):
            self.disk.blocks[i] = "SWAP_FREE"
            
        self.processes = {} # pid -> Process
        self.lru_queue = [] # List of pids to track LRU (First In First Out / Least Recently Used)
        
    def start_process(self, pid, blocks_needed):
        if blocks_needed > self.ram_size:
            raise Exception("Process requires more blocks than total RAM")
            
        if pid in self.processes:
            raise Exception("Process ID already exists")
            
        process = Process(pid, blocks_needed)
        self.processes[pid] = process
        
        # Try to load into RAM
        self._load_into_ram(process)
        
    def _load_into_ram(self, process):
        free_ram = sum(1 for b in self.ram if b == "FREE")
        
        # If not enough RAM, we must swap out older processes
        while free_ram < process.blocks_needed and self.lru_queue:
            victim_pid = self.lru_queue.pop(0) # Evict oldest process in RAM
            self._swap_out(self.processes[victim_pid])
            free_ram = sum(1 for b in self.ram if b == "FREE")
            
        if free_ram < process.blocks_needed:
            raise Exception("Cannot free enough RAM to load process")
            
        # Allocate RAM blocks
        allocated = 0
        process.ram_blocks = []
        for i in range(self.ram_size):
            if self.ram[i] == "FREE":
                self.ram[i] = process.pid
                process.ram_blocks.append(i)
                allocated += 1
                if allocated == process.blocks_needed:
                    break
                    
        process.state = "RUNNING"
        self.lru_queue.append(process.pid)
        
    def _swap_out(self, process):
        """Move process from RAM to Swap Space on disk."""
        if process.state != "RUNNING":
            return
            
        # Find free swap blocks on disk
        free_swap = []
        for i in range(self.swap_start, self.swap_start + self.swap_size):
            if self.disk.blocks[i] == "SWAP_FREE":
                free_swap.append(i)
                
        if len(free_swap) < len(process.ram_blocks):
            raise Exception("Out of Swap Space! System Crash!")
            
        # Move to swap
        process.swap_blocks = free_swap[:len(process.ram_blocks)]
        for swap_idx in process.swap_blocks:
            self.disk.blocks[swap_idx] = f"SWAP_{process.pid}"
            
        # Free RAM
        for ram_idx in process.ram_blocks:
            self.ram[ram_idx] = "FREE"
            
        process.ram_blocks = []
        process.state = "SWAPPED"
        
    def stop_process(self, pid):
        if pid not in self.processes:
            raise Exception("Process not found")
            
        process = self.processes[pid]
        
        # Free RAM
        for ram_idx in process.ram_blocks:
            self.ram[ram_idx] = "FREE"
            
        # Free Swap
        for swap_idx in process.swap_blocks:
            self.disk.blocks[swap_idx] = "SWAP_FREE"
            
        if pid in self.lru_queue:
            self.lru_queue.remove(pid)
            
        del self.processes[pid]
