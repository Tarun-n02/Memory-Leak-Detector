import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import re

class MemoryLeakGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Valgrind Memory Leak GUI")

        self.process_label = tk.Label(root, text="Enter Process:")
        self.process_label.pack(pady=10)
        
        self.process_entry = tk.Entry(root)
        self.process_entry.pack(pady=5)
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.run_button = tk.Button(root, text="Run Valgrind", command=self.run_valgrind)
        self.run_button.pack()

    def run_valgrind(self):
        try:
            process_path = f"./{str(self.process_entry.get())}"
            valgrind_output = subprocess.run(
                ["valgrind", "--leak-check=full", process_path], 
                shell=False,
                capture_output=True,
                text=True
            )
            
            if "All heap blocks were freed -- no leaks are possible" in valgrind_output.stderr:
                self.text_area.insert(tk.END, "Memory leaks: No\n\n")
                memory_summary = re.search(r"total heap usage: .* bytes allocated", valgrind_output.stderr)
                if memory_summary:
                    self.text_area.insert(tk.END, memory_summary.group() + "\n")
                
            else:
                self.text_area.insert(tk.END, "Memory leaks: Yes\n\n")
                memory_summary = re.search(r"total heap usage: .* bytes allocated", valgrind_output.stderr)
                if memory_summary:
                    self.text_area.insert(tk.END, memory_summary.group().capitalize() + "\n\n")
                if "LEAK SUMMARY" in valgrind_output.stderr:
                    self.text_area.insert(tk.END, "Leak summary:\n")
                    m1 = re.search(r"definitely lost: .* blocks", valgrind_output.stderr)
                    if m1:
                        self.text_area.insert(tk.END, "\t\t" + m1.group().capitalize() + "\n")
                    m2 = re.search(r"indirectly lost: .* blocks", valgrind_output.stderr)
                    if m1:
                        self.text_area.insert(tk.END, "\t\t" + m2.group().capitalize() + "\n")
                    m3 = re.search(r"possibly lost: .* blocks", valgrind_output.stderr)
                    if m1:
                        self.text_area.insert(tk.END, "\t\t" + m3.group().capitalize() + "\n")
                    m4 = re.search(r"still reachable: .* blocks", valgrind_output.stderr)
                    if m1:
                        self.text_area.insert(tk.END, "\t\t" + m4.group().capitalize() + "\n")
                    m5 = re.search(r"suppressed: .* blocks", valgrind_output.stderr)
                    if m1:
                        self.text_area.insert(tk.END, "\t\t" + m5.group().capitalize() + "\n")
                
        except FileNotFoundError:
            messagebox.showerror("Error", "Valgrind executable not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryLeakGUI(root)
    root.mainloop()

