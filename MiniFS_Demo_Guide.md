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

## 2A. Storage Management & Contiguous Allocation

### 📖 Theoretical Definition
File allocation methods define how disk blocks are allocated for files. **Contiguous Allocation** requires that each file occupies a set of contiguous (physically adjacent) blocks on the disk. 
- **Advantage:** Fast sequential and direct read performance; minimal disk head movement.
- **Disadvantage:** Suffers from **External Fragmentation** over time as files are created and deleted, leaving scattered holes that require periodic compaction (defragmentation).

### 💻 Where it is implemented
- **Logic:** `src/disk.py` (`_allocate_contiguous` method)
- **GUI:** `src/gui.py` (The Virtual Disk canvas visualization)

### 🚀 How to show the demo
1. Launch the application:
   ```powershell
   python src/main.py
   ```
2. In the startup dialog, select **"Contiguous Allocation"** and click **OK**.
3. Verify the bottom status bar reads: `Strategy: Contiguous`.
4. Select `readme.txt` (or create a file `notes.txt`).
5. Click **Write** and enter text requiring multiple blocks (e.g., enter 150 characters to occupy 3 blocks).
6. Click **OK**.

### 👁️ What to observe
- Look at the **Virtual Disk & Swap Space** at the bottom.
- Three green `[FREE]` blocks will turn into red `[USED]` blocks.
- Because allocation is contiguous, the red blocks are grouped strictly together in a single unbroken sequence (e.g., blocks `0, 1, 2`).
- Highlight `notes.txt` in the File Tree and verify the **File Information** panel displays:
  `Allocated Blocks: [0, 1, 2]`.

### 🗣️ What to tell the examiner
> *"In Contiguous Allocation, every file must occupy consecutive physical blocks on disk. This provides optimal sequential access speed, but as files are deleted, free space gets fragmented into isolated holes, making large contiguous allocations fail even when total free space is sufficient."*

---

## 2B. Storage Management & Linked Allocation (FAT Style)

### 📖 Theoretical Definition
In **Linked Allocation**, each file is represented as a linked list of disk blocks that can be scattered anywhere across the disk. MiniFS implements a **File Allocation Table (FAT)**, where block-to-block pointers are kept in a centralized table structure rather than embedded inside the data blocks themselves.
- **Advantage:** **Completely eliminates External Fragmentation.** Any free block anywhere on disk can be allocated to any file without needing contiguous space or compaction.
- **Disadvantage:** Slower random/direct access because accessing block $N$ requires traversing the pointer chain from the start.

### 💻 Where it is implemented
- **Logic:** `src/disk.py` (`_allocate_linked` method, `self.fat` dictionary table)
- **GUI:** `src/filesystem.py` (FAT Chain display in `get_metadata`), `src/gui.py`

### 🚀 How to show the demo
1. Launch the application:
   ```powershell
   python src/main.py
   ```
2. In the startup dialog, select **"Linked Allocation (FAT style)"** and click **OK**.
3. Verify the bottom status bar reads: `Strategy: Linked`.
4. Create three files in `/`: `f1.txt`, `f2.txt`, and `f3.txt`.
5. Write data to each file:
   - Select `f1.txt` -> Click **Write** -> Enter 100 characters (allocates blocks `[0, 1]`).
   - Select `f2.txt` -> Click **Write** -> Enter 100 characters (allocates blocks `[2, 3]`).
   - Select `f3.txt` -> Click **Write** -> Enter 100 characters (allocates blocks `[4, 5]`).
6. Select `f2.txt` and click **Delete** (confirm with Yes).
   - Blocks `[2, 3]` turn green (`FREE`), leaving a 2-block hole between `f1.txt` and `f3.txt`.
7. Create a new file `large.txt`.
8. Click **Write** on `large.txt` and enter 250 characters (requires 4 blocks).

### 👁️ What to observe
- On the **Virtual Disk & Swap Space**:
  - In contiguous allocation, 4 blocks would fail to fit in the 2-block hole `[2, 3]` and would be pushed further down the disk.
  - In **Linked Allocation**, the OS seamlessly fills the hole at blocks `[2, 3]` and continues into `[6, 7]`. Red blocks now appear at `2, 3, 6, 7`!
- Single-click `large.txt` in the File Tree and inspect the **File Information** panel:
  - `FAT Chain: [2] -> [3] -> [6] -> [7] -> EOF`
  - `Allocated Blocks: [2, 3, 6, 7]`

