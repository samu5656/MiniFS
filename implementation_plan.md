# MiniFS — 2-Day Implementation Plan

## 1. Project Overview

**Project Name:** MiniFS — Simulated Operating System File System

**Duration:** 2 Days

**Team Size:** 2 Members

**Technology:**

* Python 3
* Tkinter
* JSON for optional persistence
* Standard Python libraries only wherever possible

**Project Type:** Operating Systems Mini Project

**OS Topic:** File Systems and Storage Management

---

## 2. Project Objective

Build a small user-space simulation of an Operating System file system.

MiniFS should allow users to:

* Create directories
* Navigate directories
* Create files
* Write data to files
* Read files
* Delete files
* Rename files
* Display file metadata
* Simulate file permissions
* Allocate virtual disk blocks
* Free blocks when files are deleted
* Visualize virtual disk usage
* Demonstrate fragmentation

The project is a **simulation**, not a real kernel-level file system.

The application should demonstrate how an OS manages:

* Files
* Directories
* File metadata
* Storage blocks
* File allocation
* Permissions
* Free space
* Fragmentation

---

# 3. Final User Experience

The application should provide a simple graphical interface.

Example:

```text
+-------------------------------------------------------------+
|                       MiniFS                                |
+-------------------------------------------------------------+
| Current Path: /home/projects                                |
+-------------------------------------------------------------+
|                                                             |
|  File System Tree        |       File Information            |
|                           |                                  |
|  /                        | Name: project.txt                |
|  ├── home                 | Type: File                       |
|  │   └── projects        | Size: 120 bytes                  |
|  │       ├── notes.txt   | Owner: user                     |
|  │       └── project.txt | Permissions: rw-r--r--           |
|                           | Blocks: 5, 6, 7                   |
|                           |                                  |
+-------------------------------------------------------------+
| Virtual Disk                                                |
|                                                             |
| [USED][USED][FREE][USED][USED][FREE][FREE][USED]            |
|                                                             |
+-------------------------------------------------------------+
| Create | Delete | Read | Write | Rename | Refresh           |
+-------------------------------------------------------------+
```

The application should also provide a simple command interface if practical:

```text
mkdir projects
cd projects
touch notes.txt
write notes.txt "Operating Systems"
cat notes.txt
ls
pwd
rm notes.txt
```

The GUI is the primary interface.

The CLI is optional if time becomes limited.

---

# 4. Core OS Concepts

The project must demonstrate these concepts clearly:

1. File system
2. Files
3. Directories
4. File metadata
5. File allocation
6. Virtual disk blocks
7. Free-space management
8. File permissions
9. Storage utilization
10. Fragmentation

---

# 5. Simplified File System Model

MiniFS will use a simulated virtual disk.

Example:

```text
Virtual Disk
------------------------------------------------
Block 0   -> File System Metadata
Block 1   -> Root Directory
Block 2   -> notes.txt
Block 3   -> notes.txt
Block 4   -> project.txt
Block 5   -> FREE
Block 6   -> project.txt
Block 7   -> FREE
Block 8   -> FREE
------------------------------------------------
```

The disk should contain a fixed number of blocks.

Recommended default:

```text
Total blocks = 64
Block size   = 64 bytes
```

These values should be configurable.

---

# 6. Recommended Architecture

Use a simple layered architecture.

```text
                 MiniFS GUI
                     |
                     v
              File System API
                     |
        +------------+------------+
        |            |            |
        v            v            v
   Directory      File       Permissions
   Manager       Manager       Manager
        |            |            |
        +------------+------------+
                     |
                     v
              Block Manager
                     |
                     v
               Virtual Disk
```

Recommended modules:

```text
src/
├── main.py
├── filesystem.py
├── disk.py
├── models.py
├── permissions.py
├── gui.py
└── storage.py
```

The agent may modify this structure if there is a strong reason, but should avoid unnecessary restructuring.

---

# 7. Data Model

## File

Each file should contain at least:

```text
name
type
size
content
owner
permissions
created_at
modified_at
allocated_blocks
```

Example:

