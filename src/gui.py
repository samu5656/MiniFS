import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class MiniFSGUI:
    def __init__(self, root, fs):
        self.root = root
        self.fs = fs
        self.root.title("MiniFS")
        self.root.geometry("800x600")
        
        self._build_ui()
        # Bind resize event to redraw disk correctly
        self.disk_canvas.bind("<Configure>", lambda e: self.update_disk())
        self.refresh()

    def _build_ui(self):
        # Top frame: Path
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.path_var = tk.StringVar()
        tk.Label(top_frame, text="Current Path: ", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(top_frame, textvariable=self.path_var, font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Action Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="New File", command=self.new_file).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="New Directory", command=self.new_dir).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Read", command=self.read_file).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Write", command=self.write_file).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Rename", command=self.rename).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Delete", command=self.delete).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Up (..)", command=self.go_up).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=2)

        # Middle frame: Tree + Info
        mid_frame = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        mid_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tree_frame = tk.Frame(mid_frame)
        
        # Tree
        self.tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse")
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        mid_frame.add(tree_frame, minsize=250)
        
        # Info Panel
        info_frame = tk.LabelFrame(mid_frame, text="File Information", padx=5, pady=5)
        self.info_text = tk.Text(info_frame, width=40, state=tk.DISABLED, font=("Consolas", 10))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        mid_frame.add(info_frame, minsize=250)

        # Bottom frame: Disk + Stats
        bot_frame = tk.LabelFrame(self.root, text="Virtual Disk", padx=5, pady=5)
        bot_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.stats_var = tk.StringVar()
        tk.Label(bot_frame, textvariable=self.stats_var, justify=tk.LEFT, font=("Consolas", 10)).pack(side=tk.TOP, anchor="w")
        
        self.disk_canvas = tk.Canvas(bot_frame, height=40, bg="#f0f0f0")
        self.disk_canvas.pack(side=tk.TOP, fill=tk.X, pady=5)

    def refresh(self):
        self.path_var.set(self.fs.pwd())
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            items = self.fs.ls()
            for name in items:
                obj = self.fs.current_directory.children[name]
                prefix = "[DIR]" if obj.type == "directory" else "[FILE]"
                self.tree.insert("", "end", iid=name, text=f"{prefix} {name}")
        except Exception as e:
            # Print to console as well so we can see it
            print(f"Error in refresh: {e}")
            messagebox.showerror("Error", f"Failed to refresh: {e}")

        self.update_stats()
        self.update_disk()
        self.clear_info()

    def update_stats(self):
        stats = self.fs.disk.get_statistics()
        s = f"Total Blocks: {stats['Total Blocks']} | Used: {stats['Used Blocks']} | Free: {stats['Free Blocks']} | Usage: {stats['Usage']} | Fragmentation (Simulated): {stats['Fragmentation']} region(s)"
        self.stats_var.set(s)

    def update_disk(self):
        self.disk_canvas.delete("all")
        width = self.disk_canvas.winfo_width()
        if width <= 1: 
            return # not fully rendered yet
            
        blocks = self.fs.disk.total_blocks
        if blocks == 0: return
        
        block_w = width / blocks
        for i, state in enumerate(self.fs.disk.blocks):
            x1 = i * block_w
            y1 = 5
            x2 = x1 + block_w - 2
            y2 = 35
            # Red for USED, Green for FREE
            color = "#4CAF50" if state == "FREE" else "#F44336" 
            self.disk_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
            
    def clear_info(self):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)

    def on_select(self, event=None):
        selection = self.tree.selection()
        if not selection: return
        name = selection[0]
        try:
            meta = self.fs.get_metadata(name)
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, meta)
            self.info_text.config(state=tk.DISABLED)
        except Exception as e:
            pass

    def on_double_click(self, event):
        selection = self.tree.selection()
        if not selection: return
        name = selection[0]
        obj = self.fs.current_directory.children[name]
        if obj.type == "directory":
            try:
                self.fs.cd(name)
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def go_up(self):
        try:
            self.fs.cd("..")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def new_file(self):
        name = simpledialog.askstring("New File", "Enter file name:")
        if name:
            try:
                self.fs.create_file(name)
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def new_dir(self):
        name = simpledialog.askstring("New Directory", "Enter directory name:")
        if name:
            try:
                self.fs.mkdir(name)
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def read_file(self):
        selection = self.tree.selection()
        if not selection: 
            messagebox.showwarning("Warning", "Select a file to read")
            return
        name = selection[0]
        try:
            content = self.fs.read_file(name)
            messagebox.showinfo(f"Read {name}", content if content else "<Empty File>")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def write_file(self):
        selection = self.tree.selection()
        if not selection: 
            messagebox.showwarning("Warning", "Select a file to write")
            return
        name = selection[0]
        content = simpledialog.askstring("Write File", f"Enter content for {name}:")
        if content is not None:
            try:
                self.fs.write_file(name, content)
                self.refresh()
                self.on_select() # refresh metadata
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def rename(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select an item to rename")
            return
        old_name = selection[0]
        new_name = simpledialog.askstring("Rename", f"Enter new name for {old_name}:")
        if new_name:
            try:
                self.fs.rename_file(old_name, new_name)
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select an item to delete")
            return
        name = selection[0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
            obj = self.fs.current_directory.children[name]
            try:
                if obj.type == "directory":
                    self.fs.rmdir(name)
                else:
                    self.fs.delete_file(name)
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))
