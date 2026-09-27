import tkinter as tk
from disk import VirtualDisk
from filesystem import FileSystem
from gui import MiniFSGUI

def main():
    print("MiniFS - Starting GUI...")
    disk = VirtualDisk(64, 64)
    fs = FileSystem(disk, current_user="user")
    
    # Pre-populate with some data for demonstration
    fs.mkdir("projects")
    fs.create_file("readme.txt")
    fs.write_file("readme.txt", "Welcome to MiniFS!")
    
    root = tk.Tk()
    app = MiniFSGUI(root, fs)
    
    # Force window to maximize to guarantee visibility
    try:
        root.state('zoomed')
    except tk.TclError:
        pass # zoomed might fail on some platforms
    
    root.lift()
    root.focus_force()
    
    print("Entering mainloop (Maximized)")
    root.mainloop()

if __name__ == "__main__":
    main()
