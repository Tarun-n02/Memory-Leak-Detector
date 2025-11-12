"""
Memory Leak Detector GUI - Windows/WSL Compatible
A graphical tool to compile C programs and detect memory leaks using Valgrind
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import subprocess
import re
import os
import platform


class MemoryLeakGUI:
    """Main GUI application for memory leak detection"""
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("Memory Leak Detector GUI (Windows/WSL)")
        self.root.geometry("800x600")
        
        # Initialize tool availability flags
        self.wsl_available = False
        self.wsl_gcc_available = False
        self.wsl_valgrind_available = False

        # Build the user interface
        self._create_widgets()
        
        # Check for available tools on startup
        self.check_tools()

    def _create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === FILE SELECTION SECTION ===
        self._create_file_selection_section(main_frame)
        
        # === ACTION BUTTONS SECTION ===
        self._create_buttons_section(main_frame)
        
        # === OUTPUT DISPLAY SECTION ===
        self._create_output_section(main_frame)
        
        # === STATUS BAR ===
        self._create_status_bar(main_frame)

    def _create_file_selection_section(self, parent):
        """Create the file selection input area"""
        process_frame = tk.Frame(parent)
        process_frame.pack(fill=tk.X, pady=(0, 10))

        # Label
        self.process_label = tk.Label(
            process_frame, 
            text="Select C Source File or Executable:",
            font=("Arial", 10, "bold")
        )
        self.process_label.pack(anchor=tk.W)
        
        # Input field with browse button
        input_frame = tk.Frame(process_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.process_entry = tk.Entry(input_frame, font=("Arial", 10))
        self.process_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.browse_button = tk.Button(
            input_frame, 
            text="Browse", 
            command=self.browse_file,
            width=10
        )
        self.browse_button.pack(side=tk.RIGHT)

    def _create_buttons_section(self, parent):
        """Create the action buttons"""
        button_frame = tk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.compile_button = tk.Button(
            button_frame, 
            text="Compile C File", 
            command=self.compile_c_file,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        )
        self.compile_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.run_button = tk.Button(
            button_frame, 
            text="Analyze Memory", 
            command=self.analyze_memory,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        )
        self.run_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_button = tk.Button(
            button_frame, 
            text="Clear Output", 
            command=self.clear_output,
            width=15
        )
        self.clear_button.pack(side=tk.LEFT)

    def _create_output_section(self, parent):
        """Create the output text display area"""
        output_label = tk.Label(
            parent, 
            text="Output:",
            font=("Arial", 10, "bold")
        )
        output_label.pack(anchor=tk.W)
        
        self.text_area = scrolledtext.ScrolledText(
            parent, 
            wrap=tk.WORD, 
            height=25,
            font=("Consolas", 9),
            bg="#f5f5f5"
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def _create_status_bar(self, parent):
        """Create the status bar at the bottom"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(
            parent, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.pack(fill=tk.X, pady=(5, 0))

    # ========== FILE SELECTION ==========
    
    def browse_file(self):
        """Open file browser to select C source file or executable"""
        file_types = [
            ("C Source Files", "*.c"),
            ("Executable Files", "*.exe"),
            ("All Files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Select C source file or executable",
            filetypes=file_types
        )
        if filename:
            self.process_entry.delete(0, tk.END)
            self.process_entry.insert(0, filename)

    # ========== TOOL DETECTION ==========
    
    def check_tools(self):
        """Check availability of GCC and Valgrind on Windows and WSL"""
        tools_status = []
        self.wsl_available = False
        self.wsl_gcc_available = False
        self.wsl_valgrind_available = False
        
        # Check for Windows native GCC (MinGW)
        self._check_windows_gcc(tools_status)
        
        # Check for Windows native Valgrind (rarely available)
        self._check_windows_valgrind(tools_status)
        
        # Check for WSL and its tools
        self._check_wsl_tools(tools_status)
        
        # Display results
        self._display_tool_status(tools_status)

    def _check_windows_gcc(self, tools_status):
        """Check if GCC is available natively on Windows"""
        try:
            result = subprocess.run(
                ["gcc", "--version"], 
                capture_output=True, 
                text=True, 
                shell=True,
                timeout=5
            )
            if result.returncode == 0:
                tools_status.append("✓ GCC compiler available (Windows)")
            else:
                tools_status.append("✗ GCC compiler not found (Windows)")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            tools_status.append("✗ GCC compiler not found (Windows)")

    def _check_windows_valgrind(self, tools_status):
        """Check if Valgrind is available natively on Windows"""
        try:
            result = subprocess.run(
                ["valgrind", "--version"], 
                capture_output=True, 
                text=True, 
                shell=True,
                timeout=5
            )
            if result.returncode == 0:
                tools_status.append("✓ Valgrind available (Windows)")
            else:
                tools_status.append("✗ Valgrind not available (Windows)")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            tools_status.append("✗ Valgrind not available (Windows)")

    def _check_wsl_tools(self, tools_status):
        """Check if WSL is available and check for GCC/Valgrind in WSL"""
        try:
            result = subprocess.run(
                ["wsl", "--status"], 
                capture_output=True, 
                text=True, 
                shell=True,
                timeout=5
            )
            
            if result.returncode == 0:
                tools_status.append("✓ WSL available")
                self.wsl_available = True
                
                # Check GCC in WSL
                self._check_wsl_gcc(tools_status)
                
                # Check Valgrind in WSL
                self._check_wsl_valgrind(tools_status)
            else:
                tools_status.append("✗ WSL not available")
                
        except (FileNotFoundError, subprocess.TimeoutExpired):
            tools_status.append("✗ WSL not available")

    def _check_wsl_gcc(self, tools_status):
        """Check if GCC is installed in WSL"""
        try:
            result = subprocess.run(
                ["wsl", "gcc", "--version"], 
                capture_output=True, 
                text=True, 
                shell=True,
                timeout=5
            )
            if result.returncode == 0:
                tools_status.append("✓ GCC available in WSL")
                self.wsl_gcc_available = True
            else:
                tools_status.append("✗ GCC not installed in WSL")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            tools_status.append("✗ GCC not installed in WSL")

    def _check_wsl_valgrind(self, tools_status):
        """Check if Valgrind is installed in WSL"""
        try:
            result = subprocess.run(
                ["wsl", "valgrind", "--version"], 
                capture_output=True, 
                text=True, 
                shell=True,
                timeout=5
            )
            if result.returncode == 0:
                tools_status.append("✓ Valgrind available in WSL")
                self.wsl_valgrind_available = True
            else:
                tools_status.append("✗ Valgrind not installed in WSL")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            tools_status.append("✗ Valgrind not installed in WSL")

    def _display_tool_status(self, tools_status):
        """Display tool availability status in the output area"""
        self.text_area.insert(tk.END, "=" * 50 + "\n")
        self.text_area.insert(tk.END, "TOOL STATUS\n")
        self.text_area.insert(tk.END, "=" * 50 + "\n")
        
        for status in tools_status:
            self.text_area.insert(tk.END, f"{status}\n")
        
        # Show setup instructions if WSL is available but tools are missing
        if self.wsl_available and (not self.wsl_gcc_available or not self.wsl_valgrind_available):
            self.text_area.insert(tk.END, "\n" + "=" * 50 + "\n")
            self.text_area.insert(tk.END, "📝 SETUP INSTRUCTIONS\n")
            self.text_area.insert(tk.END, "=" * 50 + "\n")
            self.text_area.insert(tk.END, "To install missing tools, open Ubuntu from Start Menu and run:\n\n")
            self.text_area.insert(tk.END, "  sudo apt update && sudo apt install -y gcc valgrind\n")
        
        self.text_area.insert(tk.END, "\n" + "=" * 50 + "\n\n")

    # ========== COMPILATION ==========
    
    def compile_c_file(self):
        """Compile C source file to executable using available GCC compiler"""
        # Validate input
        file_path = self.process_entry.get().strip()
        if not file_path:
            messagebox.showerror("Error", "Please select a C source file!")
            return
        
        if not file_path.endswith('.c'):
            messagebox.showinfo("Info", "Selected file is not a C source file (.c)")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
        
        # Start compilation
        self.status_var.set("Compiling...")
        self.text_area.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.text_area.insert(tk.END, f"COMPILING: {os.path.basename(file_path)}\n")
        self.text_area.insert(tk.END, "=" * 50 + "\n")
        
        try:
            # Try WSL GCC first (preferred for memory analysis)
            if self.wsl_available and self.wsl_gcc_available:
                success = self._compile_with_wsl_gcc(file_path)
                if success:
                    return
            
            # Fallback to Windows native GCC
            self._compile_with_windows_gcc(file_path)
                
        except FileNotFoundError:
            error_msg = "GCC compiler not found!\n"
            error_msg += "Please install GCC in WSL or MinGW on Windows."
            messagebox.showerror("Error", error_msg)
            self.text_area.insert(tk.END, f"✗ {error_msg}\n")
            self.status_var.set("GCC not found")
            
        except Exception as e:
            messagebox.showerror("Error", f"Compilation error: {str(e)}")
            self.text_area.insert(tk.END, f"✗ Unexpected error: {str(e)}\n")
            self.status_var.set("Compilation error")

    def _compile_with_wsl_gcc(self, file_path):
        """Compile using WSL GCC compiler"""
        self.text_area.insert(tk.END, "Using WSL GCC compiler...\n")
        
        # Convert Windows path to WSL path (e.g., C:\path -> /mnt/c/path)
        wsl_path = self._windows_path_to_wsl(file_path)
        exe_name = file_path[:-2]  # Remove .c extension
        wsl_exe = wsl_path[:-2]
        
        # Compile with debugging symbols (-g flag)
        compile_cmd = ["wsl", "gcc", "-g", "-o", wsl_exe, wsl_path]
        
        result = subprocess.run(
            compile_cmd, 
            capture_output=True, 
            text=True, 
            shell=True,
            timeout=30
        )
        
        if result.returncode == 0:
            self.text_area.insert(tk.END, f"✓ Compilation successful!\n")
            self.text_area.insert(tk.END, f"  Executable: {exe_name}\n")
            
            # Update entry field with executable path
            self.process_entry.delete(0, tk.END)
            self.process_entry.insert(0, exe_name)
            
            self.status_var.set("Compilation successful (WSL)")
            return True
        else:
            self.text_area.insert(tk.END, f"✗ Compilation failed:\n{result.stderr}\n")
            self.status_var.set("Compilation failed")
            return False

    def _compile_with_windows_gcc(self, file_path):
        """Compile using Windows native GCC compiler"""
        self.text_area.insert(tk.END, "Using Windows GCC compiler...\n")
        
        # Create executable name
        exe_name = file_path[:-2] + ".exe" if platform.system() == "Windows" else file_path[:-2]
        
        # Compile with debugging symbols
        compile_cmd = ["gcc", "-g", "-o", exe_name, file_path]
        
        result = subprocess.run(
            compile_cmd, 
            capture_output=True, 
            text=True, 
            shell=True,
            timeout=30
        )
        
        if result.returncode == 0:
            self.text_area.insert(tk.END, f"✓ Compilation successful!\n")
            self.text_area.insert(tk.END, f"  Executable: {exe_name}\n")
            
            # Update entry field with executable path
            self.process_entry.delete(0, tk.END)
            self.process_entry.insert(0, exe_name)
            
            self.status_var.set("Compilation successful")
        else:
            self.text_area.insert(tk.END, f"✗ Compilation failed:\n{result.stderr}\n")
            self.status_var.set("Compilation failed")

    def _windows_path_to_wsl(self, windows_path):
        """Convert Windows path to WSL path format"""
        # Replace backslashes with forward slashes
        wsl_path = windows_path.replace('\\', '/')
        # Convert drive letter (e.g., C: -> /mnt/c)
        if ':' in wsl_path:
            drive = wsl_path[0].lower()
            wsl_path = f"/mnt/{drive}{wsl_path[2:]}"
        return wsl_path

    # ========== MEMORY ANALYSIS ==========
    
    def analyze_memory(self):
        """Analyze executable for memory leaks using Valgrind"""
        # Validate input
        executable_path = self.process_entry.get().strip()
        if not executable_path:
            messagebox.showerror("Error", "Please select an executable file!")
            return
        
        if not os.path.exists(executable_path):
            messagebox.showerror("Error", f"File not found: {executable_path}")
            return
        
        # Start analysis
        self.status_var.set("Analyzing memory...")
        self.text_area.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.text_area.insert(tk.END, f"MEMORY ANALYSIS: {os.path.basename(executable_path)}\n")
        self.text_area.insert(tk.END, "=" * 50 + "\n")
        
        try:
            # Try Valgrind analysis (preferred method)
            if self.try_valgrind(executable_path):
                return
            
            # Fallback: Basic execution without memory leak detection
            self.basic_analysis(executable_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis error: {str(e)}")
            self.text_area.insert(tk.END, f"✗ Error: {str(e)}\n")
            self.status_var.set("Analysis error")

    def try_valgrind(self, executable_path):
        """
        Attempt to run Valgrind memory leak detection
        Returns True if Valgrind ran successfully, False otherwise
        """
        # Try WSL Valgrind (primary method for Windows)
        if self.wsl_available and self.wsl_valgrind_available:
            return self._run_wsl_valgrind(executable_path)
        
        # Try native Valgrind (rare on Windows)
        return self._run_native_valgrind(executable_path)

    def _run_wsl_valgrind(self, executable_path):
        """Run Valgrind through WSL"""
        try:
            self.text_area.insert(tk.END, "Running Valgrind memory check (WSL)...\n")
            
            # Convert Windows path to WSL format
            wsl_path = self._windows_path_to_wsl(executable_path)
            
            # Valgrind command with full leak checking
            valgrind_cmd = [
                "wsl", "valgrind",
                "--leak-check=full",       # Detailed leak information
                "--track-origins=yes",     # Track origin of uninitialized values
                "--show-leak-kinds=all",   # Show all types of leaks
                wsl_path
            ]
            
            result = subprocess.run(
                valgrind_cmd, 
                capture_output=True, 
                text=True, 
                shell=True, 
                timeout=30
            )
            
            # Parse and display results
            self.parse_valgrind_output(result.stderr)
            self.status_var.set("Valgrind analysis complete (WSL)")
            return True
                
        except subprocess.TimeoutExpired:
            self.text_area.insert(tk.END, "⚠ Valgrind execution timed out (30 seconds)\n")
            self.text_area.insert(tk.END, "The program may be hanging or taking too long.\n")
            return False
            
        except Exception as e:
            self.text_area.insert(tk.END, f"✗ WSL Valgrind error: {str(e)}\n")
            return False

    def _run_native_valgrind(self, executable_path):
        """Run Valgrind natively on Windows (rarely available)"""
        try:
            self.text_area.insert(tk.END, "Trying native Valgrind...\n")
            
            valgrind_cmd = [
                "valgrind",
                "--leak-check=full",
                "--track-origins=yes",
                executable_path
            ]
            
            result = subprocess.run(
                valgrind_cmd, 
                capture_output=True, 
                text=True, 
                shell=False, 
                timeout=30
            )
            
            self.parse_valgrind_output(result.stderr)
            self.status_var.set("Valgrind analysis complete")
            return True
                
        except FileNotFoundError:
            self.text_area.insert(tk.END, "⚠ Valgrind not available.\n")
            self.text_area.insert(tk.END, "Install Valgrind in WSL for memory leak detection.\n")
            self.text_area.insert(tk.END, "Falling back to basic analysis...\n\n")
            return False
            
        except subprocess.TimeoutExpired:
            self.text_area.insert(tk.END, "⚠ Valgrind execution timed out\n")
            return False
            
        except Exception:
            return False

    def parse_valgrind_output(self, valgrind_stderr):
        """Parse and display Valgrind output in a user-friendly format"""
        
        # Check for memory leaks
        if "All heap blocks were freed -- no leaks are possible" in valgrind_stderr:
            self.text_area.insert(tk.END, "\n✓ RESULT: No memory leaks detected!\n\n")
        else:
            self.text_area.insert(tk.END, "\n⚠ RESULT: Memory leaks detected!\n\n")
        
        # Extract and display memory usage summary
        memory_summary = re.search(r"total heap usage: .* bytes allocated", valgrind_stderr)
        if memory_summary:
            self.text_area.insert(tk.END, f"Memory usage: {memory_summary.group()}\n")
        
        # Extract and display leak summary
        if "LEAK SUMMARY" in valgrind_stderr:
            self.text_area.insert(tk.END, "\n" + "-" * 50 + "\n")
            self.text_area.insert(tk.END, "Leak Summary:\n")
            self.text_area.insert(tk.END, "-" * 50 + "\n")
            
            leak_patterns = [
                (r"definitely lost: .* blocks", "Definitely lost"),
                (r"indirectly lost: .* blocks", "Indirectly lost"),
                (r"possibly lost: .* blocks", "Possibly lost"),
                (r"still reachable: .* blocks", "Still reachable"),
                (r"suppressed: .* blocks", "Suppressed")
            ]
            
            for pattern, label in leak_patterns:
                match = re.search(pattern, valgrind_stderr)
                if match:
                    self.text_area.insert(tk.END, f"  {label}: {match.group().split(':')[1].strip()}\n")
        
        # Display full Valgrind output for detailed analysis
        self.text_area.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.text_area.insert(tk.END, "Full Valgrind Output:\n")
        self.text_area.insert(tk.END, "=" * 50 + "\n")
        self.text_area.insert(tk.END, f"{valgrind_stderr}\n")

    def basic_analysis(self, executable_path):
        """
        Basic program execution without Valgrind
        This only shows if the program runs, not memory leaks
        """
        self.text_area.insert(tk.END, "\n" + "-" * 50 + "\n")
        self.text_area.insert(tk.END, "Running basic execution (no memory leak detection)...\n")
        self.text_area.insert(tk.END, "-" * 50 + "\n")
        
        try:
            # Execute the program
            result = subprocess.run(
                [executable_path], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            # Display exit code
            self.text_area.insert(tk.END, f"\nExit code: {result.returncode}")
            if result.returncode == 0:
                self.text_area.insert(tk.END, " (Success)\n")
            else:
                self.text_area.insert(tk.END, " (Error)\n")
            
            # Display program output
            if result.stdout:
                self.text_area.insert(tk.END, f"\nProgram output:\n{result.stdout}\n")
            
            # Display program errors
            if result.stderr:
                self.text_area.insert(tk.END, f"\nProgram errors:\n{result.stderr}\n")
            
            # Remind user about Valgrind
            self.text_area.insert(tk.END, "\n" + "!" * 50 + "\n")
            self.text_area.insert(tk.END, "⚠ NOTE: Memory leak detection requires Valgrind!\n")
            self.text_area.insert(tk.END, "Install WSL and Valgrind for full memory analysis.\n")
            self.text_area.insert(tk.END, "!" * 50 + "\n")
            
            self.status_var.set("Basic analysis complete (no leak detection)")
            
        except subprocess.TimeoutExpired:
            self.text_area.insert(tk.END, "\n⚠ Program execution timed out (10 seconds)\n")
            self.text_area.insert(tk.END, "The program may be hanging or waiting for input.\n")
            self.status_var.set("Execution timed out")
            
        except Exception as e:
            self.text_area.insert(tk.END, f"\n✗ Execution error: {str(e)}\n")
            self.status_var.set("Execution error")

    # ========== UTILITY FUNCTIONS ==========

    def clear_output(self):
        """Clear the output text area and refresh tool status"""
        self.text_area.delete(1.0, tk.END)
        self.check_tools()


# ========== MAIN ENTRY POINT ==========

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryLeakGUI(root)
    root.mainloop()