```python
{
    "name": "notes.txt",
    "type": "file",
    "size": 120,
    "content": "Operating Systems",
    "owner": "user",
    "permissions": "rw-r--r--",
    "created_at": "...",
    "modified_at": "...",
    "allocated_blocks": [4, 5]
}
```

---

## Directory

A directory should contain:

```text
name
type
children
created_at
```

Example:

```python
{
    "name": "projects",
    "type": "directory",
    "children": {},
    "created_at": "..."
}
```

---

# 8. File Allocation

For the first version, use **contiguous allocation**.

Example:

```text
File A requires 3 blocks

Before:

[FREE][FREE][FREE][FREE][FREE]

After:

[A][A][A][FREE][FREE]
```

When a file is deleted:

```text
[A][A][A][FREE][FREE]
          ↓
[FREE][FREE][FREE][FREE][FREE]
```

The project should visualize the allocation.

Do NOT implement complicated allocation strategies unless all required features are already complete.

---

# 9. Phase Breakdown

# PHASE 1 — Project Foundation + Virtual Disk

## Goal

Create the project structure and implement a working virtual disk.

## Tasks

1. Create Python project structure.
2. Create virtual disk abstraction.
3. Implement configurable block count.
4. Implement configurable block size.
5. Represent blocks as used/free.
6. Implement block allocation.
7. Implement block release.
8. Implement basic disk statistics.

Example:

```text
Total Blocks: 64
Used Blocks: 10
Free Blocks: 54
Usage: 15.6%
```

## Required functions

Conceptually:

```text
allocate_blocks(count)
free_blocks(blocks)
get_free_blocks()
get_used_blocks()
get_usage()
```

## Testing

Test:

```text
Allocate 3 blocks
Check usage
Free those 3 blocks
Check usage again
```

## Deliverable

A working virtual disk module with tests.

---

# PHASE 2 — File Operations

## Goal

Implement the basic file system operations.

## Features

Implement:

```text
create file
write file
read file
delete file
rename file
```

Example:

```text
create notes.txt

write notes.txt "Operating Systems"

read notes.txt

Output:
Operating Systems
```

## Requirements

When a file is created:

* Create file metadata.
* Calculate required blocks.
* Allocate blocks.
* Store file content.
* Track allocated blocks.

When a file is deleted:

* Remove metadata.
* Free allocated blocks.

When a file is renamed:

* Change only the file name.
* Preserve content and metadata.

## Testing

Test:

```text
create
write
read
rename
delete
```

Also test:

* Empty file
* Large file
* Non-existent file
* Duplicate file name
* Deleting a file

## Deliverable

Fully functional basic file operations.

---

# PHASE 3 — Directory Management

## Goal

Implement hierarchical directories.

## Features

Implement:

```text
mkdir
rmdir
cd
pwd
ls
```

Example:

```text
mkdir projects

cd projects

mkdir os

cd os

pwd

/projects/os
```

Directory tree:

```text
/
└── projects
    └── os
        ├── notes.txt
        └── project.txt
```

## Requirements

Support:

```text
/
.
..
```

The root directory must always exist.

Prevent deletion of non-empty directories unless recursive deletion is explicitly implemented and tested.

## Testing

Test:

* Create nested directories.
* Navigate between directories.
* List contents.
* Create files inside directories.
* Delete empty directories.
* Attempt to delete non-empty directories.

## Deliverable

A functional hierarchical file system.

---

# PHASE 4 — Metadata + Permissions

## Goal

Add OS-style file metadata and permissions.

## Metadata

Display:

```text
Name
Type
Size
Owner
Created Time
Modified Time
Allocated Blocks
Permissions
```

Example:

```text
Name: notes.txt
Type: File
Size: 120 bytes
Owner: user
Permissions: rw-r--r--
Blocks: [4,5]
```

## Permissions

Implement simplified Unix-style permissions:

```text
r = read
w = write
x = execute
```

Example:

```text
rw-r--r--
```

Interpretation:

```text
Owner   -> rw-
Group   -> r--
Others  -> r--
```

At minimum support:

```text
read
write
execute
```

The application should be able to check whether an operation is allowed.

Example:

