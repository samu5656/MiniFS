from disk import VirtualDisk
from filesystem import FileSystem

def main():
    print("MiniFS - Phase 2 File Operations Demo\n")
    
    disk = VirtualDisk(64, 64)
    fs = FileSystem(disk)
    
    print("1. Creating file 'notes.txt'")
    fs.create_file("notes.txt")
    print(f"Files: {list(fs.files.keys())}")
    
    print("\n2. Writing to 'notes.txt'")
    fs.write_file("notes.txt", "Operating Systems Project")
    print(f"Content: {fs.read_file('notes.txt')}")
    print(disk.get_statistics())
    
    print("\n3. Renaming to 'project_notes.txt'")
    fs.rename_file("notes.txt", "project_notes.txt")
    print(f"Files: {list(fs.files.keys())}")
    
    print("\n4. Deleting 'project_notes.txt'")
    fs.delete_file("project_notes.txt")
    print(f"Files: {list(fs.files.keys())}")
    print(disk.get_statistics())

if __name__ == "__main__":
    main()