### 🗣️ What to tell the examiner
> *"Notice how Linked Allocation completely solves External Fragmentation without needing defragmentation. Even though the 4 blocks were non-contiguous, the filesystem used the 2 free blocks trapped between existing files and continued with the next available blocks. The File Allocation Table links block 2 to 3, 3 to 6, 6 to 7, and terminates with EOF (-1)."*

---

## 2C. Storage Management & Indexed Allocation (Inode Style)

### 📖 Theoretical Definition
**Indexed Allocation** (the strategy used in Unix/Linux filesystems via **Inodes**) consolidates all pointers for a file into a single dedicated block called the **Index Block (Inode)**. The directory points to this index block, and the index block contains an array of direct pointers to each data block of the file.
- **Advantage:** Combines the best of both worlds:
  1. Supports fast, direct $O(1)$ random access to any logical block by reading the index entry directly.
  2. Prevents external fragmentation because data blocks can reside anywhere on disk.
- **Disadvantage:** Storage overhead for the index block itself (even small 1-block files require an extra index block).

### 💻 Where it is implemented
- **Logic:** `src/disk.py` (`_allocate_indexed` method: allocates 1 index block + $N$ data blocks)
- **GUI:** `src/filesystem.py` (`get_metadata` separates Index Block from Data Blocks), `src/gui.py`

### 🚀 How to show the demo
1. Launch the application:
   ```powershell
   python src/main.py
   ```
2. In the startup dialog, select **"Indexed Allocation (Inode style)"** and click **OK**.
3. Verify the bottom status bar reads: `Strategy: Indexed`.
4. Create a new file called `report.txt`.
5. Select `report.txt`, click **Write**, and enter 50 characters (requires 1 data block).
6. Click `report.txt` in the File Tree and inspect the **File Information** panel.
7. Click **Write** again and enter 200 characters (requires 4 data blocks).

### 👁️ What to observe
- When you first wrote 50 characters (1 data block), observe that **2 blocks** were allocated on the Virtual Disk.
- In the **File Information** panel, point out:
  - `Index Block: 0` (The Inode block storing block pointers)
  - `Data Blocks: [1]` (The payload block)
  - `Total Blocks: 2 (1 Index + 1 Data)`
- When you wrote 200 characters (4 data blocks), inspect the updated panel:
  - `Index Block: 0`
  - `Data Blocks: [1, 2, 3, 4]`
  - `Total Blocks: 5 (1 Index + 4 Data)`

### 🗣️ What to tell the examiner
> *"Indexed Allocation is how modern Unix filesystems structure Inodes. Rather than chaining pointers across the disk, the first allocated block is reserved exclusively as an Index Block. It contains direct address pointers to data blocks [1, 2, 3, 4]. If the OS needs to jump to the 3rd block of the file, it can do so in O(1) time without traversing intermediate blocks, while still preventing external fragmentation."*

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
- When you add `P1`, `P2`, and `P3`, watch the **Virtual RAM** canvas fill up completely with blue blocks representing those processes (6 + 6 + 4 = 16 blocks).
- Notice the **Virtual Disk & Swap Space** at the bottom: the last 16 blocks (blocks 48 to 63) are **Yellow**, representing dedicated, unallocated Swap Space (`SWAP_FREE`).
- When you add `P4` (which requires 4 blocks), RAM has 0 free blocks. The OS performs **Swapping**:
  1. A dialog pops up:
     ```text
     Swapping Occurred
     Process P4 started successfully.
     
     [OS Swapping Event]
     Virtual RAM was full! The OS evicted P1 from RAM to the Virtual Disk Swap Space (Orange blocks).
     ```
  2. In the **Virtual RAM**:
     - `P1` has been evicted.
     - `P4` is loaded into slots 0..3 (blue).
     - Slots 4..5 are green (`FREE`).
  3. In the **Virtual Disk & Swap Space**:
     - Blocks 48 to 53 turn **Orange** and display **`P1`** on each block.
- Optional bonus action: Click **Stop Process**, enter `P1`, and watch the orange blocks on the disk immediately return to yellow (`SWAP_FREE`), proving swap deallocation.

### 🗣️ What to tell the examiner
> *"When P4 arrived, the 16-block Virtual RAM was 100% saturated. The OS memory manager used Least Recently Used (LRU) page replacement to select the oldest process (P1) as the victim. P1 was swapped out of RAM into the dedicated swap partition on disk (highlighted in orange as P1), freeing up memory for P4 to execute immediately."*

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
