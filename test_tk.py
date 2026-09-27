import tkinter as tk

root = tk.Tk()
root.title("Test Window")
root.geometry("400x300+100+100")
root.attributes('-topmost', True)

label = tk.Label(root, text="Can you see this?", font=("Arial", 20))
label.pack(expand=True)

print("Test window started")
root.after(2000, root.destroy)
root.mainloop()
print("Test window closed successfully")
