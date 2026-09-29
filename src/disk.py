class VirtualDisk:
    def __init__(self, total_blocks=64, block_size=64, allocation_strategy="contiguous"):
        """Initialize the virtual disk with configurable blocks, size, and allocation strategy."""
        self.total_blocks = total_blocks
        self.block_size = block_size
        self.allocation_strategy = allocation_strategy
        self.blocks = ["FREE"] * total_blocks
        self.fat = {i: None for i in range(total_blocks)}

    def allocate_blocks(self, count):
        """
        Allocate blocks according to the selected allocation strategy.
        """
        if count <= 0:
            raise ValueError("Count must be greater than 0")

        if self.allocation_strategy == "contiguous":
            return self._allocate_contiguous(count)
        elif self.allocation_strategy == "linked":
            return self._allocate_linked(count)
        elif self.allocation_strategy == "indexed":
            return self._allocate_indexed(count)
        else:
            raise ValueError(f"Unknown allocation strategy: {self.allocation_strategy}")

    def _allocate_contiguous(self, count):
        start_idx = -1
        current_len = 0

        for i in range(self.total_blocks):
            if self.blocks[i] == "FREE":
                if current_len == 0:
                    start_idx = i
                current_len += 1
                if current_len == count:
                    allocated = list(range(start_idx, start_idx + count))
                    for idx in allocated:
                        self.blocks[idx] = "USED"
                    return allocated
            else:
                current_len = 0

        raise Exception("Not enough contiguous free space")

    def _allocate_linked(self, count):
        free_indices = [i for i, b in enumerate(self.blocks) if b == "FREE"]
        if len(free_indices) < count:
            raise Exception("Not enough free space")
        
        allocated = free_indices[:count]
        for i in range(count):
            idx = allocated[i]
            self.blocks[idx] = "USED"
            if i < count - 1:
                self.fat[idx] = allocated[i+1]
            else:
                self.fat[idx] = -1 # End of file
        return allocated

    def _allocate_indexed(self, count):
        # We need count + 1 blocks (1 for the index block)
        free_indices = [i for i, b in enumerate(self.blocks) if b == "FREE"]
        if len(free_indices) < count + 1:
            raise Exception("Not enough free space for data and index blocks")
        
        allocated = free_indices[:count + 1]
        for idx in allocated:
            self.blocks[idx] = "USED"
        return allocated

    def free_blocks(self, block_indices):
        """Free a list of allocated blocks."""
        for idx in block_indices:
            if idx < 0 or idx >= self.total_blocks:
                raise ValueError(f"Invalid block index: {idx}")
            self.blocks[idx] = "FREE"
            self.fat[idx] = None

    def get_free_blocks(self):
        """Return the count of free blocks."""
        return sum(1 for b in self.blocks if b == "FREE")

    def get_used_blocks(self):
        """Return the count of used blocks."""
        return sum(1 for b in self.blocks if b == "USED")

    def get_usage(self):
        """Return the disk usage as a percentage."""
        if self.total_blocks == 0:
            return 0.0
        return (self.get_used_blocks() / self.total_blocks) * 100

    def get_fragmentation(self):
        """Calculate the number of separated free-space regions (simulation metric)."""
        regions = 0
        in_free_region = False
        for state in self.blocks:
            if state == "FREE":
                if not in_free_region:
                    regions += 1
                    in_free_region = True
            else:
                in_free_region = False
        return regions

    def get_fragmentation_percent(self):
        """Calculate fragmentation as a percentage of free blocks that are not contiguous."""
        regions = self.get_fragmentation()
        if regions <= 1:
            return 0.0
            
        free_blocks = self.get_free_blocks()
        if free_blocks <= 1:
            return 0.0
            
        # Percentage of free space regions out of total free blocks.
        frag = ((regions - 1) / (free_blocks - 1)) * 100
        return min(100.0, frag)

    def get_statistics(self):
        """Return basic disk statistics."""
        return {
            "Total Blocks": self.total_blocks,
            "Used Blocks": self.get_used_blocks(),
            "Free Blocks": self.get_free_blocks(),
            "Usage": f"{self.get_usage():.1f}%",
            "Fragmentation": self.get_fragmentation(),
            "Fragmentation %": f"{self.get_fragmentation_percent():.1f}%",
            "Strategy": self.allocation_strategy.capitalize()
        }
