class VirtualDisk:
    def __init__(self, total_blocks=64, block_size=64):
        """Initialize the virtual disk with a configurable number of blocks and block size."""
        self.total_blocks = total_blocks
        self.block_size = block_size
        self.blocks = ["FREE"] * total_blocks

    def allocate_blocks(self, count):
        """
        Allocate a contiguous sequence of blocks.
        A real OS stores files on physical storage blocks. 
        MiniFS simulates those blocks using Python data structures.
        """
        if count <= 0:
            raise ValueError("Count must be greater than 0")

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

    def free_blocks(self, block_indices):
        """Free a list of allocated blocks."""
        for idx in block_indices:
            if idx < 0 or idx >= self.total_blocks:
                raise ValueError(f"Invalid block index: {idx}")
            self.blocks[idx] = "FREE"

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

    def get_statistics(self):
        """Return basic disk statistics."""
        return {
            "Total Blocks": self.total_blocks,
            "Used Blocks": self.get_used_blocks(),
            "Free Blocks": self.get_free_blocks(),
            "Usage": f"{self.get_usage():.1f}%"
        }
