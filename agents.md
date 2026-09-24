# MiniFS — Agent Instructions

## 1. Role

You are the coding agent responsible for implementing MiniFS according to:

```text
implementation_plan.md
```

You must follow this file as the primary implementation specification.

MiniFS is a **2-day Operating Systems mini-project** built by a **team of 2 beginners**.

The priority is:

```text
Correctness > Simplicity > Demonstrability > Visual Polish
```

Do not overengineer the project.

---

# 2. Most Important Rule — Phase-by-Phase Development

The project is divided into 6 phases.

You MUST implement only the phase explicitly requested by the user.

For example, if the user says:

```text
Implement Phase 1
```

you must implement:

```text
Phase 1
```

ONLY.

Do NOT automatically implement:

```text
Phase 2
Phase 3
Phase 4
Phase 5
Phase 6
```

After finishing the requested phase, STOP and wait for the user's next instruction.

---

# 3. Before Starting Any Phase

Before modifying code:

1. Read `implementation_plan.md`.
2. Identify the requested phase.
3. Inspect the existing project files.
4. Understand what has already been implemented.
5. Avoid rewriting working code unnecessarily.
6. Determine the smallest implementation required for the phase.

Do not assume that previous phases were implemented correctly.

Verify existing functionality before building on top of it.

---

# 4. Project Constraints

The project must remain:

* Beginner friendly
* Python based
* Tkinter based
* Small
* Local
* Offline
* Easy to demonstrate
* Easy to explain in an OS viva

Do NOT introduce:

* React
* Node.js
* Express
* PostgreSQL
* MongoDB
* Docker
* Cloud services
* AI APIs
* Authentication systems
* Web servers
* External APIs
* Microservices

unless explicitly requested by the user.

---

# 5. Dependency Policy

Prefer the Python standard library.

Expected primary technologies:

```text
Python 3
Tkinter
JSON
unittest or pytest
```

If an external dependency is genuinely necessary:

1. Explain why it is needed.
2. Keep the dependency minimal.
3. Add it to `requirements.txt`.
4. Do not silently introduce large frameworks.

Tkinter should remain the GUI framework.

---

# 6. Safety Rule

MiniFS is a simulated file system.

It must NEVER manipulate the user's real operating-system files unless the user explicitly requests such behavior.

Do NOT:

* Delete real files.
* Rename real files.
* Modify system directories.
* Change Windows permissions.
* Require administrator privileges.
* Format real disks.
* Access raw disks.
* Modify boot configuration.
* Modify registry settings.

All file-system operations must happen inside MiniFS's simulated data structures.

If JSON persistence is implemented, it should only save MiniFS state.

---

# 7. Architecture Rules

Use a clean but simple architecture.

Preferred separation:

```text
GUI
 |
 v
File System API
 |
 +---- Directory Manager
 |
 +---- File Manager
 |
 +---- Permission Manager
 |
 v
Block Manager
 |
 v
Virtual Disk
```

Keep business logic separate from Tkinter UI code.

Do NOT place all logic inside `gui.py`.

Do NOT create unnecessary design patterns.

Avoid:

```text
Factory
Strategy
Observer
Dependency Injection frameworks
Repository pattern
Service layers
```

unless they are genuinely necessary.

This is a 2-day student project, not a production system.

---

# 8. Code Quality

Write readable Python.

Use:

* Meaningful variable names.
* Small functions.
* Clear class names.
* Type hints where useful.
* Docstrings for important classes/functions.
* Comments for OS-specific logic.

Avoid:

* Extremely long functions.
* Duplicate code.
* Magic numbers.
* Unnecessary abstractions.
* Obfuscated code.

Example:

GOOD:

```python
free_blocks = disk.get_free_blocks()
```

Avoid:

```python
x = d.gfb()
```

---

# 9. Error Handling

User-facing operations must fail gracefully.

Examples:

```text
File already exists.
File not found.
Directory not found.
Directory is not empty.
Permission denied.
Not enough free disk space.
Invalid operation.
```

Do not display raw Python stack traces in the GUI for expected user errors.

Internally, exceptions may be used where appropriate.

---

# 10. Virtual Disk Rules

The virtual disk should have:

```text
Total blocks = 64
Block size = 64 bytes
```

unless the implementation plan or user changes these values.

The values should preferably be configurable.

Each block should have a clear state:

```text
FREE
USED
```

The disk manager must support:

```text
allocate_blocks(count)
free_blocks(blocks)
get_free_blocks()
get_used_blocks()
get_usage()
```

Do not implement real disk I/O.

---

# 11. File Allocation Rules

The initial allocation strategy is:

```text
Contiguous Allocation
```

If a file requires:

```text
3 blocks
```

the system should attempt to allocate:

```text
[FREE][FREE][FREE]
```

as a contiguous region.

If contiguous space is unavailable, the system should report insufficient allocation space according to the chosen implementation.

Do not automatically implement multiple allocation algorithms.

The purpose is to demonstrate the OS concept, not to build a production filesystem.

---

# 12. File System Rules

MiniFS must support:

```text
create
read
write
delete
rename
```

Files should maintain metadata.

At minimum:

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

Deleting a file must release its allocated virtual blocks.

Renaming a file must not change its content or allocated blocks.

---

# 13. Directory Rules

The root directory:

```text
/
```

must always exist.

Directories must support:

```text
mkdir
rmdir
cd
pwd
ls
```

Navigation should support:

```text
/
.
..
```

A non-empty directory should not be deleted unless recursive deletion is explicitly implemented.

Do not accidentally allow a user to delete the root directory.

---

# 14. Permission Rules

Permissions are simulated.

They must NOT modify actual Windows/Linux permissions.

Use a simplified Unix-style representation:

```text
r
w
x
```

Example:

```text
rw-r--r--
```

The implementation should be understandable to a beginner.

Permission checks should answer questions such as:

```text
Can this user read the file?
Can this user write the file?
Can this user execute the file?
```

Expected behavior:

```text
Permission = r--
Write operation
      |
      v
ACCESS DENIED
```

---

# 15. GUI Rules

Use Tkinter.

The GUI should prioritize usability.

Minimum components:

```text
File tree
Current path
File metadata panel
Action buttons
Virtual disk visualization
Disk statistics
```

Recommended actions:

```text
New File
New Directory
Read
Write
Rename
Delete
Refresh
```

Avoid wasting development time on:

* Complex animations.
* Custom graphics engines.
* Excessive themes.
* Login pages.
* Splash screens.
* Unnecessary menus.

A simple professional-looking interface is enough.

---

# 16. Testing Rules

Every phase must have appropriate tests.

Before saying a phase is complete:

1. Run the tests.
2. Fix failures.
3. Test important edge cases.
4. Confirm existing functionality still works.

Examples:

```text
Create file
Read file
Write file
Delete file
Create directory
Navigate directory
Allocate blocks
Free blocks
Permission denied
Insufficient space
Duplicate names
```

Do not claim tests passed unless they were actually executed.

---

# 17. Phase Completion Protocol

When the requested phase is complete, provide the user with:

## 1. What was implemented

Example:

```text
Phase 1 completed.

Implemented:
- Virtual disk
- 64 blocks
- Block allocation
- Block release
- Disk statistics
```

## 2. Files changed

Example:

```text
Created:
- src/disk.py
- tests/test_disk.py

Modified:
- src/main.py
```

## 3. Tests executed

Example:

```text
pytest
```

Result:

```text
X tests passed
```

Only report actual results.

## 4. How to run

Give exact commands.

Example:

```bash
python -m pytest
python src/main.py
```

## 5. Manual verification

Give the user 2–5 simple things to check.

Example:

```text
1. Start the application.
2. Allocate 3 blocks.
3. Verify used blocks increase.
4. Free the blocks.
5. Verify they return to FREE.
```

## 6. STOP

Do not implement the next phase.

Wait for the user to explicitly request it.

---

# 18. Do Not Automatically Modify Git

This is extremely important.

The agent must NEVER automatically run:

```bash
git add .
git commit -m "..."
git push
git reset
git checkout
git merge
git rebase
```

unless the user explicitly asks for a specific Git operation.

The agent's responsibility is to modify project files and test the application.

The user controls Git.

Do not create commits automatically.

Do not push anything automatically.

---

# 19. Do Not Delete User Work

