import tkinter as tk
from tkinter import simpledialog, messagebox
from disk import VirtualDisk
from filesystem import FileSystem
from gui import MiniFSGUI

class StrategyDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Select Allocation Strategy:").pack(pady=5)
        self.var = tk.StringVar(value="contiguous")
        tk.Radiobutton(master, text="Contiguous Allocation", variable=self.var, value="contiguous").pack(anchor="w")
        tk.Radiobutton(master, text="Linked Allocation (FAT style)", variable=self.var, value="linked").pack(anchor="w")
        tk.Radiobutton(master, text="Indexed Allocation (Inode style)", variable=self.var, value="indexed").pack(anchor="w")
        return None
        
    def apply(self):
        self.result = self.var.get()

def main():
    print("MiniFS - Starting GUI...")
    root = tk.Tk()
    root.withdraw() # Hide the main window temporarily
    
    dialog = StrategyDialog(root, title="MiniFS Startup")
    strategy = dialog.result if hasattr(dialog, 'result') and dialog.result else "contiguous"
    
    print(f"MiniFS - Selected strategy: {strategy}")
    disk = VirtualDisk(64, 64, allocation_strategy=strategy)
    from memory import MemoryManager
    mem_mgr = MemoryManager(disk)
    fs = FileSystem(disk, current_user="user")
    
    # Pre-populate with some data for demonstration
    fs.mkdir("projects")
    fs.create_file("readme.txt")
    fs.write_file("readme.txt", "Welcome to MiniFS!")
    
    root.deiconify() # Show main window again
    app = MiniFSGUI(root, fs, mem_mgr)
    
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
