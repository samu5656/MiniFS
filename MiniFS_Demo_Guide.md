# MiniFS Demonstration & Theory Guide

This guide is designed to help you present the MiniFS project. For every Operating System concept implemented, it provides the theoretical background, the location of the implementation in the codebase, and a step-by-step walkthrough of how to demo it to your examiner.

---

## 1. File Systems & Hierarchical Directory Structure

### 📖 Theoretical Definition
A File System is the method and data structure an operating system uses to keep track of files on a disk or partition. It organizes files into a hierarchical directory structure (a tree), allowing users to create, read, navigate, and manage data efficiently using paths (e.g., `/projects/notes.txt`).

### 💻 Where it is implemented
- **Files:** `src/models.py` (File & Directory classes), `src/filesystem.py`
- **Navigation:** `src/filesystem.py` (`mkdir`, `cd`, `ls` functions)
- **GUI:** `src/gui.py` (Treeview UI on the left)

### 🚀 How to show the demo
1. Launch the app (`python src/main.py`).
2. Click the **New Directory** button and name it `projects`.
3. Click **New Directory** again and name it `documents`.
4. Double-click on `projects` in the file tree on the left.
5. Click **New File** and name it `notes.txt`.

### 👁️ What to observe
- The **Current Path** at the top updates from `/` to `/projects`.
- The **File Tree** successfully visually nests `notes.txt` inside `projects`. 
- Clicking **Up (..)** will take you back to the root directory, demonstrating dynamic traversal of the tree structure.

---

## 2. Storage Management & Contiguous Allocation

### 📖 Theoretical Definition
File allocation methods define how disk blocks are allocated for files. **Contiguous Allocation** requires that each file occupies a set of contiguous (physically adjacent) blocks on the disk. This allows for fast sequential read performance but suffers from external fragmentation over time.

### 💻 Where it is implemented
- **Logic:** `src/disk.py` (`allocate_blocks` and `free_blocks` methods)
- **GUI:** `src/gui.py` (The Virtual Disk canvas visualization)

### 🚀 How to show the demo
1. Select the `notes.txt` file you created.
2. Click **Write** and enter a sentence (e.g., `"Operating Systems are amazing."`).
3. Click OK.

### 👁️ What to observe
- Look at the **Virtual Disk & Swap Space** visualization at the bottom of the window. 
- Some of the green `[FREE]` blocks will instantly turn into red `[USED]` blocks. 
- Because the allocation is contiguous, the red blocks will be clustered perfectly together in a single row without gaps.
- The **System Stats** text below the disk will show an increase in "Used Blocks" and "Usage %".

---

## 3. Metadata & File Control Blocks (FCB)

### 📖 Theoretical Definition
A File Control Block (FCB) or Inode is a file system structure in which the OS stores all metadata about a file (except its name/actual data). Metadata includes file type, size, ownership, access permissions, creation timestamps, and pointers to the disk blocks that hold the file's content.

### 💻 Where it is implemented
- **Logic:** `src/models.py` (The `File` class properties)
- **GUI:** `src/gui.py` (The File Information panel)

### 🚀 How to show the demo
1. Single-click on `notes.txt` in the File Tree to highlight it.