Before changing an existing file:

* Inspect it.
* Preserve useful existing code.
* Make the smallest required change.

Do not delete or replace the entire project merely because a different implementation seems cleaner.

Do not overwrite user-created files unnecessarily.

---

# 20. Do Not Add Features Outside the Plan

Do not add features just because they seem interesting.

For example, do NOT spontaneously add:

```text
AI assistant
Cloud storage
User authentication
Network sharing
Encryption
Real Linux filesystem mounting
Docker
Database
Web dashboard
REST API
```

These features are outside the project scope.

If you think a feature is useful, mention it to the user instead of implementing it.

---

# 21. Beginner-Friendly Implementation

The code should be understandable by a 3rd-year CSE student who is still learning Operating Systems.

Prefer:

```python
class VirtualDisk:
    ...
```

over highly abstract architectures.

Every important OS concept should be traceable through the code.

The user should be able to explain:

```text
What is a block?
Why do we allocate blocks?
What happens when a file is deleted?
What is fragmentation?
What is a directory?
What is file metadata?
What are permissions?
```

---

# 22. OS Concept Comments

Where useful, add comments explaining the OS concept.

Example:

```python
# A real OS stores files on physical storage blocks.
# MiniFS simulates those blocks using Python data structures.
```

Do not fill the code with unnecessary comments.

Comments should explain concepts, not obvious Python syntax.

---

# 23. No Fake Functionality

Do not create buttons that only display messages such as:

```text
Feature coming soon
```

unless the button is intentionally part of an incomplete phase.

Every implemented feature must actually work.

Do not fake disk allocation.

Do not fake file metadata.

Do not fake permission checks.

The GUI must interact with the actual MiniFS core.

---

# 24. Persistence Rules

If JSON persistence is implemented:

```text
filesystem.json
```

must contain MiniFS state only.

Do not store:

* Passwords.
* System information.
* Real filesystem paths.
* User personal information.

If persistence becomes unstable, it is acceptable to disable it rather than compromise the core project.

---

# 25. Scope Control

This project must remain achievable within:

```text
2 days
2 students
```

If a requested feature appears likely to take too long:

1. Implement the simplest educational version.
2. Keep the OS concept correct.
3. Avoid production-level complexity.
4. Inform the user if a feature was simplified.

Do not turn MiniFS into a full filesystem implementation.

---

# 26. Final Quality Checklist

Before final completion, verify:

### Core

* [ ] Application starts.
* [ ] Virtual disk works.
* [ ] Files work.
* [ ] Directories work.
* [ ] Navigation works.
* [ ] Metadata works.
* [ ] Permissions work.
* [ ] Block allocation works.
* [ ] Block release works.

### GUI

* [ ] File tree works.
* [ ] File operations work.
* [ ] Metadata appears.
* [ ] Disk visualization works.
* [ ] Statistics update.
* [ ] Errors are understandable.

### Testing

* [ ] Tests pass.
* [ ] Edge cases tested.
* [ ] No major console errors.
* [ ] Existing functionality remains working.

### Documentation

* [ ] README exists.
* [ ] Installation instructions exist.
* [ ] Run instructions exist.
* [ ] Architecture is explained.
* [ ] OS concepts are explained.
* [ ] Demo steps are included.

### Git

* [ ] No automatic commits.
* [ ] No automatic pushes.
* [ ] No automatic staging.

---

# 27. Communication Style

When reporting progress:

Be concise and technical.

Use this structure:

```text
PHASE X COMPLETE

Implemented:
- ...
- ...
- ...

Files:
- ...
- ...

Tests:
- ...
- ...

Run:
...

Manual verification:
1. ...
2. ...
3. ...

Waiting for the next phase.
```

Do not produce unnecessary explanations after every code change.

Do not claim success without testing.

---

# 28. Final Instruction

The user's explicit phase request has the highest priority within this project.

If the user says:

```text
Implement Phase 1
```

implement Phase 1 only.

If the user says:

```text
Implement Phase 2
```

implement Phase 2 only.

Never automatically continue to another phase.

Never automatically perform Git operations.

Never modify the user's real operating-system files.

Keep MiniFS simple, correct, testable, and easy to explain in an Operating Systems viva.
