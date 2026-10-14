# MiniFS

MiniFS is a simulated file system project designed for a 2-day Operating Systems mini-project. It demonstrates core OS concepts such as file management, directory hierarchies, metadata, permissions, storage allocation, fragmentation, memory management (swapping), and CPU scheduling.

## Features

- **Virtual Disk & File System Core:** Simulates a storage device with contiguous block allocation.
- **File & Directory Management:** Create, read, write, rename, and delete files/directories.
- **Buffer Cache:** Simulates file system caching to improve read/write performance, demonstrating cache hits and misses.
- **Metadata & Permissions:** Simulates Unix-style permissions and displays file metadata (owner, size, allocation, etc.).
- **File Locking:** Simulates mutual exclusion by allowing files to be locked/unlocked, preventing unauthorized access.
- **Defragmentation:** Resolves disk fragmentation by compacting used blocks and grouping free space together.
- **Memory Management (Swapping):** Simulates Virtual RAM. When RAM is full, it automatically swaps inactive processes to the disk (Swap Space) to accommodate new processes.
- **CPU Scheduling:** Simulates process execution using a Round Robin scheduling algorithm, complete with visual queues and time slices.
- **Graphical User Interface (GUI):** A beginner-friendly Tkinter interface with real-time visualizers for the Virtual Disk, RAM, and CPU processes.

## Project Structure

```text
MiniFS/
├── src/
│   ├── main.py           # Application entry point
│   ├── disk.py           # Virtual disk and block management
│   ├── filesystem.py     # File system operations, caching, and API
│   ├── models.py         # Data models for File and Directory
│   ├── permissions.py    # Simulated access control and locking
│   ├── memory.py         # Virtual RAM and Swapping logic
│   ├── cpu.py            # Round Robin CPU Scheduler
│   └── gui.py            # Tkinter graphical interface
├── tests/                # Unittest suite
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

## Setup & Installation

Since this project relies on Python standard libraries, no external installations are strictly necessary.

1. Ensure you have **Python 3.x** installed.
2. Clone or download the repository.
3. (Optional) Install dependencies (currently empty as we use standard libraries):
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To launch the MiniFS GUI, run:

```bash
python src/main.py
```

## Running Tests

To verify the core logic, run the test suite:

```bash
python -m unittest discover tests
```

## Demonstration Steps

1. **Start the application:** Run `python src/main.py`.
2. **File Operations & Allocation:** Create a file, write data to it, and watch the Virtual Disk allocate blocks (turning red). Read the file to see the Buffer Cache stats update.
3. **File Locking (Mutual Exclusion):** Select a file and click **Lock/Unlock**. Observe the metadata update to show the lock status.
4. **Fragmentation & Defragmentation:** Create multiple files and write data. Delete a file in the middle to create a gap (fragmentation). Click **Defragment** to compact the disk and resolve the fragmentation.
5. **Memory Management (Swapping):** Start multiple processes until the Virtual RAM (blue blocks) is full. Start one more process and watch the system swap an old process out to the Swap Space on the disk (orange blocks).
6. **CPU Scheduling:** Switch to the **CPU Scheduler** tab. Add multiple processes with burst times. Click **Auto Run** to watch the Round Robin scheduler execute them using time slices, moving them from the Ready Queue to Completion.
