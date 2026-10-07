import time

class Process:
    def __init__(self, pid, burst_time):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.state = "READY" # READY, RUNNING, COMPLETED

class CPUScheduler:
    def __init__(self, algorithm="RR", quantum=2):
        self.algorithm = algorithm
        self.quantum = quantum
        self.ready_queue = []
        self.current_process = None
        self.completed_processes = []
        self.time = 0
        self.current_slice = 0

    def add_process(self, pid, burst_time):
        p = Process(pid, burst_time)
        self.ready_queue.append(p)
        return p

    def step(self):
        """Execute one step (time unit) of the scheduler."""
        if self.current_process is None or self.current_process.state == "COMPLETED" or self.current_process.state == "READY":
            if not self.ready_queue:
                self.current_process = None
                return False # Nothing to run
            
            # Context switch
            self.current_process = self.ready_queue.pop(0)
            self.current_process.state = "RUNNING"
            self.current_slice = 0
            
        # Execute for 1 time unit
        self.current_process.remaining_time -= 1
        self.time += 1
        self.current_slice += 1
        
        if self.current_process.remaining_time <= 0:
            self.current_process.remaining_time = 0
            self.current_process.state = "COMPLETED"
            self.completed_processes.append(self.current_process)
            # Will pick next process on next step
        elif self.algorithm == "RR" and self.current_slice >= self.quantum:
            # Time slice expired
            self.current_process.state = "READY"
            self.ready_queue.append(self.current_process)
            # Will pick next process on next step
            
        return True