### 👁️ What to observe
- The **File Information** panel on the right side of the screen immediately populates.
- Point out to the examiner that it displays the File Name, Type, Size in bytes, Owner, Permissions (e.g., `rw-r--r--`), and most importantly, the **Allocated Blocks** (the exact array index numbers on the virtual disk where the file's data resides).

---

## 4. Fragmentation & Defragmentation (Compaction)

### 📖 Theoretical Definition
**External Fragmentation** occurs when free memory/disk space is separated into small blocks and is interspersed among allocated files, making it difficult to allocate new large files despite having enough total free space. **Defragmentation (Compaction)** is the process of physically moving file blocks closer together to consolidate all free space into one large contiguous block.

### 💻 Where it is implemented
- **Logic:** `src/disk.py` (`defragment` method)
- **GUI:** `src/gui.py` (`defragment` button and Fragmentation stats)

### 🚀 How to show the demo
1. Create a file called `temp1.txt` and write data into it.
2. Create a file called `temp2.txt` and write data into it. 
3. You now have a solid line of red blocks.
4. Select `temp1.txt` and click **Delete**.

### 👁️ What to observe
- The blocks that `temp1.txt` occupied turn back to green (`FREE`), but they are trapped between the system blocks and `temp2.txt`. This represents **Fragmentation**. 
- Point out the **Fragmentation %** in the System Stats jumping above 0%.
- **Action:** Click the **Defragment** button.
- **Observe:** The red blocks of `temp2.txt` shift to the left, closing the green gap. The fragmentation percentage drops back to 0, demonstrating Compaction.

---

## 5. File Locking (Mutual Exclusion / Concurrency Control)

### 📖 Theoretical Definition
When multiple processes attempt to access a file simultaneously, it can lead to data corruption or race conditions. **Mutual Exclusion** is achieved using File Locks, ensuring that if a process locks a file for writing/reading, no other process can access it until it is unlocked.

### 💻 Where it is implemented
- **Logic:** `src/permissions.py` or `src/models.py` (Lock flags on files)
- **GUI:** `src/gui.py` (`Lock/Unlock` button)

### 🚀 How to show the demo
1. Select a file (e.g., `notes.txt`).
2. Click the **Lock/Unlock** button.

### 👁️ What to observe
- A popup will confirm the file is locked.
- The **File Information** panel will update to show the file is now `Locked`.
- Explain that in a real OS, this prevents other processes from writing to the file while we are working on it. (Click it again to unlock).

---

## 6. Memory Management: Virtual RAM & Swapping

### 📖 Theoretical Definition
When the physical memory (RAM) is completely filled by running processes, the OS uses **Swapping**. It moves an inactive or blocked process out of the RAM and stores it on a dedicated portion of the hard disk called **Swap Space (Virtual Memory)**. This frees up RAM so a new process can be loaded and executed.

### 💻 Where it is implemented
- **Logic:** `src/memory.py` (RAM size limits and Swap Space allocation)
- **GUI:** `src/gui.py` (Virtual RAM visualizer and the `Start Process` / `Stop Process` buttons)

### 🚀 How to show the demo
1. Ensure the **Virtual RAM** canvas at the bottom is empty (green blocks).
2. Click **Start Process**. ID: `P1`, Blocks needed: `6`.
3. Start another. ID: `P2`, Blocks needed: `6`.
4. Start another. ID: `P3`, Blocks needed: `4`. (RAM is now 100% full).
5. Start a final process. ID: `P4`, Blocks needed: `4`.

### 👁️ What to observe
- When you add `P1`, `P2`, and `P3`, watch the **Virtual RAM** canvas fill up with blue blocks representing those processes.
- When you add `P4` (which exceeds the 16-block RAM limit), the OS performs **Swapping**.
- Observe the **Virtual Disk** below the RAM. Orange blocks (`SWAP_USED`) will appear on the disk. Tell the examiner: *"The OS just evicted an older process from RAM to the Disk's Swap Space to make room for P4."*

---

## 7. CPU Scheduling (Round Robin)

### 📖 Theoretical Definition
A CPU Scheduler dictates which process in the ready queue gets to use the CPU. **Round Robin (RR)** is a preemptive scheduling algorithm where each process is assigned a fixed time slot (Time Quantum). If the process doesn't finish within its slot, it is paused (context switched), placed at the back of the queue, and the CPU is given to the next process.

### 💻 Where it is implemented
- **Logic:** `src/cpu.py` (`CPUScheduler` class, `step` function)
- **GUI:** `src/gui.py` (CPU Scheduler Tab, Ready/Completed Queues)

### 🚀 How to show the demo
1. Click on the **CPU Scheduler** tab at the very top of the window.
2. Click **Add Process**. ID: `P1`, Burst Time: `5`.
3. Click **Add Process**. ID: `P2`, Burst Time: `3`.
4. Click **Add Process**. ID: `P3`, Burst Time: `7`.
5. Click **Auto Run**.

### 👁️ What to observe
- The three processes start in the **Ready Queue**.
- In the center **CPU (Executing)** box, you will see `P1` load in. 
- Watch the **Remaining Time** tick down. Because of the Time Quantum, `P1` won't finish entirely. It gets interrupted, put back into the Ready Queue, and `P2` starts running.
- Once a process's Remaining Time hits 0, it drops into the **Completed** queue. This visually proves that the system is sharing CPU time fairly among all processes rather than executing them sequentially (First-Come, First-Serve).

---

## 8. Buffer Cache (I/O Performance)

### 📖 Theoretical Definition
Disk I/O is very slow compared to RAM. The OS uses a **Buffer Cache** (a portion of main memory) to store frequently or recently accessed disk blocks. When a file is read, the OS first checks the Cache (Cache Hit). If the data is not there, it reads from the disk (Cache Miss) and saves a copy in the cache for future use.

### 💻 Where it is implemented
- **Logic:** `src/filesystem.py` (Cache policy intercepting reads/writes)
- **GUI:** `src/gui.py` (System Stats panel: Buffer Cache Stats)

### 🚀 How to show the demo
1. In the File System tab, select a file you wrote data to (e.g., `notes.txt`).
2. Click **Read**. 
3. Click **Read** a second time.

### 👁️ What to observe
- Look at the text just above the Virtual RAM canvas: `Buffer Cache [Policy] | Stats...`
- The first time you read the file, it will register a **Miss** (because it had to fetch it from the virtual disk).
- The second time you read the file, it will register a **Hit** (because the OS remembered the file data in the cache). Explain that this dramatically speeds up real operating systems.
