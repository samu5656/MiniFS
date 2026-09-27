# MiniFS

MiniFS is a simulated file system project designed for a 2-day Operating Systems mini-project. It demonstrates core OS concepts such as file management, directory hierarchies, metadata, permissions, storage allocation, and fragmentation.

## Features

- **Virtual Disk:** Simulates a storage device with configurable blocks.
- **File & Directory Management:** Create, read, write, rename, and delete files/directories.
- **Hierarchical Structure:** Navigate through a tree of directories.
- **Metadata & Permissions:** Simulates Unix-style permissions (`rw-r--r--`) and displays file metadata (owner, size, allocation, etc.).
- **Graphical User Interface (GUI):** A simple, beginner-friendly Tkinter interface to visualize the file system tree and real-time disk block allocation.
- **Fragmentation Metric:** Demonstrates storage fragmentation by calculating the number of separated free-space regions.

## Project Structure

```text
MiniFS/
├── src/
│   ├── main.py           # Application entry point
│   ├── disk.py           # Virtual disk and block management
│   ├── filesystem.py     # File system operations and API
│   ├── models.py         # Data models for File and Directory
│   ├── permissions.py    # Simulated access control
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
2. **View Metadata:** Click on `readme.txt` to see its file metadata.
3. **Read File:** Click the **Read** button to view the file's contents.
4. **Create a File:** Navigate to a directory, click **New File**, and provide a name.
5. **Write Data:** Select the new file, click **Write**, and enter text. Watch the Virtual Disk allocate red blocks!
6. **Demonstrate Fragmentation:** Create multiple files, write data to them, and then delete a file from the middle. Notice how the free blocks (green) are separated, and the simulated Fragmentation metric increases.
7. **Test Permissions:** The system uses simplified permissions. For example, if a user lacks write access, attempting to write will raise an "ACCESS DENIED" error.
