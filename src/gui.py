import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class MiniFSGUI:
    def __init__(self, root, fs, mem_mgr=None, cpu_scheduler=None):
        self.root = root
        self.fs = fs
        self.mem_mgr = mem_mgr
        self.cpu = cpu_scheduler
        self.root.title("MiniFS")
        self.root.geometry("800x600")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.fs_frame = tk.Frame(self.notebook)
        self.cpu_frame = tk.Frame(self.notebook)
        
        self.notebook.add(self.fs_frame, text="File System")
        self.notebook.add(self.cpu_frame, text="CPU Scheduler")
        
        self._build_ui()
        self._build_cpu_ui()
        # Bind resize event to redraw disk/ram correctly
        self.disk_canvas.bind("<Configure>", lambda e: self.update_disk())
        if hasattr(self, 'ram_canvas'):
            self.ram_canvas.bind("<Configure>", lambda e: self.update_ram())
        self.refresh()

    def _build_ui(self):
        # Top frame: Path
        top_frame = tk.Frame(self.fs_frame)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.path_var = tk.StringVar()
        tk.Label(top_frame, text="Current Path: ", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(top_frame, textvariable=self.path_var, font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Action Buttons
        btn_frame = tk.Frame(self.fs_frame)
        btn_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="New File", command=self.new_file).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="New Directory", command=self.new_dir).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Read", command=self.read_file).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Write", command=self.write_file).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Rename", command=self.rename).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Delete", command=self.delete).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Defragment", command=self.defragment).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Start Process", command=self.start_process).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Stop Process", command=self.stop_process).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Lock/Unlock", command=self.toggle_lock).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Up (..)", command=self.go_up).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=2)

        # Middle frame: Tree + Info
        mid_frame = tk.PanedWindow(self.fs_frame, orient=tk.HORIZONTAL)
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
        bot_frame = tk.LabelFrame(self.fs_frame, text="System Stats", padx=5, pady=5)
        bot_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.stats_var = tk.StringVar()
        tk.Label(bot_frame, textvariable=self.stats_var, justify=tk.LEFT, font=("Consolas", 10)).pack(side=tk.TOP, anchor="w")
        
        self.cache_stats_var = tk.StringVar()
        tk.Label(bot_frame, textvariable=self.cache_stats_var, justify=tk.LEFT, font=("Consolas", 10)).pack(side=tk.TOP, anchor="w")
        
        tk.Label(bot_frame, text="Virtual RAM (Memory):", font=("Arial", 9, "bold")).pack(side=tk.TOP, anchor="w")
        self.ram_canvas = tk.Canvas(bot_frame, height=30, bg="#f0f0f0")
        self.ram_canvas.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        tk.Label(bot_frame, text="Virtual Disk & Swap Space:", font=("Arial", 9, "bold")).pack(side=tk.TOP, anchor="w")
        self.disk_canvas = tk.Canvas(bot_frame, height=30, bg="#f0f0f0")
        self.disk_canvas.pack(side=tk.TOP, fill=tk.X, pady=2)

    def _build_cpu_ui(self):
        if not self.cpu:
            tk.Label(self.cpu_frame, text="CPU Simulator Not Available", font=("Arial", 14)).pack(pady=20)
            return
            
        # Controls
        ctrl_frame = tk.Frame(self.cpu_frame)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        tk.Button(ctrl_frame, text="Add Process", command=self.add_cpu_process).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="Step Scheduler", command=self.step_cpu).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="Auto Run", command=self.auto_run_cpu).pack(side=tk.LEFT, padx=2)
        
        self.cpu_time_var = tk.StringVar(value="Time: 0")
        tk.Label(ctrl_frame, textvariable=self.cpu_time_var, font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=10)
        
        # CPU Box
        cpu_box = tk.LabelFrame(self.cpu_frame, text="CPU (Executing)", padx=10, pady=10)
        cpu_box.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        self.cpu_current_var = tk.StringVar(value="IDLE")
        tk.Label(cpu_box, textvariable=self.cpu_current_var, font=("Consolas", 16, "bold"), fg="blue").pack(pady=10)
        
        # Queues
        q_frame = tk.PanedWindow(self.cpu_frame, orient=tk.HORIZONTAL)
        q_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Ready Queue
        rq_frame = tk.LabelFrame(q_frame, text="Ready Queue")
        self.rq_listbox = tk.Listbox(rq_frame, font=("Consolas", 12))
        self.rq_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        q_frame.add(rq_frame, minsize=300)
        
        # Completed
        comp_frame = tk.LabelFrame(q_frame, text="Completed")
        self.comp_listbox = tk.Listbox(comp_frame, font=("Consolas", 12), fg="gray")
        self.comp_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        q_frame.add(comp_frame, minsize=300)
        
        self.update_cpu_ui()

    def add_cpu_process(self):
        if not self.cpu: return
        pid = simpledialog.askstring("New Process", "Enter Process ID (e.g., P1):")
        if not pid: return
        burst = simpledialog.askinteger("New Process", "Enter Burst Time (1-20):", minvalue=1, maxvalue=20)
        if not burst: return
        self.cpu.add_process(pid, burst)
        self.update_cpu_ui()
        
    def step_cpu(self):
        if not self.cpu: return
        self.cpu.step()
        self.update_cpu_ui()
        
    def auto_run_cpu(self):
        if not self.cpu: return
        if self.cpu.step():
            self.update_cpu_ui()
            self.root.after(500, self.auto_run_cpu)
            
    def update_cpu_ui(self):
        if not self.cpu: return
        self.cpu_time_var.set(f"Time: {self.cpu.time} | Algo: {self.cpu.algorithm}")
        
        if self.cpu.current_process:
            p = self.cpu.current_process
            self.cpu_current_var.set(f"[{p.pid}] Remaining: {p.remaining_time}")
        else:
            self.cpu_current_var.set("IDLE")
            
        self.rq_listbox.delete(0, tk.END)
        for p in self.cpu.ready_queue:
            self.rq_listbox.insert(tk.END, f"[{p.pid}] Burst: {p.burst_time} | Rem: {p.remaining_time}")
            
        self.comp_listbox.delete(0, tk.END)
        for p in self.cpu.completed_processes:
            self.comp_listbox.insert(tk.END, f"[{p.pid}] Completed")

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
        if hasattr(self, 'update_ram'):
            self.update_ram()
        self.clear_info()

    def update_stats(self):
        stats = self.fs.disk.get_statistics()
        s = f"Total Blocks: {stats['Total Blocks']} | Used: {stats['Used Blocks']} | Free: {stats['Free Blocks']} | Usage: {stats['Usage']}\nFragmentation: {stats.get('Fragmentation %', '0%')} ({stats['Fragmentation']} region(s)) | Strategy: {stats.get('Strategy', 'Contiguous')}"
        self.stats_var.set(s)
        if hasattr(self.fs, 'cache'):
            self.cache_stats_var.set(f"Buffer Cache [{self.fs.cache.policy}] | {self.fs.cache.get_stats()}")

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
            y1 = 2
            x2 = x1 + block_w - 2
            y2 = 28
            # Colors
            if state == "FREE":
                color = "#4CAF50" # Green
            elif state == "SWAP_FREE":
                color = "#FFC107" # Yellow
            elif state.startswith("SWAP_"):
                color = "#FF9800" # Orange (used swap)
            else:
                color = "#F44336" # Red (used disk)
                
            self.disk_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
            if state.startswith("SWAP_"):
                pid_text = state.replace("SWAP_", "")
                self.disk_canvas.create_text(x1 + (block_w/2), 15, text=pid_text, font=("Arial", 7, "bold"), fill="black")
    def update_ram(self):
        if not self.mem_mgr: return
        self.ram_canvas.delete("all")
        width = self.ram_canvas.winfo_width()
        if width <= 1: 
            return
            
        blocks = self.mem_mgr.ram_size
        if blocks == 0: return
        
        block_w = width / blocks
        for i, state in enumerate(self.mem_mgr.ram):
            x1 = i * block_w
            y1 = 2
            x2 = x1 + block_w - 2
            y2 = 28
            if state == "FREE":
                color = "#4CAF50" # Green
            else:
                color = "#2196F3" # Blue (Process)
                
            self.ram_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
            if state != "FREE":
                self.ram_canvas.create_text(x1 + (block_w/2), 15, text=state, font=("Arial", 7))
                
    def start_process(self):
        if not self.mem_mgr: return
        pid = simpledialog.askstring("Start Process", "Enter Process ID (e.g., P1):")
        if not pid: return
        blocks = simpledialog.askinteger("Start Process", "Enter Memory Blocks needed (1-16):", minvalue=1, maxvalue=16)
        if not blocks: return
        
        try:
            evicted = self.mem_mgr.start_process(pid, blocks)
            self.update_ram()
            self.update_disk()
            if evicted:
                evicted_names = ", ".join(evicted)
                messagebox.showinfo(
                    "Swapping Occurred",
                    f"Process {pid} started successfully.\n\n"
                    f"[OS Swapping Event]\n"
                    f"Virtual RAM was full! The OS evicted {evicted_names} from RAM to the Virtual Disk Swap Space (Orange blocks)."
                )
            else:
                messagebox.showinfo("Process Started", f"Process {pid} started successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def stop_process(self):
        if not self.mem_mgr: return
        pid = simpledialog.askstring("Stop Process", "Enter Process ID to stop (e.g., P1):")
        if not pid: return
        
        try:
            self.mem_mgr.stop_process(pid)
            self.update_ram()
            self.update_disk()
            messagebox.showinfo("Process Stopped", f"Process {pid} stopped and memory freed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
            self.update_stats() # update cache stats
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

    def defragment(self):
        try:
            self.fs.defragment()
            self.refresh()
            self.on_select() # refresh metadata if file selected
            messagebox.showinfo("Defragmentation", "Disk compacted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to defragment: {e}")

    def toggle_lock(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a file to lock/unlock")
            return
        name = selection[0]
        try:
            is_locked = self.fs.toggle_lock(name)
            self.refresh()
            self.on_select()
            messagebox.showinfo("Lock Status", f"File '{name}' is now {'Locked' if is_locked else 'Unlocked'}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