```text
Can user read notes.txt?
YES

Can user write notes.txt?
YES
```

Do not implement real operating-system permissions.

These are simulated permissions inside MiniFS.

## Testing

Test different permission configurations.

Example:

```text
Permission: r--
Attempt write
Result: ACCESS DENIED
```

## Deliverable

Files and directories display metadata and support simulated access control.

---

# PHASE 5 — Tkinter GUI + Virtual Disk Visualization

## Goal

Create the graphical interface.

## GUI Requirements

The interface should contain:

### 1. File System Tree

Display:

```text
/
├── documents
│   ├── notes.txt
│   └── report.txt
└── projects
```

### 2. Current Path

Example:

```text
Current Path: /projects
```

### 3. File Information Panel

Display selected file metadata.

### 4. Action Buttons

At minimum:

```text
New File
New Directory
Read
Write
Rename
Delete
Refresh
```

### 5. Virtual Disk Panel

Display blocks visually.

Example:

```text
+----+----+----+----+----+----+
| 00 | 01 | 02 | 03 | 04 | 05 |
|USED|USED|FREE|USED|FREE|FREE|
+----+----+----+----+----+----+
```

The visualization must clearly distinguish:

```text
USED
FREE
```

### 6. Statistics

Display:

```text
Total Blocks
Used Blocks
Free Blocks
Usage %
```

## GUI Principles

Keep the interface simple.

Do NOT spend excessive time on:

* Animations
* Complex themes
* Login systems
* Advanced styling
* Web frameworks

Functionality is more important than visual polish.

## Deliverable

A functional GUI that demonstrates the file system.

---

# PHASE 6 — Fragmentation + Testing + Documentation + Demo

## Goal

Finish the project and prepare it for demonstration.

## Fragmentation

Demonstrate how deleting files creates free spaces.

Example:

```text
Before deletion:

[A][A][A][B][B][B][C][C]

Delete B:

[A][A][A][FREE][FREE][FREE][C][C]
```

Display a simple fragmentation indicator.

Possible calculation:

```text
Fragmentation =
number of separated free-space regions
```

The calculation does not need to represent a real production filesystem metric.

Clearly label it as a simulation metric.

## Final Testing

Test:

* File creation
* File writing
* File reading
* File deletion
* File renaming
* Directory creation
* Directory navigation
* Directory deletion
* Permissions
* Block allocation
* Block release
* Fragmentation
* GUI actions
* Invalid operations
* Duplicate names
* Insufficient disk space

## Error Handling

Show user-friendly errors.

Examples:

```text
File already exists.

File not found.

Directory is not empty.

Permission denied.

Not enough free disk space.

Invalid file name.
```

Do not expose Python stack traces to normal users.

---

# 10. Team Division

## Member 1 — File System Core

Responsible for:

```text
disk.py
filesystem.py
models.py
permissions.py
storage.py
```

Main work:

* Virtual disk
* Block allocation
* File operations
* Directory data model
* Metadata
* Permissions
* Fragmentation calculations
* Core tests

---

## Member 2 — GUI + Integration

Responsible for:

```text
gui.py
main.py
```

Main work:

* Tkinter interface
* File tree
* Buttons
* Dialogs
* Metadata display
* Virtual disk visualization
* Statistics
* Integration with file system core
* UI testing

Both members should understand the entire project before the final presentation.

---

# 11. Day 1 Schedule

## First 30 minutes

Understand:

```text
File system
Directory
File metadata
Block
File allocation
Fragmentation
```

Then create the project.

---

## Hours 1–2

Complete Phase 1.

Virtual disk must work.

---

## Hours 2–4

Complete Phase 2.

File operations must work.

---

## Hours 4–6

Complete Phase 3.

Directories must work.

---

## End of Day 1

The following must work without GUI:

```text
mkdir
cd
pwd
ls
create
write
read
rename
delete
```

---

# 12. Day 2 Schedule

## Hours 1–2

Complete Phase 4.

Metadata + permissions.

---

## Hours 2–5

Complete Phase 5.

Tkinter GUI.

---

## Hours 5–6

Complete Phase 6.

Fragmentation + testing.

---

## Final 1–2 Hours

