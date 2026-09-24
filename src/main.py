from disk import VirtualDisk
from filesystem import FileSystem

def main():
    print("MiniFS - Phase 4 Metadata & Permissions Demo\n")
    
    disk = VirtualDisk(64, 64)
    fs = FileSystem(disk, current_user="alice")
    
    print("1. User 'alice' creates 'shared.txt'")
    fs.create_file("shared.txt")
    fs.write_file("shared.txt", "Hello World")
    print(f"Metadata:\n{fs.get_metadata('shared.txt')}")
    
    print("\n2. User 'bob' tries to read 'shared.txt' (Permissions: rw-r--r--)")
    fs.current_user = "bob"
    print(f"Bob reads: {fs.read_file('shared.txt')}")
    
    print("\n3. User 'bob' tries to write to 'shared.txt'")
    try:
        fs.write_file("shared.txt", "Bob's text")
    except Exception as e:
        print(f"Error: {e}")
        
    print("\n4. User 'alice' changes permissions to 'rw-rw-r--'")
    fs.current_user = "alice"
    # Using 'others' permission for 'bob' in this simplified model.
    # So we change 'others' to 'rw-' -> rw-r--rw-
    fs.chmod("shared.txt", "rw-r--rw-")
    print(f"Metadata updated:\n{fs.get_metadata('shared.txt')}")
    
    print("\n5. User 'bob' tries to write again")
    fs.current_user = "bob"
    fs.write_file("shared.txt", "Bob's text")
    print(f"Bob reads: {fs.read_file('shared.txt')}")

if __name__ == "__main__":
    main()