Prepare:

* README
* Screenshots
* Demo
* Viva questions
* Architecture diagram
* GitHub repository
* Final cleanup

---

# 13. Minimum Viable Product

If time becomes limited, the following features are mandatory:

### Must Have

```text
Virtual disk
File creation
File writing
File reading
File deletion
Directories
Navigation
Metadata
Block allocation
Block visualization
GUI
```

### Should Have

```text
Rename
Permissions
Fragmentation visualization
JSON persistence
```

### Nice to Have

```text
CLI
Advanced permission editing
Search
Sorting
Animations
Dark mode
```

Nice-to-have features must NOT delay the mandatory features.

---

# 14. Persistence

If time permits, store the MiniFS state in JSON.

Example:

```text
filesystem.json
```

This allows the user to close and reopen the application without losing the simulated file system.

If persistence causes bugs or consumes too much time, it may be omitted.

---

# 15. Restrictions

Do NOT:

* Build a real kernel module.
* Modify the host operating system's real file system.
* Require administrator privileges.
* Delete or modify real user files.
* Implement unnecessary networking.
* Add a database.
* Add authentication.
* Add cloud services.
* Add AI.
* Add Docker.
* Add unnecessary external dependencies.
* Overengineer the architecture.

MiniFS must remain a small educational OS project.

---

# 16. Final Demonstration Flow

The final demo should follow this sequence:

### Step 1

Open MiniFS.

### Step 2

Show the empty virtual disk.

```text
[FREE][FREE][FREE][FREE]...
```

### Step 3

Create:

```text
documents
projects
```

### Step 4

Create:

```text
documents/notes.txt
projects/project.txt
```

### Step 5

Write content.

```text
notes.txt
"Operating System File Systems"
```

### Step 6

Show metadata.

```text
Size
Owner
Permissions
Blocks
Created time
Modified time
```

### Step 7

Show virtual disk allocation.

```text
[USED][USED][FREE][USED][USED]...
```

### Step 8

Delete a file.

Show newly released blocks.

### Step 9

Explain fragmentation.

```text
[USED][FREE][USED][FREE][FREE][USED]
```

### Step 10

Demonstrate permissions.

```text
Write -> ACCESS DENIED
```

### Step 11

Show disk statistics.

```text
Total: 64
Used: 12
Free: 52
Usage: 18.75%
```

---

# 17. Expected Final Project Structure

A reasonable final structure is:

```text
MiniFS/
│
├── agents.md
├── implementation_plan.md
├── README.md
├── requirements.txt
├── filesystem.json
│
├── src/
│   ├── main.py
│   ├── filesystem.py
│   ├── disk.py
│   ├── models.py
│   ├── permissions.py
│   ├── storage.py
│   └── gui.py
│
└── tests/
    ├── test_disk.py
    ├── test_filesystem.py
    ├── test_permissions.py
    └── test_directories.py
```

The exact structure can be simplified if necessary.

---

# 18. Completion Criteria

The project is considered complete when:

* [ ] Application starts successfully.
* [ ] Virtual disk is created.
* [ ] Files can be created.
* [ ] Files can be written.
* [ ] Files can be read.
* [ ] Files can be renamed.
* [ ] Files can be deleted.
* [ ] Directories can be created.
* [ ] Directories can be navigated.
* [ ] Directories can be deleted when empty.
* [ ] File metadata is displayed.
* [ ] Permissions are simulated.
* [ ] Blocks are allocated and released.
* [ ] Disk usage is displayed.
* [ ] Virtual blocks are visually displayed.
* [ ] Fragmentation can be demonstrated.
* [ ] Invalid operations are handled.
* [ ] Tests pass.
* [ ] README is complete.
* [ ] Project can be demonstrated in approximately 5–10 minutes.

---

# 19. Important Agent Rule

The AI coding agent must implement **ONLY ONE PHASE AT A TIME**.

After completing a phase:

1. Run tests.
2. Verify the implementation.
3. Explain what changed.
4. List changed files.
5. Explain how to run it.
6. Stop.

The agent must NOT automatically begin the next phase.

The human developer will explicitly request the next phase.
